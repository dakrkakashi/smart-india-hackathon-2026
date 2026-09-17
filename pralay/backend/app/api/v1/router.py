"""
Unified V1 API Router aggregation
Mounts all sub-routers under /api/v1
"""

from fastapi import APIRouter

from app.api.v1.regions import router as regions_router
from app.api.v1.sensors import router as sensors_router
from app.api.v1.predictions import router as predictions_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.evacuations import router as evacuations_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.scenarios import router as scenarios_router

api_v1_router = APIRouter()

api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(predictions_router)
api_v1_router.include_router(alerts_router)
api_v1_router.include_router(evacuations_router)
api_v1_router.include_router(regions_router)
api_v1_router.include_router(sensors_router)
api_v1_router.include_router(scenarios_router)
