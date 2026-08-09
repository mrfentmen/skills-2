# SLO: 99.9% availability over a 1-hour window
# SLI: Request success rate (successful requests / total requests)
# Window: 1 hour (3600 seconds)
# Error budget: 0.1% of requests can fail
# Budget calculation: allowed_errors = total_requests * (1 - SLO)
# Instrumentation: track successes, failures, and latency per request
# Release gate: deploy only if remaining budget >= 0 for both error rate and latency
# Fallback: return cached data when dependency fails, labeled as degraded
# Bounded retry: max 3 attempts with exponential backoff + jitter (100ms * 2^n + n*17%31 capped at 500ms)
# Postmortem finding: fallback must be explicitly labeled as degraded, not disguised as full
# Regression check: assert that degraded response is returned when dependency fails

SLO = 0.999
LATENCY_SLO_MS = 200
WINDOW_REQUESTS = 10_000  # 1-hour window at ~2.78 req/sec

class AvailabilityTracker:
    def __init__(self):
        self.successes = 0
        self.failures = 0
        self.latency_samples = []

    def record_request(self, success: bool, latency_ms: int):
        if success:
            self.successes += 1
        else:
            self.failures += 1
        if 0 <= latency_ms <= 10_000:
            self.latency_samples.append(latency_ms)

    def budget_status(self) -> dict:
        total = self.successes + self.failures
        if total == 0:
            return {"status": "no-data", "deploy_allowed": False}
        error_rate = self.failures / total
        latency_good = sum(1 for lat in self.latency_samples if lat <= LATENCY_SLO_MS)
        latency_rate = latency_good / len(self.latency_samples) if self.latency_samples else 0.0
        remaining = (1 - SLO) - error_rate
        latency_remaining = latency_rate - SLO
        deploy_allowed = remaining >= 0 and latency_remaining >= 0
        return {
            "status": "healthy" if deploy_allowed else "spent",
            "error_rate": error_rate,
            "latency_rate": latency_rate,
            "remaining": remaining,
            "latency_remaining": latency_remaining,
            "deploy_allowed": deploy_allowed
        }

def bounded_retry(dependency_call, max_attempts=3):
    diagnostics = []
    for attempt in range(max_attempts):
        result = dependency_call()
        if result["status"] == "ok":
            return {"status": "full", "value": result["value"], "attempts": attempt + 1, "diagnostics": diagnostics}
        if result["status"] == "throttle" and attempt + 1 < max_attempts:
            delay_ms = min(100 * (2 ** attempt) + (attempt * 17 % 31), 500)
            diagnostics.append({"kind": "retry", "delay_ms": delay_ms})
            continue
        return {"status": "degraded", "value": result.get("cached", None), "attempts": attempt + 1, "diagnostics": diagnostics, "reason": result.get("reason", "dependency unavailable")}
    return {"status": "degraded", "value": None, "attempts": max_attempts, "diagnostics": diagnostics, "reason": "retry budget exhausted"}

def mock_dependency(response_sequence):
    def call():
        if not response_sequence:
            return {"status": "down", "reason": "no responses left"}
        resp = response_sequence.pop(0)
        if resp == "ok":
            return {"status": "ok", "value": 200}
        if resp == "throttle":
            return {"status": "throttle"}
        if resp == "down":
            return {"status": "down", "reason": "dependency down"}
        return {"status": "error", "reason": "invalid response"}
    return call

# Demo
tracker = AvailabilityTracker()

# Simulate 10,000 requests with 10 failures and some latency samples
for _ in range(9990):
    tracker.record_request(True, 150)
for _ in range(10):
    tracker.record_request(False, 250)
tracker.record_request(True, 180)
tracker.record_request(True, 220)
tracker.record_request(True, 300)

budget = tracker.budget_status()
print({"slo": f"{SLO*100}% availability over {WINDOW_REQUESTS} requests", "window": "1 hour", "sli": "request success rate", "budget": budget})

# Release gate check
if not budget["deploy_allowed"]:
    print("DEPLOY BLOCKED: error budget spent")
else:
    print("DEPLOY ALLOWED: error budget healthy")

# Fallback and retry demo
response_sequence = ["throttle", "ok"]
dependency_call = mock_dependency(response_sequence)
result = bounded_retry(dependency_call)
print({"retry_success": result})

# Postmortem regression: ensure degraded response when dependency fails
response_sequence_fail = ["down"]
dependency_call_fail = mock_dependency(response_sequence_fail)
degraded_result = bounded_retry(dependency_call_fail)
assert degraded_result["status"] == "degraded", "Regression: fallback must be labeled degraded"
print({"postmortem_regression_check": degraded_result})

# Blameless finding: "Dependency failures must return explicitly labeled degraded responses; cached data is not a full response."
# Regression check: assert degraded_result["status"] == "degraded" when dependency fails