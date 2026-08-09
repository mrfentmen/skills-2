import time
import random
from dataclasses import dataclass
from typing import Dict, Optional
from functools import wraps
import logging

# customer: mobile app users report 503s when fetching product images during flash sales
# working backwards: we need a fetch service that never overloads the image CDN, even under 10x load
# contract-first: v1 GET /fetch?url={image_url} returns {status, bytes, cached} with strict validation and versioned errors

@dataclass
class FetchResponse:
    status: int
    bytes: int
    cached: bool
    version: str = "v1"

class FetchService:
    def __init__(self, max_rate_per_sec: int = 10, timeout_ms: int = 2000):
        self.max_rate_per_sec = max_rate_per_sec
        self.timeout_ms = timeout_ms
        self.token_bucket = max_rate_per_sec
        self.last_refill = time.time()
        self.metrics: Dict[str, list] = {"latency": [], "errors": 0, "requests": 0}
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("fetch_service")

    def _refill_bucket(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.token_bucket = min(self.max_rate_per_sec, self.token_bucket + elapsed * self.max_rate_per_sec)
        self.last_refill = now

    def _acquire_token(self) -> bool:
        self._refill_bucket()
        if self.token_bucket >= 1:
            self.token_bucket -= 1
            return True
        return False

    def _simulate_fetch(self, url: str) -> tuple[int, int, bool]:
        time.sleep(random.uniform(0.05, 0.15))  # simulate network
        return (200, random.randint(5000, 15000), random.random() < 0.3)

    def fetch(self, url: str) -> FetchResponse:
        start = time.perf_counter()
        self.metrics["requests"] += 1

        # validation
        if not url or not url.startswith("https://"):
            self.metrics["errors"] += 1
            return FetchResponse(400, 0, False)

        # rate limit
        if not self._acquire_token():
            self.metrics["errors"] += 1
            return FetchResponse(429, 0, False)

        # timeout and retry with backoff
        attempt = 0
        while attempt < 3:
            try:
                status, size, cached = self._simulate_fetch(url)
                latency_ms = round((time.perf_counter() - start) * 1000)
                self.metrics["latency"].append(latency_ms)
                return FetchResponse(status, size, cached)
            except Exception as e:
                attempt += 1
                if attempt == 3:
                    self.metrics["errors"] += 1
                    return FetchResponse(500, 0, False)
                sleep_time = min(4000, 100 * 2 ** attempt) * random.uniform(0.5, 1.0)
                time.sleep(sleep_time / 1000)

        self.metrics["errors"] += 1
        return FetchResponse(500, 0, False)

    def golden_signals(self) -> dict:
        latency = self.metrics["latency"]
        p50 = sorted(latency)[len(latency) // 2] if latency else 0
        return {
            "latency_p50": p50,
            "traffic": self.metrics["requests"],
            "errors": self.metrics["errors"],
            "saturation": round(self.metrics["errors"] / self.metrics["requests"], 4) if self.metrics["requests"] else 0.0
        }

# fitness function: fails the build if any handler calls a network resource directly
def _fitness_check():
    import inspect
    for name, method in inspect.getmembers(FetchService, predicate=inspect.isfunction):
        if name == "fetch":
            source = inspect.getsource(method)
            if "requests.get" in source or "urllib" in source:
                raise AssertionError("Direct network calls detected in fetch handler")

# runbook: 429 -> scale up rate limit or add CDN capacity; 500 -> check upstream health and retry budget
def runbook(alarm: str) -> str:
    mapping = {
        "429": "Scale rate limit or add CDN capacity; verify token bucket refill rate",
        "500": "Check upstream image service health; verify retry budget and timeout settings",
        "400": "Validate input URL format; ensure HTTPS and non-empty"
    }
    return mapping.get(alarm, "Review logs and escalate to on-call")

# demo
if __name__ == "__main__":
    _fitness_check()
    service = FetchService(max_rate_per_sec=5, timeout_ms=2000)
    urls = ["https://example.com/image1.jpg", "https://bad.url", "https://example.com/image2.png"]

    for url in urls:
        resp = service.fetch(url)
        print(f"Fetched {url}: status={resp.status}, bytes={resp.bytes}, cached={resp.cached}, version={resp.version}")

    print("\nGolden signals:", service.golden_signals())
    print("Runbook for 429:", runbook("429"))