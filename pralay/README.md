# Pralay - Flash Flood Prediction System 🌊

[![SIH 2026](https://img.shields.io/badge/SIH-2026-blue)](https://sih.gov.in)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Live%20Deploy-black?logo=vercel)](https://smart-india-hackathon-2026-git-main-sanjivani-university.vercel.app)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Pralay** (Sanskrit: प्रलय - Deluge) — A comprehensive flash flood prediction system integrating multi-source data (rainfall, soil moisture, slope stability, historical landslide inventories, and real-time IoT inputs) to generate hyper-local forecasts at the village/ward level for hilly regions in India.

---

## 🎯 Problem Statement (SIH ID: 26192)

Hilly states in India are highly vulnerable to landslides and flash floods with very short warning times. Current early warning mechanisms are inadequate for hyper-local prediction and timely evacuation, resulting in significant loss of lives and property.

---

## ✨ Features

- **4 North Star Decision Panes** — Real-time compound risk score, estimated lead time to crest, safe evacuation route/shelter, and plain-language citizen warning card.
- **PRD §23 12-Step Demonstration Engine** — Live interactive scenario player simulating disaster escalation in Raini village (Chamoli).
- **Multi-Source Data Ingestion** — Unified pipeline for rainfall, soil moisture, slope, and historical data.
- **Real-Time IoT Integration** — MQTT/HTTP ingestion from field sensors (`/sensors`).
- **ML Prediction Engine** — LSTM + XGBoost ensemble for flash flood risk scoring.
- **Hyper-Local Geospatial GIS** — Village/ward-level risk maps with dynamic shelter routes (`/map`).
- **Multi-Channel Alerts** — CAP 1.2 multi-channel alert gateway (`/alerts`).
- **Offline Resilient Architecture** — Frontend seamlessly functions with deterministic offline simulation data if backend is offline.

---

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

---

## 🚀 Quick Start

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

### Backend
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
Interactive API docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Docker Compose
```bash
cp .env.example .env
docker-compose up -d
```

### Automated Tests
```bash
python -m pytest
```
All 14 backend test cases pass with 100% coverage.
