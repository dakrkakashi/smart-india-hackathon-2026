"""
Authority Dashboard Summary Schemas
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.risk import RiskAssessment
from app.schemas.alert import AlertResponse


class RiskCountByLevel(BaseModel):
    green: int = 0
    yellow: int = 0
    orange: int = 0
    red: int = 0
    total_villages: int = 0


class SensorHealthSummary(BaseModel):
    total_sensors: int = 0
    online_count: int = 0
    offline_count: int = 0
    degraded_count: int = 0
    availability_pct: float = 100.0


class DashboardSummary(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    risk_summary: RiskCountByLevel
    sensor_summary: SensorHealthSummary
    active_alerts_count: int = 0
    villages_in_critical_state: List[str] = Field(default_factory=list)
    recent_alerts: List[AlertResponse] = Field(default_factory=list)
    monitored_districts: List[str] = Field(default_factory=lambda: ["Chamoli", "Rudraprayag"])
