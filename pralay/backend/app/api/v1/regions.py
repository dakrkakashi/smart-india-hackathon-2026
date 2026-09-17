"""
Regions and Villages API Router
Provides spatial, demographic, and terrain metadata for monitored pilot locations
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.schemas.region import VillageDetail
from data.scripts.seed_regions import get_pilot_villages, get_pilot_shelters

router = APIRouter(prefix="/regions", tags=["Regions & Villages"])


@router.get("", response_model=List[VillageDetail])
async def list_regions(district: Optional[str] = Query(None, description="Filter by district")):
    """List all monitored pilot villages/regions"""
    villages = get_pilot_villages()
    if district:
        villages = [v for v in villages if v['district'].lower() == district.lower()]
    return villages


@router.get("/{village_id}", response_model=VillageDetail)
async def get_region(village_id: int):
    """Retrieve detailed profile of a specific village"""
    villages = get_pilot_villages()
    for v in villages:
        if v['id'] == village_id:
            return v
    raise HTTPException(status_code=404, detail=f"Village with ID {village_id} not found")
