"""
Field validation module for insurance claims.

Validates extracted data and identifies missing or inconsistent fields.
"""

from typing import List, Dict, Any
from .models import ClaimData
from .config import Config


class ClaimValidator:
    """Validates claim data and identifies issues"""
    
    def __init__(self):
        """Initialize the validator with mandatory fields"""
        self.mandatory_fields = Config.MANDATORY_FIELDS
    
    def get_field_value(self, claim_data: ClaimData, field_path: str) -> Any:
        """
        Get a field value from nested claim data structure.
        
        Args:
            claim_data: The claim data object
            field_path: Field identifier (e.g., 'policy_number', 'estimated_damage')
            
        Returns:
            Field value or None if not found
        """
        # Map field paths to actual nested locations
        field_mapping = {
            'policy_number': claim_data.policy_information.policy_number,
            'policyholder_name': claim_data.policy_information.policyholder_name,
            'date_of_loss': claim_data.incident_information.date_of_loss,
            'location': claim_data.incident_information.location,
            'claim_type': claim_data.claim_type,
            'estimated_damage': claim_data.asset_details.estimated_damage,
            'claimant': claim_data.involved_parties.claimant,
            'description': claim_data.incident_information.description,
        }
        
        return field_mapping.get(field_path)
    
    def validate_claim(self, claim_data: ClaimData) -> List[str]:
        """
        Validate claim data and return list of missing mandatory fields.
        
        Args:
            claim_data: The extracted claim data
            
        Returns:
            List of missing field names
        """
        missing_fields = []
        
        for field in self.mandatory_fields:
            value = self.get_field_value(claim_data, field)
            
            # Check if field is missing or empty
            if value is None or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)
        
        return missing_fields
    
    def check_data_consistency(self, claim_data: ClaimData) -> List[str]:
        """
        Check for data inconsistencies.
        
        Args:
            claim_data: The extracted claim data
            
        Returns:
            List of inconsistency warnings
        """
        warnings = []
        
        # Check if estimated damage matches initial estimate
        if claim_data.asset_details.estimated_damage and claim_data.initial_estimate:
            if claim_data.asset_details.estimated_damage != claim_data.initial_estimate:
                warnings.append("Estimated damage and initial estimate do not match")
        
        # Check if claimant matches policyholder (when they should be the same)
        if claim_data.involved_parties.claimant and claim_data.policy_information.policyholder_name:
            # This is just a warning, not an error
            if claim_data.involved_parties.claimant.lower() != claim_data.policy_information.policyholder_name.lower():
                warnings.append("Claimant differs from policyholder (may be third-party claim)")
        
        # Check for negative damage amounts
        if claim_data.asset_details.estimated_damage is not None:
            if claim_data.asset_details.estimated_damage < 0:
                warnings.append("Estimated damage is negative")
        
        return warnings
    
    def get_validation_summary(self, claim_data: ClaimData) -> Dict[str, Any]:
        """
        Get complete validation summary.
        
        Args:
            claim_data: The extracted claim data
            
        Returns:
            Dictionary with validation results
        """
        missing_fields = self.validate_claim(claim_data)
        warnings = self.check_data_consistency(claim_data)
        
        return {
            'is_valid': len(missing_fields) == 0,
            'missing_fields': missing_fields,
            'warnings': warnings,
            'total_missing': len(missing_fields)
        }
