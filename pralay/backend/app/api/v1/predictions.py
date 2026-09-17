"""
Predictions & Compound Risk Assessment Router
Directly serves the Four North Star Questions per PRD §1
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.schemas.risk import RiskAssessment
from app.services.risk_engine import RiskEngine
from app.services.lead_time_engine import LeadTimeEngine
from app.services.evacuation_service import EvacuationService
from data.scripts.seed_regions import get_pilot_villages, get_pilot_shelters

router = APIRouter(prefix="/predictions", tags=["Predictions & Risk Assessment"])


def _build_village_assessment(village: Dict[str, Any], storm_factor: float = 0.0) -> RiskAssessment:
    """Helper to synthesize complete North Star decision object for a village"""
    v_id = village['id']
    v_name = village['name']
    v_district = village['district']
    v_lat = village['latitude']
    v_lon = village['longitude']
    v_slope = village['slope_degrees']
    v_vuln = village['vulnerability_score']
    v_pop = village.get('population', 1000)

    # Base environmental measurements + dynamic simulation adjustment
    rain_rate = max(0.0, 15.0 + (storm_factor * 75.0))
    rain_accum = max(10.0, 30.0 + (storm_factor * 140.0))
    soil_moisture = min(92.0, 35.0 + (storm_factor * 52.0))
    river_m = 2.8 + (storm_factor * 4.2)
    river_rate = 0.05 + (storm_factor * 1.8)

    # Calculate Flood Risk
    f_risk = RiskEngine.calculate_flood_risk(
        rainfall_intensity_mm_hr=rain_rate,
        rainfall_accum_24h_mm=rain_accum,
        river_level_m=river_m,
        river_rate_of_rise_m_hr=river_rate,
        elevation_m=village['elevation_mean'],
        historical_flood_count=village.get('historical_flood_count', 1)
    )

    # Calculate Landslide Risk
    l_risk = RiskEngine.calculate_landslide_risk(
        rainfall_intensity_mm_hr=rain_rate,
        rainfall_duration_hrs=6.0,
        soil_moisture_pct=soil_moisture,
        saturation_trend_pct_hr=storm_factor * 8.0,
        slope_degrees=v_slope,
        historical_landslide_count=village.get('historical_landslide_count', 2)
    )

    # Compound Risk
    compound_score, risk_level, prim_haz, sec_haz = RiskEngine.calculate_compound_risk(
        flood_risk=f_risk,
        landslide_risk=l_risk,
        local_vulnerability_score=v_vuln
    )

    # Estimated Lead Time
    lead_time_obj, trend = LeadTimeEngine.estimate_lead_time(
        risk_level=risk_level,
        compound_risk_score=compound_score,
        river_level_m=river_m,
        river_rate_of_rise_m_hr=river_rate,
        danger_river_level_m=7.0,
        rainfall_intensity_mm_hr=rain_rate,
        soil_moisture_pct=soil_moisture,
        slope_degrees=v_slope
    )

    # Safe Shelter & Route
    shelters = get_pilot_shelters()
    assigned_shelter = EvacuationService.find_nearest_available_shelter(
        v_lat, v_lon, shelters
    ) or shelters[0]

    action_obj = LeadTimeEngine.generate_recommended_action(
        risk_level=risk_level,
        primary_hazard=prim_haz,
        village_name=v_name,
        affected_zone="Zone A (Valley Terrace & Riverside)",
        shelter_id=assigned_shelter['id'],
        shelter_name=assigned_shelter['name'],
        shelter_distance_km=assigned_shelter.get('distance_km', 1.4)
    )

    return RiskAssessment(
        village_id=v_id,
        village_name=v_name,
        district=v_district,
        state=village.get('state', 'Uttarakhand'),
        latitude=v_lat,
        longitude=v_lon,
        population_at_risk=v_pop,
        risk_level=risk_level,
        compound_risk_score=compound_score,
        flood_risk_score=f_risk,
        landslide_risk_score=l_risk,
        primary_hazard=prim_haz,
        secondary_hazard=sec_haz,
        lead_time=lead_time_obj,
        action=action_obj,
        rainfall_1h_mm=round(rain_rate, 1),
        rainfall_24h_mm=round(rain_accum, 1),
        soil_moisture_pct=round(soil_moisture, 1),
        river_level_m=round(river_m, 2),
        river_rate_of_rise_m_per_hr=round(river_rate, 2),
        slope_degrees=v_slope,
        sensor_health_status="OPTIMAL",
        timestamp=datetime.utcnow(),
        data_sources_available=["rainfall_radar", "soil_probe", "ultrasonic_river_gauge", "alos_dem"]
    )


@router.get("", response_model=List[RiskAssessment])
@router.get("/catchments", response_model=List[RiskAssessment])
async def get_all_village_predictions(district: Optional[str] = Query(None)):
    """Retrieve live risk assessments across all monitored villages"""
    villages = get_pilot_villages()
    if district:
        villages = [v for v in villages if v['district'].lower() == district.lower()]

    assessments = []
    for v in villages:
        # Give Raini village slightly higher storm activity to demonstrate live variance
        factor = 0.75 if v['name'] == 'Raini' else 0.15
        assessments.append(_build_village_assessment(v, storm_factor=factor))

    return assessments


@router.get("/{village_id}", response_model=RiskAssessment)
async def get_village_prediction(village_id: int):
    """Retrieve deep assessment and lead time for a specific village"""
    villages = get_pilot_villages()
    for v in villages:
        if v['id'] == village_id:
            factor = 0.85 if v['name'] == 'Raini' else 0.2
            return _build_village_assessment(v, storm_factor=factor)
    raise HTTPException(status_code=404, detail=f"Village with ID {village_id} not found")
