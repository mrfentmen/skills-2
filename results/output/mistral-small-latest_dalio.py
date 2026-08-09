import math
import random

# === REGIME CLASSIFICATION ===
# growth: "above expectations" (ISM PMI > 50, unemployment falling)
# inflation: "below expectations" (CPI YoY < 3%, breakevens stable)
# regime = {"growth": "above", "inflation": "below"}
regime = {"growth": "above", "inflation": "below"}

# === RETURN STREAMS (15 uncorrelated) ===
# 15 assets with hardcoded returns: 10 beta (market exposures), 5 alpha (idiosyncratic)
# Beta streams: S&P 500, 10Y Treasury, Gold, Euro Stoxx, EM equities, etc.
# Alpha streams: merger arb, convertible arb, volatility selling, reinsurance, tail hedging
random.seed(42)
n = 15
returns = []
for i in range(n):
    if i < 10:
        # Beta streams: correlated with growth/inflation
        base = 0.05 + 0.02 * (1 if regime["growth"] == "above" else -1)
        noise = random.gauss(0, 0.03)
        returns.append(base + noise)
    else:
        # Alpha streams: idiosyncratic, low correlation to macro
        alpha_base = 0.03 + 0.01 * (1 if random.random() > 0.5 else -1)
        alpha_noise = random.gauss(0, 0.02)
        returns.append(alpha_base + alpha_noise)

# === VOLATILITIES (annualized) ===
vols = [0.15, 0.12, 0.18, 0.20, 0.22, 0.10, 0.16, 0.14, 0.19, 0.17,  # beta streams
        0.08, 0.07, 0.09, 0.06, 0.05]  # alpha streams

# === BETA vs ALPHA ATTRIBUTION ===
beta_returns = returns[:10]
alpha_returns = returns[10:]
beta_contribution = sum(beta_returns) / len(beta_returns)
alpha_contribution = sum(alpha_returns) / len(alpha_returns)

# === RISK-PARITY ALLOCATION ===
inv_vol = [1.0 / v for v in vols]
total_inv = sum(inv_vol)
weights = [round(w / total_inv, 6) for w in inv_vol]

# === SHOCK SCENARIO: 2008 GFC ===
# Simulate drawdowns: S&P -37%, 10Y -15%, Gold +5%, EM -50%, etc.
shock_returns = [
    -0.37, -0.15, 0.05, -0.50, -0.45,  # beta shocks
    -0.10, -0.08, -0.12, -0.05, -0.07,  # beta shocks
    -0.20, -0.18, -0.22, -0.15, -0.10   # alpha shocks
]
shock_pnl = sum(w * r for w, r in zip(weights, shock_returns))

# === AUDIT LOG ===
decision = {
    "timestamp": "2023-11-15T00:00:00Z",
    "regime": regime,
    "thesis": "All-weather portfolio with risk parity and alpha/beta split",
    "expected_outcome": "Positive Sharpe, drawdown < 20% in GFC-like shock",
    "invalidation_trigger": "Cumulative 12-month loss > 15% or regime shift",
    "postmortem": None  # Filled if invalidated
}

# === PRINT RESULTS ===
print("=== DALIO PORTFOLIO ANALYSIS ===")
print(f"Regime: growth={regime['growth']}, inflation={regime['inflation']}")
print("\nBeta vs Alpha Attribution:")
print(f"Beta contribution: {beta_contribution:.4f}")
print(f"Alpha contribution: {alpha_contribution:.4f}")
print("\nRisk-Parity Weights (inverse volatility, normalized):")
for i, w in enumerate(weights):
    print(f"Asset {i+1}: {w:.4f}")
print(f"\nTotal portfolio volatility (approx): {math.sqrt(sum((w*v)**2 for w, v in zip(weights, vols))):.4f}")
print("\nHistorical Shock Scenario (2008 GFC):")
print(f"Portfolio loss: {shock_pnl:.4f}")
print("\nAudit Log:")
print(f"Decision: {decision['thesis']}")
print(f"Regime at decision: {decision['regime']}")
print(f"Expected outcome: {decision['expected_outcome']}")
print(f"Invalidation trigger: {decision['invalidation_trigger']}")
print(f"Postmortem: {decision['postmortem'] or 'No invalidation yet'}")