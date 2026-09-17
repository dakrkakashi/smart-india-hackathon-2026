# Smart India Hackathon 2026 - Pralay 🌊

[![SIH 2026](https://img.shields.io/badge/SIH-2026-blue)](https://sih.gov.in)
[![Vercel Ready](https://img.shields.io/badge/Vercel-Deployed-black?logo=vercel)](https://vercel.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Pralay** (Sanskrit: प्रलय - Deluge) — A hyper-local flash flood early warning and disaster response system combining real-time IoT sensors, rainfall forecasting (IMD/ISRO), ML-driven flood risk prediction, and automated evacuation routing for hilly and flood-prone regions in India.

---

## 🎯 Problem Statement (SIH ID: 26192)

Hilly and river-basin regions in India face severe vulnerability to flash floods and cloudbursts with extremely short warning windows. Conventional early warning mechanisms operate at coarse regional levels, lacking the village/ward-level granularity required for timely evacuation and NDRF disaster response coordination.

---

## ✨ Key Capabilities

- **Hyper-Local Risk Mapping**: Interactive GIS dashboard rendering village-level flood risk alerts, real-time river gauges, and safe evacuation corridors.
- **Multi-Source Ingestion**: Ingests IMD rainfall telemetry, soil moisture data, digital elevation models, and IoT sensor streams.
- **ML Prediction Engine**: Hybrid LSTM + XGBoost deterministic risk estimation with confidence scoring and lead-time projections.
- **Resilient Offline Fallback**: The frontend dashboard operates reliably with mock simulations even if backend services are offline.
- **Disaster Response Tools**: Live shelter capacity tracking, multi-channel alert dispatch, and 12-step scenario simulations.

---

## 🚀 Deploying to Vercel

This repository is pre-configured for instant deployment on [Vercel](https://vercel.com):

### Option A: Automatic Root Build (Recommended)
1. Import this repository into Vercel from your GitHub dashboard.
2. Vercel automatically detects [`vercel.json`](file:///vercel.json) at the root:
   - **Framework Preset**: Vite
   - **Build Command**: `cd pralay/frontend && npm install && npm run build`
   - **Output Directory**: `pralay/frontend/dist`
3. Click **Deploy**.

### Option B: Monorepo Subdirectory Build
1. Import this repository into Vercel.
2. In the configuration screen, click **Edit** next to **Root Directory** and select:
   ```
   pralay/frontend
   ```
3. Leave Build Command and Output Directory as default (`npm run build`, `dist`).
4. Click **Deploy**.

*(Optional)* Set the environment variable `VITE_API_URL` to your production FastAPI backend URL (e.g., hosted on Render, Railway, or AWS).

---

## 💻 Local Development

### Frontend
```bash
cd pralay/frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

### Backend
```bash
cd pralay/backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload
```
Access backend API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

### Docker Compose
```bash
cd pralay
cp .env.example .env
docker-compose up -d
```

---

## 📂 Repository Structure

```text
├── vercel.json                        # Root Vercel build & SPA rewrite config
├── PRALAY_SIH_2026_Presentation.pptx  # Official SIH 2026 6-slide presentation deck
├── PRALAY_SIH_2026_Presentation.pdf   # Exported presentation deck (PDF)
├── plans/                             # Architectural roadmaps & PRD specifications
│   ├── completed_plans/               # Implemented GIS & PRD milestones
│   └── pending_plans/                 # Long-term roadmaps & research tracks
└── pralay/
    ├── frontend/                      # React 18 + TypeScript + Vite + Tailwind + Leaflet
    │   ├── src/                       # Dashboard, RiskMap, stores, API clients
    │   └── vercel.json                # Frontend SPA routing configuration
    ├── backend/                       # FastAPI asynchronous API server
    │   ├── app/                       # Endpoints, schemas, models, risk engine
    │   └── tests/                     # Automated test suites
    ├── ml/                            # Machine learning models & prediction pipelines
    ├── iot/                           # ESP32 firmware, MQTT broker, and sensor simulator
    ├── data/                          # Geospatial data, elevation & soil datasets
    ├── deploy/                        # Docker, Nginx, and Kubernetes manifests
    └── docker-compose.yml             # Full-stack container orchestration
```

---

## 👥 Team & License

Developed for **Smart India Hackathon (SIH) 2026**.
Licensed under the [MIT License](LICENSE).
