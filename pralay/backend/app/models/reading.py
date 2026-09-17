"""
Sensor Reading models for time-series data
Uses TimescaleDB hypertables for efficient time-series storage
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.models import BaseModel


class SensorReading(BaseModel):
    """
    Individual sensor reading - time-series data
    This table will be converted to a TimescaleDB hypertable partitioned by timestamp
    """

    __tablename__ = "sensor_readings"

    # Foreign Key to Sensor
    sensor_id = Column(Integer, ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False, index=True)
    sensor = relationship("Sensor", back_populates="readings")

    # Timestamp (for TimescaleDB partitioning)
    timestamp = Column(String(50), nullable=False, index=True)  # ISO 8601 format

    # Reading Value
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)  # mm, %, cm, °C, etc.

    # Quality Indicators
    quality_score = Column(Float, default=1.0)  # 0-1, where 1 is perfect quality
    is_anomaly = Column(Integer, default=0)  # boolean - flagged by anomaly detection
    is_validated = Column(Integer, default=0)  # boolean - manually validated

    # Sensor State at Reading Time
    battery_level = Column(Float, nullable=True)
    signal_strength = Column(Float, nullable=True)

    # Processing Metadata
    processed = Column(Integer, default=0)  # boolean - has been ingested by ML pipeline
    raw_payload = Column(String(500), nullable=True)  # Original MQTT/HTTP payload for debugging

    # Composite index for efficient time-series queries
    __table_args__ = (
        Index('ix_sensor_readings_sensor_timestamp', 'sensor_id', 'timestamp'),
    )

    def __repr__(self):
        return f"<SensorReading(sensor_id={self.sensor_id}, value={self.value}{self.unit}, timestamp='{self.timestamp}')>"


class AggregatedReading(BaseModel):
    """
    Pre-aggregated sensor readings for faster dashboard queries
    Stores hourly/daily aggregations: min, max, avg, sum
    """

    __tablename__ = "aggregated_readings"

    # Reference
    sensor_id = Column(Integer, ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False, index=True)

    # Time Window
    timestamp = Column(String(50), nullable=False, index=True)  # Start of time window
    aggregation_interval = Column(String(20), nullable=False)  # 'hourly', 'daily', '15min'

    # Aggregated Values
    value_min = Column(Float, nullable=False)
    value_max = Column(Float, nullable=False)
    value_avg = Column(Float, nullable=False)
    value_sum = Column(Float, nullable=False)
    reading_count = Column(Integer, nullable=False)  # Number of readings in this window

    # Quality
    quality_avg = Column(Float, default=1.0)
    anomaly_count = Column(Integer, default=0)

    __table_args__ = (
        Index('ix_aggregated_sensor_timestamp', 'sensor_id', 'timestamp'),
    )

    def __repr__(self):
        return f"<AggregatedReading(sensor_id={self.sensor_id}, interval='{self.aggregation_interval}', avg={self.value_avg})>"
