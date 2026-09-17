"""
Transparent Compound Risk Engine
Implements deterministic, physics-grounded weighted models per PRD §9 & §10
"""

from typing import Dict, Any, Tuple
from app.utils.constants import RiskLevel, HazardType, RISK_THRESHOLDS


class RiskEngine:
    """
    Transparent weighted risk calculation engine.
    Computes Flash Flood Risk, Landslide Risk, and Compound Village Risk.
    Scores are strictly normalized to 0 - 100.
    """

    @staticmethod
    def calculate_flood_risk(
        rainfall_intensity_mm_hr: float,
        rainfall_accum_24h_mm: float,
        river_level_m: float,
        river_rate_of_rise_m_hr: float,
        elevation_m: float,
        drainage_efficiency_score: float = 0.5,  # 0.0 (choked) to 1.0 (free flowing)
        historical_flood_count: int = 0,
        warning_river_level_m: float = 5.0,
        danger_river_level_m: float = 7.0,
    ) -> float:
        """
        Calculates Flash Flood Risk score (0 - 100).
        Weights:
        - River level relative to danger mark (30%)
        - River rate of rise (25%)
        - Rainfall intensity (20%)
        - Rainfall 24h accumulation (10%)
        - Drainage / elevation factor (10%)
        - Historical flood frequency (5%)
        """
        # 1. River level ratio (0 - 1.0 capped)
        river_norm = max(0.0, min(1.0, river_level_m / max(0.1, danger_river_level_m)))
        if river_level_m >= danger_river_level_m:
            river_norm = 1.0 + min(0.5, (river_level_m - danger_river_level_m) / 2.0)
            river_norm = min(1.0, river_norm)

        # 2. River rate of rise (>= 1.5 m/hr is catastrophic mountain flash flood)
        rate_norm = max(0.0, min(1.0, river_rate_of_rise_m_hr / 1.5))

        # 3. Rainfall intensity (IMD: >= 50 mm/hr is torrential downpour/cloudburst)
        rain_int_norm = max(0.0, min(1.0, rainfall_intensity_mm_hr / 60.0))

        # 4. 24h accumulation (>= 150 mm is very heavy rain)
        accum_norm = max(0.0, min(1.0, rainfall_accum_24h_mm / 150.0))

        # 5. Drainage factor (lower efficiency = higher ponding)
        drainage_norm = 1.0 - max(0.0, min(1.0, drainage_efficiency_score))

        # 6. Historical susceptibility
        hist_norm = max(0.0, min(1.0, historical_flood_count / 5.0))

        # Weighted combination
        score = (
            (river_norm * 0.30) +
            (rate_norm * 0.25) +
            (rain_int_norm * 0.20) +
            (accum_norm * 0.10) +
            (drainage_norm * 0.10) +
            (hist_norm * 0.05)
        ) * 100.0

        return round(max(0.0, min(100.0, score)), 2)

    @staticmethod
    def calculate_landslide_risk(
        rainfall_intensity_mm_hr: float,
        rainfall_duration_hrs: float,
        soil_moisture_pct: float,
        saturation_trend_pct_hr: float,
        slope_degrees: float,
        historical_landslide_count: int = 0,
    ) -> float:
        """
        Calculates Landslide Risk score (0 - 100).
        Weights:
        - Soil moisture saturation level (30%)
        - Slope steepness (25%)
        - Rainfall intensity & duration (25%)
        - Soil saturation rate of increase (15%)
        - Historical landslide recurrence (5%)
        """
        # 1. Soil saturation (>= 80% volumetric water content is critical liquefied threshold)
        soil_norm = max(0.0, min(1.0, (soil_moisture_pct - 20.0) / 65.0))

        # 2. Slope angle (30 - 45 degrees is high landslide frequency)
        if slope_degrees < 10.0:
            slope_norm = 0.05
        elif slope_degrees < 25.0:
            slope_norm = (slope_degrees - 10.0) / 30.0
        elif slope_degrees <= 45.0:
            slope_norm = 0.5 + ((slope_degrees - 25.0) / 20.0) * 0.5
        else:
            # Over 45 degrees is rockfall
            slope_norm = 0.9

        slope_norm = max(0.0, min(1.0, slope_norm))

        # 3. Rainfall intensity and cumulative duration
        intensity_norm = max(0.0, min(1.0, rainfall_intensity_mm_hr / 50.0))
        duration_factor = max(0.0, min(1.0, rainfall_duration_hrs / 24.0))
        rain_trigger = (intensity_norm * 0.6) + (duration_factor * 0.4)

        # 4. Saturation trend rate (positive rate = rapid pore-water pressure buildup)
        trend_norm = max(0.0, min(1.0, saturation_trend_pct_hr / 10.0))

        # 5. Historical landslide count
        hist_norm = max(0.0, min(1.0, historical_landslide_count / 5.0))

        score = (
            (soil_norm * 0.30) +
            (slope_norm * 0.25) +
            (rain_trigger * 0.25) +
            (trend_norm * 0.15) +
            (hist_norm * 0.05)
        ) * 100.0

        return round(max(0.0, min(100.0, score)), 2)

    @classmethod
    def calculate_compound_risk(
        cls,
        flood_risk: float,
        landslide_risk: float,
        local_vulnerability_score: float = 0.5,  # 0.0 (resilient) to 1.0 (extreme vulnerability)
        real_time_escalation_boost: float = 0.0,
    ) -> Tuple[float, RiskLevel, HazardType, HazardType]:
        """
        Calculates unified Compound Risk score (0 - 100).
        Equation:
        Compound = max(flood, landslide) * 0.65 + min(flood, landslide) * 0.20 + vulnerability * 15 + escalation_boost
        Returns: (compound_score, risk_level, primary_hazard, secondary_hazard)
        """
        f = max(0.0, min(100.0, flood_risk))
        l = max(0.0, min(100.0, landslide_risk))
        v = max(0.0, min(1.0, local_vulnerability_score))

        higher_risk = max(f, l)
        lower_risk = min(f, l)

        # Compound formula preserves dominant hazard while compounding secondary threat
        compound_score = (higher_risk * 0.65) + (lower_risk * 0.20) + (v * 15.0) + real_time_escalation_boost
        compound_score = round(max(0.0, min(100.0, compound_score)), 2)

        # Determine Primary & Secondary Hazards
        if f > l + 15.0:
            primary = HazardType.FLASH_FLOOD
            secondary = HazardType.LANDSLIDE if l >= 30.0 else HazardType.NONE
        elif l > f + 15.0:
            primary = HazardType.LANDSLIDE
            secondary = HazardType.FLASH_FLOOD if f >= 30.0 else HazardType.NONE
        elif f >= 30.0 or l >= 30.0:
            primary = HazardType.COMPOUND
            secondary = HazardType.FLASH_FLOOD if f >= l else HazardType.LANDSLIDE
        else:
            primary = HazardType.NONE
            secondary = HazardType.NONE

        # Risk level classification
        risk_level = cls.classify_risk_level(compound_score)

        return compound_score, risk_level, primary, secondary

    @staticmethod
    def classify_risk_level(score: float) -> RiskLevel:
        """Categorize score into standard 4-tier alert scale"""
        if score >= 80.0:
            return RiskLevel.RED
        elif score >= 60.0:
            return RiskLevel.ORANGE
        elif score >= 30.0:
            return RiskLevel.YELLOW
        else:
            return RiskLevel.GREEN
