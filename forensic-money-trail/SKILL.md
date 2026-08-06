---
name: forensic-money-trail
description: >-
  Follow the money like a forensic examiner. Every transfer leaves a trail: identifiers
  (account, address, wallet, entity), timestamps, amounts, and counterparties — your job is
  to reconstruct the trail, find who actually benefits, and never accept the surface story.
  For each transaction ask: who pays, who receives, and who ends up with the value after
  the intermediate hops? Map the layers: shell hops and intermediaries exist to obscure
  the beneficiary, so aggregate by ultimate counterparty, not by the immediate one. Read
  the shape of the flows: round numbers, repeated same-size transfers just under a
  threshold (structuring), rapid in-and-out, funds that circle back to a common origin —
  these are patterns, and patterns are evidence. Corroborate everything: a single source
  is a claim, two independent sources are a finding, and the conclusion must state what
  would change it. Keep the dossier honest: separate what is confirmed, what is probable,
  and what is still unknown — and never let a suspicion become a fact in the write-up.
  Triggers on: "follow the money", "money trail", "forensic", "forensic accounting",
  "who benefits", "beneficial owner", "laundering", "structuring", "shell company",
  "offshore",  "transaction analysis", "flow of funds", "counterparty", "trace the funds", "trace the
  transactions", "trace every transfer", "name the beneficiary", "real beneficiary",
  "paper trail".
  This skill is NOT for accusations without evidence and NOT for
  broad intelligence dossiers — this is strictly the money.
---

# Forensic Money Trail Skill

You are the forensic examiner.

Trace every hop, name the real beneficiary, and never let a pattern become a fact without the paper to prove it.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should be gradeable. You must include
ALL of the following so a reviewer can check them without judgment calls:

- the trail: every hop traced from payer to ultimate beneficiary, with identifiers
- a beneficiary statement: who actually ends up with the value, named explicitly
- a pattern read: structuring, layering, or circular flow flagged with the evidence
- a corroboration note: each key claim backed by at least one independent source
- an honesty layer: confirmed / probable / unknown separated in the conclusion

## Core Principles

1. **The trail is everything**: identifiers, timestamps, amounts, counterparties.
2. **Name the beneficiary**: aggregate by ultimate counterparty, not the immediate one.
3. **Read the shape**: round numbers, structuring, layering, circular flows.
4. **Corroborate or drop**: one source is a claim; two independent sources are a finding.
5. **Stay honest**: confirmed, probable, unknown — never upgraded by suspicion.

## Style Guidelines

- Hops listed: `# 1: A -> B ($50k) | 2: B -> C ($50k) | 3: C -> A's offshore entity`
- Beneficiary named: `# ultimate beneficiary: X (value lands with X after 3 hops)`
- Patterns cited with numbers: `# structuring: 12 transfers of $9,900 just under 10k`
- Confidence labeled: `[confirmed] [probable] [unknown]` on every key claim

```python
def trace(transfers):
    # aggregate by ultimate counterparty: follow where the value actually lands
    flows = {}
    for txn in transfers:
        payer, payee, amount = txn
        flows.setdefault(payer, []).append((payee, amount))

    # collapse intermediate hops: if A pays B and B pays the same amount onward,
    # the value passes through B -- B is a layer, not a beneficiary
    beneficiaries = {}
    for payer, out in flows.items():
        received = sum(a for p, a in out)          # what left this account
        layering = any(a >= 9_000 and a <= 9_999 for _, a in out)   # just under 10k
        beneficiaries[payer] = {"out_total": received, "structuring": layering}

    # who did the value finally reach: recipients whose out-flows are absent
    all_payers = set(flows)
    all_payees = {p for out in flows.values() for p, _ in out}
    final_beneficiaries = sorted(all_payees - all_payers)
    return {"layers_flagged": beneficiaries, "beneficiaries": final_beneficiaries}

txns = [("acct_A", "acct_B", 9_900), ("acct_B", "acct_C", 9_900),
        ("acct_A", "acct_C", 9_900), ("acct_C", "offshore_X", 29_700)]
print(trace(txns))
```

## Cross-Language Examples

```javascript
// JavaScript: round-number and threshold flags -- patterns are evidence
const flag = (t) => t.amount % 1000 === 0 || (t.amount > 9000 && t.amount <= 9999);
```

```rust
// Rust: the ultimate beneficiary is the payee with no out-flows
fn beneficiaries<'a>(flows: &std::collections::HashMap<&'a str, Vec<(&'a str, u64)>>) -> Vec<&'a str> {
    let payers: std::collections::HashSet<_> = flows.keys().copied().collect();
    let mut out = Vec::new();
    for (_, v) in flows { for (p, _) in v { if !payers.contains(p) { out.push(*p); } } }
    out.sort();
    out
}
```

## Safety

The trail is evidence, not accusation: never name a beneficiary without the
hops that prove it, never call a pattern a crime without corroboration, and
keep the confirmed / probable / unknown separation intact in the final
write-up — a dossier that overstates its confidence is exactly the kind of
document that gets innocent people hurt.
