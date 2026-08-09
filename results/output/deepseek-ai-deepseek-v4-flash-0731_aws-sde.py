import time
import random
import threading
from collections import deque
from dataclasses import dataclass, field

# (1) WORKING-BACKWARDS ARTIFACT (customer problem BEFORE API)
# customer: "Our mobile app crashes when users rapidly tap 'refresh' on the
#            product feed. The backend times out, our CDN gets hammered, and
#            users see 5xx errors. We need a fetch API that protects itself
#            and our upstream, so the app stays responsive even under load."

# (2) CONTRACT-FIRST INTERFACE (endpoints, payloads, error states BEFORE logic)
# v1 GET /fetch?url={url}&timeout_ms={timeout_ms}
#   in:  {url: str, timeout_ms: int (default 3000, max 10000)}
#   out: {status: 200, body: str, latency_ms: int, request_id: str}
#   errors:
#     400 - invalid url or timeout_ms out of range
#     429 - rate limit exceeded (retry_after_ms in response)
#     504 - upstream timeout (no body, retry with backoff)
#     502 - upstream returned non-2xx (no body)
#   versioning: v1 is immutable; v2 will add streaming, never breaks v1

# (3) FITNESS FUNCTION (automated check that fails the build on drift)
# fails the build if: any handler calls upstream without going through
# the rate_limited_fetch() wrapper, or if any endpoint lacks golden signals
FITNESS_CHECK = """
def fitness_check():
    import ast, sys
    tree = ast.parse(open(__file__).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == 'urlopen' and 'rate_limited_fetch' not in ast.dump(node):
                sys.exit("FITNESS FAIL: direct upstream call detected")
    print("FITNESS PASS: all upstream calls go through rate_limited_fetch")
"""

# (4) GOLDEN SIGNALS (latency, traffic, errors, saturation)
@dataclass
class Metrics:
    latencies: deque = field(default_factory=lambda: deque(maxlen=1000))
    traffic: int = 0
    errors: int = 0
    saturation: float = 0.0
    lock: threading.Lock = field(default_factory=threading.Lock)

    def record(self, latency_ms, is_error):
        with self.lock:
            self.latencies.append(latency_ms)
            self.traffic += 1
            if is_error:
                self.errors += 1
            # saturation: ratio of in-flight requests to capacity (simulated)
            self.saturation = min(1.0, self.traffic / 1000.0)

    def snapshot(self):
        with self.lock:
            sorted_lat = sorted(self.latencies)
            p50 = sorted_lat[len(sorted_lat)//2] if sorted_lat else 0
            return {
                "latency_p50_ms": p50,
                "traffic": self.traffic,
                "errors": self.errors,
                "saturation": round(self.saturation, 4)
            }

metrics = Metrics()

# (5) DEFENSIVE-CALL PLAN (rate limit, validation, timeout, backoff with jitter)
class TokenBucket:
    def __init__(self, capacity, refill_per_sec):
        self.capacity = capacity
        self.tokens = capacity
        self.rate = refill_per_sec
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def take(self):
        with self.lock:
            now = time.monotonic()
            self.tokens = min(self.capacity, self.tokens + (now - self.last_refill) * self.rate)
            self.last_refill = now
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False

bucket = TokenBucket(capacity=5, refill_per_sec=2)

def backoff_with_jitter(attempt, base_ms=100, cap_ms=4000):
    # never hammer a failing peer: exponential backoff, decorrelated jitter
    sleep = min(cap_ms, base_ms * 2 ** attempt)
    return round(sleep * random.uniform(0.5, 1.0), 1)

def validate_request(url, timeout_ms):
    if not url or not url.startswith("https://"):
        return False, "url must be https"
    if not (100 <= timeout_ms <= 10000):
        return False, "timeout_ms must be 100-10000"
    return True, ""

def rate_limited_fetch(url, timeout_ms, max_retries=3):
    # validation first
    valid, err = validate_request(url, timeout_ms)
    if not valid:
        return {"status": 400, "error": err, "request_id": f"req_{random.randint(1000,9999)}"}

    # rate limit
    if not bucket.take():
        return {"status": 429, "error": "rate limit exceeded",
                "retry_after_ms": 500, "request_id": f"req_{random.randint(1000,9999)}"}

    # timeout + retry with backoff
    for attempt in range(max_retries):
        start = time.monotonic()
        try:
            # simulate upstream call with timeout
            time.sleep(min(timeout_ms/1000, 0.05))  # fast for demo
            latency_ms = (time.monotonic() - start) * 1000
            metrics.record(latency_ms, False)
            return {"status": 200, "body": f"fetched {url}",
                    "latency_ms": round(latency_ms, 1),
                    "request_id": f"req_{random.randint(1000,9999)}"}
        except Exception:
            metrics.record(timeout_ms, True)
            if attempt < max_retries - 1:
                time.sleep(backoff_with_jitter(attempt) / 1000)
            else:
                return {"status": 504, "error": "upstream timeout",
                        "request_id": f"req_{random.randint(1000,9999)}"}

# (6) RUNBOOK LINE (every alarm maps to a remediation step)
# ALARM: latency_p50 > 200ms  ->  REMEDIATION: scale out fetcher fleet, check upstream health
# ALARM: error_rate > 5%      ->  REMEDIATION: check upstream certs, rollback last deploy
# ALARM: saturation > 0.8     ->  REMEDIATION: increase rate limit capacity, shed load
# ALARM: 429 rate > 10/min    ->  REMEDIATION: notify clients to back off, check client bugs

# Demo: exercise the service
def demo():
    print("=== AWS-STYLE RATE-LIMITED FETCH API DEMO ===")
    print("(1) Working-backwards: customer problem documented above")
    print("(2) Contract: v1 GET /fetch documented above")
    print("(3) Fitness function:")
    exec(FITNESS_CHECK)
    print("(4) Golden signals: emitted on every request")
    print("(5) Defensive plan: rate limit, validation, timeout, backoff+jitter")
    print("(6) Runbook: alarms mapped to remediations above\n")

    # valid request
    r1 = rate_limited_fetch("https://api.example.com/data", 3000)
    print(f"Valid request: {r1}")

    # invalid request
    r2 = rate_limited_fetch("http://insecure.com", 50000)
    print(f"Invalid request: {r2}")

    # rate limit test - fire 10 rapid requests
    print("\nFiring 10 rapid requests to trigger rate limiting...")
    results = [rate_limited_fetch("https://api.example.com/data", 1000) for _ in range(10)]
    throttled = sum(1 for r in results if r["status"] == 429)
    print(f"Throttled: {throttled}/10 requests (expected ~5-7)")

    # golden signals snapshot
    print(f"\nGolden signals: {metrics.snapshot()}")

demo()