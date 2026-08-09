# Boiler Room Research Note: Fictional "Quantum Widgets Inc." (Ticker: QWI)
# ----------------------------------------------------------------------
# (1) HARD VERDICT
# ----------------------------------------------------------------------
# BUY CASE:  QWI's new "NanoWidget" line has 3 signed pre-orders from
#            fictional industrial distributors, and gross margin guidance
#            of 45% (vs. 32% legacy) implies operating leverage.
# BEAR CASE: The company burns cash at $2M/quarter; if pre-orders slip,
#            dilution risk is real. Competitor "MegaGadget" is cutting prices.
# TRIGGER:   Q1 earnings (fictional date: 2025-04-15) — watch for
#            pre-order conversion rate and gross margin confirmation.
# INVALIDATION: If Q1 gross margin < 38% OR any pre-order is cancelled,
#            the thesis breaks.
# CONFIDENCE: 0.55 (moderate — based on limited public data, high uncertainty)
#
# (2) CURRENT SOURCES USED; EVIDENCE SEPARATED FROM HYPE
# ----------------------------------------------------------------------
# EVIDENCE (sourced, verifiable):
#   - QWI Q4 2024 press release (fictional URL: qwi.example.com/q4-2024)
#     -> reported $12M revenue, $2M operating loss, $8M cash on hand.
#   - Fictional industry report "Widget Weekly" (2025-02-01) -> lists
#     QWI's NanoWidget pre-orders as "3 confirmed, 2 in negotiation."
#   - Fictional competitor filing (MegaGadget 10-K, 2025-01-30) ->
#     price cut of 8% on comparable products.
# HYPE (promotional language, NOT evidence):
#   - "NanoWidget will revolutionize the industry" — no data behind it.
#   - "QWI is the next Tesla of widgets" — unsupported comparison.
#
# (3) NO GUARANTEED RETURNS ARE PROMISED
# ----------------------------------------------------------------------
# This note is a speculative analysis. There is NO promise of profit,
# no "sure thing," and no certainty. The confidence level is a
# probability estimate, not a guarantee. Markets can move against
# any thesis for reasons not captured here.
#
# (4) FOLLOW-UP PLAN: WHAT NEW DATA WOULD CHANGE THE VERDICT
# ----------------------------------------------------------------------
# - If Q1 2025 shows > 3 pre-orders converted to paid orders AND gross
#   margin >= 42%, raise confidence to 0.7 and upgrade to "strong buy."
# - If any pre-order is cancelled OR cash balance drops below $4M,
#   lower confidence to 0.3 and flip to "avoid."
# - If competitor price cuts accelerate (another 5%+ cut), re-evaluate
#   the bear case as dominant.
# - New data sources: Q1 10-Q filing, customer contract announcements,
#   channel checks with distributors.

def build_research_note():
    """Return the full research note as a structured dict and print it."""
    note = {
        "ticker": "QWI",
        "company": "Quantum Widgets Inc. (fictional)",
        "hard_verdict": {
            "buy_case": "NanoWidget line: 3 signed pre-orders, 45% gross margin guidance vs 32% legacy",
            "bear_case": "Cash burn $2M/quarter; competitor MegaGadget cutting prices 8%",
            "trigger": "Q1 2025 earnings (fictional date 2025-04-15) — pre-order conversion and margin",
            "invalidation": "Q1 gross margin < 38% OR any pre-order cancelled",
            "confidence": 0.55,  # moderate, not a guarantee
        },
        "sources": {
            "evidence": [
                "QWI Q4 2024 press release (fictional URL: qwi.example.com/q4-2024): $12M revenue, $2M op loss, $8M cash",
                "Widget Weekly industry report (2025-02-01): 3 confirmed pre-orders, 2 in negotiation",
                "MegaGadget 10-K (2025-01-30): 8% price cut on comparable products",
            ],
            "hype_separated": [
                "HYPE: 'NanoWidget will revolutionize the industry' — no data",
                "HYPE: 'QWI is the next Tesla of widgets' — unsupported comparison",
            ],
        },
        "no_guaranteed_returns": (
            "Speculative analysis only. No promise of profit. Confidence is a "
            "probability estimate, not certainty. Markets can move against any thesis."
        ),
        "follow_up_plan": {
            "upgrade_if": "Q1: >3 pre-orders converted AND gross margin >= 42% -> confidence 0.7, strong buy",
            "downgrade_if": "Any pre-order cancelled OR cash < $4M -> confidence 0.3, avoid",
            "re_evaluate_if": "Competitor price cuts accelerate (another 5%+ cut)",
            "new_data_sources": [
                "Q1 10-Q filing",
                "Customer contract announcements",
                "Channel checks with distributors",
            ],
        },
    }
    return note

def print_note(note):
    """Print the research note in a readable, checkable format."""
    print("=" * 60)
    print(f"BOILER ROOM RESEARCH NOTE — {note['ticker']} ({note['company']})")
    print("=" * 60)
    print("\n(1) HARD VERDICT")
    v = note["hard_verdict"]
    print(f"  BUY CASE:      {v['buy_case']}")
    print(f"  BEAR CASE:     {v['bear_case']}")
    print(f"  TRIGGER:       {v['trigger']}")
    print(f"  INVALIDATION:  {v['invalidation']}")
    print(f"  CONFIDENCE:    {v['confidence']} (0-1, not a guarantee)")
    print("\n(2) SOURCES — EVIDENCE SEPARATED FROM HYPE")
    print("  EVIDENCE (sourced):")
    for e in note["sources"]["evidence"]:
        print(f"    - {e}")
    print("  HYPE (promotional, NOT evidence):")
    for h in note["sources"]["hype_separated"]:
        print(f"    - {h}")
    print("\n(3) NO GUARANTEED RETURNS")
    print(f"  {note['no_guaranteed_returns']}")
    print("\n(4) FOLLOW-UP PLAN — WHAT NEW DATA CHANGES THE VERDICT")
    f = note["follow_up_plan"]
    print(f"  UPGRADE IF:    {f['upgrade_if']}")
    print(f"  DOWNGRADE IF:  {f['downgrade_if']}")
    print(f"  RE-EVALUATE:   {f['re_evaluate_if']}")
    print("  NEW DATA SOURCES TO WATCH:")
    for s in f["new_data_sources"]:
        print(f"    - {s}")
    print("=" * 60)

# Build and print the note
note = build_research_note()
print_note(note)