"""
IoT Sensor models for field devices
Tracks sensor registration, location, and health status
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import enum

from app.models import BaseModel


class SensorType(str, enum.Enum):
    """Types of sensors deployed in the field"""
    SOIL_MOISTURE = "soil_moisture"
    RAIN_GAUGE = "rain_gauge"
    WATER_LEVEL = "water_level"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    SLOPE_INCLINOMETER = "slope_inclinometer"
    PORE_PRESSURE = "pore_pressure"


class SensorStatus(str, enum.Enum):
    """Operational status of sensor"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    FAULTY = "faulty"
    DECOMMISSIONED = "decommissioned"


class Sensor(BaseModel):
    """
    IoT Sensor device registration and metadata
    Each sensor is deployed at a specific location within a region
    """

    __tablename__ = "sensors"

    # Basic Info
    sensor_id = Column(String(100), unique=True, nullable=False, index=True)  # Device unique ID
    name = Column(String(255), nullable=False)
    sensor_type = Column(SQLEnum(SensorType), nullable=False, index=True)
    manufacturer = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)

    # Location
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, index=True)
    region = relationship("Region", back_populates="sensors")

    # PostGIS location (exact GPS coordinates)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    latitude = Column(Float, nullable=False)  # Denormalized for easy access
    longitude = Column(Float, nullable=False)  # Denormalized for easy access
    elevation = Column(Float, nullable=True)  # meters above sea level

    # Installation Details
    installation_date = Column(String(50), nullable=True)  # ISO date
    installed_by = Column(String(255), nullable=True)

    # Status & Health
    status = Column(SQLEnum(SensorStatus), default=SensorStatus.ACTIVE, index=True)
    battery_level = Column(Float, nullable=True)  # 0-100 percentage
    signal_strength = Column(Float, nullable=True)  # dBm or percentage
    last_reading_at = Column(String(50), nullable=True)  # ISO datetime
    last_heartbeat_at = Column(String(50), nullable=True)  # ISO datetime

    # Connectivity
    connection_type = Column(String(50), default="mqtt")  # mqtt, http, lorawan
    mqtt_topic = Column(String(255), nullable=True)
    reporting_interval = Column(Integer, default=300)  # seconds (default 5 min)

    # Calibration
    calibration_date = Column(String(50), nullable=True)
    calibration_offset = Column(Float, default=0.0)
    calibration_multiplier = Column(Float, default=1.0)

    # Power Management
    is_solar_powered = Column(Integer, default=1)  # boolean
    power_backup_hours = Column(Integer, nullable=True)

    # Metadata
    notes = Column(String(500), nullable=True)

    # Relationships
    readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sensor(id={self.id}, sensor_id='{self.sensor_id}', type='{self.sensor_type}', status='{self.status}')>"

    @property
    def is_online(self):
        """Check if sensor is reporting (based on last_heartbeat_at)"""
        # Implementation will check if last_heartbeat_at is within acceptable threshold
        return self.status == SensorStatus.ACTIVE and self.last_heartbeat_at is not None
