def price_bet(probability, payoff, cost, risk_limit, modeled_max_loss, moat, target, window_days, evidence):
    import math
    numbers = (probability, payoff, cost, risk_limit, modeled_max_loss)
    if (any(isinstance(value, bool) for value in numbers) or not all(math.isfinite(value) for value in numbers) or not 0 <= probability <= 1
            or payoff < 0 or cost < 0 or risk_limit < 0 or modeled_max_loss < 0
            or not isinstance(moat, str) or not moat.strip()
            or not isinstance(target, str) or not target.strip()
            or not isinstance(window_days, int) or isinstance(window_days, bool) or window_days <= 0
            or evidence not in {"measured", "weak"}):
        return {"decision": "reject", "reason": "invalid bet contract", "ev": 0.0, "modeled_max_loss": modeled_max_loss, "risk_limit": risk_limit, "moat": moat if isinstance(moat, str) else "", "metric": target if isinstance(target, str) else "", "window_days": window_days if isinstance(window_days, int) and not isinstance(window_days, bool) else 0, "rollback": "not applicable", "cut": []}
    ev = probability * payoff - cost
    if evidence == "weak":
        decision = "measure-more"
    elif ev > 0 and cost <= risk_limit and modeled_max_loss <= risk_limit:
        decision = "bet"
    else:
        decision = "reject"
    return {"decision": decision, "ev": round(ev, 2),
            "modeled_max_loss": modeled_max_loss, "risk_limit": risk_limit,
            "moat": moat, "metric": target, "window_days": window_days,
            "rollback": "stop if metric misses target at window end",
            "cut": ["decorative dashboard", "unmeasured integration"]}

# (1) Expected value: probability=0.6, payoff=100, cost=30, value=0.6*100-30=30
# (2) Maximum loss=35, risk limit=40, rollback: stop if metric misses target at window end
# (3) Moat hypothesis: owned activation data (data quality compounds with each user)
# (4) Compounding metric: activation +5pp, window: 30 days
# (5) Cut list: decorative dashboard, unmeasured integration
# (6) Working code returns bet/reject/measure-more

report = price_bet(0.6, 100, 30, 40, 35, "owned activation data", "activation +5pp", 30, "measured")
print(report["decision"])