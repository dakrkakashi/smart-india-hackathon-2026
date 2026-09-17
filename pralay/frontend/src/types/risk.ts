export type RiskLevel = 'GREEN' | 'YELLOW' | 'ORANGE' | 'RED';
export type HazardType = 'NONE' | 'FLASH_FLOOD' | 'LANDSLIDE' | 'COMPOUND';

export interface EstimatedLeadTime {
  label: string;
  minutes: number | null;
  hours: number | null;
  confidence_score: number;
  trend_description: string;
}

export interface RecommendedAction {
  action: string;
  priority: string;
  affected_zone: string;
  nearest_shelter_id: number | null;
  nearest_shelter_name: string | null;
  shelter_distance_km: number | null;
  evacuation_route_id: string | null;
  safe_path_instructions: string | null;
  special_warnings: string[];
}

export interface RiskAssessment {
  village_id: number;
  village_name: string;
  district: string;
  state: string;
  latitude: number;
  longitude: number;
  population_at_risk: number;
  risk_level: RiskLevel;
  compound_risk_score: number;
  flood_risk_score: number;
  landslide_risk_score: number;
  primary_hazard: HazardType;
  secondary_hazard?: HazardType | null;
  lead_time: EstimatedLeadTime;
  action: RecommendedAction;
  rainfall_1h_mm: number;
  rainfall_24h_mm: number;
  soil_moisture_pct: number;
  river_level_m?: number | null;
  river_rate_of_rise_m_per_hr?: number | null;
  slope_degrees: number;
  sensor_health_status: string;
  timestamp: string;
  data_sources_available: string[];
}

export interface CitizenAlertCard {
  severity_label: string;
  hazard_title: string;
  village_name: string;
  estimated_lead_time: string;
  action_directive: string;
  assigned_shelter: string;
  evacuation_advice: string;
  emergency_contact: string;
  timestamp: string;
}

export interface Shelter {
  id: number;
  name: string;
  code: string;
  shelter_type: string;
  region_id: number | null;
  latitude: number;
  longitude: number;
  capacity: number;
  current_occupancy: number;
  available_capacity: number;
  is_available: boolean;
  elevation_meters?: number | null;
  has_drinking_water: boolean;
  has_power_backup: boolean;
  has_medical_facility: boolean;
  contact_person?: string | null;
  contact_phone?: string | null;
}

export interface DemonstrationStep {
  step: number;
  timestamp: string;
  description: string;
  environmental_inputs: {
    rainfall_intensity_mm_hr: number;
    rainfall_accum_24h_mm: number;
    soil_moisture_pct: number;
    river_level_m: number;
    river_rate_of_rise_m_hr: number;
  };
  assessment: {
    flood_risk_score: number;
    landslide_risk_score: number;
    compound_risk_score: number;
    risk_level: RiskLevel;
    primary_hazard: HazardType;
    estimated_lead_time_minutes: number | null;
  };
  decisions: {
    affected_zone: string;
    recommended_shelter: string;
    evacuation_route_id: string;
    action: string;
  };
  authority_dispatch?: any;
  citizen_card?: CitizenAlertCard | null;
}
