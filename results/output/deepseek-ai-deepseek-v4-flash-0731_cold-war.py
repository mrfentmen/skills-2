def build_dossier():
    # ============================================================
    # DECISION: Should we increase production capacity next quarter?
    # ============================================================

    # --- SOURCE LEDGER ---
    # S1: Internal production report (high reliability, primary)
    # S2: Supplier interview (medium reliability, secondary)
    # S3: Industry newsletter (low reliability, tertiary, possibly copied)
    # S4: Competitor press release (medium reliability, primary but self-serving)

    # --- EVIDENCE TIERS ---
    # FACT: Direct observation from a reliable source
    # INFERENCE: Logical conclusion drawn from facts
    # WEAK SIGNAL: Unconfirmed, low-confidence indicator
    # UNKNOWN: No data available
    # POSSIBLE DISINFO: Suspected deliberate misinformation

    facts = [
        {
            "text": "Current capacity utilization is at 85%.",
            "source": "S1",
            "reliability": "high",
            "independent": True,
        },
        {
            "text": "Supplier lead times increased by 20% in the last month.",
            "source": "S2",
            "reliability": "medium",
            "independent": True,
        },
    ]

    inferences = [
        {
            "text": "If utilization stays above 80%, we risk delivery delays.",
            "source": "S1 + S2",
            "reliability": "medium",
            "independent": True,
        },
        {
            "text": "Competitor's new product launch may be a response to our market share gains.",
            "source": "S4",
            "reliability": "medium",
            "independent": True,
        },
    ]

    weak_signals = [
        {
            "text": "Unverified rumor of a major supplier shutdown.",
            "source": "S3",
            "reliability": "low",
            "independent": False,  # S3 may have copied from S2
        },
    ]

    unknowns = [
        {
            "text": "Actual next-quarter demand forecast.",
            "source": "none",
            "reliability": "missing",
            "independent": False,
        },
        {
            "text": "Competitor's true production capacity.",
            "source": "none",
            "reliability": "missing",
            "independent": False,
        },
    ]

    possible_disinfo = [
        {
            "text": "Competitor claims they are 'expanding aggressively' — may be a bluff to deter us.",
            "source": "S4",
            "reliability": "low (self-serving)",
            "independent": True,
        },
    ]

    # --- COMPETING HYPOTHESES ---
    # H1: Demand is genuinely rising, requiring capacity expansion.
    # H2: Supplier delays are temporary, no capacity change needed.
    # H3: Competitor is signaling to discourage our expansion (deliberate disinformation).

    hypotheses = [
        {
            "name": "H1: Genuine demand increase",
            "support": 2,  # facts + inferences
            "reliability": 2,  # medium
            "falsifier": "If next-quarter orders drop below current levels, H1 weakens.",
        },
        {
            "name": "H2: Temporary supplier disruption",
            "support": 1,  # only weak signal
            "reliability": 1,  # low
            "falsifier": "If supplier lead times remain elevated for two more months, H2 weakens.",
        },
        {
            "name": "H3: Competitor bluff",
            "support": 1,  # possible disinfo
            "reliability": 1,  # low
            "falsifier": "If competitor's actual production data shows real expansion, H3 weakens.",
        },
    ]

    # --- CONFIDENCE LEVELS (tied to evidence quality) ---
    # H1: medium (based on two independent medium/high reliability sources)
    # H2: low (only one weak signal)
    # H3: low (only self-serving press release)

    # --- CONTRADICTIONS / COLLECTION GAPS ---
    # S3 repeats S2's rumor; not independent corroboration.
    # No direct data on competitor's actual capacity or next-quarter demand.

    # --- OUTPUT ---
    print("=== INTELLIGENCE DOSSIER ===")
    print("\n--- FACTS ---")
    for f in facts:
        print(f"  - {f['text']} [Source: {f['source']}, Reliability: {f['reliability']}, Independent: {f['independent']}]")

    print("\n--- INFERENCES ---")
    for i in inferences:
        print(f"  - {i['text']} [Source: {i['source']}, Reliability: {i['reliability']}, Independent: {i['independent']}]")

    print("\n--- WEAK SIGNALS ---")
    for w in weak_signals:
        print(f"  - {w['text']} [Source: {w['source']}, Reliability: {w['reliability']}, Independent: {w['independent']}]")

    print("\n--- UNKNOWNS ---")
    for u in unknowns:
        print(f"  - {u['text']} [Source: {u['source']}, Reliability: {u['reliability']}]")

    print("\n--- POSSIBLE DISINFO ---")
    for d in possible_disinfo:
        print(f"  - {d['text']} [Source: {d['source']}, Reliability: {d['reliability']}, Independent: {d['independent']}]")

    print("\n--- COMPETING HYPOTHESES ---")
    for h in hypotheses:
        confidence = "medium" if h["support"] >= 2 and h["reliability"] >= 2 else "low"
        print(f"  - {h['name']} | Confidence: {confidence} | Falsifier: {h['falsifier']}")

    print("\n--- COLLECTION GAPS ---")
    print("  - No independent verification of competitor's capacity claims.")
    print("  - Next-quarter demand forecast is missing.")
    print("  - S3 is correlated with S2; not independent corroboration.")

    print("\n--- RECOMMENDATION ---")
    print("  - Do not expand capacity yet. Collect next-quarter demand data and verify competitor's actual production before acting.")

build_dossier()