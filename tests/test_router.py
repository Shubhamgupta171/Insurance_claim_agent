"""
Unit tests for the claim router module.
"""

import pytest
from src.router import ClaimRouter
from src.models import (
    ClaimData, PolicyInformation, IncidentInformation,
    InvolvedParties, AssetDetails, RouteType
)


class TestClaimRouter:
    """Test cases for ClaimRouter"""
    
    @pytest.fixture
    def router(self):
        """Create router instance"""
        return ClaimRouter()
    
    @pytest.fixture
    def fast_track_claim(self):
        """Create a claim eligible for fast-track"""
        return ClaimData(
            policy_information=PolicyInformation(
                policy_number="POL-123456",
                policyholder_name="John Doe"
            ),
            incident_information=IncidentInformation(
                date_of_loss="2026-02-01",
                location="123 Main St",
                description="Minor fender bender"
            ),
            involved_parties=InvolvedParties(
                claimant="John Doe"
            ),
            asset_details=AssetDetails(
                estimated_damage=15000.0,
                damage_description="Minor bumper damage"
            ),
            claim_type="auto"
        )
    
    @pytest.fixture
    def fraud_claim(self):
        """Create a claim with fraud indicators"""
        return ClaimData(
            policy_information=PolicyInformation(
                policy_number="POL-789012",
                policyholder_name="Suspicious Person"
            ),
            incident_information=IncidentInformation(
                date_of_loss="2026-02-01",
                location="Empty lot",
                description="This claim appears fraudulent and inconsistent with evidence. The damage seems staged."
            ),
            involved_parties=InvolvedParties(
                claimant="Suspicious Person"
            ),
            asset_details=AssetDetails(
                estimated_damage=20000.0
            ),
            claim_type="auto"
        )
    
    @pytest.fixture
    def injury_claim(self):
        """Create an injury claim"""
        return ClaimData(
            policy_information=PolicyInformation(
                policy_number="POL-345678",
                policyholder_name="Injured Person"
            ),
            incident_information=IncidentInformation(
                date_of_loss="2026-02-01",
                location="Highway 95",
                description="Collision resulted in personal injury. Driver transported to hospital by ambulance."
            ),
            involved_parties=InvolvedParties(
                claimant="Injured Person"
            ),
            asset_details=AssetDetails(
                estimated_damage=30000.0
            ),
            claim_type="injury"
        )
    
    def test_router_initialization(self, router):
        """Test that router initializes correctly"""
        assert router is not None
        assert router.fast_track_threshold == 25000
    
    def test_fast_track_routing(self, router, fast_track_claim):
        """Test fast-track routing for eligible claims"""
        route, reasoning = router.route_claim(fast_track_claim, [])
        
        assert route == RouteType.FAST_TRACK
        assert "fast-track" in reasoning.lower()
        assert "$15,000" in reasoning
    
    def test_manual_review_missing_fields(self, router, fast_track_claim):
        """Test manual review routing for missing fields"""
        missing_fields = ['policy_number', 'claimant']
        route, reasoning = router.route_claim(fast_track_claim, missing_fields)
        
        assert route == RouteType.MANUAL_REVIEW
        assert "missing" in reasoning.lower()
    
    def test_fraud_investigation_routing(self, router, fraud_claim):
        """Test investigation flag routing for fraud indicators"""
        route, reasoning = router.route_claim(fraud_claim, [])
        
        assert route == RouteType.INVESTIGATION
        assert "fraud" in reasoning.lower() or "investigation" in reasoning.lower()
    
    def test_injury_specialist_routing(self, router, injury_claim):
        """Test specialist queue routing for injury claims"""
        route, reasoning = router.route_claim(injury_claim, [])
        
        assert route == RouteType.SPECIALIST_QUEUE
        assert "injury" in reasoning.lower() or "specialist" in reasoning.lower()
    
    def test_check_fraud_indicators(self, router, fraud_claim):
        """Test fraud indicator detection"""
        has_fraud, keywords = router.check_fraud_indicators(fraud_claim)
        
        assert has_fraud == True
        assert len(keywords) > 0
    
    def test_check_injury_claim(self, router, injury_claim):
        """Test injury claim detection"""
        is_injury, indicators = router.check_injury_claim(injury_claim)
        
        assert is_injury == True
        assert len(indicators) > 0
    
    def test_high_value_manual_review(self, router):
        """Test manual review for high-value claims"""
        high_value_claim = ClaimData(
            policy_information=PolicyInformation(
                policy_number="POL-999999",
                policyholder_name="Rich Person"
            ),
            incident_information=IncidentInformation(
                date_of_loss="2026-02-01",
                location="Luxury area"
            ),
            involved_parties=InvolvedParties(
                claimant="Rich Person"
            ),
            asset_details=AssetDetails(
                estimated_damage=50000.0
            ),
            claim_type="auto"
        )
        
        route, reasoning = router.route_claim(high_value_claim, [])
        
        assert route == RouteType.MANUAL_REVIEW
        assert "$50,000" in reasoning
