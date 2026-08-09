def second_level(consensus, priced_in, hidden_cost):
    return {"consensus": consensus,
            "already_priced_in": priced_in,
            "hidden_cost": hidden_cost,
            "verdict": "skeptical" if hidden_cost > priced_in else "defensible"}

def price_vs_value(value, total_cost_of_ownership):
    return {"value": value, "price": total_cost_of_ownership,
            "buy": value > total_cost_of_ownership}

# === INVESTMENT MEMO: TECHNOLOGY ETF (QQQ) vs. VALUE ETF (VTV) ===
# Second-level pass:
# consensus: "Tech will outperform forever due to AI and cloud adoption"
# priced in: everyone's allocation to growth stocks, high multiples, and narrative-driven inflows
# hidden cost: mean reversion risk when AI hype fades, margin compression from rising rates, and concentration risk in top 10 holdings (~50% of QQQ)

# Risk location:
# The risky part is the "safe" part: the liquidity and popularity of QQQ itself. The moment everyone believes tech is the only game in town is when the cycle turns. The risk is least perceived in the ETF wrapper—it feels diversified, but it's a single bet on one sector's narrative.

# Preparation move:
# Unpredictable: a 30% drawdown in tech due to regulatory shock or earnings miss. Prepared: 15% cash buffer, stop-loss at 10% below entry, and a paired short position in QQQ via inverse ETF (SQQQ) sized to 20% of portfolio. This hedges the outlier without betting on direction.

# Temperature reading:
# The room is euphoric: AI stocks trade at 50x sales, media celebrates "the new dot-com," and retail inflows into QQQ are at all-time highs. This is the time to question, not adopt. The cycle implies mean reversion is overdue, but timing is impossible—position defensively.

# Price-vs-value audit:
# Price: QQQ's expense ratio (0.20%), tracking error, and the opportunity cost of not owning value stocks (VTV) which trade at 15x earnings vs. QQQ's 30x. Value: one more year of AI-driven growth. Total cost of ownership: 15% underperformance if the cycle turns in 12 months. No deal.

print("=== INVESTMENT MEMO: TECHNOLOGY ETF (QQQ) vs. VALUE ETF (VTV) ===")
print("\nSecond-level analysis:")
print(second_level(
    "Tech will outperform forever due to AI and cloud adoption",
    "everyone's allocation to growth stocks, high multiples, and narrative-driven inflows",
    "mean reversion risk when AI hype fades, margin compression from rising rates, and concentration risk in top 10 holdings (~50% of QQQ)"
))

print("\nRisk location:")
print("# The risky part is the 'safe' part: the liquidity and popularity of QQQ itself. The moment everyone believes tech is the only game in town is when the cycle turns.")

print("\nPreparation move:")
print("# Unpredictable: a 30% drawdown in tech due to regulatory shock or earnings miss. Prepared: 15% cash buffer, stop-loss at 10% below entry, and a paired short position in QQQ via inverse ETF (SQQQ) sized to 20% of portfolio.")

print("\nTemperature reading:")
print("# The room is euphoric: AI stocks trade at 50x sales, media celebrates 'the new dot-com,' and retail inflows into QQQ are at all-time highs. This is the time to question, not adopt.")

print("\nPrice-vs-value audit:")
print(price_vs_value(1, 1.5))
print("# Price: QQQ's expense ratio (0.20%), tracking error, and the opportunity cost of not owning value stocks (VTV) which trade at 15x earnings vs. QQQ's 30x. Value: one more year of AI-driven growth. Total cost of ownership: 15% underperformance if the cycle turns in 12 months. No deal.")