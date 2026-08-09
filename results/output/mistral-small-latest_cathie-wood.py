def wrights_law(cost_now, cost_per_doubling, doublings):
    return cost_now * (cost_per_doubling ** doublings)

def tam_model(base_tam, cagr_5y):
    return base_tam * ((1 + cagr_5y) ** 5)

def arkk_score(name, people, execution, moat, product_10x, thesis_risk, cagr_5y):
    ok = (product_10x and execution >= 0.7 and moat >= 0.5
          and cagr_5y >= 0.15 and thesis_risk <= 0.4)
    return {
        "name": name,
        "buy": ok,
        "people": people,
        "execution": execution,
        "moat": moat,
        "product_10x": product_10x,
        "thesis_risk": thesis_risk,
        "cagr_5y": cagr_5y,
        "valuation": tam_model(1000, cagr_5y) if ok else 0
    }

# EV battery cost decline model (Wright's Law)
# cost_per_doubling = 0.78 (22% decline per cumulative doubling of production)
# doublings_to_crossing = 5 (crossing point at ~$60/kWh, unlocking S-curve adoption)
initial_cost = 150.0  # $/kWh in 2023
cost_per_doubling = 0.78
doublings = 5
cost_after_5_doublings = wrights_law(initial_cost, cost_per_doubling, doublings)

# 5-year TAM model with 15% CAGR hurdle
# Base TAM: $100B in 2023, growing at 15% CAGR to ~$201B by 2028
base_tam = 100.0  # $B
cagr_5y = 0.15
tam_5y = tam_model(base_tam, cagr_5y)

# Six-axis scoring for EV battery leader
score = arkk_score(
    name="EV Battery Leader",
    people=0.85,        # Strong leadership with deep domain expertise
    execution=0.8,      # On track to 500 GWh capacity by 2025
    moat=0.75,          # Vertical integration and proprietary cell chemistry
    product_10x=True,   # 3x energy density vs 2020 baseline
    thesis_risk=0.25,   # Regulatory and commodity price risks
    cagr_5y=0.25        # 25% CAGR over 5 years (above 15% hurdle)
)

# Early-not-wrong position: Current drawdown (~50% from peak) is deep-value entry
# Rationale: Cost curve inflection at $60/kWh triggers mass adoption S-curve
# Market misprices the 5-year trajectory, focusing on short-term noise
# "We're not wrong, we're early" — concentration into highest-conviction names

print("EV Battery Cost Curve Model:")
print(f"Initial cost: ${initial_cost}/kWh")
print(f"Cost after {doublings} doublings: ${cost_after_5_doublings:.2f}/kWh")
print(f"Crossing point ($60/kWh) reached at {5 - (cost_after_5_doublings / 60):.1f} doublings remaining")
print("\n5-Year TAM Model:")
print(f"Base TAM: ${base_tam}B | 5-Year CAGR: {cagr_5y*100:.0f}% | Projected TAM: ${tam_5y:.1f}B")
print("\nARKK Six-Axis Scorecard:")
print(score)