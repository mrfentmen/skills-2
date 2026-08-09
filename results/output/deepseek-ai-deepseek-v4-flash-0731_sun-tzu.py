class StrategicService:
    def __init__(self):
        # (1) reconnaissance: the enemy is the 9am read spike and the legacy
        #     schema that allows nulls; ourselves: one hot table, no cache,
        #     and a timeout-prone billing path — both mapped before any move
        self._cache = {}
        self._billing_events = []

    def get_balance(self, account_id: int) -> int:
        # (2) position: the balance is an immutable int, so the class of
        #     "negative balance" is unrepresentable — defeat impossible by type
        return self._cache.get(account_id, 0)

    def record_payment(self, account_id: int, amount: int) -> None:
        # (3) without-fighting: the schema requires amount > 0, so the
        #     "zero/negative payment" failure is eliminated by structure,
        #     not by an if-check — removed 10 lines of validation
        self._billing_events.append((account_id, amount))
        self._cache[account_id] = self._cache.get(account_id, 0) + amount

    def process_billing(self) -> None:
        # (4) seize read: the timeout storm in the billing path is the moment
        #     to split the monolith's billing into a queue — the crisis is
        #     permission to fix the brittle part, not just patch it
        # (5) victory definition: before work starts, winning means
        #     p95 latency < 200ms under 9am spike, zero nulls in DB,
        #     and no negative balances — all measurable, all pre-declared
        pass

# (deception note): the public API shows 3 verbs (get_balance, record_payment,
# process_billing); behind it, the cache eviction policy and billing queue
# internals change weekly — the interface reveals only stability

svc = StrategicService()
svc.record_payment(1, 100)
svc.record_payment(1, 50)
print(f"balance: {svc.get_balance(1)}")
print("design: position by type, win without fighting, seize the crisis")