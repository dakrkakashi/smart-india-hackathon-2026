"""
Estimated Lead-Time Engine
Answers North Star Question 3: HOW SOON?
Computes the projected response window before critical hazard impact per PRD §12
"""

from typing import Optional, Dict, Any, Tuple
from app.utils.constants import RiskLevel, HazardType, LEAD_TIME_LABEL, ACTION_RECOMMENDATIONS
from app.schemas.risk import EstimatedLeadTime, RecommendedAction


class LeadTimeEngine:
    """
    Hydrological and Geotechnical lead time estimation.
    Estimates minutes remaining until critical breach / landslide rupture occurs.
    """

    @classmethod
    def estimate_lead_time(
        cls,
        risk_level: RiskLevel,
        compound_risk_score: float,
        river_level_m: Optional[float],
        river_rate_of_rise_m_hr: Optional[float],
        danger_river_level_m: float = 7.0,
        rainfall_intensity_mm_hr: float = 0.0,
        rainfall_rate_of_change_mm_hr2: float = 0.0,  # intensity trend
        soil_moisture_pct: float = 40.0,
        soil_saturation_trend_pct_hr: float = 0.0,
        slope_degrees: float = 20.0,
        sensor_reliability: float = 0.90,
    ) -> Tuple[EstimatedLeadTime, str]:
        """
        Calculates estimated lead time in minutes and trend description.
        Returns: (EstimatedLeadTime, trend_description)
        """
        # Case 1: Green / Normal - No urgent lead time constraint
        if risk_level == RiskLevel.GREEN or compound_risk_score < 30.0:
            return (
                EstimatedLeadTime(
                    label=LEAD_TIME_LABEL,
                    minutes=None,
                    hours=None,
                    confidence_score=sensor_reliability,
                    trend_description="Conditions normal; no threshold breach expected in the next 12 hours."
                ),
                "Stable"
            )

        # Estimate time to critical river breach
        flood_lead_minutes = 9999
        if river_level_m is not None and river_rate_of_rise_m_hr and river_rate_of_rise_m_hr > 0.1:
            margin_m = max(0.0, danger_river_level_m - river_level_m)
            if margin_m <= 0:
                flood_lead_minutes = 15  # Already breaching; urgent remaining time for ground evacuation
            else:
                hrs_to_breach = margin_m / river_rate_of_rise_m_hr
                flood_lead_minutes = int(hrs_to_breach * 60)

        # Estimate time to critical landslide threshold (saturation >= 85% on steep slopes)
        landslide_lead_minutes = 9999
        if slope_degrees >= 25.0 and soil_saturation_trend_pct_hr > 0.5:
            moisture_margin = max(0.0, 85.0 - soil_moisture_pct)
            if moisture_margin <= 0:
                landslide_lead_minutes = 20  # Liquefaction imminent
            else:
                hrs_to_liquefaction = moisture_margin / soil_saturation_trend_pct_hr
                landslide_lead_minutes = int(hrs_to_liquefaction * 60)

        # Rainfall burst escalation factor
        rain_surge_penalty = 0
        if rainfall_rate_of_change_mm_hr2 > 10.0:  # cloudburst acceleration
            rain_surge_penalty = 15

        # Take minimum lead time across active threats
        active_estimates = [m for m in [flood_lead_minutes, landslide_lead_minutes] if m < 9000]

        if not active_estimates:
            # Fallback heuristic based on compound risk score
            if risk_level == RiskLevel.RED:
                estimated_minutes = max(15, int(45 - ((compound_risk_score - 80) * 1.5)))
            elif risk_level == RiskLevel.ORANGE:
                estimated_minutes = max(45, int(120 - ((compound_risk_score - 60) * 3.0)))
            else:  # YELLOW
                estimated_minutes = max(120, int(300 - ((compound_risk_score - 30) * 6.0)))
        else:
            estimated_minutes = max(10, min(active_estimates) - rain_surge_penalty)

        # Describe the velocity of escalation
        if estimated_minutes <= 30:
            trend = "CRITICAL: Rapid hazard surge underway. Threshold breach imminent."
        elif estimated_minutes <= 60:
            trend = "HIGH ALERT: Active escalation observed across sensors."
        elif estimated_minutes <= 180:
            trend = "MODERATE: Progressive water accumulation and soil saturation detected."
        else:
            trend = "WATCH: Gradual rise in environmental indices."

        return (
            EstimatedLeadTime(
                label=LEAD_TIME_LABEL,
                minutes=estimated_minutes,
                hours=round(estimated_minutes / 60.0, 2),
                confidence_score=sensor_reliability,
                trend_description=trend
            ),
            trend
        )

    @classmethod
    def generate_recommended_action(
        cls,
        risk_level: RiskLevel,
        primary_hazard: HazardType,
        village_name: str,
        affected_zone: str = "Zone A (Riverbank & Lower Terrace)",
        shelter_id: Optional[int] = 1,
        shelter_name: str = "Government Senior Secondary School - Safe Shelter 01",
        shelter_distance_km: float = 1.4,
    ) -> RecommendedAction:
        """
        Builds operational action directive for field teams and citizens
        """
        base_instruction = ACTION_RECOMMENDATIONS.get(risk_level, "Monitor local conditions.")

        if risk_level == RiskLevel.RED:
            action_text = f"URGENT: Evacuate {village_name} ({affected_zone}) immediately to {shelter_name}."
            priority = "URGENT"
            warnings = [
                "Do NOT cross swollen mountain streams or flooded causeways",
                "Stay clear of steep cut-slopes susceptible to debris slide",
                "Follow marked ridge pathway to shelter"
            ]
        elif risk_level == RiskLevel.ORANGE:
            action_text = f"PREPARE EVACUATION: Stage transport and move vulnerable citizens in {affected_zone} to {shelter_name}."
            priority = "HIGH"
            warnings = [
                "Inspect local culverts and stream flows",
                "Prepare emergency kit and communication devices"
            ]
        elif risk_level == RiskLevel.YELLOW:
            action_text = f"WATCH: Alert disaster management volunteers in {village_name}. Stand by for escalation."
            priority = "MEDIUM"
            warnings = ["Restrict non-essential travel along vulnerable riverbed roads"]
        else:
            action_text = f"NORMAL: Continue continuous environmental observation for {village_name}."
            priority = "LOW"
            warnings = []

        return RecommendedAction(
            action=action_text,
            priority=priority,
            affected_zone=affected_zone,
            nearest_shelter_id=shelter_id,
            nearest_shelter_name=shelter_name,
            shelter_distance_km=shelter_distance_km,
            evacuation_route_id=f"ROUTE-{village_name[:3].upper()}-01",
            safe_path_instructions=f"Proceed uphill along Main PWD Ridge Road toward {shelter_name}. Avoid valley trail.",
            special_warnings=warnings
        )
