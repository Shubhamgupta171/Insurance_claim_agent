"""
Configuration settings for the insurance claims agent.

Manages environment variables, API keys, and routing rules.
"""

import os
from typing import List, Set
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # OpenAI API Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Routing Thresholds
    FAST_TRACK_THRESHOLD: float = float(os.getenv("FAST_TRACK_THRESHOLD", "25000"))
    
    # Mandatory Fields
    MANDATORY_FIELDS: Set[str] = {
        "policy_number",
        "policyholder_name",
        "date_of_loss",
        "location",
        "claim_type",
        "estimated_damage",
        "claimant"
    }
    
    # Fraud Detection Keywords
    FRAUD_KEYWORDS: Set[str] = {
        "fraud",
        "fraudulent",
        "inconsistent",
        "staged",
        "suspicious",
        "fabricated",
        "false",
        "deceptive",
        "misleading",
        "contradictory"
    }
    
    # Injury-related Keywords
    INJURY_KEYWORDS: Set[str] = {
        "injury",
        "injured",
        "bodily injury",
        "personal injury",
        "medical",
        "hospital",
        "ambulance",
        "emergency",
        "paramedic"
    }
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration settings"""
        if not cls.OPENAI_API_KEY:
            print("Warning: OpenAI API key not set. AI extraction will not work.")
            return False
        return True
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get the OpenAI API key"""
        return cls.OPENAI_API_KEY


# Field mapping for ACORD form extraction
ACORD_FIELD_MAPPING = {
    "policy_number": ["POLICY NUMBER", "Policy Number", "Policy #"],
    "policyholder_name": ["NAME OF INSURED", "Insured Name", "Policyholder"],
    "date_of_loss": ["DATE OF LOSS", "Loss Date", "Incident Date"],
    "time_of_loss": ["TIME", "Loss Time"],
    "location": ["LOCATION OF LOSS", "Loss Location", "Incident Location"],
    "description": ["DESCRIPTION OF ACCIDENT", "Incident Description"],
    "claimant": ["NAME OF INSURED", "Claimant Name"],
    "phone": ["PHONE", "Phone Number", "Contact Phone"],
    "email": ["E-MAIL", "Email Address"],
    "vin": ["V.I.N.", "VIN", "Vehicle Identification Number"],
    "make": ["MAKE", "Vehicle Make"],
    "model": ["MODEL", "Vehicle Model"],
    "year": ["YEAR", "Vehicle Year"],
    "damage_description": ["DESCRIBE DAMAGE", "Damage Description"],
    "estimate_amount": ["ESTIMATE AMOUNT", "Estimated Damage", "Initial Estimate"],
    "police_report": ["REPORT NUMBER", "Police Report Number"]
}
