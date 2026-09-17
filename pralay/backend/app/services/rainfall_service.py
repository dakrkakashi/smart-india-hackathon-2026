"""
Rainfall Ingestion and Processing Service
Handles rainfall intensity, accumulation windows, and spatial fallback interpolation
"""

import math
from typing import Dict, List, Optional
from datetime import datetime


class RainfallService:
    """Computes accumulation windows and provides fallback spatial interpolation"""

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Haversine distance in kilometers"""
        R = 6371.0
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @classmethod
    def interpolate_nearest_stations(
        cls,
        target_lat: float,
        target_lon: float,
        available_stations: List[Dict[str, float]],
        power: float = 2.0
    ) -> float:
        """
        Inverse Distance Weighting (IDW) interpolation fallback
        Used when village local rain gauge is offline/unavailable.
        available_stations: [{'lat': float, 'lon': float, 'rainfall_mm': float}, ...]
        """
        if not available_stations:
            return 0.0

        weights_sum = 0.0
        weighted_val_sum = 0.0

        for station in available_stations:
            dist = cls.calculate_distance(target_lat, target_lon, station['lat'], station['lon'])
            if dist < 0.1:  # Co-located station
                return station['rainfall_mm']
            
            w = 1.0 / (dist ** power)
            weights_sum += w
            weighted_val_sum += w * station['rainfall_mm']

        if weights_sum == 0.0:
            return 0.0

        return round(weighted_val_sum / weights_sum, 2)

    @staticmethod
    def compute_accumulation_windows(
        intensity_mm_hr: float,
        history_hourly_readings: Optional[List[float]] = None
    ) -> Dict[str, float]:
        """
        Computes 1h, 3h, 6h, 24h, and 72h accumulations.
        If full historical series is unavailable, projects physical estimates from intensity trend.
        """
        if not history_hourly_readings:
            # Synthetic conservative progression based on current intensity
            h1 = round(intensity_mm_hr, 1)
            h3 = round(intensity_mm_hr * 2.3, 1)
            h6 = round(intensity_mm_hr * 4.1, 1)
            h24 = round(intensity_mm_hr * 9.5, 1)
            h72 = round(h24 * 2.1, 1)
            return {
                "accum_1h_mm": h1,
                "accum_3h_mm": h3,
                "accum_6h_mm": h6,
                "accum_24h_mm": h24,
                "accum_72h_mm": h72,
            }

        # Calculate exact windows from provided reverse-chronological hourly readings
        count = len(history_hourly_readings)
        h1 = history_hourly_readings[0] if count >= 1 else intensity_mm_hr
        h3 = sum(history_hourly_readings[:3]) if count >= 3 else sum(history_hourly_readings)
        h6 = sum(history_hourly_readings[:6]) if count >= 6 else sum(history_hourly_readings)
        h24 = sum(history_hourly_readings[:24]) if count >= 24 else sum(history_hourly_readings)
        h72 = sum(history_hourly_readings[:72]) if count >= 72 else sum(history_hourly_readings)

        return {
            "accum_1h_mm": round(h1, 1),
            "accum_3h_mm": round(h3, 1),
            "accum_6h_mm": round(h6, 1),
            "accum_24h_mm": round(h24, 1),
            "accum_72h_mm": round(h72, 1),
        }
