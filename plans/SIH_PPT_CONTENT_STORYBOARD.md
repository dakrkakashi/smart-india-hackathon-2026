# SIH 2026 Presentation Storyboard & Approved Copy
**Problem Statement:** 26192 — Flash Flood Prediction System for Hilly Regions  
**Organization:** Ministry of Home Affairs (NDRF / DM Division)  
**Team:** Team Pralay | **Product:** PRALAYADARSHI (PRALAY)

---

## 🎯 Executive Core
- **USP Line:** `Compound Risk → Lead Time → Action`
- **4 North Star Questions:**
  1. *WHERE is the risk?* (Hyperlocal village-level catchment polygons)
  2. *HOW SEVERE?* (Compound Risk 0–100: GREEN, YELLOW, ORANGE, RED)
  3. *HOW SOON?* (Explicitly labeled "Estimated Lead Time", e.g. 35 mins)
  4. *WHAT NOW?* (Assigned high-ground shelter + safe ridge bypass route)
- **Signature Stat:** `35 Minutes` estimated lead-time window before surge impact.
- **Closing Mantra:** `DETECT EARLIER. IDENTIFY LOCALLY. ACT IN TIME.`

---

## 📑 Slide-by-Slide Blueprint (Strict 6-Slide Template)

### Slide 1: Title Page
- **Header:** Smart India Hackathon 2026 | Theme: Disaster Management | Category: Software
- **Hero Title:** PRALAYADARSHI
- **Hero Tagline:** Compound Risk → Lead Time → Action
- **Subtitle:** Hyperlocal Flash Flood & Debris-Flow Early Warning with Ridge Evacuation Intelligence
- **PS Box:** Problem Statement 26192 | Ministry of Home Affairs | NDRF / DM Division
- **Visuals:** Signature "35 Minutes Could Save a Village" callout card + 4-tier risk status strip (GREEN, YELLOW, ORANGE, RED).
- **Speaker Notes:** Opening pitch introducing the problem of rapid mountain flash floods in Chamoli and our philosophy of Compound Risk → Lead Time → Action.

### Slide 2: Proposed Solution & North Star Architecture
- **Problem vs. Solution Comparison:**
  - *Current Gaps:* 100+ km² district-wide vague alerts, fragmented telemetry silos, zero evacuation routing, severe warning fatigue.
  - *PRALAY Innovation:* Hyperlocal village watersheds, physics-based multi-source fusion, dynamic lead-time minutes, automated shelter routing.
- **The 4 North Star Question Panes:**
  - [1. WHERE] Village catchment polygons (Raini, Tharali, Joshimath).
  - [2. HOW SEVERE] Compound 0–100 scale: GREEN / YELLOW / ORANGE / RED.
  - [3. HOW SOON] Dynamic "Estimated Lead Time" in minutes.
  - [4. WHAT NOW] Safe shelter assignment above flood lines + ridge evacuation waypoints.
- **Dual-Interface Paradigm:** Authority Command Control Room vs. Plain-Language Citizen Alert Card (PRD §18).

### Slide 3: Technical Approach & Multi-Source Fusion Pipeline
- **5-Step End-to-End Pipeline:** SENSE → VALIDATE & FUSE → ASSESS → PREDICT → ACT.
- **Technology Stack Chips:** Python FastAPI, PostgreSQL + PostGIS, TimescaleDB Hypertables, Redis/Celery, ESP32 MQTT Telemetry, React 18 + Vite, TypeScript + Tailwind.
- **Deterministic Compound Risk Formulation:**
  $$\text{Compound Risk} = \max(\text{Flood}, \text{Landslide}) \times 0.65 + \min(\text{Flood}, \text{Landslide}) \times 0.20 + \text{Vuln} \times 15$$
- **Engineering Safety Guardrails:**
  - Outlier & sensor timeout detection: Source marked `UNAVAILABLE`, never assumed 0.
  - 30-minute alert fatigue cooldown suppression + immediate auto-escalation on severity spike.
  - Active flood plain exclusion: Shelters in flood zones are filtered out.

### Slide 4: Feasibility, Viability & Implementation Roadmap
- **3-Phase Phased Rollout:**
  - *Phase A: Pilot Prototype (Months 1–3, Complete)*: 5 catchments in Chamoli & Rudraprayag, 14/14 tests passing, interactive 12-step simulator.
  - *Phase B: Field Telemetry & IoT (Months 4–7)*: Solar ESP32 nodes, ultrasonic stream sensors, LoRaWAN edge mesh across Mandakini & Alaknanda basins.
  - *Phase C: State Scale & Operations (Months 8–12)*: SDMA integration, CWC telemetry feeds, multi-lingual vernacular SMS dispatch.
- **Risk Mitigation Matrix:**
  - *IMD Outage:* Local caching + IDW spatial fallback interpolation.
  - *Sensor Breakdown:* Heartbeat watcher flags `UNAVAILABLE`; model degrades gracefully.
  - *Cellular Dropouts:* LoRaWAN edge mesh buffering 72h on flash.
  - *Alert Fatigue:* 30-minute cooldown suppression + dual-threshold confirmation.
- **Cost Viability:** Ultra-low capital expenditure: ₹12,000–₹18,000 per solar node with 5-year operational life.

### Slide 5: Impact, Operational Benefits & Target Metrics
- **Target KPI Callout Cards:**
  - *30–45 Mins*: Target Estimated Lead Time window for pre-impact evacuation.
  - *< 10%*: False Positive Rate target to eliminate warning fatigue.
  - *< 5%*: Missed Event target for zero-compromise community protection.
  - *> 0.90*: F1-Score target for balanced precision-recall performance.
- **Stakeholder Benefit Pillars:**
  - *NDRF & SDMA Commanders:* Common operational picture, pre-staged rescue deployment, real-time shelter capacity tracking.
  - *District Magistrates & State Officials:* Defensible decision support, audit-ready automated incident logs.
  - *Vulnerable Citizens & Gram Panchayats:* Plain-language SMS alerts directing families to safe high-ground shelters.
- **Closing Callout:** `DETECT EARLIER. IDENTIFY LOCALLY. ACT IN TIME.`

### Slide 6: Research, References & Technical Grounding
- **4 Research Quadrants:**
  - *1. Datasets & Telemetry:* IMD AWS & Doppler radar, CWC river gauge baselines, NASA SRTM 30m DEM, Survey of India village boundaries.
  - *2. Geotechnical & Hydrological Models:* Infinite Slope Stability (Factor of Safety), SCS-CN Runoff & SPI, Topographic Wetness Index (TWI), Sequence Modeling (LSTM/XGBoost).
  - *3. Historical Disaster Inventories:* GSI National Landslide Inventory, Uttarakhand SDMA 2013 & 2021 forensic records, Chamoli Rishi Ganga archives.
  - *4. Protocols & Governance:* NDMA Standard Operating Protocols, WMO Early Warnings for All (EW4All), Sendai Framework Target G, TRAI emergency SMS regulations.
- **Footer:** Smart India Hackathon 2026 | Prepared for Ministry of Home Affairs & NDRF | PRALAYADARSHI
