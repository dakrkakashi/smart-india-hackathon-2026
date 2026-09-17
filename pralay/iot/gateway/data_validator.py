"""
IoT Sensor Data Validator
Enforces PRD §8 Data Validation Requirements:
- Outlier detection & spike rejection
- Physical bounds validation
- Duplicate detection
- Sensor health tracking (marks source as UNAVAILABLE on failure; never treats as normal 0)
"""

from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timedelta


class SensorDataValidator:
    """Validates raw IoT telemetry before feeding downstream risk engines"""

    # Physical valid limits
    BOUNDS = {
        "rainfall": {"min": 0.0, "max": 300.0, "max_jump": 80.0},        # mm/hr
        "soil_moisture": {"min": 0.0, "max": 100.0, "max_jump": 25.0},   # %
        "water_level": {"min": 0.0, "max": 35.0, "max_jump": 3.0},       # meters
        "temperature": {"min": -30.0, "max": 55.0, "max_jump": 10.0},    # Celsius
    }

    def __init__(self, timeout_minutes: int = 15):
        self.timeout_minutes = timeout_minutes
        # Sensor tracking: {sensor_id: {'last_value': float, 'last_time': datetime, 'status': str, 'fail_count': int}}
        self._sensor_states: Dict[str, Dict[str, Any]] = {}
        self._seen_payload_hashes: set = set()

    def validate_reading(
        self,
        sensor_id: str,
        sensor_type: str,
        value: Optional[float],
        timestamp: Optional[datetime] = None
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validates an incoming reading.
        Returns: (is_valid: bool, status_reason: str, telemetry_metadata: dict)
        """
        now = timestamp or datetime.utcnow()
        state = self._sensor_states.setdefault(sensor_id, {
            'last_value': None,
            'last_time': None,
            'status': 'ONLINE',
            'fail_count': 0
        })

        # 1. Check missing value
        if value is None:
            state['fail_count'] += 1
            state['status'] = 'UNAVAILABLE'
            return False, "ERR_MISSING_VALUE: Sensor reported null/missing reading", state

        # 2. Check duplicate payload within window
        payload_key = f"{sensor_id}:{value}:{now.isoformat()}"
        if payload_key in self._seen_payload_hashes:
            return False, "ERR_DUPLICATE: Identical reading timestamp already recorded", state
        self._seen_payload_hashes.add(payload_key)
        if len(self._seen_payload_hashes) > 10000:
            self._seen_payload_hashes.clear()

        # 3. Check physical boundary limits
        limits = self.BOUNDS.get(sensor_type.lower())
        if limits:
            if value < limits['min'] or value > limits['max']:
                state['fail_count'] += 1
                state['status'] = 'DEGRADED'
                return False, f"ERR_OUT_OF_BOUNDS: Value {value} exceeds valid physical range [{limits['min']}, {limits['max']}]", state

            # 4. Check abnormal rate of spike
            if state['last_value'] is not None and state['last_time'] is not None:
                elapsed_min = max(0.1, (now - state['last_time']).total_seconds() / 60.0)
                if elapsed_min <= 10.0:  # Only check spikes for closely spaced readings
                    jump = abs(value - state['last_value'])
                    if jump > limits['max_jump']:
                        state['fail_count'] += 1
                        state['status'] = 'ANOMALOUS_SPIKE'
                        return False, f"ERR_ABNORMAL_SPIKE: Jump of {jump:.1f} exceeds physical limit {limits['max_jump']}", state

        # All checks passed: mark healthy and update state
        state['last_value'] = value
        state['last_time'] = now
        state['status'] = 'ONLINE'
        state['fail_count'] = 0
        return True, "VALID", state

    def check_timeouts(self, current_time: Optional[datetime] = None) -> Dict[str, str]:
        """
        Audits all registered sensors.
        If a sensor has not transmitted in > timeout_minutes, marks it UNAVAILABLE.
        PRD §8 requirement: Never silently treat missing sensor data as normal.
        """
        now = current_time or datetime.utcnow()
        health_report = {}
        for sensor_id, state in self._sensor_states.items():
            if state['last_time'] is None:
                state['status'] = 'NEVER_REPORTED'
            else:
                elapsed_min = (now - state['last_time']).total_seconds() / 60.0
                if elapsed_min > self.timeout_minutes:
                    state['status'] = 'UNAVAILABLE'
            health_report[sensor_id] = state['status']
        return health_report
