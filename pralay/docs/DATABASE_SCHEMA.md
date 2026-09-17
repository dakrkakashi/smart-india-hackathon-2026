# Database Schema Documentation

**Pralay Flash Flood Prediction System**  
**Version:** 0.1.0  
**Database:** PostgreSQL 16 + PostGIS + TimescaleDB

---

## Overview

The Pralay database schema is designed to support:
- Hierarchical administrative regions with geospatial boundaries
- Real-time IoT sensor data with time-series optimization
- ML-driven risk assessment and prediction
- Multi-level early warning alert system
- Historical disaster data for ML training

## Tables

### 1. regions

Administrative boundaries with hierarchical structure.

**Key Fields:**
- `boundary` (MULTIPOLYGON) - Administrative boundary
- `centroid` (POINT) - Center point
- `region_type` - ENUM: state, district, block, village, ward
- `parent_id` - Self-referential FK for hierarchy
- `vulnerability_level` - ENUM: low, moderate, high, very_high, extreme

**Use Cases:**
- Store village/ward boundaries from Census data
- Calculate affected population in risk zones
- Hierarchical region filtering

### 2. sensors

IoT sensor device registry.

**Key Fields:**
- `sensor_id` - Unique device identifier (e.g., ESP32 MAC address)
- `sensor_type` - ENUM: soil_moisture, rain_gauge, water_level, etc.
- `location` (POINT) - GPS coordinates
- `status` - ENUM: active, inactive, maintenance, faulty, decommissioned
- `last_heartbeat_at` - Latest communication timestamp
- `mqtt_topic` - MQTT subscription topic

**Use Cases:**
- Register field sensors
- Monitor sensor health (battery, signal)
- Map sensor coverage

### 3. sensor_readings ⚡ TimescaleDB Hypertable

Time-series sensor measurements.

**Key Fields:**
- `sensor_id` - FK to sensors
- `timestamp` - ISO 8601 datetime
- `value` - Measured value
- `unit` - Measurement unit (mm, %, cm, °C)
- `quality_score` - 0-1 data quality indicator

**Optimizations:**
- Partitioned by `created_at` (1-day chunks)
- Composite index on (sensor_id, timestamp)
- Automatic data retention policies possible

**Use Cases:**
- Store real-time sensor readings from MQTT
- Query time-series data for ML features
- Dashboard charts (rainfall trends, soil moisture)

### 4. aggregated_readings

Pre-computed hourly/daily sensor statistics.

**Key Fields:**
- `sensor_id` - FK to sensors
- `aggregation_interval` - 'hourly', 'daily', '15min'
- `value_min`, `value_max`, `value_avg`, `value_sum` - Statistics
- `reading_count` - Number of raw readings

**Use Cases:**
- Fast dashboard queries
- Historical trend analysis
- Reduce query load on raw readings table

### 5. risk_zones

Geographic zones with ML-predicted flood risk.

**Key Fields:**
- `geometry` (POLYGON) - Zone boundary (e.g., grid cell)
- `risk_level` - ENUM: none, low, moderate, high, extreme
- `risk_score` - 0-1 probability from ML model
- `confidence` - Model confidence score
- `lead_time_hours` - Time until risk materializes
- `rainfall_intensity`, `soil_saturation`, `slope_stability_factor` - Contributing factors

**Use Cases:**
- Store ML prediction outputs
- Generate risk heatmaps
- Trigger alerts when risk exceeds threshold

### 6. alerts

Early warning alerts and notifications.

**Key Fields:**
- `alert_code` - Unique identifier (e.g., "UKD-CHM-20260916-001")
- `severity` - ENUM: green, yellow, orange, red
- `status` - ENUM: pending, dispatched, acknowledged, in_progress, resolved
- `affected_population` - Estimated people at risk
- `evacuation_routes` - JSON array of route data
- `sms_sent`, `push_sent`, `email_sent` - Notification status

**Lifecycle:**
```
pending → dispatched → acknowledged → in_progress → resolved
                                                   ↘ cancelled / expired
```

**Use Cases:**
- Issue evacuation warnings
- Track alert acknowledgment by officials
- Post-event accuracy evaluation

### 7. historical_disasters

Past flood and landslide events for ML training.

**Key Fields:**
- `event_date` - Date of disaster
- `event_type` - 'flash_flood', 'landslide', 'cloudburst'
- `location` (POINT) - Event location
- `rainfall_24h`, `rainfall_72h` - Rainfall before event
- `casualties`, `affected_population` - Impact data
- `label` - 1=disaster, 0=no disaster (for ML)

**Use Cases:**
- Train ML models
- Identify high-risk patterns
- Validate prediction accuracy

### 8. terrain_grids

DEM-derived terrain characteristics.

**Key Fields:**
- `geometry` (POLYGON) - Grid cell (e.g., 90m × 90m)
- `elevation` - Height above sea level (meters)
- `slope_angle` - Degrees
- `twi` - Topographic Wetness Index
- `spi` - Stream Power Index
- `soil_type`, `soil_cohesion`, `soil_friction_angle` - Soil properties

**Use Cases:**
- Store processed DEM data
- ML feature engineering (terrain + rainfall → risk)
- Slope stability calculations

### 9. drainage_basins

Watershed delineation.

**Key Fields:**
- `boundary` (POLYGON) - Watershed boundary
- `outlet_point` (POINT) - Basin outlet
- `area_sq_km` - Basin area
- `concentration_time_hours` - Time for water to reach outlet
- `parent_basin_id` - Hierarchical sub-basins

**Use Cases:**
- Understand water flow patterns
- Calculate runoff accumulation
- Basin-level risk aggregation

## Relationships

```
regions (1) ──→ (N) sensors
regions (1) ──→ (N) risk_zones
regions (1) ──→ (N) alerts
regions (1) ──→ (N) historical_disasters
regions (1) ──→ (N) terrain_grids

sensors (1) ──→ (N) sensor_readings
sensors (1) ──→ (N) aggregated_readings

regions (1) ──→ (N) regions  [self-referential hierarchy]
drainage_basins (1) ──→ (N) drainage_basins  [self-referential]
```

## Indexes

**Performance-Critical Indexes:**
- `ix_sensor_readings_sensor_timestamp` - Time-series queries
- `ix_sensors_region_id` - Regional sensor filtering
- `ix_risk_zones_risk_level` - High-risk zone queries
- `ix_alerts_status` - Active alert filtering
- `ix_historical_disasters_event_date` - Temporal queries

## Extensions Required

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
```

## Sample Data Flow

1. **Sensor Registration:**
   ```
   ESP32 → MQTT → IoT Gateway → INSERT INTO sensors
   ```

2. **Real-Time Data Ingestion:**
   ```
   Sensor Reading → MQTT → Celery Worker → INSERT INTO sensor_readings
   ```

3. **ML Prediction Pipeline:**
   ```
   SELECT terrain + weather + sensor data
   → ML Model (LSTM + XGBoost)
   → INSERT INTO risk_zones
   ```

4. **Alert Generation:**
   ```
   IF risk_zone.risk_score > threshold:
     INSERT INTO alerts
     → Notification Service (SMS/Push)
   ```

---

**Migration:** `alembic upgrade head`  
**Rollback:** `alembic downgrade -1`
