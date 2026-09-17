"""
Sensor Reading Ingestion Schemas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ReadingIngest(BaseModel):
    """Payload sent by IoT gateway or sensor simulator"""
    sensor_id: str
    sensor_type: str  # rainfall, soil_moisture, water_level, etc.
    value: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    unit: Optional[str] = None
    battery: Optional[float] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class BatchReadingIngest(BaseModel):
    readings: List[ReadingIngest]


class ReadingResponse(BaseModel):
    id: Optional[int] = None
    sensor_id: str
    timestamp: datetime
    value: float
    is_valid: bool = True
    anomaly_flag: int = 0

    model_config = ConfigDict(from_attributes=True)
