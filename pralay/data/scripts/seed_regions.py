"""
Seed Data Generator for Pilot Hilly Regions: Chamoli & Rudraprayag (Uttarakhand)
Provides realistic geospatial, demographic, terrain, sensor, and shelter profiles.
"""

from typing import List, Dict, Any

PILOT_VILLAGES: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Raini",
        "code": "UK-CHM-001",
        "district": "Chamoli",
        "state": "Uttarakhand",
        "region_type": "village",
        "latitude": 30.4900,
        "longitude": 79.7040,
        "elevation_mean": 2150.0,
        "slope_degrees": 38.5,
        "population": 780,
        "households": 145,
        "vulnerability_score": 0.88,
        "historical_flood_count": 2,      # Chamoli 2021 disaster epicenter
        "historical_landslide_count": 4,
        "drainage_basin": "Rishi Ganga / Dhauli Ganga Basin"
    },
    {
        "id": 2,
        "name": "Tharali",
        "code": "UK-CHM-002",
        "district": "Chamoli",
        "state": "Uttarakhand",
        "region_type": "village",
        "latitude": 30.0633,
        "longitude": 79.5022,
        "elevation_mean": 1380.0,
        "slope_degrees": 28.0,
        "population": 2450,
        "households": 490,
        "vulnerability_score": 0.76,
        "historical_flood_count": 3,      # Pindar River flash floods
        "historical_landslide_count": 3,
        "drainage_basin": "Pindar River Catchment"
    },
    {
        "id": 3,
        "name": "Joshimath",
        "code": "UK-CHM-003",
        "district": "Chamoli",
        "state": "Uttarakhand",
        "region_type": "village",
        "latitude": 30.5574,
        "longitude": 79.5667,
        "elevation_mean": 1890.0,
        "slope_degrees": 34.2,
        "population": 16700,
        "households": 3400,
        "vulnerability_score": 0.92,      # Subsidence & steep slopes
        "historical_flood_count": 1,
        "historical_landslide_count": 6,
        "drainage_basin": "Alaknanda Basin"
    },
    {
        "id": 4,
        "name": "Sonprayag",
        "code": "UK-RDP-001",
        "district": "Rudraprayag",
        "state": "Uttarakhand",
        "region_type": "village",
        "latitude": 30.6300,
        "longitude": 79.0010,
        "elevation_mean": 1820.0,
        "slope_degrees": 32.5,
        "population": 1150,
        "households": 210,
        "vulnerability_score": 0.85,
        "historical_flood_count": 3,      # Mandakini confluence
        "historical_landslide_count": 5,
        "drainage_basin": "Mandakini - Vasuki Ganga Confluence"
    },
    {
        "id": 5,
        "name": "Ukhimath",
        "code": "UK-RDP-002",
        "district": "Rudraprayag",
        "state": "Uttarakhand",
        "region_type": "village",
        "latitude": 30.5186,
        "longitude": 79.0970,
        "elevation_mean": 1311.0,
        "slope_degrees": 24.0,
        "population": 3800,
        "households": 720,
        "vulnerability_score": 0.65,
        "historical_flood_count": 1,
        "historical_landslide_count": 2,
        "drainage_basin": "Middle Mandakini Basin"
    }
]

PILOT_SHELTERS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Raini Upper Primary School & Panchayat Bhavan",
        "code": "SHL-CHM-001",
        "region_id": 1,
        "latitude": 30.4930,
        "longitude": 79.7070,
        "capacity": 300,
        "current_occupancy": 0,
        "elevation_meters": 2240.0,
        "is_available": True,
        "is_in_flood_plain": False,
        "has_drinking_water": True,
        "has_power_backup": True,
        "has_medical_facility": True,
        "contact_person": "Gram Pradhan Raini",
        "contact_phone": "+91-9412000001"
    },
    {
        "id": 2,
        "name": "Government Intermediate College (GIC) Tharali",
        "code": "SHL-CHM-002",
        "region_id": 2,
        "latitude": 30.0680,
        "longitude": 79.5050,
        "capacity": 600,
        "current_occupancy": 35,
        "elevation_meters": 1450.0,
        "is_available": True,
        "is_in_flood_plain": False,
        "has_drinking_water": True,
        "has_power_backup": True,
        "has_medical_facility": True,
        "contact_person": "SDM Tharali Control Room",
        "contact_phone": "+91-9412000002"
    },
    {
        "id": 3,
        "name": "Joshimath Community Centre - Ravigram",
        "code": "SHL-CHM-003",
        "region_id": 3,
        "latitude": 30.5620,
        "longitude": 79.5710,
        "capacity": 800,
        "current_occupancy": 50,
        "elevation_meters": 1960.0,
        "is_available": True,
        "is_in_flood_plain": False,
        "has_drinking_water": True,
        "has_power_backup": True,
        "has_medical_facility": True,
        "contact_person": "Nagar Palika Joshimath",
        "contact_phone": "+91-9412000003"
    },
    {
        "id": 4,
        "name": "Sonprayag High-Altitude GMVN Tourist Rest House",
        "code": "SHL-RDP-001",
        "region_id": 4,
        "latitude": 30.6350,
        "longitude": 79.0040,
        "capacity": 450,
        "current_occupancy": 10,
        "elevation_meters": 1890.0,
        "is_available": True,
        "is_in_flood_plain": False,
        "has_drinking_water": True,
        "has_power_backup": True,
        "has_medical_facility": True,
        "contact_person": "Disaster Relief Officer Sonprayag",
        "contact_phone": "+91-9412000004"
    },
    {
        "id": 5,
        "name": "Ukhimath Omkareshwar Community Shelter",
        "code": "SHL-RDP-002",
        "region_id": 5,
        "latitude": 30.5220,
        "longitude": 79.1010,
        "capacity": 500,
        "current_occupancy": 0,
        "elevation_meters": 1390.0,
        "is_available": True,
        "is_in_flood_plain": False,
        "has_drinking_water": True,
        "has_power_backup": True,
        "has_medical_facility": True,
        "contact_person": "Tehsildar Ukhimath",
        "contact_phone": "+91-9412000005"
    }
]

PILOT_SENSORS: List[Dict[str, Any]] = [
    {"sensor_id": "SN-RAIN-01", "region_id": 1, "type": "rainfall", "name": "Raini Tipping Bucket Rain Gauge", "lat": 30.4905, "lng": 79.7042, "unit": "mm/h", "status": "online"},
    {"sensor_id": "SN-SOIL-01", "region_id": 1, "type": "soil_moisture", "name": "Raini Slope Capacitive Soil Sensor", "lat": 30.4910, "lng": 79.7048, "unit": "%", "status": "online"},
    {"sensor_id": "SN-RIVR-01", "region_id": 1, "type": "water_level", "name": "Rishi Ganga Ultrasonic Level Sensor", "lat": 30.4892, "lng": 79.7031, "unit": "m", "status": "online"},
    {"sensor_id": "SN-RAIN-02", "region_id": 2, "type": "rainfall", "name": "Tharali IMD Weather Station Rain Gauge", "lat": 30.0635, "lng": 79.5025, "unit": "mm/h", "status": "online"},
    {"sensor_id": "SN-RIVR-02", "region_id": 2, "type": "water_level", "name": "Pindar River Radar Water Level Gauge", "lat": 30.0620, "lng": 79.5015, "unit": "m", "status": "online"},
    {"sensor_id": "SN-SOIL-02", "region_id": 2, "type": "soil_moisture", "name": "Tharali Valley Slope Saturation Probe", "lat": 30.0645, "lng": 79.5030, "unit": "%", "status": "online"},
    {"sensor_id": "SN-SOIL-03", "region_id": 3, "type": "soil_moisture", "name": "Joshimath Slope Stability Moisture Node", "lat": 30.5570, "lng": 79.5660, "unit": "%", "status": "online"},
    {"sensor_id": "SN-RIVR-03", "region_id": 4, "type": "water_level", "name": "Mandakini Ultrasonic Stream Gauge", "lat": 30.6295, "lng": 79.0005, "unit": "m", "status": "online"},
]


def get_pilot_villages():
    return PILOT_VILLAGES


def get_pilot_shelters():
    return PILOT_SHELTERS


def get_pilot_sensors():
    return PILOT_SENSORS


if __name__ == "__main__":
    print(f"Loaded {len(PILOT_VILLAGES)} pilot villages, {len(PILOT_SHELTERS)} shelters, and {len(PILOT_SENSORS)} IoT sensors.")
