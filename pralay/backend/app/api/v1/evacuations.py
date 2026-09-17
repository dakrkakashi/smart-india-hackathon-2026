"""
Evacuation Planning & Shelters API Router
Implements PRD §15 Safe Shelter Assignment & Hazard-Avoidance Routing
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any

from app.schemas.shelter import ShelterResponse
from app.services.evacuation_service import EvacuationService
from data.scripts.seed_regions import get_pilot_villages, get_pilot_shelters

router = APIRouter(prefix="/evacuations", tags=["Evacuation & Shelters"])


@router.get("/shelters", response_model=List[ShelterResponse])
async def list_shelters(region_id: Optional[int] = Query(None)):
    """List all disaster relief shelters, capacities, and availability"""
    shelters = get_pilot_shelters()
    if region_id:
        shelters = [s for s in shelters if s.get('region_id') == region_id]
    
    # Calculate available capacity
    result = []
    for s in shelters:
        avail = max(0, s['capacity'] - s.get('current_occupancy', 0))
        result.append({**s, "available_capacity": avail})
    return result


@router.get("/route/{village_id}")
async def get_evacuation_route(village_id: int):
    """
    Computes real-time safest evacuation route to nearest available shelter
    avoiding riverbeds, low culverts, and active landslide slopes.
    """
    villages = get_pilot_villages()
    village = next((v for v in villages if v['id'] == village_id), None)
    if not village:
        raise HTTPException(status_code=404, detail=f"Village {village_id} not found")

    shelters = get_pilot_shelters()
    assigned = EvacuationService.find_nearest_available_shelter(
        village['latitude'], village['longitude'], shelters
    ) or shelters[0]

    route = EvacuationService.compute_safe_evacuation_route(
        village['name'], village['latitude'], village['longitude'], assigned
    )
    return route
