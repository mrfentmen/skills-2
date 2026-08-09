import math

def evaluate(probability, gross_payout, fee, risk_limit):
    # (1) Normalized stake: 1 unit. Payout is GROSS: winning unit returns gross_payout (includes stake).
    # (2) Inputs: probability, gross_payout, fee (charged every attempt), risk_limit (max acceptable loss).
    # Validate all inputs are finite and within bounds.
    values = (probability, gross_payout, fee, risk_limit)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("all inputs must be finite")
    if not (0 <= probability <= 1) or gross_payout <= 0 or fee < 0 or risk_limit < 0:
        raise ValueError("invalid probability, payout, fee, or risk limit")

    stake = 1.0
    # Win payoff: gross payout minus stake (since gross includes stake) minus fee.
    win = gross_payout - stake - fee
    # Loss payoff: lose stake plus fee.
    loss = -stake - fee

    # (2) Expected value, variance, maximum loss.
    ev = probability * win + (1 - probability) * loss
    variance = probability * (win - ev) ** 2 + (1 - probability) * (loss - ev) ** 2
    max_loss = -loss  # positive number representing worst-case loss

    # (3) Edge holder: opportunity if EV > 0, else house.
    edge_holder = "opportunity" if ev > 0 else "house"

    # (4) Action gate: positive EV, max loss within risk limit, and inputs complete (already validated).
    # (5) Abstain if EV <= 0 or max loss exceeds limit.
    action = "act" if ev > 0 and max_loss <= risk_limit else "abstain"

    return {
        "probability": probability,
        "gross_payout": gross_payout,
        "fee": fee,
        "risk_limit": risk_limit,
        "stake": stake,
        "win_payoff": round(win, 3),
        "loss_payoff": round(loss, 3),
        "ev": round(ev, 3),
        "variance": round(variance, 3),
        "max_loss": round(max_loss, 3),
        "edge_holder": edge_holder,
        "action": action,
        "assumptions": {
            "payout_is_gross": True,
            "stake_normalized": stake,
            "fee_charged_every_attempt": True,
            "probability_in_[0,1]": True
        }
    }

# Demo: tiny casino game — e.g., a single number on a simplified wheel.
# Probability of win = 0.5, gross payout = 2.1 (includes stake), fee = 0.05, risk limit = 1.5.
report = evaluate(0.5, 2.1, 0.05, 1.5)
print("Analysis:")
for key, value in report.items():
    print(f"  {key}: {value}")

# Show abstain for non-positive EV (house edge).
report_house = evaluate(0.45, 2.0, 0.1, 1.0)
print("\nHouse-edge example:")
for key, value in report_house.items():
    print(f"  {key}: {value}")

# Show abstain for risk limit breach.
report_risk = evaluate(0.6, 2.5, 0.0, 0.5)
print("\nRisk-limit breach example:")
for key, value in report_risk.items():
    print(f"  {key}: {value}")

# Show abstain for invalid input (missing/invalid probability).
try:
    evaluate(1.2, 2.0, 0.0, 1.0)
except ValueError as e:
    print(f"\nInvalid input example: {e}")