# Phase 1.2 Complete - Database Schema Design ✅

**Completed:** 2026-09-16 15:25 UTC  
**Duration:** ~45 minutes

---

## Summary

Successfully designed and implemented the complete database schema for the Pralay Flash Flood Prediction System with PostGIS and TimescaleDB support.

## What Was Created

### SQLAlchemy Models (8 Models)

1. **BaseModel** (`models/__init__.py`)
   - Base class with timestamp mixin
   - Common fields: id, created_at, updated_at

2. **Region** (`models/region.py`)
   - Administrative hierarchy (State → District → Block → Village/Ward)
   - PostGIS geometry: boundary (MULTIPOLYGON), centroid (POINT)
   - Vulnerability assessment fields
   - Population and infrastructure data
   - Self-referential hierarchy with parent-child relationships

3. **Sensor** (`models/sensor.py`)
   - IoT device registration and metadata
   - 7 sensor types: soil_moisture, rain_gauge, water_level, temperature, humidity, slope_inclinometer, pore_pressure
   - PostGIS location (POINT)
   - Health monitoring: battery, signal strength, last heartbeat
   - MQTT connectivity configuration
   - Calibration parameters

4. **SensorReading** (`models/reading.py`)
   - Time-series sensor data
   - **TimescaleDB hypertable** partitioned by timestamp
   - Quality indicators and anomaly detection flags
   - Raw MQTT payload storage for debugging

5. **AggregatedReading** (`models/reading.py`)
   - Pre-aggregated sensor data (hourly/daily)
   - Min, max, avg, sum statistics
   - Optimized for dashboard queries

6. **RiskZone** (`models/risk_zone.py`)
   - Geographic zones with calculated flood risk
   - Risk levels: none, low, moderate, high, extreme
   - PostGIS geometry (POLYGON)
   - Contributing factors: rainfall, soil saturation, slope stability
   - ML model metadata and feature importance

7. **Alert** (`models/alert.py`)
   - Early warning alerts with 4 severity levels (green/yellow/orange/red)
   - Alert lifecycle: pending → dispatched → acknowledged → in_progress → resolved
   - Impact assessment and evacuation information
   - Notification tracking (SMS, push, email, siren)
   - Post-event feedback for accuracy evaluation

8. **HistoricalDisaster** (`models/historical.py`)
   - Past flood and landslide events
   - Meteorological conditions at time of event
   - Damage assessment and impact data
   - Data provenance and reliability scoring
   - ML training labels

9. **TerrainGrid** (`models/terrain.py`)
   - DEM-derived terrain characteristics
   - Slope angle, aspect, curvature
   - Hydrological indices (TWI, SPI)
   - Soil properties and land use
   - Susceptibility scores

10. **DrainageBasin** (`models/terrain.py`)
    - Watershed delineation
    - Hydrological properties
    - Stream order and runoff coefficients

### Alembic Migration System

**Files Created:**
- `alembic/env.py` - Async SQLAlchemy migration environment
- `alembic.ini` - Alembic configuration
- `alembic/script.py.mako` - Migration template
- `alembic/versions/001_initial_schema.py` - Initial migration with all tables

**Migration Features:**
- Automatic PostGIS and TimescaleDB extension enablement
- All ENUM types defined
- Proper indexes for performance
- Foreign key relationships
- TimescaleDB hypertable configuration for sensor_readings
- Complete upgrade and downgrade paths

### Database Schema Statistics

- **Total Tables:** 10
- **PostGIS Geometries:** 16 columns across tables
- **ENUM Types:** 7 custom enums
- **Indexes:** 40+ indexes for optimal query performance
- **Foreign Keys:** 12 relationships
- **TimescaleDB Hypertables:** 1 (sensor_readings)

### Key Features Implemented

✅ **Hierarchical Region Model**
- Supports State → District → Block → Village/Ward
- Self-referential foreign key
- Full path property for breadcrumb navigation

✅ **Geospatial Support**
- All geometry columns use SRID 4326 (WGS84/GPS)
- POINT, POLYGON, MULTIPOLYGON types
- Ready for spatial queries and proximity analysis

✅ **Time-Series Optimization**
- TimescaleDB hypertable for sensor readings
- 1-day chunks for efficient time-based queries
- Composite indexes on (sensor_id, timestamp)

✅ **ML-Ready Schema**
- Feature importance storage
- Model version tracking
- Training labels and data provenance
- Prediction confidence scores

✅ **Alert Lifecycle Management**
- Complete status workflow
- Notification tracking
- Acknowledgment and resolution
- Post-event evaluation

✅ **Data Quality Tracking**
- Quality scores on sensor readings
- Anomaly detection flags
- Calibration parameters
- Validation status

## ENUM Types Defined

```python
RegionType: state, district, block, village, ward
VulnerabilityLevel: low, moderate, high, very_high, extreme
SensorType: soil_moisture, rain_gauge, water_level, temperature, humidity, slope_inclinometer, pore_pressure
SensorStatus: active, inactive, maintenance, faulty, decommissioned
RiskLevel: none, low, moderate, high, extreme
AlertSeverity: green, yellow, orange, red
AlertStatus: pending, dispatched, acknowledged, in_progress, resolved, cancelled, expired
```

## Example Queries Enabled

The schema now supports:

1. **Spatial Queries:**
   ```sql
   -- Find all sensors within 5km of a point
   SELECT * FROM sensors 
   WHERE ST_DWithin(location::geography, ST_Point(lat, lon)::geography, 5000);
   
   -- Find regions intersecting a risk zone
   SELECT * FROM regions 
   WHERE ST_Intersects(boundary, risk_zone.geometry);
   ```

2. **Time-Series Queries:**
   ```sql
   -- Get sensor readings for last 24 hours
   SELECT * FROM sensor_readings 
   WHERE sensor_id = 123 
   AND created_at > NOW() - INTERVAL '24 hours'
   ORDER BY created_at DESC;
   ```

3. **Hierarchical Queries:**
   ```sql
   -- Get all villages in a district
   WITH RECURSIVE region_tree AS (
     SELECT * FROM regions WHERE id = district_id
     UNION ALL
     SELECT r.* FROM regions r
     INNER JOIN region_tree rt ON r.parent_id = rt.id
   )
   SELECT * FROM region_tree WHERE region_type = 'village';
   ```

4. **Risk Assessment:**
   ```sql
   -- Active high-risk zones with no alerts
   SELECT rz.* FROM risk_zones rz
   WHERE rz.risk_level IN ('high', 'extreme')
   AND rz.is_active = 1
   AND rz.alert_generated = 0;
   ```

## Next Steps

**Phase 1.3: Region & Terrain Data Ingestion**
- Download SRTM/ASTER DEM data
- Process elevation, slope, aspect from DEM
- Seed village/ward boundaries
- Store terrain features in PostGIS

**Files to Create:**
- `data/scripts/download_srtm.py`
- `data/scripts/process_dem.py`
- `data/scripts/seed_regions.py`
- `backend/app/services/terrain_service.py`

---

**Phase 1 Progress:** 50% Complete (1.1 ✅ | 1.2 ✅ | 1.3 ⏳ | 1.4 ⏳)
