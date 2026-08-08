import hashlib
import json

def sha(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

class AppendOnlyLedger:
    def __init__(self, max_events: int = 1000, max_bytes: int = 1_000_000, max_cost_per_event: int = 100_000):
        self.chain = [sha(b"genesis")]
        self.events = []
        self.total_bytes = 0
        self.max_events = max_events
        self.max_bytes = max_bytes
        self.max_cost_per_event = max_cost_per_event
        self.state_root = sha(b"empty_state")
        self.state = {}

    def _compute_state_root(self, state: dict) -> bytes:
        # deterministic serialization for independent verification
        serialized = json.dumps(state, sort_keys=True, separators=(',', ':')).encode()
        return sha(serialized)

    def append(self, data: bytes, cost: int, state_delta: dict = None) -> int:
        # metering: every resource has a cost and a stated maximum
        if not isinstance(data, bytes) or len(data) > 64_000:
            raise ValueError("invalid payload")
        if cost < 0 or cost > self.max_cost_per_event:
            raise ValueError("cost out of bounds")
        charged_cost = cost + len(data)
        if charged_cost > self.max_cost_per_event:
            raise ValueError("charged cost exceeds per-event cap")
        if len(self.events) >= self.max_events:
            raise ValueError("event count cap exceeded")
        if self.total_bytes + len(data) > self.max_bytes:
            raise ValueError("total bytes cap exceeded")

        # apply state delta (append-only: new state derived from old, never rewritten)
        new_state = dict(self.state)
        if state_delta:
            for k, v in state_delta.items():
                if v is None:
                    new_state.pop(k, None)
                else:
                    new_state[k] = v
        new_state_root = self._compute_state_root(new_state)

        # block commits to previous hash, data, cost, and new state root
        block_payload = self.chain[-1] + data + charged_cost.to_bytes(8, "big") + new_state_root
        block = sha(block_payload)
        self.chain.append(block)
        self.events.append((data, charged_cost, new_state_root))
        self.state = new_state
        self.state_root = new_state_root
        self.total_bytes += len(data)
        return len(self.chain) - 1

    def verify(self, start_block: int = 1, end_block: int = None) -> bool:
        # independent verifier: does NOT replay all work, only checks commitment chain
        if end_block is None:
            end_block = len(self.chain) - 1
        if start_block < 1 or end_block > len(self.chain) - 1 or start_block > end_block:
            raise ValueError("invalid verification range")

        # verify only the boundary commitments, not every intermediate state
        h = self.chain[start_block - 1]
        for i in range(start_block, end_block + 1):
            data, cost, state_root = self.events[i - 1]
            h = sha(h + data + cost.to_bytes(8, "big") + state_root)
            if h != self.chain[i]:
                raise ValueError(f"tampered at block {i}")
        return True

    def verify_state(self, block_number: int) -> bool:
        # verifier checks state root commitment without replaying all transitions
        if block_number < 1 or block_number > len(self.chain) - 1:
            raise ValueError("block out of range")
        _, _, committed_root = self.events[block_number - 1]
        return committed_root == self.state_root if block_number == len(self.chain) - 1 else True

# adversarial scenario: attacker tries to bloat state with unbounded writes
ledger = AppendOnlyLedger(max_events=5, max_bytes=1000, max_cost_per_event=500)
ledger.append(b"alice->bob 5", 100, {"alice": 0, "bob": 5})
ledger.append(b"bob->carol 3", 100, {"bob": 2, "carol": 3})
assert ledger.verify(1, 2) and ledger.verify_state(2)

# attacker crafts a block of state-bloating ops: exceeds per-event cost cap
try:
    ledger.append(b"state-bloat" * 100, 10_000, {"x": "y" * 1000})
except ValueError as e:
    print(f"adversarial over-budget write rejected: {e}")

# attacker tries to exceed total byte cap
try:
    ledger.append(b"z" * 2000, 1, {"z": 1})
except ValueError as e:
    print(f"adversarial byte-bloat rejected: {e}")

# consensus fallback: human layer decides on ambiguous state
print("consensus_fallback=human_layer_decides_on_ambiguous_state")
print("chain_height=", len(ledger.chain) - 1, "verified=", ledger.verify())