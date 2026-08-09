# Azure-style service: resilient queue processor with Service Bus-like semantics
# Infrastructure as code: Bicep template (snippet) to deploy SB queue + consumer
# resource queue 'customerQueue' = {
#   type: 'Microsoft.ServiceBus/queues'
#   properties: { maxDeliveryCount: 3, enablePartitioning: true }
# }
# resource consumer 'queueProcessor' = {
#   type: 'Microsoft.Web/sites'
#   kind: 'functionapp'
#   properties: { siteConfig: { runtime: 'python3.11' } }
# }

# Paved path: Azure Service Bus + Functions with built-in retry + circuit breaker
#   vs. bespoke queue + worker: SB provides partitioning, dead-lettering, and
#   enterprise-grade SLAs; Functions provide auto-scale and bindings.

# Retry policy: Polly-style exponential backoff with jitter + circuit breaker
#   overload plan: maxDeliveryCount=3 on queue + circuit breaker trips after 5
#   consecutive failures to prevent thundering herd.

# Null-safety: use Optional[str] and non-nullable defaults; warnings-as-errors via
#   mypy --strict and dataclasses with field(default_factory=...)

# Backward compatibility: existing message schema { "id": str, "name": str } kept;
#   new fields ignored by old consumers; versioned contracts via headers.

# Structured telemetry: print JSON lines to stdout for ingestion by Azure Monitor

import json
import random
import time
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

# --- Domain model ---
@dataclass
class Message:
    id: str
    name: str
    version: int = 1  # backward-compatible default

class Status(Enum):
    SUCCESS = "success"
    RETRY = "retry"
    FAIL = "fail"

# --- Resilience primitives ---
class RetryPolicy:
    def __init__(self, base: float = 0.05, exponent: float = 2.0, jitter: float = 0.02):
        self.base = base
        self.exponent = exponent
        self.jitter = jitter

    def delay(self, attempt: int) -> float:
        delay = self.base * (self.exponent ** attempt)
        jitter = random.uniform(-self.jitter, self.jitter)
        return max(0.0, delay + jitter)

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.opened_at: Optional[float] = None

    def is_open(self) -> bool:
        if self.opened_at is None:
            return False
        return time.time() - self.opened_at < self.reset_timeout

    def record_success(self) -> None:
        self.failures = 0
        self.opened_at = None

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.opened_at = time.time()

# --- Queue simulation ---
class Queue:
    def __init__(self):
        self._messages: List[Message] = []

    def enqueue(self, msg: Message) -> None:
        self._messages.append(msg)

    def dequeue(self) -> Optional[Message]:
        return self._messages.pop(0) if self._messages else None

# --- Processor ---
class QueueProcessor:
    def __init__(self, queue: Queue, retry_policy: RetryPolicy, breaker: CircuitBreaker):
        self.queue = queue
        self.retry_policy = retry_policy
        self.breaker = breaker

    def process(self) -> None:
        while True:
            msg = self.queue.dequeue()
            if msg is None:
                break

            attempt = 0
            while True:
                if self.breaker.is_open():
                    print(json.dumps({"status": Status.FAIL.value, "msg": "breaker_open", "id": msg.id}))
                    break

                try:
                    # Simulate external call
                    if msg.id == "fail":
                        raise ConnectionError("downstream failure")
                    print(json.dumps({"status": Status.SUCCESS.value, "msg": "processed", "id": msg.id}))
                    self.breaker.record_success()
                    break
                except Exception as e:
                    attempt += 1
                    if attempt > 3:
                        print(json.dumps({"status": Status.FAIL.value, "msg": "max_retries", "id": msg.id, "error": str(e)}))
                        self.breaker.record_failure()
                        break
                    delay = self.retry_policy.delay(attempt)
                    time.sleep(delay)
                    print(json.dumps({"status": Status.RETRY.value, "msg": "retrying", "id": msg.id, "delay": delay}))

# --- Demo ---
if __name__ == "__main__":
    q = Queue()
    q.enqueue(Message(id="1", name="Ada"))
    q.enqueue(Message(id="2", name="Bob"))
    q.enqueue(Message(id="fail", name="Eve"))
    q.enqueue(Message(id="3", name="Carl"))

    retry_policy = RetryPolicy(base=0.05, exponent=2.0, jitter=0.02)
    breaker = CircuitBreaker(failure_threshold=5, reset_timeout=30.0)
    processor = QueueProcessor(q, retry_policy, breaker)
    processor.process()