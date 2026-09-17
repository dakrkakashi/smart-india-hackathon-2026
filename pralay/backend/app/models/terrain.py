"""
Terrain and topographic data models
Stores processed DEM-derived terrain features
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.models import BaseModel


class TerrainGrid(BaseModel):
    """
    Grid cell with terrain characteristics derived from DEM
    Each cell represents a small area (e.g., 90m x 90m for SRTM)
    """

    __tablename__ = "terrain_grids"

    # Location
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True, index=True)
    region = relationship("Region")

    # Grid Identifier
    grid_code = Column(String(50), unique=True, index=True)  # e.g., "UKD-CHM-12345"

    # Geometry
    geometry = Column(Geometry(geometry_type="POLYGON", srid=4326), nullable=False)
    centroid = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

    # Elevation Data
    elevation = Column(Float, nullable=False)  # meters
    elevation_min = Column(Float, nullable=True)  # within cell
    elevation_max = Column(Float, nullable=True)  # within cell
    elevation_std = Column(Float, nullable=True)  # standard deviation

    # Slope Analysis
    slope_angle = Column(Float, nullable=False)  # degrees
    slope_aspect = Column(Float, nullable=True)  # degrees (0-360, North=0)
    slope_category = Column(String(50), nullable=True)  # 'gentle', 'moderate', 'steep', 'very_steep'

    # Curvature
    profile_curvature = Column(Float, nullable=True)  # convex/concave
    plan_curvature = Column(Float, nullable=True)  # diverging/converging flow

    # Hydrological Indices
    twi = Column(Float, nullable=True)  # Topographic Wetness Index
    spi = Column(Float, nullable=True)  # Stream Power Index
    flow_accumulation = Column(Float, nullable=True)
    flow_direction = Column(Integer, nullable=True)  # D8 direction code

    # Soil Properties
    soil_type = Column(String(100), nullable=True)
    soil_depth = Column(Float, nullable=True)  # meters
    soil_cohesion = Column(Float, nullable=True)  # kPa
    soil_friction_angle = Column(Float, nullable=True)  # degrees
    soil_permeability = Column(Float, nullable=True)  # m/s

    # Land Use / Cover
    land_use = Column(String(100), nullable=True)  # forest, agriculture, barren, urban
    vegetation_density = Column(Float, nullable=True)  # 0-1

    # Risk Factors
    landslide_susceptibility = Column(Float, default=0.0)  # 0-1
    flood_susceptibility = Column(Float, default=0.0)  # 0-1

    # Data Source
    dem_source = Column(String(100), default="SRTM")  # SRTM, ASTER, Cartosat
    dem_resolution = Column(Integer, default=90)  # meters

    __table_args__ = (
        Index('ix_terrain_grids_slope', 'slope_angle'),
    )

    def __repr__(self):
        return f"<TerrainGrid(id={self.id}, grid='{self.grid_code}', elevation={self.elevation}m, slope={self.slope_angle}°)>"


class DrainageBasin(BaseModel):
    """
    Watershed / drainage basin delineation
    Important for understanding water flow patterns
    """

    __tablename__ = "drainage_basins"

    # Basic Info
    basin_code = Column(String(50), unique=True, index=True)
    name = Column(String(255), nullable=True)

    # Geometry
    boundary = Column(Geometry(geometry_type="POLYGON", srid=4326), nullable=False)
    outlet_point = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)

    # Characteristics
    area_sq_km = Column(Float, nullable=False)
    perimeter_km = Column(Float, nullable=True)
    stream_order = Column(Integer, nullable=True)  # Strahler order

    # Hydrological Properties
    average_slope = Column(Float, nullable=True)
    concentration_time_hours = Column(Float, nullable=True)  # Time for water to reach outlet
    runoff_coefficient = Column(Float, nullable=True)  # 0-1

    # Parent-Child Relationship
    parent_basin_id = Column(Integer, ForeignKey("drainage_basins.id"), nullable=True)
    parent = relationship("DrainageBasin", remote_side="DrainageBasin.id", backref="sub_basins")

    def __repr__(self):
        return f"<DrainageBasin(id={self.id}, code='{self.basin_code}', area={self.area_sq_km}km²)>"
