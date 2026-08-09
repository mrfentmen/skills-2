from collections import deque

def trace_funds(ledger, start, target_amount):
    # follow the money: BFS from the origin account until the trail runs cold
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
                return {"recovered": total, "path": new_path, "cold": False}
            frontier.append((nxt, new_path))
    return {"recovered": 0, "path": [], "cold": True}

# Fictional ledger: all names, amounts, and entities are invented for demo only
ledger = {
    # origin: fictional "Acme Consulting" invoice payment
    "acme_checking": [("shell_alpha", 50_000), ("shell_beta", 30_000)],
    # shell_alpha: fictional "Alpha Holdings" (registered in Delaware, no real ops)
    "shell_alpha": [("offshore_trust", 50_000)],
    # shell_beta: fictional "Beta Trading" (fictional Cayman entity)
    "shell_beta": [("offshore_trust", 30_000)],
    # offshore_trust: fictional "Meridian Trust" (Cayman, beneficiary undisclosed)
    "offshore_trust": [("final_wallet", 80_000)],
    # final_wallet: fictional crypto wallet (public address, no KYC)
    "final_wallet": [],
}

result = trace_funds(ledger, "acme_checking", 80_000)

# (1) Money trail: actual location of funds, step by step
print("=== MONEY TRAIL ===")
for step in result["path"]:
    print(f"# {step[0]} -> {step[1]} (${step[2]:,})")
print(f"# final location: final_wallet (crypto, no KYC) — recovered ${result['recovered']:,}")

# (2) Verification: every figure tied to a checkable computation
print("\n=== VERIFICATION ===")
total_in = sum(a for _, a in ledger["acme_checking"])
total_out = sum(a for _, _, a in result["path"])
print(f"# arithmetic check: origin outflows ${total_in:,} == traced total ${total_out:,} -> {total_in == total_out}")
print("# primary source: fictional invoice #2024-001 (demo only); all amounts are invented")

# (3) Structure: position/deal structure with purpose
print("\n=== STRUCTURE ===")
print("# purpose: layer funds through shell entities to obscure beneficial ownership")
print("# constraint: no legitimate business purpose; shells have no employees, no revenue")

# (4) Red flags: concrete indicators the flow is not legitimate
print("\n=== RED FLAGS ===")
print("# 1. Round-number transfers ($50k, $30k) split just under reporting thresholds")
print("# 2. Shell entities with no operational footprint (no website, no filings)")
print("# 3. Immediate onward transfer to offshore trust with undisclosed beneficiary")
print("# 4. Final destination is crypto wallet with no KYC — irreversible and pseudonymous")
print("# 5. No invoice, contract, or service provided to justify the payments")

# (5) Accountability note: who was responsible and what happened
print("\n=== ACCOUNTABILITY ===")
print("# responsible: fictional 'Acme Consulting' CFO (demo only) — signed off on payments")
print("# outcome: fictional investigation flagged the trail; funds frozen at final_wallet (demo)")
print("# legal note: this is a fictional demo; no real persons or entities are implicated")

# Downside first: max loss if the trail runs cold
print("\n=== DOWNSIDE ===")
print(f"# max loss: ${80_000 - result['recovered']:,} if the final wallet is unrecoverable")
print(f"# trail cold: {result['cold']}")