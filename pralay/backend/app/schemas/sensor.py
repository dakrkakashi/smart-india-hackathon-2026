"""
Sensor Pydantic Schemas
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.models.sensor import SensorType, SensorStatus


class SensorBase(BaseModel):
    sensor_id: str
    region_id: Optional[int] = None
    sensor_type: SensorType
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation: Optional[float] = None
    unit: Optional[str] = None
    sampling_interval_sec: int = 300
    warning_threshold: Optional[float] = None
    critical_threshold: Optional[float] = None


class SensorCreate(SensorBase):
    pass


class SensorStatusUpdate(BaseModel):
    status: SensorStatus
    battery_level: Optional[float] = None
    signal_strength: Optional[int] = None
    firmware_version: Optional[str] = None


class SensorResponse(SensorBase):
    id: int
    status: SensorStatus
    battery_level: Optional[float] = None
    signal_strength: Optional[int] = None
    last_reading_value: Optional[float] = None
    last_reading_time: Optional[datetime] = None
    is_operational: bool = True
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
