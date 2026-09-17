"""
Region, Village, Ward models with PostGIS geometry support
Represents administrative boundaries and geographic regions
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import enum

from app.models import BaseModel


class RegionType(str, enum.Enum):
    """Types of administrative regions"""
    STATE = "state"
    DISTRICT = "district"
    BLOCK = "block"
    VILLAGE = "village"
    WARD = "ward"


class VulnerabilityLevel(str, enum.Enum):
    """Vulnerability classification for regions"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"


class Region(BaseModel):
    """
    Administrative region model with hierarchical structure
    Supports State > District > Block > Village/Ward hierarchy
    """

    __tablename__ = "regions"

    # Basic Info
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, index=True)  # Census code or unique identifier
    region_type = Column(SQLEnum(RegionType), nullable=False, index=True)

    # Hierarchy
    parent_id = Column(Integer, ForeignKey("regions.id"), nullable=True, index=True)
    parent = relationship("Region", remote_side="Region.id", backref="children")

    # Geospatial Data (PostGIS)
    # SRID 4326 = WGS84 (GPS coordinates)
    boundary = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326), nullable=True)
    centroid = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)

    # Geographic Info
    area_sq_km = Column(Float, nullable=True)
    elevation_min = Column(Float, nullable=True)  # meters
    elevation_max = Column(Float, nullable=True)  # meters
    elevation_mean = Column(Float, nullable=True)  # meters

    # Population & Vulnerability
    population = Column(Integer, nullable=True)
    households = Column(Integer, nullable=True)
    vulnerability_score = Column(Float, default=0.0)  # 0-1 scale
    vulnerability_level = Column(SQLEnum(VulnerabilityLevel), default=VulnerabilityLevel.LOW)

    # Risk Assessment
    historical_flood_count = Column(Integer, default=0)
    historical_landslide_count = Column(Integer, default=0)
    last_disaster_date = Column(String(50), nullable=True)  # ISO date string

    # Infrastructure
    has_early_warning_system = Column(Integer, default=0)  # boolean as int
    evacuation_shelters_count = Column(Integer, default=0)
    hospitals_count = Column(Integer, default=0)
    roads_accessible = Column(Integer, default=1)  # boolean as int

    # Metadata
    data_source = Column(String(255), nullable=True)  # e.g., "Census 2021", "ISRO Bhuvan"
    notes = Column(String(500), nullable=True)

    # Relationships
    sensors = relationship("Sensor", back_populates="region", cascade="all, delete-orphan")
    risk_zones = relationship("RiskZone", back_populates="region", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="region", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Region(id={self.id}, name='{self.name}', type='{self.region_type}')>"

    @property
    def full_path(self):
        """Get full hierarchical path (e.g., 'Uttarakhand > Chamoli > Gopeshwar')"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name
