"""
Alert Pydantic Schemas
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.models.alert import AlertSeverity, AlertStatus


class AlertBase(BaseModel):
    region_id: int
    alert_code: str
    title: str
    description: str
    severity: AlertSeverity
    alert_type: str
    risk_score: float
    confidence: float = 0.85
    lead_time_hours: Optional[float] = None
    affected_population: int = 0
    affected_villages: Optional[str] = None
    evacuation_required: int = 0
    recommended_actions: Optional[str] = None
    evacuation_routes: Optional[str] = None
    safe_zones: Optional[str] = None


class AlertCreate(AlertBase):
    pass


class AlertAcknowledge(BaseModel):
    acknowledged_by: str
    notes: Optional[str] = None


class AlertResponse(AlertBase):
    id: int
    status: AlertStatus
    issued_at: str
    acknowledged_at: Optional[str] = None
    acknowledged_by: Optional[str] = None
    sms_sent: int = 0
    push_sent: int = 0
    siren_triggered: int = 0
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CitizenAlertCard(BaseModel):
    """Simplified, jargon-free citizen warning card per PRD §18"""
    severity_label: str  # RED ALERT, ORANGE WARNING, etc.
    hazard_title: str   # FLASH FLOOD RISK
    village_name: str
    estimated_lead_time: str  # "35 minutes"
    action_directive: str     # "Move to designated safe shelter immediately"
    assigned_shelter: str     # "Government Senior Secondary School - Shelter 02"
    evacuation_advice: str    # "Avoid riverside road and low-lying culverts"
    emergency_contact: str    # "1077 (District Disaster Control Room)"
    timestamp: str
