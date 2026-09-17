"""
PRALAY - Smart India Hackathon 2026
Slide-by-Slide Content Sheet & Single Source of Truth
Problem Statement: 26192 (Disaster Management / Software)
Ministry of Home Affairs - NDRF / DM Division
"""

SLIDES_CONTENT = {
    "metadata": {
        "event": "Smart India Hackathon 2026",
        "theme": "Disaster Management",
        "category": "Software",
        "ps_id": "26192",
        "ps_title": "Flash Flood Prediction System for Hilly Regions",
        "organization": "Ministry of Home Affairs (NDRF / DM Division)",
        "project_name": "PRALAYADARSHI (PRALAY)",
        "project_tagline": "Compound Risk → Lead Time → Action",
        "hero_subtitle": "Hyperlocal Flash Flood & Debris-Flow Early Warning with Ridge Evacuation Intelligence",
        "signature_stat": "35 Minutes",
        "signature_stat_desc": "Estimated lead-time window before surge arrival — transforming panic into organized ridge evacuation.",
        "closing_mantra": "DETECT EARLIER. IDENTIFY LOCALLY. ACT IN TIME."
    },
    "slide_1": {
        "title": "PRALAYADARSHI",
        "tagline": "Compound Risk → Lead Time → Action",
        "subtitle": "Hyperlocal Flash Flood & Debris Flow Early Warning with Ridge Evacuation Intelligence",
        "ps_details": {
            "ps_id": "Problem Statement ID: 26192",
            "theme": "Theme: Disaster Management",
            "category": "Category: Software",
            "org": "Ministry of Home Affairs | NDRF / DM Division"
        },
        "team_details": {
            "team_name": "Team Pralay",
            "lead": "Team Lead & System Architects",
            "pilot_region": "Pilot Focus: Chamoli & Rudraprayag, Uttarakhand"
        },
        "value_prop": "Deterministic Physics + IoT Multi-Source Telemetry answering WHERE, HOW SEVERE, HOW SOON, and WHAT NOW for mountain communities.",
        "speaker_notes": (
            "Good morning respected jury members. We present PRALAYADARSHI for SIH Problem Statement 26192. "
            "In fragile Himalayan catchments like Chamoli and Rudraprayag, flash floods and debris flows strike in less than an hour. "
            "Current systems give regional district-level alerts that tell officials 'rain is coming', but fail to answer where the surge will hit, "
            "how soon, or where villagers should run. Our core philosophy is simple: Compound Risk leads to Lead Time, which drives immediate Action."
        )
    },
    "slide_2": {
        "title": "Proposed Solution & North Star Architecture",
        "subtitle": "Moving from Fragmented District Advisories to Hyperlocal, Actionable Decision Support",
        "columns": [
            {
                "header": "Current System Gap",
                "points": [
                    "Macro-level alerts covering 100+ km² with zero village precision.",
                    "Isolated data silos: Rainfall, river gauges, and slope geology never fused.",
                    "Zero evacuation guidance: Citizens told 'heavy rain expected' without safe paths or shelter assignments.",
                    "Widespread alert fatigue from chronic district-wide false alarms."
                ],
                "badge": "THE PROBLEM"
            },
            {
                "header": "The PRALAY Innovation",
                "points": [
                    "Hyperlocal Catchments: Village-level watershed monitoring (Raini, Tharali, Joshimath).",
                    "Deterministic Physics Fusion: River rate-of-rise + rainfall intensity + soil pore saturation.",
                    "Dynamic Lead-Time Engine: Explicit 'Estimated Lead Time' in minutes (e.g. 35 mins).",
                    "Active Evacuation Routing: Automated shelter assignment avoiding gorge flood corridors."
                ],
                "badge": "OUR SOLUTION"
            }
        ],
        "north_star_cards": [
            {
                "q": "1. WHERE IS THE RISK?",
                "ans": "Hyperlocal village catchment polygons (Lat/Lon, basin terrain, slope angle).",
                "color": "BLUE"
            },
            {
                "q": "2. HOW SEVERE?",
                "ans": "Compound Risk (0–100) mapped to 4-Tier Scale: GREEN / YELLOW / ORANGE / RED.",
                "color": "ORANGE"
            },
            {
                "q": "3. HOW SOON?",
                "ans": "Explicit 'Estimated Lead Time' in minutes (e.g. 35 mins), projected from surge rise.",
                "color": "RED"
            },
            {
                "q": "4. WHAT NOW?",
                "ans": "Designated safe shelter above flood line + turn-by-turn ridge bypass trail.",
                "color": "GREEN"
            }
        ],
        "dual_interface": {
            "authority": "Authority Operations Dashboard: Live GIS multi-hazard overlays, sensor telemetry, aggregate district metrics, and manual broadcast overrides.",
            "citizen": "Citizen Emergency Alert Card (PRD §18): Jargon-free vernacular SMS/Card — 'EVACUATE IMMEDIATELY to Raini Primary School via Upper Ridge Trail. Avoid River Ghat.'"
        },
        "speaker_notes": (
            "Slide 2 outlines our core solution architecture. Rather than building a generic dashboard, PRALAY is ruthlessly designed "
            "around four North Star operational questions: WHERE is the risk, HOW SEVERE, HOW SOON, and WHAT NOW. "
            "For disaster officials, our control room provides multi-hazard compound scores and sensor health. For the villager on the ground, "
            "we eliminate technical jargon and deliver a plain-language Citizen Card via SMS with their assigned shelter and ridge escape route."
        )
    },
    "slide_3": {
        "title": "Technical Approach & Multi-Source Fusion Pipeline",
        "subtitle": "Physics-Grounded Deterministic Computation + Multi-Source Sensor Ingestion Pipeline",
        "pipeline_steps": [
            {"num": "1", "name": "SENSE", "desc": "IoT Rain Gauges, Ultrasonic River Levels, Soil TDR & IMD Radar"},
            {"num": "2", "name": "VALIDATE & FUSE", "desc": "Spike filtering, outlier bounds check, sensor timeout & spatial IDW"},
            {"num": "3", "name": "ASSESS", "desc": "Flood Risk (0-100) + Landslide Slope Risk (0-100) + Soil Saturation"},
            {"num": "4", "name": "PREDICT", "desc": "Compound Risk Index + Dynamic Rate-of-Rise Estimated Lead Time"},
            {"num": "5", "name": "ACT", "desc": "Floodplain-excluding shelter assignment & ridge bypass evacuation routing"}
        ],
        "stack_chips": [
            "Python FastAPI", "PostgreSQL + PostGIS", "TimescaleDB Hypertables", "Redis & Celery",
            "ESP32 / MQTT Telemetry", "Pydantic V2", "React 18 + Vite", "Tailwind + TypeScript"
        ],
        "compound_formula": {
            "formula": "Compound Risk = max(Flood, Landslide) × 0.65 + min(Flood, Landslide) × 0.20 + Vulnerability × 15",
            "rationale": "Prioritizes the dominant hazard surge while compounding secondary slope failure risks and village population exposure."
        },
        "validation_guardrails": [
            "Hardware Validation: Sensor timeout marks source UNAVAILABLE, never silently assumed 0.",
            "Alert Fatigue Suppression: 30-minute cooldown suppression for recurring alerts; immediate auto-escalation on severity spike.",
            "Hydraulic Routing: Shelters located inside active flood plains are strictly excluded from assignment."
        ],
        "speaker_notes": (
            "On Slide 3, we detail our technical pipeline: Sense, Fuse, Assess, Predict, and Act. "
            "Our backend is built on FastAPI, PostGIS, and TimescaleDB hypertables for time-series telemetry. "
            "Our risk model is transparent and physics-grounded: calculating flood velocity and slope stability without black-box hallucinations. "
            "We enforce strict engineering guardrails: if an ultrasonic river sensor goes offline, it is marked UNAVAILABLE rather than silently normal, "
            "and repeating alerts are suppressed under a 30-minute cooldown to prevent warning fatigue."
        )
    },
    "slide_4": {
        "title": "Feasibility, Viability & Implementation Roadmap",
        "subtitle": "Engineering Rigor, Edge-Resilient Deployment & Phased Operational Rollout",
        "roadmap_phases": [
            {
                "phase": "Phase A: Pilot Prototype",
                "timeline": "Months 1–3 (Delivered & Verified)",
                "details": "Chamoli & Rudraprayag pilot catchments, 14/14 automated tests passing, 12-step cloudburst simulator, React decision panes."
            },
            {
                "phase": "Phase B: Field Telemetry & IoT",
                "timeline": "Months 4–7",
                "details": "Solar-powered ESP32 nodes, ultrasonic stream sensors, LoRaWAN gateways across Alaknanda & Mandakini basins."
            },
            {
                "phase": "Phase C: State & Regional Scale",
                "timeline": "Months 8–12",
                "details": "Integration with SDMA Uttarakhand, CWC hydrological feeds, multi-lingual vernacular SMS dispatch."
            }
        ],
        "risk_mitigation": [
            {
                "risk": "IMD API Outage / Network Cut",
                "mitigation": "Local station caching + Inverse Distance Weighting (IDW) spatial fallback to adjacent active nodes."
            },
            {
                "risk": "Field Sensor Physical Failure",
                "mitigation": "Heartbeat watcher flags source UNAVAILABLE; model degrades gracefully to upstream rain gauge estimates."
            },
            {
                "risk": "Mountain Cellular Dropouts",
                "mitigation": "LoRaWAN edge mesh buffering up to 72 hours of readings on SD flash; emergency alert relays."
            },
            {
                "risk": "False Alarm Alert Fatigue",
                "mitigation": "Dual-threshold confirmation + 30-minute zone cooldown suppression; instant escalation on worsening."
            }
        ],
        "cost_viability": "Low-Cost Edge Hardware: ₹12,000–₹18,000 per solar IoT monitoring node with 5-year maintenance life.",
        "speaker_notes": (
            "Slide 4 addresses feasibility and real-world viability. We have already delivered and verified Phase A with a working software prototype, "
            "14 passing integration tests, and pilot catchments in Chamoli. Our phased roadmap scales from pilot validation to solar IoT deployment. "
            "Importantly, we tackle real mountain challenges: if mountain cellular towers fail, our edge nodes buffer data via LoRaWAN; "
            "and if an upstream sensor breaks, the engine automatically degrades gracefully using spatial interpolation."
        )
    },
    "slide_5": {
        "title": "Impact, Operational Benefits & Target Metrics",
        "subtitle": "Quantifiable Life-Safety Outcomes for Mountain Communities & Disaster Responders",
        "target_metrics": [
            {"stat": "30–45 Mins", "label": "Estimated Lead Time", "sub": "Target window for pre-impact evacuation"},
            {"stat": "< 10%", "label": "False Positive Rate", "sub": "Target threshold to eliminate warning fatigue"},
            {"stat": "< 5%", "label": "Missed Event Target", "sub": "Zero-compromise disaster detection target"},
            {"stat": "> 0.90", "label": "F1-Score Target", "sub": "Balanced precision-recall performance goal"}
        ],
        "stakeholder_benefits": [
            {
                "role": "NDRF & SDMA Commanders",
                "benefit": "Common Operational Picture: Exact village catchments at risk, automated shelter capacity tracking, and pre-staged rescue deployment."
            },
            {
                "role": "District Magistrates & Officials",
                "benefit": "Defensible Decision Support: Scientific lead-time estimates and audit-ready automated incident logs for accountability."
            },
            {
                "role": "Vulnerable Citizens & Gram Panchayats",
                "benefit": "Clear Plain-Language Instructions: Plain SMS alerts naming safe high-ground shelters and avoiding lethal river corridors."
            }
        ],
        "closing_callout": "DETECT EARLIER. IDENTIFY LOCALLY. ACT IN TIME.",
        "speaker_notes": (
            "Slide 5 highlights our tangible operational impact. Our North Star target is a 30 to 45 minute estimated lead-time window, "
            "allowing families in high-risk zones like Raini to reach designated high-ground shelters before gorge waters crest. "
            "By maintaining false positive targets below 10%, we rebuild public trust in early warning systems. "
            "For NDRF commanders, PRALAY replaces vague weather warnings with high-confidence tactical intelligence."
        )
    },
    "slide_6": {
        "title": "Research, References & Technical Grounding",
        "subtitle": "Grounded in Authoritative Hydrological Standards, Geotechnical Formulations & National Datasets",
        "quadrants": [
            {
                "title": "Datasets & Telemetry Feeds",
                "items": [
                    "India Meteorological Department (IMD) AWS & Doppler Radar Rainfall",
                    "Central Water Commission (CWC) River Gauge Baselines",
                    "NASA SRTM 30m Digital Elevation Models (Slope, Aspect, Drainage)",
                    "Survey of India & Census 2011 Village Spatial Boundaries"
                ]
            },
            {
                "title": "Geotechnical & Hydrological Models",
                "items": [
                    "Deterministic Infinite Slope Stability Formulation (Factor of Safety)",
                    "SCS-CN Hydrological Runoff & Stream Power Index (SPI)",
                    "Topographic Wetness Index (TWI) for Himalayan Debris Basins",
                    "Ensemble Time-Series Sequence Modeling (LSTM / XGBoost)"
                ]
            },
            {
                "title": "Disaster Inventories & Validation",
                "items": [
                    "Geological Survey of India (GSI) National Landslide Susceptibility",
                    "Uttarakhand SDMA 2013 & 2021 Post-Disaster Forensic Archives",
                    "Chamoli Rishi Ganga Flash Flood Historical Reconstruction Data",
                    "EM-DAT International Disaster Database Records"
                ]
            },
            {
                "title": "Protocols & Governance Alignment",
                "items": [
                    "National Disaster Management Authority (NDMA) Standard Operating Protocols",
                    "WMO Early Warnings for All (EW4All) Global Guidelines",
                    "Sendai Framework for Disaster Risk Reduction (2015–2030) Target G",
                    "TRAI Guidelines for Priority Emergency Telecom Warning SMS"
                ]
            }
        ],
        "footer_note": "Smart India Hackathon 2026 | Prepared for Ministry of Home Affairs & NDRF | PRALAYADARSHI",
        "speaker_notes": (
            "Finally, Slide 6 demonstrates the scientific and institutional grounding of PRALAY. "
            "Our algorithms build upon proven hydrological formulas including the Infinite Slope model and Topographic Wetness Index, "
            "benchmarked against historical records from the 2013 Kedarnath and 2021 Chamoli disasters. "
            "Furthermore, our alert dispatch architecture strictly complies with NDMA standard operating protocols and TRAI emergency telecom guidelines. "
            "Thank you, and we look forward to your questions."
        )
    }
}
