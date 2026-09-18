import { DemonstrationStep } from "../types/risk";

export const mockScenarioSteps: DemonstrationStep[] = [
  {
    "step": 1,
    "timestamp": "14:00 UTC",
    "description": "Heavy rainfall begins over Chamoli catchment.",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 22.0,
      "rainfall_accum_24h_mm": 45.0,
      "soil_moisture_pct": 35.0,
      "river_level_m": 3.1,
      "river_rate_of_rise_m_hr": 0.05
    },
    "assessment": {
      "flood_risk_score": 31.95,
      "landslide_risk_score": 53.88,
      "compound_risk_score": 54.61,
      "risk_level": "YELLOW",
      "primary_hazard": "LANDSLIDE",
      "estimated_lead_time_minutes": 152
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "WATCH: Alert disaster management volunteers in Raini. Stand by for escalation."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 2,
    "timestamp": "14:25 UTC",
    "description": "Rainfall intensity surges to 55 mm/hr (torrential downpour).",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 55.0,
      "rainfall_accum_24h_mm": 68.0,
      "soil_moisture_pct": 48.0,
      "river_level_m": 3.6,
      "river_rate_of_rise_m_hr": 0.35
    },
    "assessment": {
      "flood_risk_score": 51.63,
      "landslide_risk_score": 68.45,
      "compound_risk_score": 68.02,
      "risk_level": "ORANGE",
      "primary_hazard": "LANDSLIDE",
      "estimated_lead_time_minutes": 582
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "PREPARE EVACUATION: Stage transport and move vulnerable citizens in Zone A (Lower Riverbank & Valley Floor) to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 3,
    "timestamp": "14:45 UTC",
    "description": "Soil moisture sensors detect rapid saturation increase (slope pore pressure building).",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 68.0,
      "rainfall_accum_24h_mm": 92.0,
      "soil_moisture_pct": 64.0,
      "river_level_m": 4.2,
      "river_rate_of_rise_m_hr": 0.6
    },
    "assessment": {
      "flood_risk_score": 61.63,
      "landslide_risk_score": 75.97,
      "compound_risk_score": 74.91,
      "risk_level": "ORANGE",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 280
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "PREPARE EVACUATION: Stage transport and move vulnerable citizens in Zone A (Lower Riverbank & Valley Floor) to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 4,
    "timestamp": "15:05 UTC",
    "description": "Rishi Ganga river water level crosses warning mark; rate of rise exceeds 1.1 m/hr.",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 78.0,
      "rainfall_accum_24h_mm": 118.0,
      "soil_moisture_pct": 74.0,
      "river_level_m": 5.4,
      "river_rate_of_rise_m_hr": 1.1
    },
    "assessment": {
      "flood_risk_score": 76.84,
      "landslide_risk_score": 80.73,
      "compound_risk_score": 81.04,
      "risk_level": "RED",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 87
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 5,
    "timestamp": "15:20 UTC",
    "description": "PRALAYADARSHI compound risk engine detects simultaneous flood + slope collapse conditions.",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 85.0,
      "rainfall_accum_24h_mm": 140.0,
      "soil_moisture_pct": 81.0,
      "river_level_m": 6.2,
      "river_rate_of_rise_m_hr": 1.45
    },
    "assessment": {
      "flood_risk_score": 87.57,
      "landslide_risk_score": 84.06,
      "compound_risk_score": 86.93,
      "risk_level": "RED",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 33
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 6,
    "timestamp": "15:35 UTC",
    "description": "Village Raini risk rating escalates into CRITICAL (RED).",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 92.0,
      "rainfall_accum_24h_mm": 165.0,
      "soil_moisture_pct": 86.0,
      "river_level_m": 6.9,
      "river_rate_of_rise_m_hr": 1.8
    },
    "assessment": {
      "flood_risk_score": 92.07,
      "landslide_risk_score": 86.01,
      "compound_risk_score": 90.25,
      "risk_level": "RED",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 10
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 7,
    "timestamp": "15:40 UTC",
    "description": "System displays CRITICAL RISK with Estimated Lead Time: 35 minutes.",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 95.0,
      "rainfall_accum_24h_mm": 175.0,
      "soil_moisture_pct": 88.0,
      "river_level_m": 7.1,
      "river_rate_of_rise_m_hr": 1.95
    },
    "assessment": {
      "flood_risk_score": 92.5,
      "landslide_risk_score": 86.05,
      "compound_risk_score": 90.54,
      "risk_level": "RED",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 35
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 8,
    "timestamp": "15:42 UTC",
    "description": "System identifies high-risk zone: Zone A (Lower Riverbank & Valley Floor Terrace).",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 95.0,
      "rainfall_accum_24h_mm": 178.0,
      "soil_moisture_pct": 88.5,
      "river_level_m": 7.2,
      "river_rate_of_rise_m_hr": 1.95
    },
    "assessment": {
      "flood_risk_score": 92.5,
      "landslide_risk_score": 86.06,
      "compound_risk_score": 90.54,
      "risk_level": "RED",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 35
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 9,
    "timestamp": "15:44 UTC",
    "description": "System identifies nearest available safe shelter outside flood plain.",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 95.0,
      "rainfall_accum_24h_mm": 180.0,
      "soil_moisture_pct": 89.0,
      "river_level_m": 7.3,
      "river_rate_of_rise_m_hr": 1.95
    },
    "assessment": {
      "flood_risk_score": 92.5,
      "landslide_risk_score": 86.08,
      "compound_risk_score": 90.54,
      "risk_level": "RED",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 35
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 10,
    "timestamp": "15:46 UTC",
    "description": "System calculates safe evacuation path avoiding flooded culverts and debris flow slopes.",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 95.0,
      "rainfall_accum_24h_mm": 182.0,
      "soil_moisture_pct": 89.0,
      "river_level_m": 7.3,
      "river_rate_of_rise_m_hr": 1.95
    },
    "assessment": {
      "flood_risk_score": 92.5,
      "landslide_risk_score": 86.09,
      "compound_risk_score": 90.54,
      "risk_level": "RED",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 35
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": null,
    "citizen_card": null
  },
  {
    "step": 11,
    "timestamp": "15:48 UTC",
    "description": "District Magistrate & NDRF Control Room receive prioritized CRITICAL alert with action blueprint.",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 95.0,
      "rainfall_accum_24h_mm": 184.0,
      "soil_moisture_pct": 89.0,
      "river_level_m": 7.4,
      "river_rate_of_rise_m_hr": 1.95
    },
    "assessment": {
      "flood_risk_score": 92.5,
      "landslide_risk_score": 86.1,
      "compound_risk_score": 90.55,
      "risk_level": "RED",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 35
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": {
      "alert_level": "RED",
      "target_village": "Raini",
      "compound_score": 90.55,
      "lead_time": "35 minutes",
      "shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route": "ROUTE-RAI-1",
      "action_required": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "citizen_card": null
  },
  {
    "step": 12,
    "timestamp": "15:50 UTC",
    "description": "Citizens in Raini receive simplified bilingual emergency warning card with shelter & route instructions.",
    "environmental_inputs": {
      "rainfall_intensity_mm_hr": 95.0,
      "rainfall_accum_24h_mm": 185.0,
      "soil_moisture_pct": 89.0,
      "river_level_m": 7.4,
      "river_rate_of_rise_m_hr": 1.95
    },
    "assessment": {
      "flood_risk_score": 92.5,
      "landslide_risk_score": 86.12,
      "compound_risk_score": 90.55,
      "risk_level": "RED",
      "primary_hazard": "COMPOUND",
      "estimated_lead_time_minutes": 35
    },
    "decisions": {
      "affected_zone": "Zone A (Lower Riverbank & Valley Floor)",
      "recommended_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route_id": "ROUTE-RAI-1",
      "action": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "authority_dispatch": {
      "alert_level": "RED",
      "target_village": "Raini",
      "compound_score": 90.55,
      "lead_time": "35 minutes",
      "shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_route": "ROUTE-RAI-1",
      "action_required": "URGENT: Evacuate Raini (Zone A (Lower Riverbank & Valley Floor)) immediately to Raini Upper Primary School & Panchayat Bhavan."
    },
    "citizen_card": {
      "severity_label": "RED ALERT",
      "hazard_title": "COMPOUND FLASH FLOOD & LANDSLIDE RISK",
      "village_name": "Raini",
      "estimated_lead_time": "35 minutes",
      "action_directive": "IMMEDIATE EVACUATION REQUIRED: Move to designated safe shelter immediately.",
      "assigned_shelter": "Raini Upper Primary School & Panchayat Bhavan",
      "evacuation_advice": "Use marked Upper Ridge Trail. Avoid riverbanks, low-lying bridges, and steep roadside slopes.",
      "emergency_contact": "District Disaster Control Room: 1077 / 01372-252107",
      "timestamp": "2026-09-18 04:15 UTC"
    }
  }
];
