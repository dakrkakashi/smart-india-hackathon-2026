"""
Initial database schema migration
Creates all tables with PostGIS and TimescaleDB support

Revision ID: 001
Create Date: 2026-09-16 15:23:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial schema"""

    # Enable PostGIS and TimescaleDB extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis_topology;")
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")

    # Create ENUM types
    region_type_enum = ENUM('state', 'district', 'block', 'village', 'ward', name='regiontype', create_type=True)
    vulnerability_level_enum = ENUM('low', 'moderate', 'high', 'very_high', 'extreme', name='vulnerabilitylevel', create_type=True)
    sensor_type_enum = ENUM('soil_moisture', 'rain_gauge', 'water_level', 'temperature', 'humidity', 'slope_inclinometer', 'pore_pressure', name='sensortype', create_type=True)
    sensor_status_enum = ENUM('active', 'inactive', 'maintenance', 'faulty', 'decommissioned', name='sensorstatus', create_type=True)
    risk_level_enum = ENUM('none', 'low', 'moderate', 'high', 'extreme', name='risklevel', create_type=True)
    alert_severity_enum = ENUM('green', 'yellow', 'orange', 'red', name='alertseverity', create_type=True)
    alert_status_enum = ENUM('pending', 'dispatched', 'acknowledged', 'in_progress', 'resolved', 'cancelled', 'expired', name='alertstatus', create_type=True)

    # Regions table
    op.create_table(
        'regions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('region_type', region_type_enum, nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('boundary', geoalchemy2.Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True),
        sa.Column('centroid', geoalchemy2.Geometry(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('area_sq_km', sa.Float(), nullable=True),
        sa.Column('elevation_min', sa.Float(), nullable=True),
        sa.Column('elevation_max', sa.Float(), nullable=True),
        sa.Column('elevation_mean', sa.Float(), nullable=True),
        sa.Column('population', sa.Integer(), nullable=True),
        sa.Column('households', sa.Integer(), nullable=True),
        sa.Column('vulnerability_score', sa.Float(), server_default='0.0'),
        sa.Column('vulnerability_level', vulnerability_level_enum, server_default='low'),
        sa.Column('historical_flood_count', sa.Integer(), server_default='0'),
        sa.Column('historical_landslide_count', sa.Integer(), server_default='0'),
        sa.Column('last_disaster_date', sa.String(length=50), nullable=True),
        sa.Column('has_early_warning_system', sa.Integer(), server_default='0'),
        sa.Column('evacuation_shelters_count', sa.Integer(), server_default='0'),
        sa.Column('hospitals_count', sa.Integer(), server_default='0'),
        sa.Column('roads_accessible', sa.Integer(), server_default='1'),
        sa.Column('data_source', sa.String(length=255), nullable=True),
        sa.Column('notes', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['regions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_regions_code', 'regions', ['code'], unique=True)
    op.create_index('ix_regions_name', 'regions', ['name'])
    op.create_index('ix_regions_parent_id', 'regions', ['parent_id'])
    op.create_index('ix_regions_region_type', 'regions', ['region_type'])

    # Sensors table
    op.create_table(
        'sensors',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('sensor_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('sensor_type', sensor_type_enum, nullable=False),
        sa.Column('manufacturer', sa.String(length=100), nullable=True),
        sa.Column('model', sa.String(length=100), nullable=True),
        sa.Column('region_id', sa.Integer(), nullable=False),
        sa.Column('location', geoalchemy2.Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('elevation', sa.Float(), nullable=True),
        sa.Column('installation_date', sa.String(length=50), nullable=True),
        sa.Column('installed_by', sa.String(length=255), nullable=True),
        sa.Column('status', sensor_status_enum, server_default='active'),
        sa.Column('battery_level', sa.Float(), nullable=True),
        sa.Column('signal_strength', sa.Float(), nullable=True),
        sa.Column('last_reading_at', sa.String(length=50), nullable=True),
        sa.Column('last_heartbeat_at', sa.String(length=50), nullable=True),
        sa.Column('connection_type', sa.String(length=50), server_default='mqtt'),
        sa.Column('mqtt_topic', sa.String(length=255), nullable=True),
        sa.Column('reporting_interval', sa.Integer(), server_default='300'),
        sa.Column('calibration_date', sa.String(length=50), nullable=True),
        sa.Column('calibration_offset', sa.Float(), server_default='0.0'),
        sa.Column('calibration_multiplier', sa.Float(), server_default='1.0'),
        sa.Column('is_solar_powered', sa.Integer(), server_default='1'),
        sa.Column('power_backup_hours', sa.Integer(), nullable=True),
        sa.Column('notes', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_sensors_sensor_id', 'sensors', ['sensor_id'], unique=True)
    op.create_index('ix_sensors_region_id', 'sensors', ['region_id'])
    op.create_index('ix_sensors_sensor_type', 'sensors', ['sensor_type'])
    op.create_index('ix_sensors_status', 'sensors', ['status'])

    # Sensor Readings table (will be converted to TimescaleDB hypertable)
    op.create_table(
        'sensor_readings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('sensor_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.String(length=50), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('quality_score', sa.Float(), server_default='1.0'),
        sa.Column('is_anomaly', sa.Integer(), server_default='0'),
        sa.Column('is_validated', sa.Integer(), server_default='0'),
        sa.Column('battery_level', sa.Float(), nullable=True),
        sa.Column('signal_strength', sa.Float(), nullable=True),
        sa.Column('processed', sa.Integer(), server_default='0'),
        sa.Column('raw_payload', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_sensor_readings_sensor_id', 'sensor_readings', ['sensor_id'])
    op.create_index('ix_sensor_readings_sensor_timestamp', 'sensor_readings', ['sensor_id', 'timestamp'])
    op.create_index('ix_sensor_readings_timestamp', 'sensor_readings', ['timestamp'])

    # Convert to TimescaleDB hypertable
    op.execute("""
        SELECT create_hypertable('sensor_readings', 'created_at',
                                 chunk_time_interval => INTERVAL '1 day',
                                 if_not_exists => TRUE);
    """)

    # Aggregated Readings table
    op.create_table(
        'aggregated_readings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('sensor_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.String(length=50), nullable=False),
        sa.Column('aggregation_interval', sa.String(length=20), nullable=False),
        sa.Column('value_min', sa.Float(), nullable=False),
        sa.Column('value_max', sa.Float(), nullable=False),
        sa.Column('value_avg', sa.Float(), nullable=False),
        sa.Column('value_sum', sa.Float(), nullable=False),
        sa.Column('reading_count', sa.Integer(), nullable=False),
        sa.Column('quality_avg', sa.Float(), server_default='1.0'),
        sa.Column('anomaly_count', sa.Integer(), server_default='0'),
        sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_aggregated_sensor_timestamp', 'aggregated_readings', ['sensor_id', 'timestamp'])

    # Risk Zones table
    op.create_table(
        'risk_zones',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=False),
        sa.Column('zone_name', sa.String(length=255), nullable=False),
        sa.Column('zone_code', sa.String(length=50), nullable=True),
        sa.Column('geometry', geoalchemy2.Geometry(geometry_type='POLYGON', srid=4326), nullable=False),
        sa.Column('centroid', geoalchemy2.Geometry(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('risk_level', risk_level_enum, server_default='none'),
        sa.Column('risk_score', sa.Float(), server_default='0.0'),
        sa.Column('confidence', sa.Float(), server_default='0.0'),
        sa.Column('lead_time_hours', sa.Float(), nullable=True),
        sa.Column('prediction_timestamp', sa.String(length=50), nullable=False),
        sa.Column('valid_until', sa.String(length=50), nullable=True),
        sa.Column('rainfall_intensity', sa.Float(), nullable=True),
        sa.Column('soil_saturation', sa.Float(), nullable=True),
        sa.Column('slope_stability_factor', sa.Float(), nullable=True),
        sa.Column('water_level', sa.Float(), nullable=True),
        sa.Column('affected_population', sa.Integer(), server_default='0'),
        sa.Column('affected_households', sa.Integer(), server_default='0'),
        sa.Column('critical_infrastructure_at_risk', sa.String(length=500), nullable=True),
        sa.Column('model_version', sa.String(length=50), nullable=True),
        sa.Column('feature_importance', sa.String(length=1000), nullable=True),
        sa.Column('is_active', sa.Integer(), server_default='1'),
        sa.Column('alert_generated', sa.Integer(), server_default='0'),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_risk_zones_region_id', 'risk_zones', ['region_id'])
    op.create_index('ix_risk_zones_risk_level', 'risk_zones', ['risk_level'])
    op.create_index('ix_risk_zones_zone_code', 'risk_zones', ['zone_code'], unique=True)

    # Alerts table
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=False),
        sa.Column('alert_code', sa.String(length=50), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=False),
        sa.Column('severity', alert_severity_enum, nullable=False),
        sa.Column('alert_type', sa.String(length=50), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('issued_at', sa.String(length=50), nullable=False),
        sa.Column('effective_at', sa.String(length=50), nullable=True),
        sa.Column('expires_at', sa.String(length=50), nullable=True),
        sa.Column('lead_time_hours', sa.Float(), nullable=True),
        sa.Column('status', alert_status_enum, server_default='pending'),
        sa.Column('acknowledged_at', sa.String(length=50), nullable=True),
        sa.Column('acknowledged_by', sa.String(length=255), nullable=True),
        sa.Column('resolved_at', sa.String(length=50), nullable=True),
        sa.Column('affected_population', sa.Integer(), server_default='0'),
        sa.Column('affected_villages', sa.String(length=500), nullable=True),
        sa.Column('evacuation_required', sa.Integer(), server_default='0'),
        sa.Column('recommended_actions', sa.String(length=1000), nullable=True),
        sa.Column('evacuation_routes', sa.String(length=1000), nullable=True),
        sa.Column('safe_zones', sa.String(length=500), nullable=True),
        sa.Column('sms_sent', sa.Integer(), server_default='0'),
        sa.Column('sms_count', sa.Integer(), server_default='0'),
        sa.Column('push_sent', sa.Integer(), server_default='0'),
        sa.Column('push_count', sa.Integer(), server_default='0'),
        sa.Column('email_sent', sa.Integer(), server_default='0'),
        sa.Column('email_count', sa.Integer(), server_default='0'),
        sa.Column('siren_triggered', sa.Integer(), server_default='0'),
        sa.Column('triggered_by', sa.String(length=100), server_default='ml_engine'),
        sa.Column('model_version', sa.String(length=50), nullable=True),
        sa.Column('source_sensors', sa.String(length=500), nullable=True),
        sa.Column('escalation_level', sa.Integer(), server_default='1'),
        sa.Column('escalated_at', sa.String(length=50), nullable=True),
        sa.Column('was_accurate', sa.Integer(), nullable=True),
        sa.Column('false_alarm', sa.Integer(), server_default='0'),
        sa.Column('feedback_notes', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_alerts_alert_code', 'alerts', ['alert_code'], unique=True)
    op.create_index('ix_alerts_region_id', 'alerts', ['region_id'])
    op.create_index('ix_alerts_severity', 'alerts', ['severity'])
    op.create_index('ix_alerts_status', 'alerts', ['status'])

    # Historical Disasters table
    op.create_table(
        'historical_disasters',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('event_date', sa.String(length=50), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('event_name', sa.String(length=255), nullable=True),
        sa.Column('region_id', sa.Integer(), nullable=True),
        sa.Column('location', geoalchemy2.Geometry(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('affected_area', geoalchemy2.Geometry(geometry_type='POLYGON', srid=4326), nullable=True),
        sa.Column('severity', sa.String(length=50), nullable=True),
        sa.Column('casualties', sa.Integer(), server_default='0'),
        sa.Column('injuries', sa.Integer(), server_default='0'),
        sa.Column('missing', sa.Integer(), server_default='0'),
        sa.Column('affected_population', sa.Integer(), server_default='0'),
        sa.Column('affected_households', sa.Integer(), server_default='0'),
        sa.Column('economic_loss_cr', sa.Float(), nullable=True),
        sa.Column('infrastructure_damage', sa.String(length=500), nullable=True),
        sa.Column('rainfall_24h', sa.Float(), nullable=True),
        sa.Column('rainfall_72h', sa.Float(), nullable=True),
        sa.Column('rainfall_intensity', sa.Float(), nullable=True),
        sa.Column('slope_angle', sa.Float(), nullable=True),
        sa.Column('elevation', sa.Float(), nullable=True),
        sa.Column('soil_type', sa.String(length=100), nullable=True),
        sa.Column('source', sa.String(length=255), nullable=True),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('reliability_score', sa.Float(), server_default='0.5'),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('notes', sa.String(length=500), nullable=True),
        sa.Column('used_for_training', sa.Integer(), server_default='1'),
        sa.Column('label', sa.Integer(), server_default='1'),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_historical_disasters_event_date', 'historical_disasters', ['event_date'])
    op.create_index('ix_historical_disasters_event_type', 'historical_disasters', ['event_type'])
    op.create_index('ix_historical_disasters_region_id', 'historical_disasters', ['region_id'])

    # Terrain Grids table
    op.create_table(
        'terrain_grids',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=True),
        sa.Column('grid_code', sa.String(length=50), nullable=True),
        sa.Column('geometry', geoalchemy2.Geometry(geometry_type='POLYGON', srid=4326), nullable=False),
        sa.Column('centroid', geoalchemy2.Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('elevation', sa.Float(), nullable=False),
        sa.Column('elevation_min', sa.Float(), nullable=True),
        sa.Column('elevation_max', sa.Float(), nullable=True),
        sa.Column('elevation_std', sa.Float(), nullable=True),
        sa.Column('slope_angle', sa.Float(), nullable=False),
        sa.Column('slope_aspect', sa.Float(), nullable=True),
        sa.Column('slope_category', sa.String(length=50), nullable=True),
        sa.Column('profile_curvature', sa.Float(), nullable=True),
        sa.Column('plan_curvature', sa.Float(), nullable=True),
        sa.Column('twi', sa.Float(), nullable=True),
        sa.Column('spi', sa.Float(), nullable=True),
        sa.Column('flow_accumulation', sa.Float(), nullable=True),
        sa.Column('flow_direction', sa.Integer(), nullable=True),
        sa.Column('soil_type', sa.String(length=100), nullable=True),
        sa.Column('soil_depth', sa.Float(), nullable=True),
        sa.Column('soil_cohesion', sa.Float(), nullable=True),
        sa.Column('soil_friction_angle', sa.Float(), nullable=True),
        sa.Column('soil_permeability', sa.Float(), nullable=True),
        sa.Column('land_use', sa.String(length=100), nullable=True),
        sa.Column('vegetation_density', sa.Float(), nullable=True),
        sa.Column('landslide_susceptibility', sa.Float(), server_default='0.0'),
        sa.Column('flood_susceptibility', sa.Float(), server_default='0.0'),
        sa.Column('dem_source', sa.String(length=100), server_default='SRTM'),
        sa.Column('dem_resolution', sa.Integer(), server_default='90'),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_terrain_grids_grid_code', 'terrain_grids', ['grid_code'], unique=True)
    op.create_index('ix_terrain_grids_region_id', 'terrain_grids', ['region_id'])
    op.create_index('ix_terrain_grids_slope', 'terrain_grids', ['slope_angle'])

    # Drainage Basins table
    op.create_table(
        'drainage_basins',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('basin_code', sa.String(length=50), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('boundary', geoalchemy2.Geometry(geometry_type='POLYGON', srid=4326), nullable=False),
        sa.Column('outlet_point', geoalchemy2.Geometry(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('area_sq_km', sa.Float(), nullable=False),
        sa.Column('perimeter_km', sa.Float(), nullable=True),
        sa.Column('stream_order', sa.Integer(), nullable=True),
        sa.Column('average_slope', sa.Float(), nullable=True),
        sa.Column('concentration_time_hours', sa.Float(), nullable=True),
        sa.Column('runoff_coefficient', sa.Float(), nullable=True),
        sa.Column('parent_basin_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['parent_basin_id'], ['drainage_basins.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_drainage_basins_basin_code', 'drainage_basins', ['basin_code'], unique=True)

    print("✅ Initial schema created successfully with PostGIS and TimescaleDB support!")


def downgrade() -> None:
    """Drop all tables"""
    op.drop_table('drainage_basins')
    op.drop_table('terrain_grids')
    op.drop_table('historical_disasters')
    op.drop_table('alerts')
    op.drop_table('risk_zones')
    op.drop_table('aggregated_readings')
    op.drop_table('sensor_readings')
    op.drop_table('sensors')
    op.drop_table('regions')

    # Drop ENUMs
    sa.Enum(name='alertstatus').drop(op.get_bind())
    sa.Enum(name='alertseverity').drop(op.get_bind())
    sa.Enum(name='risklevel').drop(op.get_bind())
    sa.Enum(name='sensorstatus').drop(op.get_bind())
    sa.Enum(name='sensortype').drop(op.get_bind())
    sa.Enum(name='vulnerabilitylevel').drop(op.get_bind())
    sa.Enum(name='regiontype').drop(op.get_bind())
