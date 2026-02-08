"""
Data models for insurance claims processing.

Defines Pydantic models for structured claim data.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class ClaimType(str, Enum):
    """Types of insurance claims"""
    AUTO = "auto"
    PROPERTY = "property"
    INJURY = "injury"
    LIABILITY = "liability"
    OTHER = "other"


class RouteType(str, Enum):
    """Claim routing destinations"""
    FAST_TRACK = "Fast-track"
    MANUAL_REVIEW = "Manual review"
    INVESTIGATION = "Investigation Flag"
    SPECIALIST_QUEUE = "Specialist Queue"


class PolicyInformation(BaseModel):
    """Policy-related information"""
    policy_number: Optional[str] = None
    policyholder_name: Optional[str] = None
    effective_dates: Optional[str] = None
    line_of_business: Optional[str] = None
    agency_customer_id: Optional[str] = None


class IncidentInformation(BaseModel):
    """Incident details"""
    date_of_loss: Optional[str] = None
    time_of_loss: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    police_report_number: Optional[str] = None


class ContactDetails(BaseModel):
    """Contact information"""
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class InvolvedParties(BaseModel):
    """Information about parties involved in the claim"""
    claimant: Optional[str] = None
    third_parties: List[str] = Field(default_factory=list)
    contact_details: Optional[ContactDetails] = None
    driver_name: Optional[str] = None
    owner_name: Optional[str] = None


class AssetDetails(BaseModel):
    """Details about damaged assets"""
    asset_type: Optional[str] = None
    asset_id: Optional[str] = None  # VIN for vehicles
    estimated_damage: Optional[float] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    damage_description: Optional[str] = None


class ClaimData(BaseModel):
    """Complete claim information extracted from FNOL"""
    policy_information: PolicyInformation = Field(default_factory=PolicyInformation)
    incident_information: IncidentInformation = Field(default_factory=IncidentInformation)
    involved_parties: InvolvedParties = Field(default_factory=InvolvedParties)
    asset_details: AssetDetails = Field(default_factory=AssetDetails)
    claim_type: Optional[str] = None
    attachments: List[str] = Field(default_factory=list)
    initial_estimate: Optional[float] = None


class ClaimOutput(BaseModel):
    """Final output format for processed claims"""
    claim_id: str
    processed_at: str
    extracted_fields: ClaimData
    missing_fields: List[str]
    recommended_route: RouteType
    reasoning: str

    class Config:
        use_enum_values = True
