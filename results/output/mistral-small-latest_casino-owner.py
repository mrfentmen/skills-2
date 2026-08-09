import math

def evaluate(probability, gross_payout, fee, risk_limit):
    """
    Normalized betting analysis for a casino game.
    (1) Normalized stake = 1.0 unit; payout is gross (includes stake on win).
    (2) probability: win chance in [0,1]; odds implied by gross_payout;
        fee charged on every attempt; EV, variance, and max loss computed.
    (3) Assumptions: gross_payout includes stake on win; fee is fixed per play;
        risk_limit is the maximum acceptable loss per unit stake.
    (4) Action gate: act only if EV > 0, max_loss <= risk_limit, and inputs valid.
    (5) Abstain for invalid inputs, missing data, or EV <= 0 or max_loss > risk_limit.
    """
    values = (probability, gross_payout, fee, risk_limit)
    if not all(math.isfinite(value) for value in values):
        return {"action": "abstain", "reason": "non-finite inputs"}
    if not (0 <= probability <= 1):
        return {"action": "abstain", "reason": "probability not in [0,1]"}
    if gross_payout <= 0:
        return {"action": "abstain", "reason": "non-positive gross payout"}
    if fee < 0:
        return {"action": "abstain", "reason": "negative fee"}
    if risk_limit < 0:
        return {"action": "abstain", "reason": "negative risk limit"}

    stake = 1.0
    win_payoff = gross_payout - stake - fee  # net win after stake and fee
    loss_payoff = -stake - fee               # net loss after stake and fee
    ev = probability * win_payoff + (1 - probability) * loss_payoff
    variance = probability * (win_payoff - ev) ** 2 + (1 - probability) * (loss_payoff - ev) ** 2
    max_loss = -loss_payoff
    edge_holder = "opportunity" if ev > 0 else "house"

    if ev > 0 and max_loss <= risk_limit:
        action = "act"
    else:
        reason = []
        if ev <= 0:
            reason.append("EV not positive")
        if max_loss > risk_limit:
            reason.append("max loss exceeds risk limit")
        action = "abstain"
        reason_str = " and ".join(reason) if reason else "EV not positive or max loss exceeded"

    sensitivity = None
    if action == "abstain":
        if ev <= 0:
            sensitivity = f"raise probability above {probability + (-ev / win_payoff):.3f} or reduce fee below {fee + (-ev):.3f}"
        if max_loss > risk_limit:
            sensitivity = f"reduce risk limit below {max_loss:.3f} or reduce fee below {fee + (risk_limit - max_loss):.3f}"

    return {
        "probability": round(probability, 3),
        "gross_payout": round(gross_payout, 3),
        "fee": round(fee, 3),
        "risk_limit": round(risk_limit, 3),
        "win_payoff": round(win_payoff, 3),
        "loss_payoff": round(loss_payoff, 3),
        "ev": round(ev, 3),
        "variance": round(variance, 3),
        "max_loss": round(max_loss, 3),
        "edge_holder": edge_holder,
        "action": action,
        "assumptions": {
            "stake": stake,
            "payout_includes_stake_on_win": True,
            "fee_charged_per_attempt": True,
            "risk_limit_per_unit_stake": True
        },
        "sensitivity": sensitivity
    }

# Demo: a simple coin-flip game with 2.2x gross payout, 0.1 fee, and 1.2 risk limit
report = evaluate(probability=0.55, gross_payout=2.20, fee=0.10, risk_limit=1.20)
print(report)

# Edge case: invalid probability
print(evaluate(probability=1.2, gross_payout=2.20, fee=0.10, risk_limit=1.20))

# Edge case: EV negative
print(evaluate(probability=0.45, gross_payout=2.20, fee=0.10, risk_limit=1.20))

# Edge case: max loss exceeds limit
print(evaluate(probability=0.55, gross_payout=2.20, fee=0.0, risk_limit=1.0))