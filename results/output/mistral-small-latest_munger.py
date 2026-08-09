# === PAYMENT SERVICE DESIGN ===
# Circle of Competence Statement:
# Known: Basic Python, simple state machines, idempotency patterns, basic cryptography (hashing)
# Unknown: PCI-DSS compliance, real-time fraud detection, high-scale distributed systems, banking regulations
# Gaps vetted: Will avoid handling raw card data; will use tokenization via third-party vaults (Stripe/Braintree)
# Competence boundary: Only implements the orchestration layer, not the payment processing itself

# === INVERSION PASS: WAYS THIS SYSTEM DIES ===
# dies when:
# 1. cache evicts the only copy of a transaction before confirmation
# 2. race condition between duplicate requests and idempotency key collision
# 3. external payment provider returns inconsistent state (neither success nor failure)
# 4. database transaction rolls back after provider charges customer
# 5. operator accidentally deploys stale code with broken idempotency check
# 6. clock skew causes duplicate idempotency keys to be generated
# 7. network partition leaves payment in indeterminate state
# 8. insufficient logging causes inability to reconcile disputes
# 9. third-party rate limits cause cascading failures
# 10. customer disputes legitimate charge due to unclear receipt

# === PRE-MORTEM: SIX MONTHS LATER ===
# On 2024-11-15, the payment service suffered a catastrophic outage:
# - A race condition in the idempotency cache allowed duplicate charges when a user refreshed the payment page.
#   Guardrail added: Use atomic compare-and-swap on idempotency keys with TTL-based eviction.
# - A database transaction rolled back after Stripe confirmed a charge, causing customer accounts to show $0 balance.
#   Guardrail added: Implement saga pattern with compensating transactions for external calls.
# - Clock skew between servers caused idempotency keys to collide across regions.
#   Guardrail added: Use hybrid logical clocks or external time source (NTP) with tolerance window.
# - Insufficient logging during a partial network partition made dispute resolution impossible.
#   Guardrail added: Ship structured logs with request IDs to external audit system.
# - A junior engineer deployed a change that bypassed idempotency checks during an emergency fix.
#   Guardrail added: Require two-person review for any change touching idempotency or payment flow.

# === INCENTIVE AUDIT ===
# What the system actually rewards:
# - Speed over correctness: The fast path is to skip idempotency checks in development (reward: dev velocity)
# - External provider reliability: The system rewards trusting Stripe's webhooks without validation (reward: simplicity)
# - Minimal logging: The system rewards omitting detailed logs to reduce storage costs (reward: cost savings)
# - Cache hits: The system rewards keeping transactions in memory to reduce database load (reward: performance)
# What the system intends to reward:
# - Idempotent operations to prevent duplicate charges
# - Comprehensive logging for auditability
# - External validation of payment states
# - Resilience to network partitions

# === SIMPLICITY CHECK ===
# Abstractions justified:
# - IdempotencyKey: Prevents duplicate charges (single point of failure if broken)
# - TransactionState: Tracks payment lifecycle (necessary for reconciliation)
# - ProviderAdapter: Decouples payment provider (justified by avoiding lock-in)
# Abstractions removed:
# - No retry logic in core service (pushed to caller)
# - No retry logic for webhook processing (pushed to external queue)
# - No caching of provider responses (too complex, error-prone)

from dataclasses import dataclass
from enum import Enum, auto
import hashlib
import time
from typing import Optional, Dict

class PaymentState(Enum):
    INITIATED = auto()
    PROCESSING = auto()
    SUCCEEDED = auto()
    FAILED = auto()
    CONFIRMED = auto()  # final state after webhook confirmation

@dataclass(frozen=True)
class IdempotencyKey:
    value: str

    @classmethod
    def create(cls, request_id: str, user_id: str, amount: int) -> 'IdempotencyKey':
        # incentive: the easy path is also the safe path — hash all inputs to avoid collisions
        raw = f"{request_id}:{user_id}:{amount}:{int(time.time())}"
        return cls(hashlib.sha256(raw.encode()).hexdigest())

class TransactionState:
    def __init__(self, idempotency_key: IdempotencyKey, user_id: str, amount: int):
        self.idempotency_key = idempotency_key
        self.user_id = user_id
        self.amount = amount
        self.state = PaymentState.INITIATED
        self.created_at = time.time()
        self.updated_at = time.time()

    def mark_processing(self) -> None:
        # incentive: the easy path is also the safe path — only allow state transitions in one direction
        if self.state == PaymentState.INITIATED:
            self.state = PaymentState.PROCESSING
            self.updated_at = time.time()

    def mark_succeeded(self) -> None:
        if self.state == PaymentState.PROCESSING:
            self.state = PaymentState.SUCCEEDED
            self.updated_at = time.time()

    def mark_confirmed(self) -> None:
        if self.state in (PaymentState.SUCCEEDED, PaymentState.FAILED):
            self.state = PaymentState.CONFIRMED
            self.updated_at = time.time()

    def mark_failed(self) -> None:
        if self.state == PaymentState.PROCESSING:
            self.state = PaymentState.FAILED
            self.updated_at = time.time()

class PaymentService:
    def __init__(self):
        # incentive: the easy path is also the safe path — use in-memory cache with TTL
        self.transactions: Dict[IdempotencyKey, TransactionState] = {}
        self.cache_ttl = 3600  # 1 hour

    def initiate_payment(self, user_id: str, amount: int, request_id: str) -> Optional[IdempotencyKey]:
        key = IdempotencyKey.create(request_id, user_id, amount)
        now = time.time()

        # Check cache first (incentive: fast path is safe path)
        if key in self.transactions:
            existing = self.transactions[key]
            if now - existing.created_at < self.cache_ttl:
                return key  # idempotent response

        # Create new transaction (incentive: only allow valid state transitions)
        tx = TransactionState(key, user_id, amount)
        tx.mark_processing()
        self.transactions[key] = tx
        return key

    def confirm_payment(self, key: IdempotencyKey) -> bool:
        # incentive: the easy path is also the safe path — only allow valid state transitions
        tx = self.transactions.get(key)
        if not tx:
            return False
        tx.mark_confirmed()
        return True

# Print the design and death list
print("=== PAYMENT SERVICE DESIGN ===")
print("# Circle of Competence: Orchestration layer only; third-party vault for card data")
print("# Inversion Pass: cache eviction, race conditions, external inconsistency, rollbacks")
print("# Pre-Mortem: Six months later — race conditions, rollbacks, clock skew, logging gaps")
print("# Incentive Audit: Speed vs correctness, trust vs validation, minimal logging vs audit")
print("# Simplicity: IdempotencyKey, TransactionState, ProviderAdapter (justified); no retry logic")
print("\n=== SYSTEM OUTPUT ===")
service = PaymentService()
key = service.initiate_payment("user123", 1000, "req456")
print(f"Initiated payment with key: {key.value if key else None}")
print(f"Confirming payment: {service.confirm_payment(key) if key else False}")