"""
PDF extraction module for ACORD FNOL documents.

Extracts structured data from insurance claim PDFs using AI-powered parsing.
"""

import pdfplumber
import json
import re
from typing import Dict, Any, Optional
from pathlib import Path

from .models import (
    ClaimData, PolicyInformation, IncidentInformation,
    InvolvedParties, AssetDetails, ContactDetails
)
from .config import Config, ACORD_FIELD_MAPPING


class PDFExtractor:
    """Extracts claim data from PDF documents"""
    
    def __init__(self, use_ai: bool = True):
        """
        Initialize the PDF extractor.
        
        Args:
            use_ai: Whether to use AI for extraction (requires OpenAI API key)
        """
        self.use_ai = use_ai and Config.validate()
        
        if self.use_ai:
            from openai import OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract raw text from PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def extract_with_ai(self, text: str) -> Dict[str, Any]:
        """
        Use OpenAI GPT-4 to extract structured data from text.
        
        Args:
            text: Raw text from PDF
            
        Returns:
            Dictionary of extracted fields
        """
        prompt = f"""
You are an insurance claims processing assistant. Extract the following information from this ACORD FNOL (First Notice of Loss) document.

Extract these fields and return ONLY a valid JSON object (no markdown, no explanations):

{{
  "policy_number": "string or null",
  "policyholder_name": "string or null",
  "effective_dates": "string or null",
  "date_of_loss": "string (YYYY-MM-DD format) or null",
  "time_of_loss": "string (HH:MM format) or null",
  "location": "string or null",
  "description": "string or null",
  "claimant": "string or null",
  "phone": "string or null",
  "email": "string or null",
  "asset_type": "string (e.g., 'Vehicle', 'Property') or null",
  "vin": "string or null",
  "make": "string or null",
  "model": "string or null",
  "year": "string or null",
  "damage_description": "string or null",
  "estimated_damage": number or null,
  "claim_type": "string (auto/property/injury/liability/other) or null",
  "police_report_number": "string or null"
}}

Document text:
{text}

Return ONLY the JSON object, nothing else.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a data extraction assistant. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            content = response.choices[0].message.content
            
            # Clean up the response (remove markdown code blocks if present)
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            return json.loads(content)
            
        except Exception as e:
            print(f"OpenAI API extraction error: {str(e)}")
            return {}
    
    def extract_with_regex(self, text: str) -> Dict[str, Any]:
        """
        Fallback: Extract data using regex patterns.
        
        Args:
            text: Raw text from PDF
            
        Returns:
            Dictionary of extracted fields
        """
        extracted = {}
        
        # Policy number pattern
        policy_match = re.search(r'POLICY NUMBER[:\s]+([A-Z0-9-]+)', text, re.IGNORECASE)
        if policy_match:
            extracted['policy_number'] = policy_match.group(1).strip()
        
        # Date of loss pattern
        date_match = re.search(r'DATE OF LOSS[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
        if date_match:
            extracted['date_of_loss'] = date_match.group(1).strip()
        
        # VIN pattern
        vin_match = re.search(r'V\.I\.N\.[:\s]+([A-HJ-NPR-Z0-9]{17})', text, re.IGNORECASE)
        if vin_match:
            extracted['vin'] = vin_match.group(1).strip()
        
        # Estimate amount pattern
        estimate_match = re.search(r'ESTIMATE AMOUNT[:\s]*\$?\s*([0-9,]+(?:\.\d{2})?)', text, re.IGNORECASE)
        if estimate_match:
            amount_str = estimate_match.group(1).replace(',', '')
            try:
                extracted['estimated_damage'] = float(amount_str)
            except ValueError:
                pass
        
        return extracted
    
    def extract_from_pdf(self, pdf_path: str) -> ClaimData:
        """
        Main extraction method - extracts structured claim data from PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            ClaimData object with extracted information
        """
        # Extract raw text
        text = self.extract_text_from_pdf(pdf_path)
        
        # Try AI extraction first, fallback to regex
        if self.use_ai:
            extracted = self.extract_with_ai(text)
        else:
            extracted = self.extract_with_regex(text)
        
        # If AI didn't get everything, supplement with regex
        if self.use_ai:
            regex_data = self.extract_with_regex(text)
            for key, value in regex_data.items():
                if key not in extracted or not extracted[key]:
                    extracted[key] = value
        
        # Build structured data models
        policy_info = PolicyInformation(
            policy_number=extracted.get('policy_number'),
            policyholder_name=extracted.get('policyholder_name'),
            effective_dates=extracted.get('effective_dates')
        )
        
        incident_info = IncidentInformation(
            date_of_loss=extracted.get('date_of_loss'),
            time_of_loss=extracted.get('time_of_loss'),
            location=extracted.get('location'),
            description=extracted.get('description'),
            police_report_number=extracted.get('police_report_number')
        )
        
        contact_details = ContactDetails(
            phone=extracted.get('phone'),
            email=extracted.get('email')
        )
        
        involved_parties = InvolvedParties(
            claimant=extracted.get('claimant'),
            contact_details=contact_details
        )
        
        asset_details = AssetDetails(
            asset_type=extracted.get('asset_type', 'Vehicle'),
            asset_id=extracted.get('vin'),
            estimated_damage=extracted.get('estimated_damage'),
            make=extracted.get('make'),
            model=extracted.get('model'),
            year=extracted.get('year'),
            damage_description=extracted.get('damage_description')
        )
        
        claim_data = ClaimData(
            policy_information=policy_info,
            incident_information=incident_info,
            involved_parties=involved_parties,
            asset_details=asset_details,
            claim_type=extracted.get('claim_type'),
            initial_estimate=extracted.get('estimated_damage')
        )
        
        return claim_data
