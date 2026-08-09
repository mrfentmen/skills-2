def build_dossier():
    # decision: should we expand into the new market this quarter?

    # Source ledger:
    # S1: competitor's quarterly report (primary filing, high reliability)
    # S2: industry analyst interview (medium reliability)
    # S3: anonymous forum post (low reliability, correlated with S1)
    # S4: internal sales data (high reliability, internal)
    # S5: competitor's press release (medium reliability, repeated in trade journals)

    # Evidence tiers:
    facts = [
        {"text": "Competitor A's market share dropped from 22% to 18% in Q2", "source": "S1 filing", "reliability": "high", "independent": True},
        {"text": "Our internal sales in adjacent region grew 8% YoY", "source": "S4 internal", "reliability": "high", "independent": True},
    ]

    inferences = [
        {"text": "Competitor A is losing ground to new entrants", "source": "S1 + S2", "reliability": "medium", "independent": True},
        {"text": "Our product quality advantage is gaining traction", "source": "S2 interview + S4 internal", "reliability": "medium", "independent": True},
    ]

    weak_signals = [
        {"text": "Rumors of Competitor A's R&D delays circulating in industry forums", "source": "S3 post", "reliability": "low", "independent": False},
        {"text": "Trade journal mentions 'strategic pivot' by Competitor A", "source": "S5 press release", "reliability": "medium", "independent": True},
    ]

    unknowns = [
        {"text": "Competitor A's actual R&D pipeline status", "source": "none", "reliability": "missing", "independent": False},
        {"text": "Customer retention rates in Competitor A's core segment", "source": "none", "reliability": "missing", "independent": False},
    ]

    disinfo = [
        {"text": "Social media claims of Competitor A's imminent bankruptcy", "source": "S3 post", "reliability": "low", "independent": False},
    ]

    # Competing hypotheses:
    # H1: Market expansion opportunity due to competitor weakness (supported by facts + inferences)
    # H2: Strategic trap - competitor is feigning weakness to lure us into over-expansion (supported by weak signals + unknowns)
    # H3: Temporary volatility - competitor's issues are cyclical and will resolve (supported by unknowns)

    hypotheses = [
        {
            "name": "market_opportunity",
            "support": 3,
            "reliability": 3,
            "falsifier": "Competitor A's market share stabilizes at 18% for two consecutive quarters without further decline",
            "confidence": "high"
        },
        {
            "name": "strategic_trap",
            "support": 2,
            "reliability": 1,
            "falsifier": "Competitor A announces major R&D breakthrough or new product line within 6 months",
            "confidence": "low"
        },
        {
            "name": "temporary_volatility",
            "support": 1,
            "reliability": 2,
            "falsifier": "Competitor A's market share recovers to 20%+ within one quarter",
            "confidence": "medium"
        }
    ]

    # Build dossier structure
    dossier = {
        "decision": "should we expand into the new market this quarter?",
        "source_ledger": {
            "S1": "competitor's quarterly report (primary filing, high reliability)",
            "S2": "industry analyst interview (medium reliability)",
            "S3": "anonymous forum post (low reliability, correlated with S1)",
            "S4": "internal sales data (high reliability, internal)",
            "S5": "competitor's press release (medium reliability, repeated in trade journals)"
        },
        "evidence": {
            "facts": facts,
            "inferences": inferences,
            "weak_signals": weak_signals,
            "unknowns": unknowns,
            "disinfo": disinfo
        },
        "hypotheses": hypotheses,
        "leading_hypothesis": max(hypotheses, key=lambda h: h["support"] * h["reliability"] if h["reliability"] > 0 else 0)["name"],
        "leading_confidence": max(hypotheses, key=lambda h: h["support"] * h["reliability"] if h["reliability"] > 0 else 0)["confidence"],
        "change_conditions": {h["name"]: h["falsifier"] for h in hypotheses}
    }

    return dossier

def print_dossier(dossier):
    print("=== COLD WAR DOSSIER ===")
    print(f"\n# decision: {dossier['decision']}\n")

    print("# Source ledger:")
    for source, desc in dossier["source_ledger"].items():
        print(f"# {source}: {desc}")

    print("\n# Evidence tiers:")
    for tier, claims in dossier["evidence"].items():
        print(f"\n# {tier.upper()}:")
        for claim in claims:
            print(f"# - {claim['text']} | source={claim['source']} | reliability={claim['reliability']} | independent={claim['independent']}")

    print("\n# Competing hypotheses:")
    for h in dossier["hypotheses"]:
        print(f"# H: {h['name']} | support={h['support']} | reliability={h['reliability']} | confidence={h['confidence']}")
        print(f"#   falsifier: {h['falsifier']}")

    print(f"\n# Leading hypothesis: {dossier['leading_hypothesis']} (confidence: {dossier['leading_confidence']})")
    print("# Change conditions:")
    for name, falsifier in dossier["change_conditions"].items():
        print(f"# - {name}: {falsifier}")

dossier = build_dossier()
print_dossier(dossier)