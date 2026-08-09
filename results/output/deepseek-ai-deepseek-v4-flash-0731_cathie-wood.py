def wrights_law(cost_now, cost_per_doubling, doublings):
    return cost_now * (cost_per_doubling ** doublings)

def cagr_5y(start, end, years=5):
    return (end / start) ** (1 / years) - 1

def arkk_score(name, people, execution, moat, product_10x, thesis_risk, cagr_5y):
    ok = (product_10x and execution >= 0.7 and moat >= 0.5
          and cagr_5y >= 0.15 and thesis_risk <= 0.4)
    return {"name": name, "buy": ok, "cagr_5y": cagr_5y, "thesis_risk": thesis_risk}

# (1) Wright's Law cost curve: EV battery cost per kWh
# cost_per_doubling = 0.82 (18% decline per cumulative doubling)
# crossing point: $100/kWh unlocks mass adoption (S-curve inflection)
cost_now = 150.0  # $/kWh today
cost_per_doubling = 0.82
doublings_to_crossing = 3  # 150 * 0.82^3 ≈ 82.7 < 100, crossing achieved
battery_cost_at_crossing = wrights_law(cost_now, cost_per_doubling, doublings_to_crossing)

# (2) 5-year TAM model with 15% CAGR hurdle
# TAM today: $200B (global EV battery market)
# 5-year TAM projection: $400B (doubling due to cost-driven adoption)
tam_now = 200e9
tam_5y = 400e9
tam_cagr = cagr_5y(tam_now, tam_5y)
hurdle = 0.15
tam_meets_hurdle = tam_cagr >= hurdle

# (3) Six-axis scoring table (people, execution, moat, product, risk, valuation)
# valuation proxy: 5-year CAGR vs hurdle
score = arkk_score(
    name="EV Battery Co",
    people=0.85,
    execution=0.75,
    moat=0.6,
    product_10x=True,  # battery cost < $100/kWh is 10x cheaper than 2010
    thesis_risk=0.3,
    cagr_5y=tam_cagr
)

# (4) Early-not-wrong position: drawdown is entry, not exit
# Current price down 40% from peak due to short-term supply glut
# Wright's Law still intact: cumulative doublings continue, cost curve bends
drawdown_stance = "40% drawdown = deep-value entry; cost curve unchanged, adoption S-curve intact"

# (5) Long-horizon note: 5-year windows only, no quarter-to-quarter trading
horizon_note = "Model evaluates 5-year windows only; no QoQ trading logic"

# Print model output
print("=== WRIGHT'S LAW COST CURVE ===")
print(f"Cost now: ${cost_now}/kWh")
print(f"Cost per doubling: {cost_per_doubling} (18% decline)")
print(f"Doublings to crossing: {doublings_to_crossing}")
print(f"Cost at crossing: ${battery_cost_at_crossing:.1f}/kWh (crosses $100 threshold)")
print(f"S-curve unlocked: mass adoption begins at crossing point")

print("\n=== 5-YEAR TAM MODEL ===")
print(f"TAM now: ${tam_now/1e9:.0f}B")
print(f"TAM in 5 years: ${tam_5y/1e9:.0f}B")
print(f"5-year CAGR: {tam_cagr*100:.1f}%")
print(f"15% CAGR hurdle met: {tam_meets_hurdle}")

print("\n=== SIX-AXIS SCORING TABLE ===")
print("Axis          | Score")
print("--------------|------")
print(f"People        | {score['people'] if 'people' in score else 0.85}")
print(f"Execution     | {score['execution'] if 'execution' in score else 0.75}")
print(f"Moat          | {score['moat'] if 'moat' in score else 0.6}")
print(f"Product (10x) | True")
print(f"Thesis risk   | {score['thesis_risk']}")
print(f"Valuation     | {score['cagr_5y']*100:.1f}% CAGR")
print(f"BUY: {score['buy']}")

print("\n=== EARLY-NOT-WRONG POSITION ===")
print(drawdown_stance)

print("\n=== LONG-HORIZON NOTE ===")
print(horizon_note)