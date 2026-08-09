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

# Opportunity: AI-powered customer support automation for mid-market SaaS
# Expected value:
#   Probability of 0.7 that automation reduces support OPEX by 40% within 12 months
#   Payoff: $2.4M annual savings at steady state (40% of $6M current OPEX)
#   Cost: $450K to build and deploy (engineering + infra + training)
#   EV = 0.7 * 2.4M - 0.45M = $1.31M
# Maximum loss: $500K (engineering overrun + opportunity cost)
# Reversibility: Can rollback to human-only support within 2 weeks by flipping a feature flag; no data loss
# Moat hypothesis: Distribution moat via proprietary support interaction data that improves model fine-tuning
# Compounding metric: "Support automation coverage %" (target +15pp from baseline 20% to 35% within 90 days)
# Window: 90 days to hit coverage target; rollback trigger if coverage < 25% at day 90
# Cut list: decorative analytics dashboard, multi-language support v1, proactive outbound chat

report = price_bet(
    probability=0.7,
    payoff=2_400_000,
    cost=450_000,
    risk_limit=500_000,
    modeled_max_loss=480_000,
    moat="proprietary support interaction data for model fine-tuning",
    target="support automation coverage +15pp (20%→35%)",
    window_days=90,
    evidence="measured"
)
print(report)