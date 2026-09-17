"""
Scenario Testing & Demo Router
Exposes the 12-Step PRD §23 Flash Flood Demonstration Scenario
"""

from fastapi import APIRouter, Query
from typing import List, Dict, Any

from iot.simulator.flood_scenario import FloodScenarioSimulator

router = APIRouter(prefix="/scenarios", tags=["Demonstration Scenarios"])


@router.post("/run-12-step")
async def run_12_step_demo(village_id: int = Query(1, description="Target pilot village ID (default 1: Raini)")):
    """
    Executes end-to-end 12-step flash flood simulation scenario strictly following PRD §23.
    Demonstrates:
    Rainfall surge -> Soil moisture saturation -> River level rise -> Compound Risk calculation
    -> GREEN to RED transition -> Estimated Lead Time (35 mins) -> Evacuation route & shelter recommendation
    -> Multi-channel authority alert & citizen plain-language warning.
    """
    simulator = FloodScenarioSimulator(target_village_id=village_id)
    steps = simulator.run_12_step_simulation()
    return {
        "status": "COMPLETED",
        "scenario_name": "PRD §23 Flash Flood & Landslide Compound Escalation",
        "target_village_id": village_id,
        "total_steps": len(steps),
        "steps": steps
    }
