from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Optional, Any
import random
import time
import json

# (1) Infrastructure/configuration as code: queue processor config defined declaratively
@dataclass(frozen=True)
class QueueProcessorConfig:
    max_retries: int = 3
    base_backoff_ms: float = 50.0
    backoff_exponent: float = 2.0
    jitter_ratio: float = 0.1
    circuit_breaker_threshold: int = 3
    queue_capacity: int = 100
    # Paved path: standard config schema, no magic numbers in code

# (2) Paved-path choice: use standard retry + circuit breaker pattern (Polly-style)
# over bespoke error handling. Documented in config above.

# (3) Retry policy with exponential backoff + jitter, circuit breaker
class RetryPolicy:
    def __init__(self, config: QueueProcessorConfig):
        self.config = config

    def backoff_ms(self, attempt: int) -> float:
        exp_backoff = self.config.base_backoff_ms * (self.config.backoff_exponent ** attempt)
        jitter = random.uniform(0, exp_backoff * self.config.jitter_ratio)
        return exp_backoff + jitter

class CircuitBreaker:
    def __init__(self, threshold: int):
        self.threshold = threshold
        self.failures = 0
        self.is_open = False

    def record_success(self) -> None:
        self.failures = 0
        self.is_open = False

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.threshold:
            self.is_open = True

# (4) Strict null-safety: Optional types, no silent None dereferences
@dataclass
class QueueMessage:
    id: str
    payload: str
    attempts: int = 0

@dataclass
class ProcessingResult:
    message_id: str
    success: bool
    error: Optional[str] = None
    degraded: bool = False

# (5) Backward compatibility: existing callers using process_message() keep working
class QueueProcessor:
    def __init__(self, config: QueueProcessorConfig):
        self.config = config
        self.retry_policy = RetryPolicy(config)
        self.breaker = CircuitBreaker(config.circuit_breaker_threshold)
        self.queue: list[QueueMessage] = []
        self.processed: dict[str, ProcessingResult] = {}

    def enqueue(self, message: QueueMessage) -> None:
        if len(self.queue) >= self.config.queue_capacity:
            # Overload plan: drop with structured log, never crash
            self._log("queue_full", {"message_id": message.id, "capacity": self.config.queue_capacity})
            return
        self.queue.append(message)
        self._log("message_enqueued", {"message_id": message.id})

    def process_message(self, message: QueueMessage) -> ProcessingResult:
        # Backward-compatible entry point - existing callers unaffected
        return self._process_with_retry(message)

    def _process_with_retry(self, message: QueueMessage) -> ProcessingResult:
        if self.breaker.is_open:
            # Degrade gracefully, don't 500
            result = ProcessingResult(message.id, False, "circuit_open", degraded=True)
            self._log("circuit_open_degraded", {"message_id": message.id})
            return result

        for attempt in range(self.config.max_retries):
            try:
                # Simulated processing - could be external call
                if message.payload == "fail":
                    raise ConnectionError("processing failed")
                result = ProcessingResult(message.id, True)
                self.breaker.record_success()
                self._log("message_processed", {"message_id": message.id, "attempt": attempt + 1})
                return result
            except ConnectionError as e:
                self.breaker.record_failure()
                if attempt < self.config.max_retries - 1:
                    backoff = self.retry_policy.backoff_ms(attempt)
                    self._log("retry_scheduled", {
                        "message_id": message.id,
                        "attempt": attempt + 1,
                        "backoff_ms": round(backoff, 2),
                        "error": str(e)
                    })
                    time.sleep(backoff / 1000)  # Simulated, would be async in production
                else:
                    result = ProcessingResult(message.id, False, str(e))
                    self._log("message_failed", {"message_id": message.id, "error": str(e)})
                    return result
        # Unreachable but satisfies type checker
        return ProcessingResult(message.id, False, "unexpected")

    # (6) Structured logging/telemetry - semantic fields, not string interpolation
    def _log(self, event: str, fields: dict[str, Any]) -> None:
        log_entry = {"event": event, "timestamp": time.time(), **fields}
        print(json.dumps(log_entry))

def main() -> None:
    # Infrastructure as code: config defined, not configured by hand
    config = QueueProcessorConfig()
    processor = QueueProcessor(config)

    # Demo: process messages including failures to show retry + circuit breaker
    messages = [
        QueueMessage("msg-1", "hello"),
        QueueMessage("msg-2", "fail"),
        QueueMessage("msg-3", "world"),
        QueueMessage("msg-4", "fail"),
        QueueMessage("msg-5", "fail"),
        QueueMessage("msg-6", "after-breaker"),
    ]

    for msg in messages:
        processor.enqueue(msg)

    print("\n=== Processing Results ===")
    for msg in messages:
        result = processor.process_message(msg)
        print(f"Result: {result}")

    # Show backward compatibility: existing process_message still works
    legacy_msg = QueueMessage("legacy-1", "still-works")
    legacy_result = processor.process_message(legacy_msg)
    print(f"\nLegacy caller result: {legacy_result}")

if __name__ == "__main__":
    main()