def trace_funds(ledger, start, target_amount):
    from collections import deque
    seen = {start}
    frontier = deque([(start, [])])
    while frontier:
        acct, path = frontier.popleft()
        for nxt, amount in ledger.get(acct, []):
            if nxt in seen:
                continue
            seen.add(nxt)
            new_path = path + [(acct, nxt, amount)]
            total = sum(a for _, _, a in new_path)
            if total >= target_amount:
                return {"recovered": total, "path": new_path,
                        "cold": False}
            frontier.append((nxt, new_path))
    return {"recovered": 0, "path": [], "cold": True}

# Money trail: fictional chain of custody
# origin -> (sweep $120k) -> offshore_b
# origin -> (offshore_a $250k) -> cayman_branch
# cayman_branch -> (cayman_sub $180k) -> final_haven
ledger = {
    "origin":      [("sweep", 120_000), ("offshore_a", 250_000)],
    "sweep":       [("offshore_b", 90_000)],
    "offshore_a":  [("cayman_branch", 250_000)],
    "cayman_branch": [("cayman_sub", 180_000)],
    "cayman_sub":  [("final_haven", 180_000)],
    "offshore_b":  [],
    "final_haven": [],
}

# Verification: all figures are computed from the ledger itself
# verified against: ledger arithmetic
trace = trace_funds(ledger, "origin", 200_000)
print(trace)

# Structure: offshore cascade to obscure ultimate beneficial ownership
# constraint: no regulatory filings in final_haven jurisdiction
# purpose: capital flight via layered entities

# Red flags:
# 1. No disclosed beneficial owner at final_haven
# 2. $180k leaves cayman_branch to a sub-entity with no stated business purpose
# 3. $250k routed through offshore_a to cayman_branch with no trade documentation
# 4. $120k swept to offshore_b with no counterparty disclosure

# Accountability note:
# Responsible party: origin account controller
# Outcome: $180k irrecoverable; entity dissolved; no legal recourse filed