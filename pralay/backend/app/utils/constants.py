"""
PRALAYADARSHI System Constants and Configuration Enums
Defines core decision standards per PRD specifications (PS 26192)
"""

from enum import Enum


class RiskLevel(str, Enum):
    """Four-tier risk classification matching authority protocols"""
    GREEN = "GREEN"      # Low: Normal monitoring
    YELLOW = "YELLOW"    # Moderate: Increased monitoring / preparedness
    ORANGE = "ORANGE"    # High: Prepare evacuation
    RED = "RED"          # Critical: Immediate evacuation


class HazardType(str, Enum):
    """Primary hazard categories"""
    NONE = "NONE"
    FLASH_FLOOD = "FLASH_FLOOD"
    LANDSLIDE = "LANDSLIDE"
    COMPOUND = "COMPOUND"


class ActionType(str, Enum):
    """Standardized operational actions for field responders and citizens"""
    MONITOR = "Continuous monitoring; verify sensor status"
    PREPARE = "Alert village response team; review shelter inventory"
    PREPARE_EVACUATION = "Initiate pre-evacuation alert for vulnerable populations"
    IMMEDIATE_EVACUATION = "Execute immediate evacuation to designated shelter via safe route"


# Compound Risk Banding Thresholds (0 - 100)
RISK_THRESHOLDS = {
    RiskLevel.GREEN: (0.0, 30.0),
    RiskLevel.YELLOW: (30.0, 60.0),
    RiskLevel.ORANGE: (60.0, 80.0),
    RiskLevel.RED: (80.0, 100.0),
}

# Standard recommended action text mapped from RiskLevel
ACTION_RECOMMENDATIONS = {
    RiskLevel.GREEN: "Maintain routine observation. No immediate action required.",
    RiskLevel.YELLOW: "Elevate watch status. Place village disaster committee on standby and inspect local drainage.",
    RiskLevel.ORANGE: "Stage evacuation transport. Move livestock and vulnerable citizens to higher ground.",
    RiskLevel.RED: "EVACUATE IMMEDIATELY. Move all residents along designated safe paths to designated shelter.",
}

# Alert fatigue cooldown window (minutes) per zone
ALERT_COOLDOWN_MINUTES = 30

# UI Safety Requirement: Text descriptor constraint (PRD §12)
LEAD_TIME_LABEL = "Estimated Lead Time"
