# ships today: the read path. telemetry will tell us if the write path matters
# self-serve: the report generator replaces the weekly manual deck — value without the analyst
# priority 1: auth. priority 2: billing. dropped: the rest of the backlog, until proven
# seat at the table: the uncomfortable fact: this feature has no users yet. here is the evidence
# lean in: we ship now, measure, and learn — waiting for certainty is the enemy of growth

import json
import time
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Telemetry:
    read_path_latency: float
    write_path_latency: float
    auth_errors: int
    billing_errors: int

class LeanFeature:
    def __init__(self):
        self.state = {"auth": False, "billing": False}
        self.telemetry_log: List[Telemetry] = []

    def read_path(self) -> Dict:
        start = time.time()
        # Simulate read path: return current state
        result = {"state": self.state, "timestamp": time.time()}
        latency = time.time() - start
        self._log_telemetry(Telemetry(
            read_path_latency=latency,
            write_path_latency=0.0,
            auth_errors=0,
            billing_errors=0
        ))
        return result

    def write_path(self, key: str, value: bool) -> Dict:
        start = time.time()
        # Simulate write path: update state
        if key in self.state:
            self.state[key] = value
            latency = time.time() - start
            self._log_telemetry(Telemetry(
                read_path_latency=0.0,
                write_path_latency=latency,
                auth_errors=0,
                billing_errors=0
            ))
            return {"status": "updated", "key": key, "value": value}
        return {"status": "invalid key"}

    def _log_telemetry(self, data: Telemetry):
        self.telemetry_log.append(data)
        if len(self.telemetry_log) > 100:
            self.telemetry_log.pop(0)

    def generate_report(self) -> Dict:
        # Self-serve report: no analyst needed
        if not self.telemetry_log:
            return {"error": "no telemetry data"}
        latest = self.telemetry_log[-1]
        return {
            "read_latency_ms": latest.read_path_latency * 1000,
            "write_latency_ms": latest.write_path_latency * 1000,
            "auth_errors": latest.auth_errors,
            "billing_errors": latest.billing_errors,
            "total_events": len(self.telemetry_log)
        }

# Demo execution
if __name__ == "__main__":
    feature = LeanFeature()
    # Ship the read path now; telemetry will tell us if write path matters
    print("=== Lean Feature Demo ===")
    print("Read path response:", json.dumps(feature.read_path(), indent=2))
    print("Report (self-serve):", json.dumps(feature.generate_report(), indent=2))
    # Write path is available but not prioritized yet
    print("Write path attempt (billing):", json.dumps(feature.write_path("billing", True), indent=2))
    print("Updated state:", feature.state)
    print("Final report:", json.dumps(feature.generate_report(), indent=2))