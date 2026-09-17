import { Shelter } from '../types/risk';
import { EvacuationRoute } from '../types/map';

export const mockShelters: Shelter[] = [
  {
    id: 1,
    name: 'Raini Upper Primary School & Panchayat Bhavan',
    code: 'SHL-CHM-001',
    shelter_type: 'School / Community Hall',
    region_id: 1,
    latitude: 30.4930,
    longitude: 79.7070,
    capacity: 300,
    current_occupancy: 0,
    available_capacity: 300,
    is_available: true,
    elevation_meters: 2240.0,
    has_drinking_water: true,
    has_power_backup: true,
    has_medical_facility: true,
    contact_person: 'Gram Pradhan Raini',
    contact_phone: '+91-9412000001'
  },
  {
    id: 2,
    name: 'Government Intermediate College (GIC) Tharali',
    code: 'SHL-CHM-002',
    shelter_type: 'College Campus',
    region_id: 2,
    latitude: 30.0680,
    longitude: 79.5050,
    capacity: 600,
    current_occupancy: 35,
    available_capacity: 565,
    is_available: true,
    elevation_meters: 1450.0,
    has_drinking_water: true,
    has_power_backup: true,
    has_medical_facility: true,
    contact_person: 'SDM Tharali Control Room',
    contact_phone: '+91-9412000002'
  },
  {
    id: 3,
    name: 'Joshimath Community Centre - Ravigram',
    code: 'SHL-CHM-003',
    shelter_type: 'Auditorium / Relief Hall',
    region_id: 3,
    latitude: 30.5620,
    longitude: 79.5710,
    capacity: 800,
    current_occupancy: 50,
    available_capacity: 750,
    is_available: true,
    elevation_meters: 1960.0,
    has_drinking_water: true,
    has_power_backup: true,
    has_medical_facility: true,
    contact_person: 'Nagar Palika Joshimath',
    contact_phone: '+91-9412000003'
  },
  {
    id: 4,
    name: 'Sonprayag High-Altitude GMVN Tourist Rest House',
    code: 'SHL-RDP-001',
    shelter_type: 'GMVN Rest House',
    region_id: 4,
    latitude: 30.6350,
    longitude: 79.0040,
    capacity: 450,
    current_occupancy: 10,
    available_capacity: 440,
    is_available: true,
    elevation_meters: 1890.0,
    has_drinking_water: true,
    has_power_backup: true,
    has_medical_facility: true,
    contact_person: 'Disaster Relief Officer Sonprayag',
    contact_phone: '+91-9412000004'
  },
  {
    id: 5,
    name: 'Ukhimath Omkareshwar Community Shelter',
    code: 'SHL-RDP-002',
    shelter_type: 'Temple Trust / Community Hall',
    region_id: 5,
    latitude: 30.5220,
    longitude: 79.1010,
    capacity: 500,
    current_occupancy: 0,
    available_capacity: 500,
    is_available: true,
    elevation_meters: 1380.0,
    has_drinking_water: true,
    has_power_backup: true,
    has_medical_facility: true,
    contact_person: 'Badrinath-Kedarnath Temple Committee',
    contact_phone: '+91-9412000005'
  }
];

export const mockRoute: EvacuationRoute = {
  route_id: 'ROUTE-RAINI-01',
  destination_shelter_id: 1,
  destination_shelter_name: 'Raini Upper Primary School & Panchayat Bhavan',
  total_distance_km: 1.2,
  estimated_transit_minutes: 20,
  status: 'CLEAR_SAFE',
  avoid_sectors: ['Valley Floor Path', 'River Culvert C-12', 'Steep Debris Sector'],
  waypoints: [
    {
      name: 'Raini Assembly Point',
      lat: 30.4905,
      lng: 79.7042,
      type: 'START'
    },
    {
      name: 'High-Elevation Ridge By-Pass (Elev 1,840m)',
      lat: 30.4938,
      lng: 79.7066,
      type: 'SAFE_CORRIDOR'
    },
    {
      name: 'Raini Upper Primary School & Panchayat Bhavan',
      lat: 30.4930,
      lng: 79.7070,
      type: 'DESTINATION'
    }
  ],
  instructions:
    'Evacuate via Upper Ridge Bypass directly to Raini Upper Primary School & Panchayat Bhavan. Distance: 1.2 km (~20 mins). Do not take riverside trail.'
};
