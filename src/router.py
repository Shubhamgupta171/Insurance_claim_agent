"""
Claim routing module.

Routes insurance claims based on business rules and extracted data.
"""

from typing import Tuple, List
from .models import ClaimData, RouteType
from .config import Config


class ClaimRouter:
    """Routes claims to appropriate queues based on business rules"""
    
    def __init__(self):
        """Initialize router with configuration"""
        self.fast_track_threshold = Config.FAST_TRACK_THRESHOLD
        self.fraud_keywords = Config.FRAUD_KEYWORDS
        self.injury_keywords = Config.INJURY_KEYWORDS
    
    def check_fraud_indicators(self, claim_data: ClaimData) -> Tuple[bool, List[str]]:
        """
        Check for fraud indicators in claim description.
        
        Args:
            claim_data: The claim data to check
            
        Returns:
            Tuple of (has_fraud_indicators, list of matched keywords)
        """
        description = claim_data.incident_information.description or ""
        damage_desc = claim_data.asset_details.damage_description or ""
        
        # Combine all text fields to search
        search_text = f"{description} {damage_desc}".lower()
        
        matched_keywords = []
        for keyword in self.fraud_keywords:
            if keyword.lower() in search_text:
                matched_keywords.append(keyword)
        
        return len(matched_keywords) > 0, matched_keywords
    
    def check_injury_claim(self, claim_data: ClaimData) -> Tuple[bool, List[str]]:
        """
        Check if claim involves injury.
        
        Args:
            claim_data: The claim data to check
            
        Returns:
            Tuple of (is_injury_claim, list of matched keywords)
        """
        # Check claim type
        if claim_data.claim_type and claim_data.claim_type.lower() == "injury":
            return True, ["claim_type: injury"]
        
        # Check description for injury keywords
        description = claim_data.incident_information.description or ""
        damage_desc = claim_data.asset_details.damage_description or ""
        
        search_text = f"{description} {damage_desc}".lower()
        
        matched_keywords = []
        for keyword in self.injury_keywords:
            if keyword.lower() in search_text:
                matched_keywords.append(keyword)
        
        return len(matched_keywords) > 0, matched_keywords
    
    def route_claim(
        self, 
        claim_data: ClaimData, 
        missing_fields: List[str]
    ) -> Tuple[RouteType, str]:
        """
        Determine the appropriate route for a claim.
        
        Routing priority:
        1. Manual Review (missing mandatory fields)
        2. Investigation Flag (fraud indicators)
        3. Specialist Queue (injury claims)
        4. Fast-track (low value, complete claims)
        
        Args:
            claim_data: The extracted claim data
            missing_fields: List of missing mandatory fields
            
        Returns:
            Tuple of (route_type, reasoning)
        """
        # Priority 1: Manual Review for missing fields
        if missing_fields:
            reasoning = (
                f"Claim requires manual review due to {len(missing_fields)} missing mandatory field(s): "
                f"{', '.join(missing_fields)}. Complete information is required before processing."
            )
            return RouteType.MANUAL_REVIEW, reasoning
        
        # Priority 2: Investigation Flag for fraud indicators
        has_fraud, fraud_keywords = self.check_fraud_indicators(claim_data)
        if has_fraud:
            reasoning = (
                f"Claim flagged for investigation due to potential fraud indicators. "
                f"Keywords detected: {', '.join(fraud_keywords)}. "
                f"Requires detailed review by fraud investigation team."
            )
            return RouteType.INVESTIGATION, reasoning
        
        # Priority 3: Specialist Queue for injury claims
        is_injury, injury_indicators = self.check_injury_claim(claim_data)
        if is_injury:
            reasoning = (
                f"Claim routed to specialist queue due to injury involvement. "
                f"Indicators: {', '.join(injury_indicators)}. "
                f"Requires assessment by injury claims specialist."
            )
            return RouteType.SPECIALIST_QUEUE, reasoning
        
        # Priority 4: Fast-track for low-value claims
        estimated_damage = claim_data.asset_details.estimated_damage
        if estimated_damage is not None and estimated_damage < self.fast_track_threshold:
            reasoning = (
                f"Claim meets fast-track criteria: estimated damage (${estimated_damage:,.2f}) "
                f"is below ${self.fast_track_threshold:,.2f} threshold and all mandatory fields "
                f"are present. No fraud indicators or injury claims detected."
            )
            return RouteType.FAST_TRACK, reasoning
        
        # Default: Manual Review for high-value claims or missing estimate
        if estimated_damage is None:
            reasoning = (
                "Claim requires manual review as estimated damage amount is not provided. "
                "Damage assessment needed before routing decision."
            )
        else:
            reasoning = (
                f"Claim requires manual review due to high estimated damage (${estimated_damage:,.2f}), "
                f"which exceeds the fast-track threshold of ${self.fast_track_threshold:,.2f}. "
                f"Requires detailed assessment by claims adjuster."
            )
        
        return RouteType.MANUAL_REVIEW, reasoning
    
    def get_routing_summary(
        self, 
        claim_data: ClaimData, 
        missing_fields: List[str]
    ) -> dict:
        """
        Get detailed routing analysis.
        
        Args:
            claim_data: The claim data
            missing_fields: List of missing fields
            
        Returns:
            Dictionary with routing analysis
        """
        route, reasoning = self.route_claim(claim_data, missing_fields)
        has_fraud, fraud_keywords = self.check_fraud_indicators(claim_data)
        is_injury, injury_indicators = self.check_injury_claim(claim_data)
        
        return {
            'recommended_route': route,
            'reasoning': reasoning,
            'fraud_indicators': {
                'detected': has_fraud,
                'keywords': fraud_keywords
            },
            'injury_indicators': {
                'detected': is_injury,
                'indicators': injury_indicators
            },
            'estimated_damage': claim_data.asset_details.estimated_damage,
            'fast_track_eligible': (
                not missing_fields and 
                not has_fraud and 
                not is_injury and
                claim_data.asset_details.estimated_damage is not None and
                claim_data.asset_details.estimated_damage < self.fast_track_threshold
            )
        }
