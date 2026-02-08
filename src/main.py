"""
Main application for Insurance Claims Processing Agent.

Orchestrates the complete claim processing workflow.
"""

import argparse
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from .extractor import PDFExtractor
from .validator import ClaimValidator
from .router import ClaimRouter
from .models import ClaimOutput
from .config import Config


class ClaimsAgent:
    """Main claims processing agent"""
    
    def __init__(self, use_ai: bool = True):
        """
        Initialize the claims agent.
        
        Args:
            use_ai: Whether to use AI for extraction
        """
        self.extractor = PDFExtractor(use_ai=use_ai)
        self.validator = ClaimValidator()
        self.router = ClaimRouter()
    
    def process_claim(self, pdf_path: str, output_path: Optional[str] = None) -> ClaimOutput:
        """
        Process a single claim from PDF to routed output.
        
        Args:
            pdf_path: Path to the FNOL PDF file
            output_path: Optional path to save JSON output
            
        Returns:
            ClaimOutput object with complete processing results
        """
        print(f"\n{'='*60}")
        print(f"Processing claim: {Path(pdf_path).name}")
        print(f"{'='*60}\n")
        
        # Step 1: Extract data from PDF
        print("Step 1: Extracting data from PDF...")
        claim_data = self.extractor.extract_from_pdf(pdf_path)
        print("✓ Extraction complete")
        
        # Step 2: Validate extracted data
        print("\nStep 2: Validating extracted fields...")
        validation_result = self.validator.get_validation_summary(claim_data)
        missing_fields = validation_result['missing_fields']
        
        if missing_fields:
            print(f"⚠ Found {len(missing_fields)} missing field(s): {', '.join(missing_fields)}")
        else:
            print("✓ All mandatory fields present")
        
        if validation_result['warnings']:
            print(f"⚠ Warnings: {'; '.join(validation_result['warnings'])}")
        
        # Step 3: Route the claim
        print("\nStep 3: Routing claim...")
        route, reasoning = self.router.route_claim(claim_data, missing_fields)
        print(f"✓ Route determined: {route}")
        
        # Create output
        claim_output = ClaimOutput(
            claim_id=str(uuid.uuid4()),
            processed_at=datetime.now().isoformat(),
            extracted_fields=claim_data,
            missing_fields=missing_fields,
            recommended_route=route,
            reasoning=reasoning
        )
        
        # Save to file if output path provided
        if output_path:
            self.save_output(claim_output, output_path)
            print(f"\n✓ Output saved to: {output_path}")
        
        # Print summary
        self.print_summary(claim_output)
        
        return claim_output
    
    def save_output(self, claim_output: ClaimOutput, output_path: str):
        """
        Save claim output to JSON file.
        
        Args:
            claim_output: The claim output object
            output_path: Path to save the JSON file
        """
        output_dict = claim_output.model_dump()
        
        with open(output_path, 'w') as f:
            json.dump(output_dict, f, indent=2)
    
    def print_summary(self, claim_output: ClaimOutput):
        """
        Print a formatted summary of the claim processing.
        
        Args:
            claim_output: The claim output object
        """
        print(f"\n{'='*60}")
        print("CLAIM PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"Claim ID: {claim_output.claim_id}")
        print(f"Processed At: {claim_output.processed_at}")
        print(f"\nRecommended Route: {claim_output.recommended_route}")
        print(f"\nReasoning: {claim_output.reasoning}")
        
        if claim_output.missing_fields:
            print(f"\nMissing Fields ({len(claim_output.missing_fields)}):")
            for field in claim_output.missing_fields:
                print(f"  - {field}")
        
        print(f"\n{'='*60}\n")


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description='Insurance Claims Processing Agent - Process ACORD FNOL documents'
    )
    parser.add_argument(
        '--input',
        type=str,
        help='Path to input PDF file'
    )
    parser.add_argument(
        '--input-dir',
        type=str,
        help='Directory containing PDF files to process'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='data/output',
        help='Directory to save output JSON files (default: data/output)'
    )
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Disable AI extraction (use regex only)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.input and not args.input_dir:
        parser.error("Either --input or --input-dir must be provided")
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize agent
    use_ai = not args.no_ai
    agent = ClaimsAgent(use_ai=use_ai)
    
    # Process files
    if args.input:
        # Process single file
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: File not found: {args.input}")
            return
        
        output_path = output_dir / f"{input_path.stem}_output.json"
        agent.process_claim(str(input_path), str(output_path))
    
    elif args.input_dir:
        # Process all PDFs in directory
        input_dir = Path(args.input_dir)
        if not input_dir.exists():
            print(f"Error: Directory not found: {args.input_dir}")
            return
        
        pdf_files = list(input_dir.glob("*.pdf"))
        if not pdf_files:
            print(f"No PDF files found in {args.input_dir}")
            return
        
        print(f"Found {len(pdf_files)} PDF file(s) to process\n")
        
        for pdf_file in pdf_files:
            output_path = output_dir / f"{pdf_file.stem}_output.json"
            try:
                agent.process_claim(str(pdf_file), str(output_path))
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {str(e)}\n")


if __name__ == "__main__":
    main()
