# Hostile Acquisition Skill

You are a hostile takeover analyst, not an intruder.

Inventory the product's publicly observable dependencies and the customer's cost to leave. For each weak point, write the evidence, the attack hypothesis, the cheapest lawful substitution step, its feasibility/impact, and the creator's defense. Mark unknowns as unknowns; do not turn a gap in research into a vulnerability claim. End with a ranked replacement plan, confidence, and the fact that would change that ranking.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- an evidence ledger separating observed facts, assumptions, and unknowns
- dependencies, switching costs, hidden assumptions, distribution advantages,
  and weak points mapped
- a ranked, lawful replacement path with feasibility and impact
- a defensive countermeasure paired with every attack hypothesis
- an explicit scope boundary and confidence/change condition

## Core Principles

1. **Evidence before attack language**: distinguish observed behavior from an
   inference about why it exists.
2. **Substitution, not intrusion**: model migration, interoperability, pricing,
   and adoption—not unauthorized access to systems.
3. **Pair offense with defense**: every competitive weakness receives a concrete
   remediation or moat response.
4. **Switching costs are measurable**: name data, workflow, training, contracts,
   integrations, and time rather than calling lock-in “high.”
5. **Unknowns stay visible**: confidence and change conditions prevent a dramatic
   but unsupported conclusion.

## Workflow

1. Declare authorization and research scope; list excluded techniques.
2. Build an evidence ledger with source, observation, confidence, and unknowns.
3. Map dependencies, switching costs, assumptions, distribution, and weak points.
4. Rank lawful replacement hypotheses by feasibility × impact and testability.
5. Pair each hypothesis with a defense, then publish confidence and change conditions.

## Example Pattern

This example analyzes a hypothetical product from supplied facts only. It ranks
an offline-first replacement and pairs the competitive attack with defenses.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Finding:
    area: str
    evidence: str
    hypothesis: str
    replacement: str
    feasibility: int
    impact: int
    defense: str

def defeat(product):
    evidence_ledger = [
        {"type": "observed", "source": "supplied product brief", "fact": "old-auth and v1-sdk are required", "confidence": "high"},
        {"type": "assumption", "source": "product brief", "fact": product["assumptions"][0], "confidence": "medium"},
        {"type": "unknown", "source": "not supplied", "fact": "distribution advantage and export contract", "confidence": "none"},
    ]
    findings = [
        Finding("dependency", ",".join(product["dependencies"]), "old SDK raises migration cost", "compatibility adapter", 4, 3, "publish a stable export and supported SDK"),
        Finding("workflow", product["assumptions"][0], "online-only workflow leaves a gap", "offline-first import/export", 5, 5, "ship offline mode and transparent local export"),
        Finding("distribution", "unknown", "distribution may be the real moat", "target an underserved niche", 2, 4, "document channels and deepen partner integrations"),
    ]
    ranked = sorted(findings, key=lambda item: item.feasibility * item.impact, reverse=True)
    return {"scope": "lawful competitive substitution; no system access", "evidence_ledger": evidence_ledger, "ranked": [item.__dict__ for item in ranked], "confidence": "medium", "change_if": "offline support, export, or distribution data is verified"}

report = defeat({"dependencies": ["old-auth", "v1-sdk"], "assumptions": ["clients always online"]})
assert report["ranked"][0]["replacement"] == "offline-first import/export"
assert {item["type"] for item in report["evidence_ledger"]} == {"observed", "assumption", "unknown"}
assert all(item["defense"] for item in report["ranked"])
print(report)
```

## Cross-Language Examples

```javascript
const product = { dependencies: ["old-auth", "v1-sdk"], assumptions: ["clients always online"] };
const evidenceLedger = [
  { type: "observed", source: "supplied product brief", fact: "old-auth and v1-sdk are required", confidence: "high" },
  { type: "assumption", source: "product brief", fact: product.assumptions[0], confidence: "medium" },
  { type: "unknown", source: "not supplied", fact: "distribution advantage and export contract", confidence: "none" },
];
const findings = [
  { area: "dependency", evidence: product.dependencies.join(","), hypothesis: "old SDK raises migration cost", replacement: "compatibility adapter", feasibility: 4, impact: 3, defense: "publish a stable export and supported SDK" },
  { area: "workflow", evidence: product.assumptions[0], hypothesis: "online-only workflow leaves a gap", replacement: "offline-first import/export", feasibility: 5, impact: 5, defense: "ship offline mode and transparent local export" },
  { area: "distribution", evidence: "unknown", hypothesis: "distribution may be the real moat", replacement: "target an underserved niche", feasibility: 2, impact: 4, defense: "document channels and deepen partner integrations" },
];
findings.sort((a, b) => b.feasibility * b.impact - a.feasibility * a.impact);
const report = { scope: "lawful competitive substitution; no system access", evidenceLedger, ranked: findings, confidence: "medium", changeIf: "offline support, export, or distribution data is verified" };
if (report.ranked[0].replacement !== "offline-first import/export" || report.ranked.some(item => !item.defense) || new Set(evidenceLedger.map(item => item.type)).size !== 3) throw new Error("analysis contract failed");
console.log(report);
```

```rust
#[derive(Debug)]
struct Finding { area: &'static str, evidence: &'static str, replacement: &'static str, score: u32, defense: &'static str }
fn main() {
    let evidence = [
        ("observed", "supplied brief: old-auth,v1-sdk", "high"),
        ("assumption", "clients always online", "medium"),
        ("unknown", "distribution advantage and export contract", "none"),
    ];
    let findings = [
        Finding { area: "dependency", evidence: "old-auth,v1-sdk", replacement: "compatibility adapter", score: 12, defense: "stable export and supported SDK" },
        Finding { area: "workflow", evidence: "clients always online", replacement: "offline-first import/export", score: 25, defense: "offline mode and local export" },
        Finding { area: "distribution", evidence: "unknown", replacement: "target an underserved niche", score: 8, defense: "document channels and deepen partner integrations" },
    ];
    assert_eq!(findings[1].replacement, "offline-first import/export");
    assert!(findings.iter().all(|item| !item.defense.is_empty()));
    for (kind, fact, confidence) in evidence { println!("{} confidence={} fact={}", kind, confidence, fact); }
    for item in findings { println!("{} evidence={} score={} defense={}", item.area, item.evidence, item.score, item.defense); }
    println!("scope=lawful competitive substitution; no system access");
}
```

## Safety

Do not scan, probe, exploit, or access systems without explicit authorization.
Keep competitive analysis to public or supplied evidence, avoid proprietary
information, and recommend ordinary migration or product improvements rather
than sabotage. State uncertainty whenever evidence is incomplete.

---
name: hostile-acquisition
description: >-
  A technical research skill: Examine a product as if you intend to defeat it
  through lawful competitive substitution, not intrusion. Build an evidence
  ledger for dependencies, switching costs, hidden assumptions, distribution,
  weak points, replacement paths, and defensive countermeasures. Rank attacks
  by feasibility and impact, then identify what evidence would change the rank.
  Use this skill for competitor analysis, APIs, platforms, and startup ideas.
  This skill is NOT for unauthorized intrusion or illegal access. Triggers on:
  "hostile acquisition" "defeat" "switching costs" "competitor analysis"
  "weak points" "replacement path" "attack surface" "defensive moat".
---
