"""
Base model classes, common mixins, and unified entity exports
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr

from app.database import Base


class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps"""

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class BaseModel(Base, TimestampMixin):
    """Base model with common fields"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


# Export all models for ease of importing across the app
from app.models.region import Region, RegionType, VulnerabilityLevel
from app.models.sensor import Sensor, SensorType, SensorStatus
from app.models.reading import SensorReading, AggregatedReading
from app.models.risk_zone import RiskZone, RiskLevel
from app.models.alert import Alert, AlertSeverity, AlertStatus
from app.models.historical import HistoricalDisaster, DisasterType
from app.models.terrain import TerrainGrid, DrainageBasin
from app.models.shelter import Shelter
from app.models.user import User, UserRole

__all__ = [
    "Base",
    "BaseModel",
    "TimestampMixin",
    "Region",
    "RegionType",
    "VulnerabilityLevel",
    "Sensor",
    "SensorType",
    "SensorStatus",
    "SensorReading",
    "AggregatedReading",
    "RiskZone",
    "RiskLevel",
    "Alert",
    "AlertSeverity",
    "AlertStatus",
    "HistoricalDisaster",
    "DisasterType",
    "TerrainGrid",
    "DrainageBasin",
    "Shelter",
    "User",
    "UserRole",
]
