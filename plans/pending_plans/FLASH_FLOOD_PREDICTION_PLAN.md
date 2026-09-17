# Flash Flood Prediction System for Hilly Regions

## Status: IN_PROGRESS

**Progress:** 15% Complete (Phase 1.1 & 1.2 Done)  
**Last Updated:** 2026-09-16 15:25 UTC  
**Current Phase:** 1.3 - Region & Terrain Data Ingestion

---

## Overview

A comprehensive flash flood prediction system that integrates multi-source data (rainfall, soil moisture, slope stability, historical landslide inventories, and real-time IoT inputs) to generate hyper-local forecasts at the village/ward level for hilly regions in India. The system provides actionable early warnings with sufficient lead time for evacuation and disaster preparedness.

## Problem Statement

Hilly states in India are highly vulnerable to landslides and flash floods with very short warning times. Current early warning mechanisms are inadequate for hyper-local prediction and timely evacuation, resulting in significant loss of lives and property.

**Target:** Develop a predictive system integrating rainfall data, soil moisture sensors, slope stability models, historical landslide inventories, and real-time IoT inputs to issue village/ward-level early warnings.

## Goals & Objectives

1. **Multi-Source Data Ingestion** - Unified pipeline for rainfall, soil moisture, slope, and historical data
2. **Real-Time IoT Integration** - MQTT/HTTP ingestion from field sensors
3. **ML Prediction Engine** - Flash flood risk scoring with lead time estimation
4. **Hyper-Local Forecasting** - Village/ward-level risk maps and alerts
5. **Early Warning Dashboard** - Real-time monitoring for NDRF/DM officials
6. **Actionable Alerts** - SMS, push notifications, siren triggers with evacuation routes
7. **Historical Analysis** - Landslide/flash flood inventory and pattern recognition

## Architecture & Tech Stack

### Backend
- **Framework:** Python FastAPI (async, high-performance)
- **ML/AI:** PyTorch / scikit-learn for flood prediction models
- **Task Queue:** Celery + Redis for async processing
- **Database:** PostgreSQL + PostGIS (geospatial), TimescaleDB extension (time-series)
- **Cache:** Redis (real-time sensor data, prediction cache)
- **Message Broker:** RabbitMQ (IoT sensor data pipeline)

### Frontend
- **Framework:** React + TypeScript
- **Mapping:** Leaflet + GeoServer (geospatial visualization)
- **Charts:** Recharts / D3.js for temporal data
- **State:** Zustand or Redux Toolkit
- **UI Kit:** Tailwind CSS + shadcn/ui

### IoT & Data
- **IoT Protocol:** MQTT (Eclipse Mosquitto broker)
- **Stream Processing:** Apache Kafka or Redis Streams
- **Data Storage:** InfluxDB (sensor time-series), PostgreSQL (relational)
- **External APIs:** IMD (India Meteorological Department) rainfall API, ISRO Bhuvan elevation data

### Deployment
- **Containerization:** Docker + Docker Compose
- **Orchestration:** Kubernetes (production)
- **CI/CD:** GitHub Actions
- **Cloud:** AWS/GCP with GovCloud for Indian govt compliance

---

## File Structure

```
pralay/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI app entry
│   │   ├── config.py                   # Settings & env config
│   │   ├── database.py                 # DB connection & session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── region.py               # Region/Village/Ward models
│   │   │   ├── sensor.py               # IoT sensor models
│   │   │   ├── reading.py              # Sensor reading models
│   │   │   ├── risk_zone.py            # Risk zone/heatmap models
│   │   │   ├── alert.py                # Alert & warning models
│   │   │   ├── historical.py           # Historical disaster data
│   │   │   └── terrain.py              # Terrain/slope models
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── region.py
│   │   │   ├── sensor.py
│   │   │   ├── reading.py
│   │   │   ├── risk.py
│   │   │   ├── alert.py
│   │   │   └── dashboard.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── regions.py          # Region/village endpoints
│   │   │   │   ├── sensors.py          # Sensor CRUD & readings
│   │   │   │   ├── predictions.py      # Prediction endpoints
│   │   │   │   ├── alerts.py           # Alert management
│   │   │   │   ├── dashboard.py        # Dashboard aggregate data
│   │   │   │   └── historical.py       # Historical data queries
│   │   │   └── router.py              # API router aggregation
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── data_ingestion.py       # Multi-source data ingestion
│   │   │   ├── iot_service.py          # MQTT sensor data handler
│   │   │   ├── rainfall_service.py     # IMD rainfall data fetcher
│   │   │   ├── soil_moisture.py        # Soil moisture processing
│   │   │   ├── slope_analysis.py       # Slope stability calculations
│   │   │   ├── terrain_service.py      # DEM/terrain processing
│   │   │   ├── prediction_engine.py    # ML prediction orchestrator
│   │   │   ├── alert_service.py        # Alert generation & dispatch
│   │   │   ├── notification_service.py # SMS/Push/Email notifications
│   │   │   └── evacuation_service.py   # Evacuation route calculation
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── features.py             # Feature engineering
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── lstm_flood.py       # LSTM-based flood prediction
│   │   │   │   ├── xgboost_risk.py     # XGBoost risk classifier
│   │   │   │   ├── ensemble.py         # Ensemble model
│   │   │   │   └── slope_stability.py  # Slope stability ML model
│   │   │   ├── training.py             # Model training pipeline
│   │   │   ├── inference.py            # Real-time inference
│   │   │   └── evaluation.py           # Model metrics & evaluation
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py           # Celery configuration
│   │   │   ├── data_fetch.py           # Scheduled data fetch tasks
│   │   │   ├── prediction_tasks.py     # Prediction scheduled tasks
│   │   │   └── alert_tasks.py          # Alert dispatch tasks
│   │   ├── workers/
│   │   │   ├── __init__.py
│   │   │   ├── mqtt_worker.py          # MQTT consumer worker
│   │   │   └── kafka_worker.py         # Kafka stream processor
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── geospatial.py           # Geo utility functions
│   │       ├── constants.py            # System constants
│   │       └── validators.py           # Input validation
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       ├── 001_initial_schema.py
│   │       └── 002_add_sensors.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api/
│   │   │   ├── test_regions.py
│   │   │   ├── test_sensors.py
│   │   │   ├── test_predictions.py
│   │   │   └── test_alerts.py
│   │   ├── test_services/
│   │   │   ├── test_prediction_engine.py
│   │   │   ├── test_alert_service.py
│   │   │   └── test_iot_service.py
│   │   └── test_ml/
│   │       ├── test_features.py
│   │       └── test_models.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── api/
│   │   │   ├── client.ts              # Axios/fetch client
│   │   │   ├── regions.ts
│   │   │   ├── sensors.ts
│   │   │   ├── predictions.ts
│   │   │   └── alerts.ts
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── map/
│   │   │   │   ├── RiskMap.tsx         # Main geospatial map
│   │   │   │   ├── HeatmapLayer.tsx    # Risk heatmap overlay
│   │   │   │   ├── SensorMarkers.tsx   # IoT sensor positions
│   │   │   │   ├── RegionBoundaries.tsx
│   │   │   │   └── EvacuationRoutes.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── DashboardPage.tsx
│   │   │   │   ├── RiskSummaryCard.tsx
│   │   │   │   ├── SensorStatusGrid.tsx
│   │   │   │   ├── RainfallChart.tsx
│   │   │   │   ├── SoilMoistureChart.tsx
│   │   │   │   ├── PredictionTimeline.tsx
│   │   │   │   └── AlertFeed.tsx
│   │   │   ├── alerts/
│   │   │   │   ├── AlertPanel.tsx
│   │   │   │   ├── AlertHistory.tsx
│   │   │   │   └── AlertConfig.tsx
│   │   │   ├── sensors/
│   │   │   │   ├── SensorList.tsx
│   │   │   │   ├── SensorDetail.tsx
│   │   │   │   └── SensorForm.tsx
│   │   │   └── regions/
│   │   │       ├── RegionList.tsx
│   │   │       ├── RegionDetail.tsx
│   │   │       └── VillageRiskView.tsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts         # Real-time alert socket
│   │   │   ├── useSensors.ts
│   │   │   └── usePredictions.ts
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── MapView.tsx
│   │   │   ├── SensorManagement.tsx
│   │   │   ├── AlertCenter.tsx
│   │   │   ├── RegionExplorer.tsx
│   │   │   ├── HistoricalAnalysis.tsx
│   │   │   └── AdminPanel.tsx
│   │   ├── store/
│   │   │   ├── index.ts
│   │   │   ├── sensorStore.ts
│   │   │   ├── alertStore.ts
│   │   │   └── regionStore.ts
│   │   └── types/
│   │       ├── region.ts
│   │       ├── sensor.ts
│   │       ├── alert.ts
│   │       ├── prediction.ts
│   │       └── terrain.ts
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   └── Dockerfile
├── iot/
│   ├── sensor_firmware/
│   │   ├── soil_moisture_sensor.ino     # Arduino/ESP32 firmware
│   │   ├── rain_gauge_sensor.ino
│   │   ├── water_level_sensor.ino
│   │   └── common/
│   │       ├── mqtt_config.h
│   │       └── wifi_manager.h
│   ├── gateway/
│   │   ├── gateway.py                   # IoT gateway aggregator
│   │   ├── mqtt_broker_config.py
│   │   └── data_validator.py
│   └── simulator/
│       ├── sensor_simulator.py          # Simulate sensor data for testing
│       └── flood_scenario.py
├── data/
│   ├── raw/
│   │   ├── imd_rainfall/               # IMD rainfall datasets
│   │   ├── srtm_elevation/             # SRTM DEM data
│   │   ├── landslide_inventory/        # Historical landslide records
│   │   └── soil_data/                  # Soil type/capacity data
│   ├── processed/
│   │   ├── features/
│   │   └── labels/
│   └── scripts/
│       ├── download_imd_data.py
│       ├── process_dem.py
│       ├── prepare_training_data.py
│       └── seed_regions.py
├── ml/
│   ├── notebooks/
│   │   ├── 01_data_exploration.ipynb
│   │   ├── 02_feature_engineering.ipynb
│   │   ├── 03_model_training.ipynb
│   │   └── 04_evaluation.ipynb
│   ├── models/
│   │   ├── trained/                    # Saved model artifacts
│   │   └── configs/                    # Model hyperparameters
│   └── scripts/
│       ├── train.py
│       ├── evaluate.py
│       └── export.py
├── deploy/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── k8s/
│   │   ├── namespace.yaml
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── postgres-statefulset.yaml
│   │   ├── redis-deployment.yaml
│   │   ├── mqtt-deployment.yaml
│   │   └── ingress.yaml
│   └── nginx/
│       └── nginx.conf
├── scripts/
│   ├── setup.sh                        # Initial project setup
│   ├── seed_data.py                    # Seed historical data
│   └── run_tests.sh
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── IoT_SETUP.md
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Implementation Steps

### Phase 1: Foundation & Data Layer (Weeks 1-3)

- [x] **1.1 Project Scaffolding** ✅ COMPLETED (2026-09-16)
  - Initialize Python backend with FastAPI, Poetry/pip
  - Initialize React frontend with Vite + TypeScript
  - Set up Docker Compose (PostgreSQL+PostGIS, Redis, MQTT broker)
  - Configure linting, formatting (ruff, eslint, prettier)
  - Files: `backend/app/main.py`, `backend/app/config.py`, `frontend/package.json`, `deploy/docker-compose.yml`
  - **Deliverables:** 30+ files created, full Docker stack ready, 343 skills installed

- [x] **1.2 Database Schema Design** ✅ COMPLETED (2026-09-16)
  - Create PostGIS-enabled tables for regions, villages, wards
  - Define sensor registration and reading tables with TimescaleDB hypertables
  - Risk zone tables with geometry columns
  - Alert tables with status tracking
  - Historical disaster inventory tables
  - Files: `backend/app/models/*.py`, `backend/alembic/versions/001_initial_schema.py`
  - **Deliverables:** 8 SQLAlchemy models, Alembic migration, complete database schema

- [ ] **1.3 Region & Terrain Data Ingestion**
  - Download SRTM/ASTER DEM data for target hilly states (Uttarakhand, Himachal, NE India)
  - Process elevation, slope angle, slope aspect, curvature from DEM
  - Seed village/ward boundary data from Census/shapefiles
  - Store terrain features in PostGIS
  - Files: `data/scripts/process_dem.py`, `data/scripts/seed_regions.py`, `backend/app/services/terrain_service.py`

- [ ] **1.4 Historical Data Pipeline**
  - Collect landslide/flash flood inventories (GSI, EM-DAT, state disaster mgmt depts)
  - Process IMD historical rainfall data
  - Create labeled dataset: date + location + rainfall + soil + slope -> flood/no-flood
  - Files: `data/scripts/download_imd_data.py`, `data/scripts/prepare_training_data.py`, `backend/app/services/data_ingestion.py`

---

### Phase 2: IoT & Real-Time Data (Weeks 3-5)

- [ ] **2.1 MQTT Broker Setup**
  - Deploy Eclipse Mosquitto in Docker
  - Define topic structure: `sensors/{region_id}/{sensor_type}/{sensor_id}`
  - Configure authentication and TLS for production
  - Files: `deploy/docker-compose.yml`, `iot/gateway/mqtt_broker_config.py`

- [ ] **2.2 IoT Sensor Firmware**
  - Write ESP32 firmware for soil moisture (capacitive sensor), rain gauge (tipping bucket), water level (ultrasonic)
  - MQTT publish with JSON payload: `{sensor_id, type, value, timestamp, battery, lat, lng}`
  - WiFi reconnection logic, deep sleep for power saving
  - Files: `iot/sensor_firmware/soil_moisture_sensor.ino`, `iot/sensor_firmware/rain_gauge_sensor.ino`, `iot/sensor_firmware/water_level_sensor.ino`, `iot/sensor_firmware/common/mqtt_config.h`

- [ ] **2.3 IoT Gateway & Data Validation**
  - MQTT subscriber service that validates, deduplicates, and routes sensor readings
  - Schema validation, outlier detection, sensor health tracking
  - Write validated readings to TimescaleDB and Redis (for real-time cache)
  - Files: `iot/gateway/gateway.py`, `iot/gateway/data_validator.py`, `backend/app/services/iot_service.py`, `backend/app/workers/mqtt_worker.py`

- [ ] **2.4 Sensor Data Simulator**
  - Create a Python simulator that generates realistic sensor readings for testing
  - Scenario-based simulation: normal, heavy rainfall, soil saturation, flash flood
  - Useful for demo and model training without physical sensors
  - Files: `iot/simulator/sensor_simulator.py`, `iot/simulator/flood_scenario.py`

- [ ] **2.5 External Data Integrations**
  - IMD rainfall API connector (fetch latest/forecast rainfall grids)
  - Integrate with existing IoT platforms if available (e.g., GEMI course correction data)
  - Scheduled Celery tasks to fetch external data every 15 minutes
  - Files: `backend/app/services/rainfall_service.py`, `backend/app/tasks/data_fetch.py`

---

### Phase 3: ML Prediction Engine (Weeks 5-8)

- [ ] **3.1 Feature Engineering Pipeline**
  - Temporal features: hourly/daily rainfall accumulation, antecedent rainfall (1h, 3h, 6h, 24h, 72h)
  - Soil features: volumetric water content, soil saturation index, drainage rate
  - Terrain features: slope angle, slope aspect, curvature, TWI (Topographic Wetness Index), SPI (Stream Power Index)
  - Combined features: rainfall intensity vs infiltration capacity, slope-rainfall interaction
  - Files: `backend/app/ml/features.py`, `ml/notebooks/02_feature_engineering.ipynb`

- [ ] **3.2 LSTM Flood Prediction Model**
  - Sequence model taking 24h window of multi-variate sensor readings
  - Input: rainfall, soil moisture, water level time series per grid cell
  - Output: probability of flash flood in next 1h, 3h, 6h
  - Training on historical labeled data
  - Files: `backend/app/ml/models/lstm_flood.py`, `ml/scripts/train.py`, `ml/scripts/evaluate.py`

- [ ] **3.3 XGBoost Risk Classifier**
  - Tabular model for static + dynamic feature combination
  - Features: slope, soil type, land use, current rainfall intensity, soil moisture
  - Binary + multi-class: no risk / moderate / high / extreme
  - Explainability via SHAP values for alert justification
  - Files: `backend/app/ml/models/xgboost_risk.py`, `ml/notebooks/03_model_training.ipynb`

- [ ] **3.4 Slope Stability Model**
  - Infinite slope model with pore water pressure estimation
  - Factor of Safety calculation using soil cohesion, friction angle, slope angle
  - ML correction factor trained on historical landslide data
  - Triggered when rainfall exceeds soil infiltration capacity on steep slopes
  - Files: `backend/app/ml/models/slope_stability.py`, `backend/app/services/slope_analysis.py`

- [ ] **3.5 Ensemble Prediction Engine**
  - Combine LSTM (temporal patterns) + XGBoost (static + dynamic) + Slope model (terrain)
  - Weighted ensemble with confidence scoring
  - Per-grid-cell risk score -> aggregated to village/ward level
  - Lead time estimation: time until risk exceeds critical threshold
  - Files: `backend/app/ml/models/ensemble.py`, `backend/app/services/prediction_engine.py`, `backend/app/ml/inference.py`

- [ ] **3.6 Model Training & Evaluation**
  - Train/test split with temporal awareness (no future data leakage)
  - Metrics: precision, recall, F1, AUC-ROC, lead time accuracy
  - Notebook-based exploration and iteration
  - Model versioning and artifact storage
  - Files: `ml/notebooks/01_data_exploration.ipynb`, `ml/notebooks/04_evaluation.ipynb`, `backend/app/ml/training.py`, `backend/app/ml/evaluation.py`

---

### Phase 4: Alert & Warning System (Weeks 8-10)

- [ ] **4.1 Alert Generation Engine**
  - Rule engine: risk score thresholds per severity level (Green/Yellow/Orange/Red)
  - Multi-factor triggers: rainfall + soil moisture + slope stability combination
  - Deduplication: suppress repeated alerts for same zone within cooldown period
  - Escalation: auto-escalate if risk continues rising
  - Files: `backend/app/services/alert_service.py`, `backend/app/models/alert.py`

- [ ] **4.2 Notification Dispatch**
  - SMS via MSG91 or TRAI-approved bulk SMS provider
  - Push notifications via Firebase Cloud Messaging (mobile app)
  - Email alerts for NDRF/DM officials
  - Webhook integration for state disaster management control rooms
  - Files: `backend/app/services/notification_service.py`, `backend/app/tasks/alert_tasks.py`

- [ ] **4.3 Evacuation Route Calculator**
  - Graph-based shortest safe path from at-risk village to safe zone
  - Using OpenStreetMap road data + terrain analysis
  - Avoid routes through high-risk zones
  - Pre-computed routes per village, updated when risk zones change
  - Files: `backend/app/services/evacuation_service.py`, `backend/app/utils/geospatial.py`

- [ ] **4.4 WebSocket Real-Time Alerts**
  - WebSocket endpoint for live alert streaming to dashboard
  - Push new predictions and alerts to connected clients
  - Client-side reconnection and alert queuing
  - Files: `backend/app/api/v1/predictions.py`, `frontend/src/hooks/useWebSocket.ts`, `frontend/src/components/dashboard/AlertFeed.tsx`

---

### Phase 5: Frontend Dashboard (Weeks 10-13)

- [ ] **5.1 Layout & Navigation**
  - Sidebar with map view, dashboard, sensor management, alerts, regions, admin
  - Responsive design for desktop (control room) and tablet (field officers)
  - Theme: dark mode for control room, high-contrast for outdoor visibility
  - Files: `frontend/src/components/layout/Layout.tsx`, `frontend/src/components/layout/Sidebar.tsx`, `frontend/src/components/layout/Header.tsx`

- [ ] **5.2 Interactive Risk Map (Core Feature)**
  - Leaflet map with village/ward boundaries as GeoJSON layers
  - Risk heatmap overlay (green-yellow-orange-red gradient)
  - Click village -> show detailed risk breakdown
  - Sensor markers with real-time status (online/offline/battery)
  - Evacuation route overlay
  - Time slider for prediction playback
  - Files: `frontend/src/components/map/RiskMap.tsx`, `frontend/src/components/map/HeatmapLayer.tsx`, `frontend/src/components/map/SensorMarkers.tsx`, `frontend/src/components/map/RegionBoundaries.tsx`, `frontend/src/components/map/EvacuationRoutes.tsx`, `frontend/src/pages/MapView.tsx`

- [ ] **5.3 Dashboard Overview**
  - Risk summary cards (total zones at risk, active alerts, sensors online)
  - Real-time rainfall chart (last 24h, per station)
  - Soil moisture trend chart
  - Prediction timeline (upcoming 6h risk forecast)
  - Live alert feed with severity indicators
  - Files: `frontend/src/components/dashboard/DashboardPage.tsx`, `frontend/src/components/dashboard/RiskSummaryCard.tsx`, `frontend/src/components/dashboard/RainfallChart.tsx`, `frontend/src/components/dashboard/SoilMoistureChart.tsx`, `frontend/src/components/dashboard/PredictionTimeline.tsx`, `frontend/src/components/dashboard/AlertFeed.tsx`, `frontend/src/pages/Dashboard.tsx`

- [ ] **5.4 Alert Management Center**
  - Active alerts list with severity, location, time, affected population
  - Alert acknowledgment and assignment to field teams
  - Historical alert log with filters
  - Alert threshold configuration per region
  - Files: `frontend/src/components/alerts/AlertPanel.tsx`, `frontend/src/components/alerts/AlertHistory.tsx`, `frontend/src/components/alerts/AlertConfig.tsx`, `frontend/src/pages/AlertCenter.tsx`

- [ ] **5.5 Sensor Management**
  - Sensor registry: list, add, edit sensors with location
  - Sensor health dashboard: battery, signal strength, last seen
  - Real-time sensor reading view
  - Sensor deployment map
  - Files: `frontend/src/components/sensors/SensorList.tsx`, `frontend/src/components/sensors/SensorDetail.tsx`, `frontend/src/components/sensors/SensorForm.tsx`, `frontend/src/pages/SensorManagement.tsx`

- [ ] **5.6 Region & Village Explorer**
  - Region hierarchy: State -> District -> Block -> Village/Ward
  - Village-level risk profile: terrain, soil, population, vulnerability score
  - Historical flood/landslide events per village
  - Infrastructure mapping: hospitals, shelters, roads
  - Files: `frontend/src/components/regions/RegionList.tsx`, `frontend/src/components/regions/RegionDetail.tsx`, `frontend/src/components/regions/VillageRiskView.tsx`, `frontend/src/pages/RegionExplorer.tsx`

- [ ] **5.7 Historical Analysis Page**
  - Date range selector for historical data
  - Past flood event replay on map
  - Frequency analysis: which villages flood most often
  - Seasonal patterns and trends
  - Files: `frontend/src/pages/HistoricalAnalysis.tsx`, `frontend/src/components/dashboard/PredictionTimeline.tsx`

---

### Phase 6: Backend API & Integration (Weeks 13-15)

- [ ] **6.1 REST API Endpoints**
  - `GET /api/v1/regions` - List all monitored regions
  - `GET /api/v1/regions/{id}/villages` - Villages in a region
  - `GET /api/v1/regions/{id}/risk` - Current risk assessment for region
  - `POST /api/v1/sensors` - Register new sensor
  - `GET /api/v1/sensors/{id}/readings` - Sensor reading history
  - `GET /api/v1/predictions/current` - All current predictions
  - `GET /api/v1/predictions/{region_id}` - Predictions for specific region
  - `GET /api/v1/alerts/active` - Active alerts
  - `POST /api/v1/alerts/{id}/acknowledge` - Acknowledge alert
  - `GET /api/v1/dashboard/summary` - Dashboard aggregate data
  - Files: `backend/app/api/v1/*.py`, `backend/app/api/router.py`

- [ ] **6.2 Scheduled Tasks (Celery Beat)**
  - Every 5 min: ingest new sensor data, update predictions
  - Every 15 min: fetch IMD rainfall forecast data
  - Every 1 hour: re-run slope stability analysis
  - Every 6 hours: retrain/fine-tune models with latest data
  - Daily: generate daily risk summary report
  - Files: `backend/app/tasks/celery_app.py`, `backend/app/tasks/data_fetch.py`, `backend/app/tasks/prediction_tasks.py`

- [ ] **6.3 Authentication & Authorization**
  - JWT-based auth for API access
  - Role-based access: Admin, NDRF Officer, DM Official, View-only
  - API key auth for IoT gateway submissions
  - Files: `backend/app/api/v1/auth.py` (new), `backend/app/models/user.py` (new)

---

### Phase 7: Testing & Quality (Weeks 15-17)

- [ ] **7.1 Unit Tests**
  - Test feature engineering pipeline
  - Test ML model inference (with mock models)
  - Test alert generation logic
  - Test notification dispatch (mocked)
  - Files: `backend/tests/test_services/*.py`, `backend/tests/test_ml/*.py`

- [ ] **7.2 API Integration Tests**
  - Test all REST endpoints with test database
  - Test WebSocket connections
  - Test MQTT message handling
  - Files: `backend/tests/test_api/*.py`

- [ ] **7.3 ML Model Validation**
  - Cross-validation on historical data
  - Confusion matrix, ROC curves, precision-recall analysis
  - Lead time accuracy analysis
  - False positive/negative rate targets (FPR < 10%, FNR < 5%)
  - Files: `ml/notebooks/04_evaluation.ipynb`, `backend/app/ml/evaluation.py`

- [ ] **7.4 Load & Performance Testing**
  - Simulate 1000+ concurrent sensor readings
  - Dashboard rendering with large GeoJSON datasets
  - Alert dispatch latency under load
  - Files: `scripts/load_test.py` (new)

---

### Phase 8: Deployment & Documentation (Weeks 17-19)

- [ ] **8.1 Docker & Kubernetes**
  - Multi-stage Dockerfiles for backend and frontend
  - Kubernetes manifests for all services
  - Persistent volumes for PostgreSQL and InfluxDB
  - ConfigMaps and Secrets for environment configuration
  - Files: `backend/Dockerfile`, `frontend/Dockerfile`, `deploy/k8s/*.yaml`

- [ ] **8.2 CI/CD Pipeline**
  - GitHub Actions: lint, test, build, push images
  - Auto-deploy to staging on main branch
  - Manual promote to production
  - Files: `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`

- [ ] **8.3 Documentation**
  - API documentation (auto-generated from FastAPI OpenAPI)
  - Architecture decision records
  - Deployment guide for NDRF/DM teams
  - IoT sensor installation guide
  - User manual for dashboard operators
  - Files: `docs/API.md`, `docs/ARCHITECTURE.md`, `docs/DEPLOYMENT.md`, `docs/IoT_SETUP.md`, `README.md`

- [ ] **8.4 Pilot Deployment**
  - Deploy for one district in Uttarakhand (e.g., Chamoli or Rudraprayag)
  - Install 10-20 IoT sensors in pilot area
  - Train local DM officials on dashboard usage
  - Monitor system performance for 2 weeks
  - Collect feedback and iterate

---

## Dependencies

### External Data Sources
- **IMD Data:** India Meteorological Department rainfall grids (api.imd.gov.in)
- **SRTM/ASTER DEM:** NASA Earthdata (90m/30m resolution elevation)
- **Census Village Boundaries:** Census of India shapefiles
- **GSI Landslide Inventory:** Geological Survey of India
- **OpenStreetMap:** Road networks for evacuation routing
- **ISRO Bhuvan:** Additional remote sensing data

### Python Packages
- `fastapi`, `uvicorn`, `sqlalchemy[asyncio]`, `alembic`
- `geoalchemy2`, `shapely`, `rasterio`, `fiona` (geospatial)
- `pytorch`, `scikit-learn`, `xgboost`, `shap` (ML)
- `celery[redis]`, `paho-mqtt` (IoT & tasks)
- `pandas`, `numpy`, `scipy` (data processing)
- `httpx` (external API calls)

### Frontend Packages
- `react`, `react-dom`, `react-router-dom`
- `leaflet`, `react-leaflet`, `@react-leaflet/core`
- `recharts` or `d3.js`
- `zustand` or `@reduxjs/toolkit`
- `tailwindcss`, `shadcn/ui`
- `socket.io-client` (WebSocket)

### Hardware (Pilot)
- ESP32 microcontrollers + sensors (soil moisture, rain gauge, ultrasonic water level)
- Solar panels + batteries for remote sensor power
- 4G/LTE modules for cellular connectivity
- SIM cards with IoT data plans

---

## Testing Strategy

| Level | Tools | Target |
|-------|-------|--------|
| Unit Tests | pytest, vitest | 80%+ coverage |
| Integration | pytest + testcontainers | API + DB correctness |
| E2E | Playwright | Critical user flows |
| Load | Locust/k6 | 1000 concurrent sensors |
| ML Validation | sklearn metrics, custom | F1 > 0.90, FNR < 5% |
| IoT | Sensor simulator | Data pipeline integrity |

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| IMD API downtime/rate limits | Missing rainfall data | Cache latest data locally, fallback to nearest station interpolation |
| Sensor failures in field | Data gaps | Redundant sensors, anomaly detection, interpolation from neighbors |
| Model overfitting to specific terrain | Poor generalization | Train on diverse hilly regions, cross-validation, transfer learning |
| Network connectivity in remote areas | Delayed alerts | Edge computing on gateway, local alert caching, satellite connectivity option |
| False alarm fatigue | Officials ignore alerts | Conservative thresholds initially, explainability, continuous calibration |
| Scale beyond pilot district | Infrastructure overload | Horizontal scaling with Kubernetes, database sharding by region |

---

## References

- [NDRF Guidelines for Disaster Management](https://ndrfindia.gov.in)
- [IMD Rainfall Data Services](https://mausam.imd.gov.in)
- [GSI Landslide Studies](https://www.geologicalsocietyofindia.org)
- [NASA SRTM Elevation Data](https://earthdata.nasa.gov)
- [OpenStreetMap India](https://www.openstreetmap.org)
- [UNDRR Sendai Framework](https://www.undrr.org/implementing-sendai-framework)
- SIH Problem ID: 26192

---

*Created: 2026-09-16 | Target: SIH 2026 Submission*
