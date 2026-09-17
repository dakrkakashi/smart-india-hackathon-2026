import { HazardType } from './risk';

export interface GeoPoint {
  lat: number;
  lng: number;
}

export interface EvacuationWaypoint {
  name: string;
  lat: number;
  lng: number;
  type: 'START' | 'SAFE_CORRIDOR' | 'DESTINATION';
}

export interface EvacuationRoute {
  route_id: string;
  destination_shelter_id: number;
  destination_shelter_name: string;
  total_distance_km: number;
  estimated_transit_minutes: number;
  status: string;
  avoid_sectors: string[];
  waypoints: EvacuationWaypoint[];
  instructions: string;
}

export interface MapFilterState {
  district: 'ALL' | string;
  hazard: 'ALL' | HazardType;
  showShelters: boolean;
}
