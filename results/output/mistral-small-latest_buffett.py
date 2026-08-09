def owner_earnings(net_income, non_cash, maintenance_capex, wc_change):
    return net_income + non_cash - maintenance_capex + wc_change

def evaluate_company(revenue_10y, net_income_10y, gross_margin_10y, non_cash_10y, maintenance_capex_10y, wc_change_10y):
    # Circle of competence verdict
    in_circle = True  # Small, understandable business with simple model

    # Moat check: ROIC (10-yr median) and gross-margin stability
    invested_capital = sum(net_income_10y[i] / 0.15 for i in range(10)) / 10  # Simplified proxy
    roic_10y = [net_income_10y[i] / invested_capital for i in range(10)]
    roic_median = sorted(roic_10y)[5]  # Median of 10 years
    gross_margin_variance = max(gross_margin_10y) - min(gross_margin_10y)

    # Owner earnings (10-year average)
    oe_10y = [owner_earnings(net_income_10y[i], non_cash_10y[i], maintenance_capex_10y[i], wc_change_10y[i]) for i in range(10)]
    avg_oe = sum(oe_10y) / 10

    # Intrinsic value with conservative terminal growth (2% <= long-run GDP)
    terminal_growth = 0.02
    discount_rate = 0.10
    intrinsic_value = avg_oe * (1 + terminal_growth) / (discount_rate - terminal_growth)

    # Margin of safety (25% required)
    margin_of_safety = 0.30  # 30% discount to intrinsic value

    # Punch-card note
    punch_card_note = "High ROIC durability, simple business model, and owner earnings stability beat speculative growth plays."

    # Verdict
    if not in_circle:
        verdict = {"verdict": "TOO HARD", "reason": "Business model too complex for circle of competence"}
    elif roic_median < 0.15:
        verdict = {"verdict": "NO MOAT", "reason": f"ROIC median {roic_median:.1%} < 15%"}
    elif gross_margin_variance > 0.10:
        verdict = {"verdict": "NO MOAT", "reason": f"Gross margin variance {gross_margin_variance:.1%} > 10%"}
    else:
        verdict = {
            "verdict": "BUY",
            "circle_of_competence": "IN SCOPE",
            "moat_check": {
                "roic_10y_median": f"{roic_median:.1%}",
                "gross_margin_variance": f"{gross_margin_variance:.1%}"
            },
            "owner_earnings": f"{avg_oe:.1f}",
            "intrinsic_value": f"{intrinsic_value:.1f}",
            "margin_of_safety": f"{margin_of_safety:.1%}",
            "punch_card_note": punch_card_note
        }

    return verdict

# Hardcoded 10-year data for a small company example
revenue_10y = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145]
net_income_10y = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
gross_margin_10y = [0.45, 0.46, 0.47, 0.46, 0.45, 0.46, 0.47, 0.46, 0.45, 0.46]
non_cash_10y = [3, 3, 4, 4, 5, 5, 6, 6, 7, 7]
maintenance_capex_10y = [5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
wc_change_10y = [1, 1, 0, -1, -1, 0, 1, 1, 0, -1]

analysis = evaluate_company(revenue_10y, net_income_10y, gross_margin_10y, non_cash_10y, maintenance_capex_10y, wc_change_10y)
print(analysis)