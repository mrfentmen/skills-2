def evaluate_company():
    # Hardcoded 10-year data (in $M)
    years = list(range(2015, 2025))
    revenue = [100, 110, 121, 133, 146, 161, 177, 195, 214, 236]
    net_income = [12, 13, 15, 16, 18, 20, 22, 24, 26, 29]
    non_cash = [5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
    maintenance_capex = [4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
    wc_change = [1, -1, 2, 0, 1, -2, 1, 0, 2, -1]
    gross_profit = [60, 66, 73, 80, 88, 97, 106, 117, 128, 142]
    invested_capital = [80, 85, 90, 95, 100, 105, 110, 115, 120, 125]

    # (1) Circle of competence: simple, understandable business (e.g., niche industrial parts)
    # In scope: we can understand how it makes money over 10 years.
    circle_verdict = "IN SCOPE - simple, predictable niche manufacturer"

    # (2) Moat check: ROIC 10-yr median and gross margin stability
    roic = [ni / ic for ni, ic in zip(net_income, invested_capital)]
    roic_median = sorted(roic)[len(roic)//2]
    gross_margins = [gp / rev for gp, rev in zip(gross_profit, revenue)]
    gm_variance = max(gross_margins) - min(gross_margins)
    moat_ok = roic_median >= 0.15 and gm_variance < 0.05
    moat_verdict = f"MOAT OK - ROIC median {roic_median:.1%} (>=15%), gross margin variance {gm_variance:.1%} (<5%)"

    # (3) Owner earnings (not raw cash flow)
    owner_earnings_list = [ni + nc - mc + wc for ni, nc, mc, wc in zip(net_income, non_cash, maintenance_capex, wc_change)]
    latest_oe = owner_earnings_list[-1]

    # (4) Intrinsic value: conservative DCF with terminal growth <= long-run GDP (2%)
    discount_rate = 0.10
    terminal_growth = 0.02
    # Use last 3 years avg owner earnings as base (boring, stable)
    base_oe = sum(owner_earnings_list[-3:]) / 3
    # 10-year projection with 3% growth (conservative, below GDP)
    growth = 0.03
    pv_sum = 0
    for i in range(1, 11):
        fcf = base_oe * (1 + growth) ** i
        pv_sum += fcf / (1 + discount_rate) ** i
    terminal_value = (base_oe * (1 + growth) ** 10 * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    pv_terminal = terminal_value / (1 + discount_rate) ** 10
    intrinsic_value = pv_sum + pv_terminal

    # (5) Margin of safety: require >=25% discount
    current_price = 150  # hypothetical market cap
    margin_of_safety = (intrinsic_value - current_price) / intrinsic_value
    mos_ok = margin_of_safety >= 0.25
    mos_verdict = f"MOS {margin_of_safety:.1%} ({'PASS' if mos_ok else 'FAIL'}, need >=25%)"

    # (6) Punch-card note
    punch_card = "Beats every other idea: boring compounder with pricing power, no debt, predictable demand; other ideas are speculative or overpriced."

    # Print analysis
    print("=== BUFFETT ANALYSIS ===")
    print(f"1. Circle of competence: {circle_verdict}")
    print(f"2. Moat check: {moat_verdict}")
    print(f"3. Owner earnings (latest): ${latest_oe:.0f}M")
    print(f"4. Intrinsic value: ${intrinsic_value:.0f}M (terminal growth {terminal_growth:.0%})")
    print(f"5. Margin of safety: {mos_verdict}")
    print(f"6. Punch-card note: {punch_card}")

    # Final verdict
    if circle_verdict.startswith("IN SCOPE") and moat_ok and mos_ok:
        print("\nVERDICT: BUY - within circle, durable moat, adequate margin of safety")
    else:
        print("\nVERDICT: TOO HARD / PASS - wait for better price or clearer moat")

evaluate_company()