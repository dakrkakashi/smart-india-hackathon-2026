"""
Terrain and DEM Analysis Service
Computes slope, aspect, curvature, and Topographic Wetness Index (TWI)
"""

import math
from typing import Dict, Any, Optional


class TerrainService:
    """Calculates topographic metrics for flash flood and landslide susceptibility"""

    @staticmethod
    def calculate_slope(elevation_difference_m: float, horizontal_distance_m: float) -> float:
        """Calculate slope angle in degrees"""
        if horizontal_distance_m <= 0:
            return 0.0
        angle_rad = math.atan(elevation_difference_m / horizontal_distance_m)
        return round(math.degrees(angle_rad), 2)

    @staticmethod
    def calculate_twi(specific_catchment_area_m2: float, slope_degrees: float) -> float:
        """
        Topographic Wetness Index (TWI) = ln(a / tan(beta))
        Higher TWI indicates high saturation and water accumulation potential (valley bottoms).
        """
        if slope_degrees <= 0:
            slope_degrees = 0.5  # prevent division by zero or tan(0)
        slope_rad = math.radians(slope_degrees)
        tan_slope = math.tan(slope_rad)
        if tan_slope <= 0:
            tan_slope = 0.01
        
        ratio = max(1.0, specific_catchment_area_m2) / tan_slope
        return round(math.log(ratio), 2)

    @staticmethod
    def calculate_spi(specific_catchment_area_m2: float, slope_degrees: float) -> float:
        """
        Stream Power Index (SPI) = a * tan(beta)
        Measures erosive power of overland water flow.
        """
        slope_rad = math.radians(max(0.1, slope_degrees))
        tan_slope = math.tan(slope_rad)
        return round(specific_catchment_area_m2 * tan_slope, 2)

    @staticmethod
    def classify_slope_hazard(slope_degrees: float) -> str:
        """
        Classify slope risk based on geotechnical vulnerability:
        < 15 deg: Low landslide risk, higher flood ponding risk
        15 - 30 deg: Moderate risk
        30 - 45 deg: High landslide & debris flow risk
        > 45 deg: Extreme rockfall & rapid slide risk
        """
        if slope_degrees < 15.0:
            return "LOW_SLOPE_HIGH_PONDING"
        elif slope_degrees < 30.0:
            return "MODERATE_SLOPE"
        elif slope_degrees <= 45.0:
            return "CRITICAL_LANDSLIDE_SLOPE"
        else:
            return "EXTREME_SLOPE_ROCKFALL"

    @classmethod
    def evaluate_village_terrain(
        cls,
        elevation_mean_m: float,
        slope_degrees: float,
        catchment_area_m2: float = 50000.0
    ) -> Dict[str, Any]:
        """Comprehensive terrain profile for a village"""
        twi = cls.calculate_twi(catchment_area_m2, slope_degrees)
        spi = cls.calculate_spi(catchment_area_m2, slope_degrees)
        hazard_cat = cls.classify_slope_hazard(slope_degrees)
        
        return {
            "elevation_mean_m": elevation_mean_m,
            "slope_degrees": slope_degrees,
            "twi": twi,
            "spi": spi,
            "slope_classification": hazard_cat,
            "is_steep_slope": slope_degrees >= 25.0,
            "is_flood_basin": twi >= 8.5
        }
