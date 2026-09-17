"""
Shelter Model for Disaster Evacuation and Relief Management
Corresponds to PRD §15 and §20
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.models import BaseModel


class Shelter(BaseModel):
    """
    Emergency shelter (school, community hall, primary health centre)
    providing refuge during flash floods or landslides.
    """
    __tablename__ = "shelters"

    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, index=True)
    shelter_type = Column(String(100), default="Community Hall")  # School, Community Centre, PHC, Stadium

    # Geographic reference
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True, index=True)
    region = relationship("Region", backref="shelters")
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)

    # Capacity & Availability
    capacity = Column(Integer, nullable=False, default=100)
    current_occupancy = Column(Integer, default=0)
    is_available = Column(Boolean, default=True, index=True)

    # Elevation & Safety characteristics
    elevation_meters = Column(Float, nullable=True)
    is_in_flood_plain = Column(Boolean, default=False)

    # Facilities & Logistics
    has_drinking_water = Column(Boolean, default=True)
    has_power_backup = Column(Boolean, default=True)
    has_medical_facility = Column(Boolean, default=False)
    contact_person = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Shelter(id={self.id}, name='{self.name}', capacity={self.capacity}, available={self.is_available})>"

    @property
    def available_capacity(self) -> int:
        return max(0, self.capacity - self.current_occupancy)
