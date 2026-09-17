"""
Pydantic Schemas for Risk Assessment and North Star Decision Objects
Answering:
1. WHERE is the risk? (Village / Location)
2. HOW SEVERE? (RiskLevel & RiskScore)
3. HOW SOON? (Estimated Lead Time)
4. WHAT NOW? (Recommended Action & Evacuation Target)
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from app.utils.constants import RiskLevel, HazardType, LEAD_TIME_LABEL


class EstimatedLeadTime(BaseModel):
    """
    Estimated lead time model adhering to PRD §12:
    Always described as 'Estimated Lead Time' to convey probabilistic decision-support.
    """
    label: str = Field(default=LEAD_TIME_LABEL, description="Standard disclaimer label")
    minutes: Optional[int] = Field(None, ge=0, description="Estimated minutes remaining until critical impact")
    hours: Optional[float] = Field(None, ge=0.0, description="Estimated hours remaining")
    confidence_score: float = Field(default=0.85, ge=0.0, le=1.0, description="Confidence in estimate based on sensor reliability")
    trend_description: str = Field(default="Stable", description="Escalating rapidly / Escalating moderately / Stable / Receding")

    @field_validator("hours", mode="before")
    def compute_hours(cls, v, values):
        return v


class RecommendedAction(BaseModel):
    """Actionable directive for district administration and ground responders"""
    action: str = Field(..., description="Prescribed operational action")
    priority: str = Field(default="STANDARD", description="LOW / MEDIUM / HIGH / URGENT")
    affected_zone: str = Field(default="Zone A", description="Specific village sector or catchment at risk")
    nearest_shelter_id: Optional[int] = Field(None, description="Assigned safe shelter ID")
    nearest_shelter_name: Optional[str] = Field(None, description="Name of safe shelter")
    shelter_distance_km: Optional[float] = Field(None, description="Distance to designated shelter in km")
    evacuation_route_id: Optional[str] = Field(None, description="Designated clear route avoiding risk corridors")
    safe_path_instructions: Optional[str] = Field(None, description="Turn-by-turn or landmark-based guidance")
    special_warnings: List[str] = Field(default_factory=list, description="Specific hazards e.g. Avoid riverside culvert")


class RiskAssessment(BaseModel):
    """
    The complete Decision Object answering the 4 North Star Questions
    """
    # 1. WHERE is the risk?
    village_id: int
    village_name: str
    district: str
    state: str = "Uttarakhand"
    latitude: float
    longitude: float
    population_at_risk: int = 0

    # 2. HOW SEVERE is the risk?
    risk_level: RiskLevel
    compound_risk_score: float = Field(..., ge=0.0, le=100.0, description="Aggregate score 0-100")
    flood_risk_score: float = Field(..., ge=0.0, le=100.0)
    landslide_risk_score: float = Field(..., ge=0.0, le=100.0)
    primary_hazard: HazardType = HazardType.COMPOUND
    secondary_hazard: Optional[HazardType] = None

    # 3. HOW SOON?
    lead_time: EstimatedLeadTime

    # 4. WHAT NOW?
    action: RecommendedAction

    # Supporting Environmental Observables
    rainfall_1h_mm: float = 0.0
    rainfall_24h_mm: float = 0.0
    soil_moisture_pct: float = 0.0
    river_level_m: Optional[float] = None
    river_rate_of_rise_m_per_hr: Optional[float] = None
    slope_degrees: float = 0.0
    sensor_health_status: str = "OPTIMAL"

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data_sources_available: List[str] = Field(default_factory=lambda: ["rainfall", "soil_moisture", "river", "terrain"])
