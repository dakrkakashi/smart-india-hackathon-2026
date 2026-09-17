"""
Unit Tests for Transparent Compound Risk Engine
"""

import pytest
from app.services.risk_engine import RiskEngine
from app.utils.constants import RiskLevel, HazardType


def test_flood_risk_bounds():
    """Ensure flood risk is always bounded between 0 and 100"""
    # Nominal calm conditions
    score_calm = RiskEngine.calculate_flood_risk(
        rainfall_intensity_mm_hr=2.0,
        rainfall_accum_24h_mm=5.0,
        river_level_m=1.2,
        river_rate_of_rise_m_hr=0.01,
        elevation_m=1500.0,
        historical_flood_count=0
    )
    assert 0.0 <= score_calm < 25.0

    # Catastrophic breach conditions
    score_severe = RiskEngine.calculate_flood_risk(
        rainfall_intensity_mm_hr=85.0,
        rainfall_accum_24h_mm=180.0,
        river_level_m=7.5,
        river_rate_of_rise_m_hr=1.9,
        elevation_m=1500.0,
        historical_flood_count=3
    )
    assert 80.0 <= score_severe <= 100.0


def test_landslide_risk_sensitivity():
    """Ensure steep slope + high soil saturation sharply spikes landslide risk"""
    # Low slope, dry soil
    score_safe = RiskEngine.calculate_landslide_risk(
        rainfall_intensity_mm_hr=5.0,
        rainfall_duration_hrs=2.0,
        soil_moisture_pct=25.0,
        saturation_trend_pct_hr=0.1,
        slope_degrees=8.0,
        historical_landslide_count=0
    )
    assert score_safe < 20.0

    # High slope (38 degrees) + saturated soil (88%)
    score_high = RiskEngine.calculate_landslide_risk(
        rainfall_intensity_mm_hr=65.0,
        rainfall_duration_hrs=8.0,
        soil_moisture_pct=88.0,
        saturation_trend_pct_hr=6.5,
        slope_degrees=38.0,
        historical_landslide_count=4
    )
    assert score_high >= 70.0


def test_compound_risk_classification():
    """Test compound integration and 4-tier banding (GREEN, YELLOW, ORANGE, RED)"""
    # Low + Low -> GREEN
    score_g, lvl_g, prim_g, _ = RiskEngine.calculate_compound_risk(15.0, 10.0, 0.2)
    assert lvl_g == RiskLevel.GREEN
    assert score_g < 30.0

    # Moderate -> YELLOW
    score_y, lvl_y, prim_y, _ = RiskEngine.calculate_compound_risk(40.0, 35.0, 0.4)
    assert lvl_y == RiskLevel.YELLOW
    assert 30.0 <= score_y < 60.0

    # High -> ORANGE
    score_o, lvl_o, prim_o, _ = RiskEngine.calculate_compound_risk(70.0, 50.0, 0.6)
    assert lvl_o == RiskLevel.ORANGE
    assert 60.0 <= score_o < 80.0

    # Critical -> RED
    score_r, lvl_r, prim_r, _ = RiskEngine.calculate_compound_risk(92.0, 88.0, 0.9)
    assert lvl_r == RiskLevel.RED
    assert score_r >= 80.0
    assert prim_r == HazardType.COMPOUND
