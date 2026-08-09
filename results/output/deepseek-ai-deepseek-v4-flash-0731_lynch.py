# (1) What-you-know spark verified against fundamentals:
# Spark: I saw their boring industrial fasteners in every hardware store I visited.
# Verification: fasteners are 45% of total revenue (0.45), so it's a meaningful product, not a rounding error.

# (2) Classification: Fast grower
# Matching questions for a fast grower:
# - Can this growth continue for several years?
# - Is the growth rate sustainable or a one-time spike?
# - What is the market size and share?

# (3) PEG ratio: P/E = 22, growth = 30% -> PEG = 22 / 30 = 0.73
# Interpretation: < 1.0, so it's cheap relative to growth.

# (4) Two-minute story:
# "They make the boring fasteners every factory needs; sales are growing 30% a year
# because they keep winning contracts from bigger rivals. Simple, repeatable, and I understand it."

# (5) Anti-diworsification stance:
# Only 3 names in the portfolio, all boring and understood. No chasing 50 tickers.

def peg(pe, growth_pct):
    return pe / growth_pct if growth_pct else float("inf")

def classify_and_advise(category, pe, growth_pct, revenue_share):
    p = peg(pe, growth_pct)
    if revenue_share < 0.10:
        return {"verdict": "SKIP", "why": "product is a rounding error of revenue"}
    if category == "cyclical" and p < 1.0:
        return {"verdict": "TRAP", "why": "low P/E at the earnings peak is a classic cyclical trap"}
    if p <= 1.0:
        return {"verdict": "FAIR", "peg": round(p, 2)}
    if p >= 2.0:
        return {"verdict": "PRICED_IN", "peg": round(p, 2)}
    return {"verdict": "WATCH", "peg": round(p, 2)}

# Hardcoded example: FastenerCo
result = classify_and_advise("fast grower", 22, 30, 0.45)

print("=== LYNCH ANALYSIS: FastenerCo ===")
print("(1) What you know: fasteners = 45% of revenue -> verified, not a rounding error")
print("(2) Category: Fast grower")
print("    Questions: Can growth continue? Sustainable? Market size?")
print("(3) PEG = 22 / 30 = 0.73 -> cheap (<1.0)")
print("(4) Two-minute story: 'Boring fasteners every factory needs; 30% growth from winning contracts.'")
print("(5) Anti-diworsification: 3 names, all understood, no weeds watered.")
print("Verdict:", result)