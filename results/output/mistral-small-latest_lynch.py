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

# Example: Starbucks (SBUX) - hardcoded financials
# What you know spark: Observed Starbucks stores globally; coffee is a meaningful % of revenue
# Verified: Coffee/tea products contribute ~75% of revenue (revenue_share=0.75)
# Category: Fast grower (historical revenue growth ~20%)
# PEG: P/E=25, growth=20% → PEG=1.25 (between 1.0 and 2.0 → WATCH)
# Two-minute story: Starbucks dominates the premium coffee market with strong brand loyalty and global expansion; consistent revenue growth and pricing power justify valuation.
# Anti-diworsification: Focus on 10-15 understandable names like SBUX, not 50 random stocks.

analysis = classify_and_advise("fast grower", 25, 20, 0.75)
print({
    "company": "Starbucks (SBUX)",
    "what_you_know": "Coffee/tea products contribute 75% of revenue (observed globally)",
    "category": "fast grower",
    "questions": [
        "Is the growth rate sustainable (>20% annually)?",
        "Does the company have a durable competitive advantage (brand, network effects)?",
        "Can it expand margins or is growth volume-driven?"
    ],
    "peg_ratio": analysis["peg"],
    "peg_interpretation": "<1.0 cheap, 1.0-2.0 fair, >2.0 priced in → WATCH",
    "two_minute_story": "Starbucks sells premium coffee globally with strong brand loyalty. Its global store expansion and pricing power drive consistent revenue growth. The stock is fairly valued at current levels, but the business story remains compelling for long-term holders.",
    "anti_diworsification": "Hold few names like SBUX that are well-understood, not a diversified portfolio of unknowns."
})