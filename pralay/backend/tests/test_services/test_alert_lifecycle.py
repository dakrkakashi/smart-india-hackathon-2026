"""
Unit Tests for Alert Generation, Fatigue Cooldown, and Auto-Escalation
"""

import pytest
from datetime import datetime, timedelta
from app.services.alert_service import AlertService
from app.models.alert import AlertSeverity


def test_alert_cooldown_and_auto_escalation():
    """Verify cooldown prevents duplicate alerts, but higher severity bypasses cooldown immediately"""
    service = AlertService()
    t0 = datetime(2026, 9, 16, 12, 0, 0)

    # 1. Initial Yellow alert
    should_emit, is_esc, _ = service.should_generate_alert(region_id=1, new_severity=AlertSeverity.YELLOW, current_time=t0)
    assert should_emit is True
    service.record_alert(region_id=1, alert_id=101, severity=AlertSeverity.YELLOW, timestamp=t0)

    # 2. Duplicate Yellow alert after only 10 minutes (within 30m cooldown)
    t_10m = t0 + timedelta(minutes=10)
    should_emit, is_esc, reason = service.should_generate_alert(region_id=1, new_severity=AlertSeverity.YELLOW, current_time=t_10m)
    assert should_emit is False
    assert "cooldown" in reason.lower()

    # 3. Severity escalation to RED after 12 minutes (MUST bypass cooldown!)
    t_12m = t0 + timedelta(minutes=12)
    should_emit, is_esc, reason = service.should_generate_alert(region_id=1, new_severity=AlertSeverity.RED, current_time=t_12m)
    assert should_emit is True
    assert is_esc is True
    assert "escalated" in reason.lower()
