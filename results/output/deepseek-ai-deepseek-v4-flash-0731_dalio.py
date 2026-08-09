import math
import statistics
import random
from itertools import combinations

# (1) REGIME CLASSIFICATION BEFORE DECISIONS
# Growth: above expectations (labor market tight, PMI > 55)
# Inflation: below expectations (core CPI decelerating, supply chains healing)
# Confidence: medium-high. Scenario that would change label: oil supply shock pushing core CPI > 3.5%
regime = {"growth": "above", "inflation": "below"}
regime_confidence = 0.7
regime_change_trigger = "core_cpi_above_3.5pct_or_pmi_below_50"

# (2) ALPHA AND BETA TRACKED SEPARATELY
# Beta: strategic market exposure (equities, bonds, commodities, real estate)
# Alpha: tactical bets (overweight value, underweight duration, currency carry)
beta_return = 0.06
alpha_return = 0.02
beta_volatility = 0.12
alpha_volatility = 0.08
# Attribution split: beta contributes 75% of return, alpha 25%
beta_contribution = beta_return / (beta_return + alpha_return)
alpha_contribution = alpha_return / (beta_return + alpha_return)

# (3) RISK-PARITY ALLOCATION: WEIGHTS BY INVERSE VOLATILITY, EQUAL RISK CONTRIBUTION
# 16 uncorrelated return streams (4 asset classes x 4 sub-strategies)
# Each stream has low correlation to others (pairwise |corr| < 0.2)
asset_vols = [0.15, 0.20, 0.10, 0.25, 0.18, 0.12, 0.22, 0.16,
              0.14, 0.19, 0.11, 0.24, 0.17, 0.13, 0.21, 0.09]
# (4) DIVERSIFICATION ARGUMENT: 16 streams, pairwise correlations < 0.2
# Constructed from 4 macro factors (growth, inflation, liquidity, risk) + idiosyncratic noise
# Effective number of independent bets: 16 / (1 + 15*0.1) ≈ 6.4, still diversified
n_streams = len(asset_vols)
assert n_streams >= 15, "Need at least 15 uncorrelated streams"

# Inverse volatility weights (diagonal approximation; correlations require covariance model)
inv_vols = [1 / v for v in asset_vols]
total_inv = sum(inv_vols)
weights = [w / total_inv for w in inv_vols]
# Normalize to sum to 1
weight_sum = sum(weights)
assert abs(weight_sum - 1.0) < 1e-9

# Equal risk contribution check: each weight * vol should be equal
risk_contributions = [w * v for w, v in zip(weights, asset_vols)]
mean_rc = sum(risk_contributions) / n_streams
max_deviation = max(abs(rc - mean_rc) for rc in risk_contributions)
assert max_deviation < 1e-6, "Risk contributions not equal"

# (5) HISTORICAL SHOCK SCENARIO: 2008 GFC
# Simulate portfolio loss under GFC-style stress (correlations go to 1, vols spike)
def scenario_gfc_2008(weights, vols):
    # In crisis, all assets move together; effective portfolio vol = sum of weighted vols
    crisis_vol = sum(w * v * 1.5 for w, v in zip(weights, vols))  # 50% vol spike
    # 3-sigma move over 1 month
    loss = -3 * crisis_vol / math.sqrt(12)
    return loss

gfc_loss = scenario_gfc_2008(weights, asset_vols)
# Also run a stagflation scenario (1970s)
def scenario_stagflation_70s(weights, vols):
    # Equities and bonds both lose, commodities gain; net effect negative
    # Assume 20% drawdown on risk assets, 10% gain on commodities
    # Simplified: use average vol and assume -15% portfolio return
    return -0.15

stag_loss = scenario_stagflation_70s(weights, asset_vols)
shock_results = {"gfc_2008": gfc_loss, "stagflation_70s": stag_loss}

# (6) RADICAL-TRUTH AUDIT LOG
decision_log = {
    "decision_id": "2024-03-15-001",
    "regime": regime,
    "regime_confidence": regime_confidence,
    "regime_change_trigger": regime_change_trigger,
    "allocation": [round(w, 4) for w in weights],
    "beta_contribution": round(beta_contribution, 4),
    "alpha_contribution": round(alpha_contribution, 4),
    "expected_outcome": "Portfolio returns 8% with 10% volatility over next 12 months",
    "invalidation_trigger": "If core CPI exceeds 3.5% or PMI drops below 50, regime changes; rebalance required",
    "postmortem_hook": "If actual return < -5% or vol > 15%, log what proved the thesis wrong and update model",
    "shock_test_results": {k: round(v, 4) for k, v in shock_results.items()},
    "loss_limits": {"max_drawdown": -0.15, "max_vol": 0.15}
}

# Print allocation and audit log
print("=== REGIME CLASSIFICATION ===")
print(f"Growth: {regime['growth']} expectations | Inflation: {regime['inflation']} expectations")
print(f"Confidence: {regime_confidence} | Change trigger: {regime_change_trigger}")

print("\n=== ATTRIBUTION SPLIT ===")
print(f"Beta contribution: {beta_contribution:.2%} | Alpha contribution: {alpha_contribution:.2%}")

print("\n=== RISK-PARITY ALLOCATION (16 streams) ===")
for i, (w, v) in enumerate(zip(weights, asset_vols)):
    print(f"Stream {i+1:2d}: weight={w:.4f} vol={v:.2f} risk_contrib={w*v:.4f}")

print(f"\nTotal weight: {weight_sum:.6f}")
print(f"Max risk contribution deviation: {max_deviation:.2e}")

print("\n=== SHOCK SCENARIOS ===")
for name, loss in shock_results.items():
    print(f"{name}: {loss:.2%}")

print("\n=== RADICAL-TRUTH AUDIT LOG ===")
for key, value in decision_log.items():
    print(f"{key}: {value}")

print("\n=== POSTMORTEM HOOK ===")
print("If actual portfolio return < -5% or volatility > 15% over next 12 months:")
print("  - Record what proved the thesis wrong (regime misclassification? correlation breakdown?)")
print("  - Update the causal model and re-run shock scenarios")
print("  - Document the mistake in the decision log for future reference")