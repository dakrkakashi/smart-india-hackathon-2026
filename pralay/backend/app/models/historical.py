"""
Historical disaster data models
Tracks past flood and landslide events for ML training
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import enum

from app.models import BaseModel


class DisasterType(str, enum.Enum):
    FLASH_FLOOD = "flash_flood"
    LANDSLIDE = "landslide"
    CLOUDBURST = "cloudburst"
    DEBRIS_FLOW = "debris_flow"


class HistoricalDisaster(BaseModel):
    """
    Historical flood and landslide events
    Used for ML model training and pattern recognition
    """

    __tablename__ = "historical_disasters"

    # Event Details
    event_date = Column(String(50), nullable=False, index=True)  # ISO date
    event_type = Column(String(50), nullable=False, index=True)  # 'flash_flood', 'landslide', 'cloudburst'
    event_name = Column(String(255), nullable=True)  # e.g., "Kedarnath Floods 2013"

    # Location
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True, index=True)
    region = relationship("Region")

    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    affected_area = Column(Geometry(geometry_type="POLYGON", srid=4326), nullable=True)

    # Severity & Impact
    severity = Column(String(50), nullable=True)  # 'minor', 'moderate', 'severe', 'catastrophic'
    casualties = Column(Integer, default=0)
    injuries = Column(Integer, default=0)
    missing = Column(Integer, default=0)
    affected_population = Column(Integer, default=0)
    affected_households = Column(Integer, default=0)

    # Damage Assessment
    economic_loss_cr = Column(Float, nullable=True)  # in crores INR
    infrastructure_damage = Column(String(500), nullable=True)  # JSON

    # Meteorological Conditions
    rainfall_24h = Column(Float, nullable=True)  # mm
    rainfall_72h = Column(Float, nullable=True)  # mm
    rainfall_intensity = Column(Float, nullable=True)  # mm/hr

    # Terrain Factors
    slope_angle = Column(Float, nullable=True)  # degrees
    elevation = Column(Float, nullable=True)  # meters
    soil_type = Column(String(100), nullable=True)

    # Data Source
    source = Column(String(255), nullable=True)  # GSI, NDMA, State Disaster Mgmt, News
    source_url = Column(String(500), nullable=True)
    reliability_score = Column(Float, default=0.5)  # 0-1

    # Notes
    description = Column(String(1000), nullable=True)
    notes = Column(String(500), nullable=True)

    # ML Training
    used_for_training = Column(Integer, default=1)  # boolean
    label = Column(Integer, default=1)  # 1=disaster occurred, 0=no disaster (for negative examples)

    def __repr__(self):
        return f"<HistoricalDisaster(id={self.id}, type='{self.event_type}', date='{self.event_date}')>"
