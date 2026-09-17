"""
Multi-Channel Notification Dispatch Service
Translates complex predictions into plain-language citizen warnings and authority dispatches
Per PRD §18 (Citizen Interface) and §14 (Notification Dispatch)
"""

from typing import Dict, Any, Optional
from datetime import datetime
from app.utils.constants import RiskLevel, HazardType
from app.schemas.alert import CitizenAlertCard


class NotificationService:
    """Dispatches alerts across SMS, Push, Web, and siren gateways"""

    @staticmethod
    def build_citizen_alert_card(
        village_name: str,
        risk_level: RiskLevel,
        primary_hazard: HazardType,
        estimated_lead_time_min: Optional[int],
        shelter_name: str,
        safe_path_summary: str = "Use marked Upper Ridge Trail",
        control_room_phone: str = "1077 / 01372-252107"
    ) -> CitizenAlertCard:
        """
        Builds clear, jargon-free citizen warning card strictly per PRD §18:
        'RED ALERT / FLASH FLOOD RISK / Your village: XYZ / Estimated lead time: 35 mins / ACTION: Move to designated safe shelter'
        """
        # Hazard title
        if primary_hazard == HazardType.FLASH_FLOOD:
            haz_title = "FLASH FLOOD RISK"
        elif primary_hazard == HazardType.LANDSLIDE:
            haz_title = "LANDSLIDE / SLOPE FAILURE RISK"
        elif primary_hazard == HazardType.COMPOUND:
            haz_title = "COMPOUND FLASH FLOOD & LANDSLIDE RISK"
        else:
            haz_title = "WEATHER ADVISORY"

        # Severity header
        sev_label = f"{risk_level.value} ALERT"

        # Action directive
        if risk_level == RiskLevel.RED:
            directive = "IMMEDIATE EVACUATION REQUIRED: Move to designated safe shelter immediately."
            avoid_text = "Avoid riverbanks, low-lying bridges, and steep roadside slopes."
        elif risk_level == RiskLevel.ORANGE:
            directive = "PREPARE TO EVACUATE: Gather emergency items and assist elderly/children to safe high ground."
            avoid_text = "Stay away from stream beds and active drainage gullies."
        elif risk_level == RiskLevel.YELLOW:
            directive = "STAY ALERT: Monitor local weather and keep battery radios/phones charged."
            avoid_text = "Do not cross fast-flowing mountain runoffs."
        else:
            directive = "NORMAL CONDITIONS: Continuous monitoring active."
            avoid_text = "None"

        lead_time_str = f"{estimated_lead_time_min} minutes" if estimated_lead_time_min else "12+ hours"

        return CitizenAlertCard(
            severity_label=sev_label,
            hazard_title=haz_title,
            village_name=village_name,
            estimated_lead_time=lead_time_str,
            action_directive=directive,
            assigned_shelter=shelter_name,
            evacuation_advice=f"{safe_path_summary}. {avoid_text}",
            emergency_contact=f"District Disaster Control Room: {control_room_phone}",
            timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        )

    @staticmethod
    def format_sms_payload(
        village_name: str,
        risk_level: RiskLevel,
        lead_time_min: Optional[int],
        shelter_name: str
    ) -> str:
        """TRAI 160-character compliant SMS for Indian mobile networks"""
        lead_str = f"~{lead_time_min}m" if lead_time_min else "N/A"
        return (
            f"[NDMA ALERT] {risk_level.value} Warning for {village_name}. "
            f"Est Lead Time: {lead_str}. Evacuate immediately to {shelter_name}. "
            f"Dial 1077 for emergency assistance."
        )[:160]

    @classmethod
    def dispatch_all_channels(
        cls,
        village_name: str,
        risk_level: RiskLevel,
        primary_hazard: HazardType,
        estimated_lead_time_min: Optional[int],
        shelter_name: str
    ) -> Dict[str, Any]:
        """Simulates end-to-end multi-channel dispatch"""
        citizen_card = cls.build_citizen_alert_card(
            village_name, risk_level, primary_hazard, estimated_lead_time_min, shelter_name
        )
        sms_text = cls.format_sms_payload(
            village_name, risk_level, estimated_lead_time_min, shelter_name
        )

        # In production this integrates with MSG91 / CDAC / Firebase / sirens
        return {
            "dispatched_at": datetime.utcnow().isoformat(),
            "channels": {
                "sms": {"status": "SUCCESS", "message": sms_text, "recipient_count": 480},
                "fcm_push": {"status": "SUCCESS", "title": citizen_card.severity_label, "delivered": 312},
                "siren_trigger": {"status": "TRIGGERED" if risk_level == RiskLevel.RED else "STANDBY"},
                "dashboard_broadcast": {"status": "STREAMED_TO_OFFICIALS"}
            },
            "citizen_card": citizen_card.dict()
        }
