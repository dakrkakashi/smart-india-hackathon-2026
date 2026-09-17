"""
Sensors and Telemetry Ingestion Router
Validates incoming IoT sensor readings and exposes telemetry status
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.schemas.sensor import SensorResponse
from app.schemas.reading import ReadingIngest, ReadingResponse
from data.scripts.seed_regions import get_pilot_sensors
from iot.gateway.data_validator import SensorDataValidator

router = APIRouter(prefix="/sensors", tags=["Sensors & Telemetry"])

# Global validator instance for health tracking
validator = SensorDataValidator(timeout_minutes=15)

# In-memory readings log for demonstration and charting
_readings_history: List[Dict[str, Any]] = []


@router.get("", response_model=List[Dict[str, Any]])
async def list_sensors(
    region_id: Optional[int] = Query(None, description="Filter by region/village ID"),
    sensor_type: Optional[str] = Query(None, description="Filter by type (rainfall, soil_moisture, water_level)")
):
    """List all deployed IoT sensors with operational health status"""
    sensors = get_pilot_sensors()
    timeouts = validator.check_timeouts()

    result = []
    for s in sensors:
        if region_id and s['region_id'] != region_id:
            continue
        if sensor_type and s['type'].lower() != sensor_type.lower():
            continue
        
        sid = s['sensor_id']
        current_status = timeouts.get(sid, "ONLINE")

        result.append({
            "id": hash(sid) % 100000,
            "sensor_id": sid,
            "name": s['name'],
            "sensor_type": s['type'],
            "region_id": s['region_id'],
            "latitude": s['lat'],
            "longitude": s['lng'],
            "unit": s['unit'],
            "status": current_status,
            "is_operational": current_status == "ONLINE",
            "battery_level": 94.5
        })
    return result


@router.post("/readings", status_code=status.HTTP_201_CREATED)
async def ingest_reading(payload: ReadingIngest):
    """
    Ingest single sensor reading from field IoT gateway.
    Applies outlier and boundary validation per PRD §8.
    """
    is_valid, msg, state = validator.validate_reading(
        sensor_id=payload.sensor_id,
        sensor_type=payload.sensor_type,
        value=payload.value,
        timestamp=payload.timestamp
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Telemetry validation failed: {msg}"
        )

    record = {
        "sensor_id": payload.sensor_id,
        "sensor_type": payload.sensor_type,
        "value": payload.value,
        "unit": payload.unit,
        "timestamp": payload.timestamp.isoformat(),
        "is_valid": True
    }
    _readings_history.append(record)
    if len(_readings_history) > 5000:
        _readings_history.pop(0)

    return {"status": "INGESTED", "sensor_id": payload.sensor_id, "timestamp": payload.timestamp}


@router.get("/{sensor_id}/history")
async def get_sensor_history(sensor_id: str, limit: int = 50):
    """Retrieve historical telemetry time-series for charting"""
    records = [r for r in _readings_history if r['sensor_id'] == sensor_id]
    return records[-limit:]
