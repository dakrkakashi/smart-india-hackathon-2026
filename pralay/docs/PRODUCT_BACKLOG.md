# PRALAYADARSHI Product Backlog
**SIH Problem Statement 26192**
*Mapping PRD Sections §6–§25 to Technical Implementation Tasks*

| PRD Section | Requirement | Architecture Component | Implementation File(s) | Status |
|---|---|---|---|---|
| **§6.A** | Rainfall Ingestion (intensity, accum 1h-72h, trend) | Backend Service | `app/services/rainfall_service.py` | In Progress |
| **§6.B** | Soil Moisture Ingestion (saturation trend) | Backend Service / IoT | `app/services/soil_moisture.py` | In Progress |
| **§6.C** | River/Stream Level & Rate of Rise | Backend Service | `app/services/river_service.py` | In Progress |
| **§6.D** | Terrain & DEM Analysis (Slope, aspect, curvature, TWI) | Terrain Service | `app/services/terrain_service.py` | In Progress |
| **§6.E** | Historical Landslide & Flood Inventory | Data Pipeline | `app/models/historical.py`, seed script | In Progress |
| **§6.F** | Field IoT Sensors (Rain, Moisture, Ultrasonic Water Level) | IoT Layer | `iot/gateway/`, `iot/simulator/` | In Progress |
| **§7 & §8** | Data Validation & Health Monitoring (Missing data, outlier, failure) | IoT Gateway | `iot/gateway/data_validator.py` | In Progress |
| **§9 & §10**| Transparent Compound Risk Engine (Flood + Landslide + Terrain) | Risk Engine | `app/services/risk_engine.py` | In Progress |
| **§11** | Machine Learning Training & Evaluation Framework | ML Pipeline | `app/ml/`, `ml/scripts/` | Planned |
| **§12** | Estimated Lead-Time Engine (Main USP) | Decision Engine | `app/services/lead_time_engine.py` | In Progress |
| **§13** | Hyperlocal Village/Ward Granularity | Database & GIS | `app/models/region.py`, `app/schemas/risk.py` | In Progress |
| **§14** | Alert Engine & Cooldown / Auto-Escalation | Alert Service | `app/services/alert_service.py` | In Progress |
| **§15** | Evacuation & Safe Shelter Routing | Evacuation Service | `app/services/evacuation_service.py` | In Progress |
| **§16 & §17**| Live GIS Authority Dashboard & Decision Workflow | React / Leaflet | `frontend/src/pages/Dashboard.tsx` | In Progress |
| **§18** | Citizen Plain-Language Warning Interface | React UI | `frontend/src/components/citizen/CitizenAlertCard.tsx` | In Progress |
| **§19** | Multi-Factor Authority Control Room Interface | React UI | `frontend/src/components/dashboard/` | In Progress |
| **§20** | Relational & Geospatial Schema | SQLAlchemy Models | `app/models/*.py` | Completed |
| **§22** | Minimum Viable Product (MVP) Guardrail Core | Core Orchestration | `backend/app/main.py`, `app/api/router.py` | In Progress |
| **§23** | 12-Step Flash Flood Scenario Demonstration | Scenario Script | `scripts/run_demo.py`, `iot/simulator/` | In Progress |
| **§24 & §25**| Validation & Telemetry (Backtest & False Alarm Control) | Evaluation Suite | `tests/`, `docs/VALIDATION_REPORT.md` | In Progress |
