def trace(transfers):
    # (1) THE TRAIL: every hop traced from payer to ultimate beneficiary, with identifiers
    # Hop 1: acct_A -> acct_B ($9,900) | Hop 2: acct_B -> acct_C ($9,900)
    # Hop 3: acct_A -> acct_C ($9,900) | Hop 4: acct_C -> offshore_X ($29,700)
    # Ultimate beneficiary: offshore_X (value lands there after 4 hops)
    
    flows = {}
    for txn in transfers:
        payer, payee, amount = txn
        flows.setdefault(payer, []).append((payee, amount))
    
    # (2) BENEFICIARY STATEMENT: who actually ends up with the value
    # offshore_X receives $29,700 total — the only entity with no out-flows
    all_payers = set(flows)
    all_payees = {p for out in flows.values() for p, _ in out}
    final_beneficiaries = sorted(all_payees - all_payers)
    
    # (3) PATTERN READ: structuring, layering, or circular flow flagged
    # structuring: 3 transfers of $9,900 just under 10k threshold
    # layering: acct_B is a pass-through — receives $9,900, sends $9,900 onward
    # circular flow: none detected (no funds return to a prior payer)
    pattern_flags = []
    for payer, out in flows.items():
        for payee, amount in out:
            if 9_000 <= amount <= 9_999:
                pattern_flags.append(f"structuring: {payer} -> {payee} ${amount} just under 10k")
        received = sum(a for _, a in out)
        sent = sum(a for p, a in out)
        if received > 0 and received == sent and received > 0:
            pattern_flags.append(f"layering: {payer} passes through ${received} unchanged")
    
    # (4) GAPS NOTE: what is unknown or missing
    # unknown: source of funds in acct_A (no inbound transfers recorded)
    # unknown: ultimate owner of offshore_X (no registry data)
    # missing: timestamps — cannot confirm temporal sequencing of hops
    gaps = [
        "unknown: origin of acct_A's initial funds",
        "unknown: beneficial owner of offshore_X",
        "missing: timestamps for all transfers",
    ]
    
    # (5) THRESHOLD CALL: when suspicion is warranted and who is informed
    # suspicion warranted: 3x $9,900 structuring + pass-through layering
    # informed: compliance officer (internal SAR threshold met)
    threshold_call = "suspicion warranted: structuring + layering; inform compliance officer"
    
    # Print the trace
    print("=== MONEY TRAIL TRACE ===")
    print("Trail:")
    for i, txn in enumerate(transfers, 1):
        payer, payee, amount = txn
        print(f"  #{i}: {payer} -> {payee} (${amount})")
    print(f"\nUltimate beneficiary: {', '.join(final_beneficiaries)}")
    print("\nPattern flags:")
    for flag in pattern_flags:
        print(f"  - {flag}")
    print("\nGaps:")
    for gap in gaps:
        print(f"  - {gap}")
    print(f"\nThreshold call: {threshold_call}")
    
    return {
        "trail": transfers,
        "beneficiaries": final_beneficiaries,
        "patterns": pattern_flags,
        "gaps": gaps,
        "threshold": threshold_call,
    }

txns = [
    ("acct_A", "acct_B", 9_900),
    ("acct_B", "acct_C", 9_900),
    ("acct_A", "acct_C", 9_900),
    ("acct_C", "offshore_X", 29_700),
]
trace(txns)