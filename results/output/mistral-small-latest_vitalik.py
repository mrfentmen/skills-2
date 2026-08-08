import hashlib
from typing import List, Tuple

def sha(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

class AppendOnlyLedger:
    def __init__(self):
        self.chain: List[bytes] = [sha(b"genesis")]
        self.events: List[Tuple[bytes, int, int]] = []  # (data, cost, nonce)
        self.total_bytes = 0
        self.max_bytes = 1_000_000
        self.max_events = 10_000
        self.max_cost_per_event = 1_000_000

    def append(self, data: bytes, cost: int) -> int:
        if not isinstance(data, bytes) or len(data) > 64_000 or cost < 0:
            raise ValueError("invalid payload or cost")
        if cost > self.max_cost_per_event:
            raise ValueError("cost exceeds per-event cap")

        nonce = len(self.events)
        charged_cost = cost + len(data)
        if charged_cost > self.max_cost_per_event:
            raise ValueError("resource cost cap exceeded")
        if len(self.events) >= self.max_events:
            raise ValueError("event count cap exceeded")
        if self.total_bytes + len(data) > self.max_bytes:
            raise ValueError("total bytes cap exceeded")

        self.events.append((data, charged_cost, nonce))
        self.total_bytes += len(data)
        block = sha(self.chain[-1] + data + charged_cost.to_bytes(8, "big") + nonce.to_bytes(8, "big"))
        self.chain.append(block)
        return len(self.chain) - 1

    def verify(self) -> bool:
        h = sha(b"genesis")
        for i, (data, cost, nonce) in enumerate(self.events, start=1):
            computed = sha(h + data + cost.to_bytes(8, "big") + nonce.to_bytes(8, "big"))
            if computed != self.chain[i]:
                raise ValueError(f"tampered at block {i}")
            h = computed
        return True

    def get_state_root(self) -> bytes:
        return self.chain[-1]

# Adversarial scenario: attacker crafts a block of state-bloating ops
ledger = AppendOnlyLedger()
ledger.append(b"alice->bob 5", 21_000)  # Valid state transition
ledger.append(b"contract_deploy", 300_000)  # Another valid transition

# Worst-case abuse: attempt to exceed byte limit
try:
    ledger.append(b"x" * 65_000, 1)  # Fails due to per-event byte cap
except ValueError as e:
    print("adversarial over-bytes write rejected:", e)

# Worst-case abuse: attempt to exceed cost limit
try:
    ledger.append(b"cheap", 1_000_001)  # Fails due to per-event cost cap
except ValueError as e:
    print("adversarial over-cost write rejected:", e)

# Consensus fallback: human layer decides when code is ambiguous
print("chain verified:", ledger.verify(), "| height:", len(ledger.chain) - 1, "| state_root:", ledger.get_state_root().hex())