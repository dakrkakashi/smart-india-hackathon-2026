"""
Integration Tests for PRALAYADARSHI API V1 Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_and_health():
    """Verify health endpoints and 4 North Star capabilities"""
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert len(data["north_star_capabilities"]) == 4

    h_res = client.get("/health")
    assert h_res.status_code == 200
    assert h_res.json()["alert_fatigue_cooldown_min"] == 30


def test_regions_endpoints():
    """Verify listing and detail for pilot villages"""
    res = client.get("/api/v1/regions")
    assert res.status_code == 200
    villages = res.json()
    assert len(villages) >= 5
    assert any(v["name"] == "Raini" for v in villages)

    res_single = client.get("/api/v1/regions/1")
    assert res_single.status_code == 200
    assert res_single.json()["name"] == "Raini"


def test_predictions_endpoint():
    """Verify compound predictions provide all 4 North Star fields"""
    res = client.get("/api/v1/predictions/1")
    assert res.status_code == 200
    data = res.json()

    # 1. WHERE
    assert data["village_name"] == "Raini"
    assert "latitude" in data and "longitude" in data

    # 2. HOW SEVERE
    assert data["risk_level"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
    assert 0.0 <= data["compound_risk_score"] <= 100.0

    # 3. HOW SOON
    assert "lead_time" in data
    assert data["lead_time"]["label"] == "Estimated Lead Time"

    # 4. WHAT NOW
    assert "action" in data
    assert data["action"]["action"] is not None
    assert data["action"]["nearest_shelter_name"] is not None


def test_citizen_alert_card():
    """Verify simplified citizen alert card per PRD §18"""
    res = client.get("/api/v1/alerts/citizen/1")
    assert res.status_code == 200
    card = res.json()
    assert "village_name" in card
    assert "action_directive" in card
    assert "assigned_shelter" in card
    assert "emergency_contact" in card


def test_evacuation_routes_and_shelters():
    """Verify evacuation routing avoiding hazard sectors"""
    res_shelters = client.get("/api/v1/evacuations/shelters")
    assert res_shelters.status_code == 200
    shelters = res_shelters.json()
    assert len(shelters) >= 4

    res_route = client.get("/api/v1/evacuations/route/1")
    assert res_route.status_code == 200
    route = res_route.json()
    assert "route_id" in route
    assert len(route["waypoints"]) >= 2
    assert "avoid_sectors" in route


def test_dashboard_summary():
    """Verify control room multi-district aggregate overview"""
    res = client.get("/api/v1/dashboard/summary")
    assert res.status_code == 200
    dash = res.json()
    assert "risk_summary" in dash
    assert "sensor_summary" in dash
    assert dash["risk_summary"]["total_villages"] >= 5


def test_12_step_demo_scenario():
    """Verify execution of PRD §23 12-step scenario demonstration"""
    res = client.post("/api/v1/scenarios/run-12-step?village_id=1")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "COMPLETED"
    assert body["total_steps"] == 12
    # Verify Step 7 displays 35 minute estimated lead time per PRD §23
    step7 = body["steps"][6]
    assert step7["step"] == 7
    assert step7["assessment"]["risk_level"] == "RED"
    assert step7["assessment"]["estimated_lead_time_minutes"] == 35


def test_sensor_ingestion_validation():
    """Verify telemetry ingestion and PRD §8 bounds validation"""
    # Valid reading
    valid_payload = {
        "sensor_id": "SN-RAIN-01",
        "sensor_type": "rainfall",
        "value": 42.5,
        "unit": "mm/h"
    }
    res_valid = client.post("/api/v1/sensors/readings", json=valid_payload)
    assert res_valid.status_code == 201

    # Invalid out-of-bounds reading (> 300 mm/hr limit)
    invalid_payload = {
        "sensor_id": "SN-RAIN-01",
        "sensor_type": "rainfall",
        "value": 999.0,
        "unit": "mm/h"
    }
    res_inv = client.post("/api/v1/sensors/readings", json=invalid_payload)
    assert res_inv.status_code == 422
