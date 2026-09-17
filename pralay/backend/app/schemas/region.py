"""
Region & Village Pydantic Schemas
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.models.region import RegionType, VulnerabilityLevel


class RegionBase(BaseModel):
    name: str
    code: str
    region_type: RegionType = RegionType.VILLAGE
    parent_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area_sq_km: Optional[float] = None
    elevation_mean: Optional[float] = None
    population: Optional[int] = None
    households: Optional[int] = None
    vulnerability_score: float = 0.0
    vulnerability_level: VulnerabilityLevel = VulnerabilityLevel.LOW


class RegionCreate(RegionBase):
    pass


class VillageDetail(RegionBase):
    id: int
    elevation_min: Optional[float] = None
    elevation_max: Optional[float] = None
    historical_flood_count: int = 0
    historical_landslide_count: int = 0
    last_disaster_date: Optional[str] = None
    evacuation_shelters_count: int = 0
    hospitals_count: int = 0
    roads_accessible: int = 1
    data_source: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class RegionResponse(RegionBase):
    id: int
    full_path: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
