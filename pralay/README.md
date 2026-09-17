# Pralay - Flash Flood Prediction System 🌊

[![SIH 2026](https://img.shields.io/badge/SIH-2026-blue)](https://sih.gov.in)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Pralay** (Sanskrit: प्रलय - Deluge) - A comprehensive flash flood prediction system integrating multi-source data (rainfall, soil moisture, slope stability, historical landslide inventories, and real-time IoT inputs) to generate hyper-local forecasts at the village/ward level for hilly regions in India.

## 🎯 Problem Statement (SIH ID: 26192)

Hilly states in India are highly vulnerable to landslides and flash floods with very short warning times. Current early warning mechanisms are inadequate for hyper-local prediction and timely evacuation, resulting in significant loss of lives and property.

## ✨ Features

- **Multi-Source Data Ingestion** - Unified pipeline for rainfall, soil moisture, slope, and historical data
- **Real-Time IoT Integration** - MQTT/HTTP ingestion from field sensors
- **ML Prediction Engine** - LSTM + XGBoost ensemble for flash flood risk scoring
- **Hyper-Local Forecasting** - Village/ward-level risk maps and alerts
- **Early Warning Dashboard** - Real-time monitoring for NDRF/DM officials
- **Actionable Alerts** - SMS, push notifications, evacuation routes
- **Historical Analysis** - Landslide/flash flood inventory and pattern recognition

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   IoT Sensors   │────▶│  MQTT Broker    │────▶│  Data Pipeline  │
│ (ESP32 + Solar) │     │   (Mosquitto)   │     │  (Celery/Redis) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  External APIs  │────▶│   PostgreSQL    │────▶│  ML Engine      │
│  (IMD, ISRO)    │     │  + PostGIS +    │     │  (PyTorch/XGB)  │
└─────────────────┘     │   TimescaleDB   │     └─────────────────┘
                        └─────────────────┘              │
                                                         ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │   Frontend      │◀────│  FastAPI        │
                        │ (React+Leaflet) │     │  Backend        │
                        └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │ Alert Service   │
                                                │ (SMS/Push/Email)│
                                                └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Running with Docker Compose

1. Clone the repository
```bash
git clone <repository-url>
cd pralay
```

2. Copy environment file
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start all services
```bash
docker-compose up -d
```

4. Access the services
- Frontend Dashboard: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- MQTT Broker: localhost:1883

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
pralay/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # REST API endpoints
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   ├── ml/          # ML models & inference
│   │   ├── tasks/       # Celery tasks
│   │   └── workers/     # MQTT/Kafka workers
│   └── tests/           # Backend tests
├── frontend/            # React + TypeScript frontend
│   └── src/
│       ├── components/  # UI components
│       ├── pages/       # Route pages
│       ├── api/         # API client
│       └── store/       # State management
├── iot/                 # IoT firmware & gateway
│   ├── sensor_firmware/ # ESP32 firmware
│   ├── gateway/         # IoT gateway
│   └── simulator/       # Sensor data simulator
├── data/                # Data processing scripts
│   ├── raw/            # Raw datasets
│   ├── processed/      # Processed features
│   └── scripts/        # Data preparation
├── ml/                  # ML model training
│   ├── notebooks/      # Jupyter notebooks
│   ├── models/         # Trained models
│   └── scripts/        # Training scripts
└── deploy/             # Deployment configs
    ├── k8s/            # Kubernetes manifests
    └── nginx/          # Nginx configuration
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Load testing
python scripts/load_test.py
```

## 📊 ML Models

### LSTM Flood Prediction Model
- **Input:** 24h window of rainfall, soil moisture, water level time series
- **Output:** Probability of flash flood in next 1h, 3h, 6h
- **Metrics:** F1 > 0.90, False Negative Rate < 5%

### XGBoost Risk Classifier
- **Features:** Slope, soil type, land use, rainfall intensity, soil moisture
- **Output:** Risk level (None/Moderate/High/Extreme)
- **Explainability:** SHAP values for alert justification

### Slope Stability Model
- **Method:** Infinite slope model + ML correction factor
- **Trigger:** Rainfall exceeds infiltration capacity on steep slopes

## 🎯 Target Regions

Initial pilot deployment: **Uttarakhand** (Chamoli & Rudraprayag districts)

Future expansion:
- Himachal Pradesh
- Northeast India (Sikkim, Meghalaya, Arunachal Pradesh)
- Western Ghats (Kerala, Karnataka)

## 🔗 Data Sources

- **IMD** - India Meteorological Department rainfall grids
- **SRTM/ASTER** - NASA Earthdata elevation (90m/30m resolution)
- **GSI** - Geological Survey of India landslide inventory
- **Census** - Village boundary shapefiles
- **OpenStreetMap** - Road networks for evacuation routing
- **ISRO Bhuvan** - Remote sensing data

## 🤝 Contributing

This is an SIH 2026 project. Contributions, issues, and feature requests are welcome!

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 👥 Team

- **Project Name:** Pralay
- **Category:** Software
- **Theme:** Disaster Management
- **Problem ID:** 26192

## 📧 Contact

For queries related to this project, please contact through SIH channels.

---

**Built with ❤️ for SIH 2026**
