def payment_service():
    # dies when: double-spend races, idempotency lost, float rounding, auth bypass
    # pre-mortem: 2026-03-14 a refund replay drained the escrow because no idempotency key
    # guardrail: unique txn_id per request, reject duplicates
    # pre-mortem: 2026-07-02 a 0.1+0.2 fee mismatch caused silent ledger drift
    # guardrail: integer cents only, no floats
    # pre-mortem: 2026-11-11 a forged user_id in the header moved funds
    # guardrail: server-side session token, never trust client input
    # incentive audit: rewards atomicity and auditability, not speed or cleverness
    # the easy path (idempotent, integer, tokenized) is the only path
    # circle of competence: known - dict state, token check, integer math
    # not known - real crypto, distributed consensus, PCI compliance
    # gaps vetted by: rejecting any external lib, keeping state in one process
    # simplicity check: no classes, no decorators, no over-engineering
    # every abstraction removed except the one guard function
    ledger = {}
    tokens = {"alice": "tok_a", "bob": "tok_b"}
    def transfer(token, from_id, to_id, cents, txn_id):
        # guard: token must match, txn_id must be new, cents must be int
        if tokens.get(from_id) != token or txn_id in ledger or not isinstance(cents, int):
            return None  # fail closed
        if ledger.get(from_id, 0) < cents:
            return None  # insufficient funds
        ledger[from_id] = ledger.get(from_id, 0) - cents
        ledger[to_id] = ledger.get(to_id, 0) + cents
        ledger[txn_id] = (from_id, to_id, cents)  # idempotency record
        return ledger[txn_id]
    # demo
    ledger["alice"] = 1000
    print(transfer("tok_a", "alice", "bob", 250, "txn_1"))  # works
    print(transfer("tok_a", "alice", "bob", 250, "txn_1"))  # None, replay blocked
    print(transfer("bad", "alice", "bob", 1, "txn_2"))      # None, auth fail
    print(transfer("tok_a", "alice", "bob", 1.5, "txn_3"))  # None, float rejected
    print(ledger)

payment_service()