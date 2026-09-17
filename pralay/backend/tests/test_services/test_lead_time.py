"""
Unit Tests for Estimated Lead-Time Engine and Evacuation Routing
"""

import pytest
from app.services.lead_time_engine import LeadTimeEngine
from app.services.evacuation_service import EvacuationService
from app.utils.constants import RiskLevel, HazardType, LEAD_TIME_LABEL


def test_lead_time_estimation_labels_and_values():
    """Verify strictly enforced 'Estimated Lead Time' label and realistic projection"""
    lead_time, trend = LeadTimeEngine.estimate_lead_time(
        risk_level=RiskLevel.RED,
        compound_risk_score=88.0,
        river_level_m=6.5,
        river_rate_of_rise_m_hr=1.8,
        danger_river_level_m=7.0,
        rainfall_intensity_mm_hr=90.0,
        soil_moisture_pct=86.0,
        slope_degrees=34.0
    )

    # Must have explicit "Estimated Lead Time" label per PRD §12
    assert lead_time.label == LEAD_TIME_LABEL
    assert lead_time.minutes is not None
    assert 10 <= lead_time.minutes <= 45
    assert lead_time.hours is not None
    assert "CRITICAL" in lead_time.trend_description or "HIGH" in lead_time.trend_description


def test_evacuation_routing_avoids_flood_plains():
    """Verify shelter selection filters out shelters located in active flood plains"""
    candidate_shelters = [
        {"id": 1, "name": "Lowland River Shed", "latitude": 30.491, "longitude": 79.705, "capacity": 100, "is_available": True, "is_in_flood_plain": True},
        {"id": 2, "name": "Elevated School Shelter", "latitude": 30.493, "longitude": 79.707, "capacity": 300, "is_available": True, "is_in_flood_plain": False}
    ]

    selected = EvacuationService.find_nearest_available_shelter(
        village_lat=30.490,
        village_lon=79.704,
        candidate_shelters=candidate_shelters
    )
    assert selected is not None
    assert selected['id'] == 2  # Must pick elevated shelter not in flood plain
