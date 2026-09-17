"""
Prediction Engine Output Schemas
"""

from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field

from app.utils.constants import RiskLevel, HazardType
from app.schemas.risk import EstimatedLeadTime, RecommendedAction


class PredictionSummary(BaseModel):
    village_id: int
    village_name: str
    district: str
    risk_level: RiskLevel
    compound_risk_score: float
    flood_risk_score: float
    landslide_risk_score: float
    primary_hazard: HazardType
    lead_time: EstimatedLeadTime
    action: RecommendedAction
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PredictionTimelinePoint(BaseModel):
    timestamp: datetime
    compound_risk_score: float
    flood_risk_score: float
    landslide_risk_score: float
    risk_level: RiskLevel
    rainfall_rate_mm: float
    soil_saturation_pct: float
    river_level_m: Optional[float] = None
