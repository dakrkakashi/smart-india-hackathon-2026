"""
Alert Generation and Cooldown Lifecycle Engine
Enforces PRD §14 alert management, deduplication, auto-escalation, and cooldown rules
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from app.utils.constants import RiskLevel, HazardType, ALERT_COOLDOWN_MINUTES
from app.models.alert import AlertSeverity, AlertStatus


class AlertService:
    """
    Manages generation, suppression of alert fatigue, and auto-escalation
    """
    def __init__(self):
        # In-memory tracking of active alerts per region_id for fast cooldown checks
        # {region_id: {'severity': AlertSeverity, 'issued_at': datetime, 'alert_id': int}}
        self._active_alert_cache: Dict[int, Dict[str, Any]] = {}

    def should_generate_alert(
        self,
        region_id: int,
        new_severity: AlertSeverity,
        current_time: Optional[datetime] = None
    ) -> Tuple_Decision:
        """
        Determines whether an alert should be emitted, suppressed due to cooldown, or escalated.
        Returns: (should_emit: bool, is_escalation: bool, reason: str)
        """
        now = current_time or datetime.utcnow()
        active = self._active_alert_cache.get(region_id)

        # 1. First alert for this region
        if not active:
            return True, False, "New hazard condition detected"

        last_severity = active['severity']
        last_time = active['issued_at']
        elapsed_minutes = (now - last_time).total_seconds() / 60.0

        severity_rank = {
            AlertSeverity.GREEN: 0,
            AlertSeverity.YELLOW: 1,
            AlertSeverity.ORANGE: 2,
            AlertSeverity.RED: 3
        }

        curr_rank = severity_rank.get(new_severity, 0)
        prev_rank = severity_rank.get(last_severity, 0)

        # 2. Auto-escalation: If severity worsened, ALWAYS generate immediately regardless of cooldown
        if curr_rank > prev_rank:
            return True, True, f"Hazard escalated from {last_severity.value.upper()} to {new_severity.value.upper()}"

        # 3. De-escalation or same severity: Check cooldown period to prevent alert fatigue
        if elapsed_minutes < ALERT_COOLDOWN_MINUTES:
            return False, False, f"Suppressed under {ALERT_COOLDOWN_MINUTES}-min cooldown (issued {int(elapsed_minutes)}m ago)"

        # Cooldown expired, allowed to emit periodic update
        return True, False, "Cooldown expired; periodic status update"

    def record_alert(self, region_id: int, alert_id: int, severity: AlertSeverity, timestamp: Optional[datetime] = None):
        """Records dispatched alert into active cache"""
        now = timestamp or datetime.utcnow()
        self._active_alert_cache[region_id] = {
            'alert_id': alert_id,
            'severity': severity,
            'issued_at': now
        }

    def acknowledge_alert(self, region_id: int, official_name: str) -> bool:
        """Marks alert acknowledged"""
        if region_id in self._active_alert_cache:
            self._active_alert_cache[region_id]['acknowledged'] = True
            self._active_alert_cache[region_id]['acknowledged_by'] = official_name
            return True
        return False


# Type alias for cleaner code
Tuple_Decision = tuple[bool, bool, str]
