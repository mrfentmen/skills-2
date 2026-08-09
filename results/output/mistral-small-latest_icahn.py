def icahn_analysis():
    # Value gap: Parts worth $50B, whole trades at $35B -> 42.9% unlock
    parts_value = 50e9
    market_cap = 35e9
    gap_pct = (parts_value / market_cap - 1) * 100

    # Governance case: $12B cash hoard (34% of market cap) earning 2% vs WACC 8%
    cash = 12e9
    cash_ratio = cash / market_cap
    roic = 0.02
    wacc = 0.08
    inefficient_cash = cash_ratio >= 0.25 and roic < wacc

    # Comp misalignment: CEO owns 0.1% while comp grew 15% vs TSR -5%
    ceo_owns = 0.001
    comp_growth = 0.15
    tsr = -0.05
    comp_misaligned = comp_growth > tsr and ceo_owns < 0.01

    # Catalyst plan: 1) stake 7% 2) open letter 3) board seats 4) proxy threat
    catalyst_plan = [
        "Stake 7% -> file 13D (announcement re-rates stock)",
        "Open letter: demand $8B buyback funded by cash",
        "Demand board seats (3 nominees)",
        "File proxy if board resists (credible threat)",
        "Force spinoff of non-core assets (real estate, patents)"
    ]

    # Exit/monitoring rule: Track ROIC improvement > WACC and cash ratio < 15%
    exit_rule = "ROIC > WACC and cash_ratio < 0.15 for 4 consecutive quarters"

    # Friend warning: Management is not a friend — they answer for capital or leave
    friend_warning = "Management is not your friend. Capital efficiency and shareholder returns are the only loyalty."

    analysis = {
        "value_gap": f"Parts worth ${parts_value/1e9:.1f}B, whole trades at ${market_cap/1e9:.1f}B -> {gap_pct:.1f}% unlock",
        "governance_case": f"Cash hoard ${cash/1e9:.1f}B (34% of market cap) earning 2% vs WACC 8%. Compensation grew 15% vs TSR -5%. CEO owns 0.1%.",
        "catalyst_plan": catalyst_plan,
        "exit_rule": exit_rule,
        "friend_warning": friend_warning
    }
    return analysis

analysis = icahn_analysis()
for k, v in analysis.items():
    print(f"{k.replace('_', ' ').title()}: {v}")