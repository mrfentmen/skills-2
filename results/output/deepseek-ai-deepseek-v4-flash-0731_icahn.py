def activist_analysis():
    # (1) VALUE GAP: worth-vs-price spread quantified
    # Sum-of-parts: core ops $18B + real estate $6B + patent portfolio $4B = $28B
    # Market cap: $21B -> gap = 28/21 - 1 = 33.3% unlock potential
    parts_value = 28e9
    market_cap = 21e9
    gap_pct = (parts_value / market_cap - 1) * 100

    # (2) GOVERNANCE CASE: misallocation documented
    # Cash: $6.5B = 31% of market cap, earning 1.2% (ROIC on cash)
    # ROIC: 6.8% vs WACC 9.5% -> value-destroying capital retention
    # Comp: CEO owns 0.3%, comp grew 42% while TSR was -5% over 3y
    cash = 6.5e9
    cash_ratio = cash / market_cap
    roic = 0.068
    wacc = 0.095
    ceo_owns = 0.003
    comp_growth = 0.42
    tsr = -0.05
    inefficient_cash = roic < wacc and cash_ratio >= 0.20
    comp_misalignment = ceo_owns < 0.01 and comp_growth > tsr

    # (3) CATALYST PLAN: escalation path sequenced
    # 1) Accumulate 6% stake -> file 13D (announcement re-rates)
    # 2) Open letter: demand $3B buyback + $1.5B special dividend
    # 3) Request 2 board seats (capital allocation committee)
    # 4) If ignored: proxy fight for 3 seats, threaten full slate
    # 5) Fallback: push spinoff of real estate into REIT
    plan = [
        "stake 6% -> file 13D",
        "open letter: $3B buyback + $1.5B special dividend",
        "demand 2 board seats (capital allocation committee)",
        "threaten proxy fight for 3 seats",
        "force spinoff of real estate into REIT if buyback blocked"
    ]

    # (4) EXIT/MONITORING RULE: thesis must keep working
    # Hold while: gap > 15%, cash ratio > 20%, no buyback announced
    # Exit if: buyback completed AND gap < 10%, or ROIC > WACC for 2 quarters
    exit_rule = "Exit when gap < 10% after buyback, or ROIC > WACC for 2 consecutive quarters"

    # (5) FRIEND WARNING: management stance explicit
    friend_warning = "Management is not your friend — they answer for capital or they leave"

    print("=== ICAHN ACTIVIST ANALYSIS ===")
    print(f"Value Gap: parts worth ${parts_value/1e9:.0f}B, trades at ${market_cap/1e9:.0f}B -> {gap_pct:.1f}% unlock")
    print(f"Governance Case: cash ${cash/1e9:.1f}B ({cash_ratio*100:.0f}% of mkt cap), ROIC {roic*100:.1f}% < WACC {wacc*100:.1f}%")
    print(f"  Comp misalignment: CEO owns {ceo_owns*100:.1f}%, comp +{comp_growth*100:.0f}% vs TSR {tsr*100:.0f}%")
    print(f"  Inefficient cash: {inefficient_cash}, Comp misalignment: {comp_misalignment}")
    print(f"Catalyst Plan: {len(plan)} steps")
    for i, step in enumerate(plan, 1):
        print(f"  {i}) {step}")
    print(f"Exit/Monitoring: {exit_rule}")
    print(f"Friend Warning: {friend_warning}")
    print(f"Qualifies for campaign: {gap_pct >= 15 and (inefficient_cash or comp_misalignment)}")

activist_analysis()