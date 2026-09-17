"""
IoT Sensor Telemetry Simulator
Generates synthetic data streams for pilot sensors in Chamoli & Rudraprayag
Supports nominal operation, sensor degradation, and storm surges.
"""

import random
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from data.scripts.seed_regions import get_pilot_sensors


class SensorSimulator:
    """Simulates real-time telemetry from hill-district IoT nodes"""

    def __init__(self):
        self.sensors = get_pilot_sensors()
        # Internal state tracking for drift & continuity
        self._state: Dict[str, Dict[str, float]] = {}
        for s in self.sensors:
            stype = s['type']
            if stype == "rainfall":
                val = 0.0
            elif stype == "soil_moisture":
                val = 32.0
            elif stype == "water_level":
                val = 2.4
            else:
                val = 15.0
            self._state[s['sensor_id']] = {'current_val': val, 'battery': 98.0}

    def generate_tick(self, storm_mode: bool = False, surge_station_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generates one observation payload for each registered sensor
        """
        readings = []
        now = datetime.utcnow()

        for s in self.sensors:
            sid = s['sensor_id']
            stype = s['type']
            state = self._state[sid]

            # Battery slowly decays
            state['battery'] = max(10.0, state['battery'] - random.uniform(0.001, 0.01))

            is_target_surge = (storm_mode and (surge_station_id is None or surge_station_id in sid))

            if stype == "rainfall":
                if is_target_surge:
                    # Cloudburst / torrential downpour
                    val = round(random.uniform(65.0, 95.0), 1)
                elif storm_mode:
                    val = round(random.uniform(20.0, 45.0), 1)
                else:
                    # Clear / light drizzle
                    val = round(random.choice([0.0, 0.0, 0.0, 0.5, 1.2, 2.0]), 1)

            elif stype == "soil_moisture":
                if is_target_surge:
                    # Rapid saturation towards liquid limit
                    state['current_val'] = min(92.0, state['current_val'] + random.uniform(1.5, 3.5))
                elif storm_mode:
                    state['current_val'] = min(75.0, state['current_val'] + random.uniform(0.5, 1.2))
                else:
                    # Slow drainage/drying
                    state['current_val'] = max(25.0, state['current_val'] - random.uniform(0.1, 0.3))
                val = round(state['current_val'], 1)

            elif stype == "water_level":
                if is_target_surge:
                    # Rapid mountain river surge
                    state['current_val'] = min(8.5, state['current_val'] + random.uniform(0.15, 0.35))
                elif storm_mode:
                    state['current_val'] = min(5.5, state['current_val'] + random.uniform(0.05, 0.12))
                else:
                    # Normal mountain stream
                    state['current_val'] = max(1.8, min(3.0, state['current_val'] + random.uniform(-0.05, 0.05)))
                val = round(state['current_val'], 2)

            else:
                val = round(random.uniform(10.0, 25.0), 1)

            readings.append({
                "sensor_id": sid,
                "sensor_type": stype,
                "sensor_name": s['name'],
                "region_id": s['region_id'],
                "value": val,
                "unit": s['unit'],
                "battery_pct": round(state['battery'], 1),
                "timestamp": now.isoformat(),
                "latitude": s['lat'],
                "longitude": s['lng'],
                "status": "ONLINE"
            })

        return readings


if __name__ == "__main__":
    sim = SensorSimulator()
    print("Generating 3 normal ticks:")
    for _ in range(3):
        batch = sim.generate_tick(storm_mode=False)
        print(f"Generated {len(batch)} sensor readings. Rain sample: {batch[0]['value']} {batch[0]['unit']}")
    
    print("\nGenerating 1 storm surge tick:")
    surge_batch = sim.generate_tick(storm_mode=True)
    for b in surge_batch:
        print(f"[{b['sensor_type'].upper():13s}] {b['sensor_id']}: {b['value']} {b['unit']}")
