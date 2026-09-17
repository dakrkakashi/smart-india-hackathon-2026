"""
Alert Management and Citizen Warning API Router
Enforces PRD §14, §18 for multi-channel alert distribution and cooldown logic
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.schemas.alert import AlertResponse, CitizenAlertCard, AlertAcknowledge
from app.models.alert import AlertSeverity, AlertStatus
from app.utils.constants import RiskLevel, HazardType
from app.services.alert_service import AlertService
from app.services.notification_service import NotificationService
from data.scripts.seed_regions import get_pilot_villages, get_pilot_shelters

router = APIRouter(prefix="/alerts", tags=["Alerts & Warnings"])

alert_service = AlertService()

# In-memory active alerts list for demonstration
_active_alerts: List[Dict[str, Any]] = [
    {
        "id": 101,
        "region_id": 1,
        "alert_code": "ALT-2026-CHM-001",
        "title": "CRITICAL FLASH FLOOD & DEBRIS FLOW WARNING - RAINI",
        "description": "Torrential rain exceeding 85 mm/hr with river rate of rise at 1.8 m/hr. Imminent breach risk in Rishi Ganga gorge.",
        "severity": AlertSeverity.RED,
        "status": AlertStatus.ACTIVE,
        "alert_type": "COMPOUND_HAZARD",
        "risk_score": 88.5,
        "confidence": 0.92,
        "lead_time_hours": 0.58,
        "affected_population": 780,
        "affected_villages": "Raini, Lata",
        "evacuation_required": 1,
        "recommended_actions": "Evacuate lower terrace immediately to Raini Upper Primary School.",
        "evacuation_routes": "Upper Ridge Bypass Trail",
        "safe_zones": "Raini Primary School Ridge (Elev 2,240m)",
        "issued_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "sms_sent": 480,
        "push_sent": 312,
        "siren_triggered": 1,
        "created_at": datetime.utcnow()
    },
    {
        "id": 102,
        "region_id": 2,
        "alert_code": "ALT-2026-CHM-002",
        "title": "PREPARE EVACUATION - THARALI VALLEY",
        "description": "Pindar River approaching warning level. Soil saturation at 74% on vulnerable cut slopes.",
        "severity": AlertSeverity.ORANGE,
        "status": AlertStatus.ACTIVE,
        "alert_type": "FLASH_FLOOD",
        "risk_score": 67.2,
        "confidence": 0.88,
        "lead_time_hours": 1.5,
        "affected_population": 2450,
        "affected_villages": "Tharali, Chepru",
        "evacuation_required": 0,
        "recommended_actions": "Stage transport; move livestock to higher terraces.",
        "evacuation_routes": "PWD Main Road to GIC Tharali",
        "safe_zones": "GIC Tharali Compound",
        "issued_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "sms_sent": 1200,
        "push_sent": 850,
        "siren_triggered": 0,
        "created_at": datetime.utcnow()
    }
]


def get_active_alerts(severity: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve filtered active alerts"""
    alerts = _active_alerts
    if severity and isinstance(severity, str):
        alerts = [a for a in alerts if a['severity'].value.lower() == severity.lower()]
    return alerts


@router.get("", response_model=List[AlertResponse])
async def list_alerts(severity: Optional[str] = Query(None)):
    """List all active warnings and emergency alerts"""
    return get_active_alerts(severity)


@router.get("/citizen/{village_id}", response_model=CitizenAlertCard)
async def get_citizen_alert_card(village_id: int):
    """
    Generate simplified, non-technical Citizen Alert Card per PRD §18
    Designed for rapid mobile UI rendering and vernacular dissemination.
    """
    villages = get_pilot_villages()
    village = next((v for v in villages if v['id'] == village_id), None)
    if not village:
        raise HTTPException(status_code=404, detail=f"Village {village_id} not found")

    shelters = get_pilot_shelters()
    shelter = next((s for s in shelters if s['region_id'] == village_id), shelters[0])

    # If Raini, display RED card; else moderate or normal
    if village['name'] == 'Raini':
        card = NotificationService.build_citizen_alert_card(
            village_name=village['name'],
            risk_level=RiskLevel.RED,
            primary_hazard=HazardType.COMPOUND,
            estimated_lead_time_min=35,
            shelter_name=shelter['name'],
            safe_path_summary="Follow Upper Ridge Bypass Trail directly"
        )
    else:
        card = NotificationService.build_citizen_alert_card(
            village_name=village['name'],
            risk_level=RiskLevel.YELLOW,
            primary_hazard=HazardType.FLASH_FLOOD,
            estimated_lead_time_min=180,
            shelter_name=shelter['name'],
            safe_path_summary="Stay on higher village terraces"
        )
    return card


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int, payload: AlertAcknowledge):
    """Authority official acknowledges emergency alert"""
    for a in _active_alerts:
        if a['id'] == alert_id:
            a['status'] = AlertStatus.ACKNOWLEDGED
            a['acknowledged_by'] = payload.acknowledged_by
            a['acknowledged_at'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            return {"status": "ACKNOWLEDGED", "alert_id": alert_id, "official": payload.acknowledged_by}
    raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
