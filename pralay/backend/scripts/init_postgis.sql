-- Initialize PostGIS and TimescaleDB extensions
-- This script runs on database initialization

-- Enable PostGIS extension for geospatial data
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Enable TimescaleDB for time-series data
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Verify extensions
SELECT PostGIS_version();
