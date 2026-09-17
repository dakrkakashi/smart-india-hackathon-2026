"""
Risk Zone models for flash flood prediction areas
Represents areas with calculated risk levels
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import enum

from app.models import BaseModel


class RiskLevel(str, enum.Enum):
    """Risk classification levels"""
    NONE = "none"           # No risk
    LOW = "low"             # Minimal risk, monitor
    MODERATE = "moderate"   # Moderate risk, prepare
    HIGH = "high"           # High risk, ready to evacuate
    EXTREME = "extreme"     # Extreme risk, evacuate immediately


class RiskZone(BaseModel):
    """
    Geographic zone with calculated flood risk
    Updated periodically by ML prediction engine
    """

    __tablename__ = "risk_zones"

    # Location
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, index=True)
    region = relationship("Region", back_populates="risk_zones")

    # Zone Identifier
    zone_name = Column(String(255), nullable=False)
    zone_code = Column(String(50), unique=True, index=True)

    # Geospatial (grid cell or polygon)
    geometry = Column(Geometry(geometry_type="POLYGON", srid=4326), nullable=False)
    centroid = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)

    # Risk Assessment
    risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.NONE, index=True)
    risk_score = Column(Float, default=0.0)  # 0-1 probability
    confidence = Column(Float, default=0.0)  # 0-1 confidence in prediction

    # Time Predictions
    lead_time_hours = Column(Float, nullable=True)  # Hours until risk materializes
    prediction_timestamp = Column(String(50), nullable=False)  # When prediction was made
    valid_until = Column(String(50), nullable=True)  # When prediction expires

    # Contributing Factors
    rainfall_intensity = Column(Float, nullable=True)  # mm/hr
    soil_saturation = Column(Float, nullable=True)  # 0-1
    slope_stability_factor = Column(Float, nullable=True)  # Factor of safety
    water_level = Column(Float, nullable=True)  # meters

    # Impact Assessment
    affected_population = Column(Integer, default=0)
    affected_households = Column(Integer, default=0)
    critical_infrastructure_at_risk = Column(String(500), nullable=True)  # JSON list

    # ML Model Info
    model_version = Column(String(50), nullable=True)
    feature_importance = Column(String(1000), nullable=True)  # JSON dict

    # Status
    is_active = Column(Integer, default=1)  # boolean - currently valid prediction
    alert_generated = Column(Integer, default=0)  # boolean - has alert been sent

    def __repr__(self):
        return f"<RiskZone(id={self.id}, zone='{self.zone_name}', risk='{self.risk_level}', score={self.risk_score:.3f})>"
