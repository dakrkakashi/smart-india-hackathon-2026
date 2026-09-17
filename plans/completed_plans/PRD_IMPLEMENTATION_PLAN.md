# PRALAYADARSHI Implementation Plan (per PRD)

## Feature Name
PRALAYADARSHI — Hyperlocal Compound-Risk & Evacuation Intelligence System (SIH PS 26192)

## Status
ACTIVE / MVP VALIDATED (Phases 0, 1, 2, 4, 5, 6, 7 Complete & Passing 14/14 Tests)

## Overview
Implementation plan derived from `plans/prd file` (Product Requirements Document). Builds on the technical architecture in `FLASH_FLOOD_PREDICTION_PLAN.md`, scoped and sequenced strictly per the PRD's functional requirements: SENSE → FUSE → ASSESS → PREDICT → ESTIMATE LEAD TIME → DECIDE → ALERT → EVACUATE → LEARN.

## Product Core (North Star)
The system answers the four PRD questions:
1. WHERE is the risk? (village-level / hyperlocal catchments)
2. HOW SEVERE? (Green/Yellow/Orange/Red compound risk)
3. HOW SOON? (Estimated Lead Time, physics-derived)
4. WHAT NOW? (Affected zone → Safe Shelter → Safe Ridge Route → Action)

## Key PRD Constraints & Rules
- **MVP risk model = transparent weighted model** (not a claimed trained AI).
- **Describe output as "estimated lead time"**, never a guaranteed warning time.
- Alert scale: GREEN (monitor) / YELLOW (preparedness) / ORANGE (prepare evacuation) / RED (immediate evacuation).
- Compound Risk = Flash Flood Risk + Landslide Risk + Local Vulnerability + Real-Time Conditions.
- Duplicate/alert fatigue control: suppress repeats per zone within 30-min cooldown period.
- Sensor failure → mark source unavailable; never silently treat missing data as normal.

---

## Architecture & Tech Stack
- **Backend:** Python FastAPI + SQLAlchemy + Pydantic v2
- **Frontend:** React + TypeScript + Vite, Lucide icons, Tailwind
- **Data:** PostgreSQL + PostGIS, TimescaleDB, GeoAlchemy2
- **IoT:** Telemetry validator, spike & duplicate detection, 12-Step PRD §23 scenario runner
- **Alerts:** Multi-channel schema, 30-min fatigue cooldown, Citizen Alert Card (PRD §18)

---

## Implementation Steps

### Phase 0 — PRD-First Scoping (Completed ✅)
- [x] 0.1 Read and baseline the PRD into implementation backlog; map every PRD section (§6–§25) to at least one task
  - File: `pralay/docs/PRODUCT_BACKLOG.md`
- [x] 0.2 Define the four core decision objects in code: RiskLevel (G/Y/O/R), RiskScore, EstimatedLeadTime, RecommendedAction
  - Files: `pralay/backend/app/utils/constants.py`, `pralay/backend/app/schemas/risk.py`
- [x] 0.3 Define MVP scope guardrail checklist (priority only to features answering the four north-star questions)
  - File: `pralay/docs/MVP_SCOPE.md`

### Phase 1 — MVP Prototype (Completed ✅)
- [x] 1A. Data Models: Shelter, User, Region, Sensor, Reading, RiskZone, Alert, Historical
  - Files: `pralay/backend/app/models/*.py`, `pralay/backend/app/schemas/*.py`
- [x] 1B. Pilot Village Database & GIS: 5 Pilot catchments in Chamoli & Rudraprayag (Raini, Tharali, Joshimath, Sonprayag, Ukhimath)
  - File: `pralay/data/scripts/seed_regions.py`
- [x] 1C. Risk Engine: Deterministic Flood (0–100), Landslide (0–100), Compound Risk (0–100) formulas
  - File: `pralay/backend/app/services/risk_engine.py`
- [x] 1D. Rainfall Input: Accumulation windows (1h, 3h, 6h, 24h, 72h) & spatial IDW interpolation
  - File: `pralay/backend/app/services/rainfall_service.py`
- [x] 1E. Lead-Time Engine: Explicit "Estimated Lead Time" labeling with rate-of-rise trend projection
  - File: `pralay/backend/app/services/lead_time_engine.py`
- [x] 1F. Alert Engine: Cooldown suppression (30-min window) and automatic hazard escalation
  - File: `pralay/backend/app/services/alert_service.py`
- [x] 1G. Evacuation Engine: Safe shelter filtering (excluding flood plain shelters) & hazard-avoidance ridge bypass routing
  - File: `pralay/backend/app/services/evacuation_service.py`
- [x] 1H. API Routers: `/regions`, `/sensors`, `/predictions`, `/alerts`, `/evacuations`, `/dashboard`, `/scenarios`
  - Files: `pralay/backend/app/api/v1/*.py`, `pralay/backend/app/main.py`

### Phase 2 — Multi-Source Fusion & IoT Validation (Completed ✅)
- [x] 2.1 Gateway validation (PRD §8): Physical limits, spike filtering, deduplication, timeout detection
  - File: `pralay/iot/gateway/data_validator.py`
- [x] 2.2 Telemetry Simulator: Realistic sensor simulation under mountain conditions
  - File: `pralay/iot/simulator/sensor_simulator.py`
- [x] 2.3 12-Step PRD §23 Scenario Runner: Full disaster escalation timeline
  - File: `pralay/iot/simulator/flood_scenario.py`

### Phase 4 & 5 — Alerts, Citizen Interface & Frontend Dashboard (Completed ✅)
- [x] 4.1 Plain-language Citizen Alert Card (PRD §18) & SMS formatting
  - Files: `pralay/backend/app/services/notification_service.py`, `pralay/frontend/src/components/citizen/CitizenAlertModal.tsx`
- [x] 5.1 The 4 North Star Question Panes (WHERE, HOW SEVERE, HOW SOON, WHAT NOW)
  - File: `pralay/frontend/src/components/dashboard/NorthStarDecisionPanes.tsx`
- [x] 5.2 Interactive 12-Step Scenario Stepper with real-time sensor gauges
  - File: `pralay/frontend/src/components/dashboard/ScenarioPlayer.tsx`
- [x] 5.3 Catchment selector across Chamoli & Rudraprayag pilot sectors
  - File: `pralay/frontend/src/components/dashboard/VillageCatchmentList.tsx`
- [x] 5.4 Master Authority Control Room Dashboard
  - File: `pralay/frontend/src/pages/Dashboard.tsx`

### Phase 6 & 7 — Reliability, Tests & Verification (Completed ✅)
- [x] 7.1 Pytest Suite: 14/14 Tests passing (API, Risk Engine, Lead Time, Alert Cooldown, Ingestion Validator)
  - Files: `pralay/backend/tests/*`
- [x] 7.2 Frontend Production Build: Clean compile in 2.06s with 0 errors
  - Directory: `pralay/frontend/dist`
