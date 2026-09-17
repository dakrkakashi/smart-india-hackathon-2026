"""
Shelter Pydantic Schemas
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ShelterBase(BaseModel):
    name: str
    code: str
    shelter_type: str = "Community Hall"
    region_id: Optional[int] = None
    latitude: float
    longitude: float
    capacity: int = 100
    current_occupancy: int = 0
    is_available: bool = True
    elevation_meters: Optional[float] = None
    has_drinking_water: bool = True
    has_power_backup: bool = True
    has_medical_facility: bool = False
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None


class ShelterCreate(ShelterBase):
    pass


class ShelterResponse(ShelterBase):
    id: int
    available_capacity: int = 100

    model_config = ConfigDict(from_attributes=True)
