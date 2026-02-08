"""
Demo script showing the insurance claims agent with mock data.

This demonstrates the complete workflow without requiring API keys.
"""

import json
from datetime import datetime
from uuid import uuid4

from src.models import (
    ClaimData, PolicyInformation, IncidentInformation,
    InvolvedParties, AssetDetails, ContactDetails, ClaimOutput
)
from src.validator import ClaimValidator
from src.router import ClaimRouter


def create_demo_claims():
    """Create sample claims for demonstration"""
    
    # 1. Fast-track claim
    fast_track = ClaimData(
        policy_information=PolicyInformation(
            policy_number="POL-2026-FT-001",
            policyholder_name="Sarah Johnson"
        ),
        incident_information=IncidentInformation(
            date_of_loss="2026-02-01",
            time_of_loss="14:30",
            location="Intersection of Main St and 5th Avenue, Springfield, IL",
            description="Minor rear-end collision at traffic light"
        ),
        involved_parties=InvolvedParties(
            claimant="Sarah Johnson",
            contact_details=ContactDetails(
                phone="(555) 123-4567",
                email="sarah.johnson@email.com"
            )
        ),
        asset_details=AssetDetails(
            asset_type="Vehicle",
            asset_id="1HGBH41JXMN109186",
            estimated_damage=12500.0,
            make="Honda",
            model="Civic",
            year="2022"
        ),
        claim_type="auto",
        initial_estimate=12500.0
    )
    
    # 2. Missing fields claim
    missing_fields = ClaimData(
        policy_information=PolicyInformation(
            policyholder_name="Robert Williams"
        ),
        incident_information=IncidentInformation(
            date_of_loss="2026-02-03",
            description="Single vehicle accident"
        ),
        involved_parties=InvolvedParties(),
        asset_details=AssetDetails(
            asset_type="Vehicle"
        )
    )
    
    # 3. Fraud investigation claim
    fraud_claim = ClaimData(
        policy_information=PolicyInformation(
            policy_number="POL-2026-INV-003",
            policyholder_name="David Thompson"
        ),
        incident_information=IncidentInformation(
            date_of_loss="2026-02-05",
            location="Empty parking lot, Chicago, IL",
            description="Damage pattern appears inconsistent with reported scenario. "
                       "The incident description contains several inconsistent details. "
                       "Damage appears staged and fraudulent."
        ),
        involved_parties=InvolvedParties(
            claimant="David Thompson",
            contact_details=ContactDetails(
                phone="(555) 345-6789",
                email="d.thompson@email.com"
            )
        ),
        asset_details=AssetDetails(
            asset_type="Vehicle",
            asset_id="WBA8E1C50GK123456",
            estimated_damage=18500.0
        ),
        claim_type="auto",
        initial_estimate=18500.0
    )
    
    # 4. Injury claim
    injury_claim = ClaimData(
        policy_information=PolicyInformation(
            policy_number="POL-2026-INJ-004",
            policyholder_name="Emily Rodriguez"
        ),
        incident_information=IncidentInformation(
            date_of_loss="2026-02-07",
            location="Intersection of Congress Ave and 6th St, Austin, TX",
            description="Two-vehicle collision resulted in personal injury. "
                       "Driver sustained whiplash. Passenger suffered broken arm. "
                       "Both transported to hospital by ambulance."
        ),
        involved_parties=InvolvedParties(
            claimant="Emily Rodriguez",
            contact_details=ContactDetails(
                phone="(555) 456-7890",
                email="emily.rodriguez@email.com"
            )
        ),
        asset_details=AssetDetails(
            asset_type="Vehicle",
            asset_id="5YJ3E1EA1KF123456",
            estimated_damage=35000.0
        ),
        claim_type="injury",
        initial_estimate=35000.0
    )
    
    # 5. High-value complex claim
    complex_claim = ClaimData(
        policy_information=PolicyInformation(
            policy_number="POL-2026-CPX-005",
            policyholder_name="Anderson Family Trust"
        ),
        incident_information=IncidentInformation(
            date_of_loss="2026-02-06",
            location="Interstate 35, Dallas, TX",
            description="Multi-vehicle collision, total loss, vehicle fire"
        ),
        involved_parties=InvolvedParties(
            claimant="Anderson Family Trust",
            contact_details=ContactDetails(
                phone="(555) 567-8901",
                email="trust@andersonfamily.com"
            )
        ),
        asset_details=AssetDetails(
            asset_type="Vehicle",
            asset_id="WDDUX8GB1PA123456",
            estimated_damage=125000.0
        ),
        claim_type="auto",
        initial_estimate=125000.0
    )
    
    return [
        ("Fast-track Claim", fast_track),
        ("Missing Fields Claim", missing_fields),
        ("Fraud Investigation Claim", fraud_claim),
        ("Injury Claim", injury_claim),
        ("High-value Complex Claim", complex_claim)
    ]


def process_demo_claim(name, claim_data, validator, router):
    """Process a single demo claim"""
    print(f"\n{'='*70}")
    print(f"Processing: {name}")
    print(f"{'='*70}\n")
    
    # Validate
    missing_fields = validator.validate_claim(claim_data)
    
    # Route
    route, reasoning = router.route_claim(claim_data, missing_fields)
    
    # Create output
    output = ClaimOutput(
        claim_id=str(uuid4()),
        processed_at=datetime.now().isoformat(),
        extracted_fields=claim_data,
        missing_fields=missing_fields,
        recommended_route=route,
        reasoning=reasoning
    )
    
    # Display summary
    print(f"Claim ID: {output.claim_id}")
    print(f"Policy: {claim_data.policy_information.policy_number or 'N/A'}")
    print(f"Policyholder: {claim_data.policy_information.policyholder_name or 'N/A'}")
    print(f"Estimated Damage: ${claim_data.asset_details.estimated_damage or 0:,.2f}")
    print(f"\nMissing Fields: {len(missing_fields)}")
    if missing_fields:
        for field in missing_fields:
            print(f"  - {field}")
    
    print(f"\n🎯 Recommended Route: {route}")
    print(f"\n💡 Reasoning: {reasoning}")
    
    # Save output
    output_file = f"data/output/demo_{name.lower().replace(' ', '_')}_output.json"
    with open(output_file, 'w') as f:
        json.dump(output.model_dump(), f, indent=2)
    
    print(f"\n✓ Output saved to: {output_file}")
    
    return output


def main():
    """Run the demo"""
    print("\n" + "="*70)
    print("INSURANCE CLAIMS PROCESSING AGENT - DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows the agent processing 5 different claim scenarios:")
    print("1. Fast-track eligible claim")
    print("2. Claim with missing mandatory fields")
    print("3. Claim with fraud indicators")
    print("4. Personal injury claim")
    print("5. High-value complex claim")
    print("\n" + "="*70)
    
    # Initialize components
    validator = ClaimValidator()
    router = ClaimRouter()
    
    # Create and process demo claims
    demo_claims = create_demo_claims()
    results = []
    
    for name, claim_data in demo_claims:
        output = process_demo_claim(name, claim_data, validator, router)
        results.append((name, output))
    
    # Summary
    print(f"\n\n{'='*70}")
    print("PROCESSING SUMMARY")
    print(f"{'='*70}\n")
    
    route_counts = {}
    for name, output in results:
        route = output.recommended_route
        route_counts[route] = route_counts.get(route, 0) + 1
        print(f"✓ {name}: {route}")
    
    print(f"\n{'='*70}")
    print("ROUTING DISTRIBUTION")
    print(f"{'='*70}\n")
    
    for route, count in sorted(route_counts.items()):
        print(f"{route}: {count} claim(s)")
    
    print(f"\n{'='*70}")
    print("✓ Demo completed successfully!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
