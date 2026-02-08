"""
Unit tests for the claim validator module.
"""

import pytest
from src.validator import ClaimValidator
from src.models import (
    ClaimData, PolicyInformation, IncidentInformation,
    InvolvedParties, AssetDetails
)


class TestClaimValidator:
    """Test cases for ClaimValidator"""
    
    @pytest.fixture
    def validator(self):
        """Create validator instance"""
        return ClaimValidator()
    
    @pytest.fixture
    def complete_claim(self):
        """Create a complete claim with all mandatory fields"""
        return ClaimData(
            policy_information=PolicyInformation(
                policy_number="POL-123456",
                policyholder_name="John Doe"
            ),
            incident_information=IncidentInformation(
                date_of_loss="2026-02-01",
                location="123 Main St"
            ),
            involved_parties=InvolvedParties(
                claimant="John Doe"
            ),
            asset_details=AssetDetails(
                estimated_damage=15000.0
            ),
            claim_type="auto"
        )
    
    @pytest.fixture
    def incomplete_claim(self):
        """Create a claim with missing fields"""
        return ClaimData(
            policy_information=PolicyInformation(
                policyholder_name="Jane Smith"
            ),
            incident_information=IncidentInformation(
                location="456 Oak Ave"
            ),
            asset_details=AssetDetails()
        )
    
    def test_validator_initialization(self, validator):
        """Test that validator initializes correctly"""
        assert validator is not None
        assert len(validator.mandatory_fields) > 0
    
    def test_validate_complete_claim(self, validator, complete_claim):
        """Test validation of complete claim"""
        missing_fields = validator.validate_claim(complete_claim)
        assert len(missing_fields) == 0
    
    def test_validate_incomplete_claim(self, validator, incomplete_claim):
        """Test validation of incomplete claim"""
        missing_fields = validator.validate_claim(incomplete_claim)
        assert len(missing_fields) > 0
        assert 'policy_number' in missing_fields
        assert 'estimated_damage' in missing_fields
    
    def test_get_validation_summary(self, validator, complete_claim):
        """Test validation summary generation"""
        summary = validator.get_validation_summary(complete_claim)
        
        assert 'is_valid' in summary
        assert 'missing_fields' in summary
        assert 'warnings' in summary
        assert summary['is_valid'] == True
    
    def test_check_data_consistency(self, validator, complete_claim):
        """Test data consistency checking"""
        warnings = validator.check_data_consistency(complete_claim)
        assert isinstance(warnings, list)
