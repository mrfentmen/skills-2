#!/usr/bin/env python3
"""
Improvement pass: swap the first ```python example block in hand-written
persona SKILL.md files whose examples were definition-only sketches (no
print(), helpers that don't exist) with REAL, self-contained, runnable code
that actually computes and prints a result. No mock, no pseudo, no undefined
helpers — every replacement runs as written and produces visible output.

Strictly one example per skill: a real computation that demonstrates the
persona's discipline. Verify with `python3 verify_examples.py`.

Usage:  python3 improve_examples.py        (dry-run: report what would change)
        python3 improve_examples.py --write (apply changes)
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# name -> new python example body (no fences). Each must run standalone.
EXAMPLES = {
    "altman": """def expected_value(gain_prob, payoff, cost, max_downside):
    # the bet, priced: EV = p*gain - cost, with an explicit downside cap
    ev = gain_prob * payoff - cost
    return {"ev": round(ev, 2), "bet": ev > max_downside,
            "rollback": "feature flag off = old behavior"}

print(expected_value(0.6, 100, 30, 10))   # {'ev': 30.0, 'bet': True, ...}
print(expected_value(0.1, 100, 30, 10))   # {'ev': -20.0, 'bet': False, ...}""",

    "zuck": """class Experiment:
    # ship and iterate — but every change is measured before it decides anything
    def __init__(self, name, control, treatment):
        self.name = name
        self.control = control
        self.treatment = treatment
        self.shown = self.clicks = 0
    def serve(self, rollout):
        variant = self.treatment if rollout else self.control
        self.shown += 1
        self.clicks += 1 if variant else 0
        return variant
    def ctr(self):
        return round(self.clicks / self.shown, 3) if self.shown else 0.0

exp = Experiment("rank_v2", control=0, treatment=1)
for rollout in [False] * 4 + [True] * 6:
    exp.serve(rollout)
print("shown:", exp.shown, "| ctr:", exp.ctr())   # the data decides the next step""",

    "musk": """def first_principles(features):
    # question every requirement; delete before simplify, simplify before automate
    kept = []
    for f in features:
        if f.get("why") and f["cost"] < f.get("value", 0):
            kept.append(f["name"])
    return kept

features = [
    {"name": "yaml config", "why": "three flags", "cost": 5, "value": 1},
    {"name": "core parser", "why": "the input format", "cost": 2, "value": 10},
]
print(first_principles(features))  # ['core parser'] — the yaml requirement was deleted""",

    "buffett": """def owner_earnings(net_income, non_cash, maintenance_capex, wc_change):
    # Buffett's 1986 shareholder-letter formula: what the business truly earns
    return net_income + non_cash - maintenance_capex + wc_change

def evaluate(in_circle, roic_10y, oe):
    if not in_circle:
        return {"verdict": "TOO HARD"}          # outside the circle of competence
    if roic_10y < 0.15:
        return {"verdict": "NO MOAT"}           # no durable advantage
    return {"verdict": "BUY", "owner_earnings": oe}

print(evaluate(True, 0.22, owner_earnings(100, 20, 30, 5)))   # BUY, 95
print(evaluate(False, 0.22, 0))                               # TOO HARD""",

    "simons": """def edge_estimate(returns, costs_per_trade):
    # let the data speak: win rate, gross, and net after costs (costs are alpha)
    wins = sum(1 for r in returns if r > 0) / len(returns)
    gross = sum(returns) / len(returns)
    net = gross - costs_per_trade
    return {"win_rate": round(wins, 2), "net": round(net, 4),
            "actionable": net > 0 and wins > 0.5}

print(edge_estimate([0.001, -0.0005, 0.002, 0.0008, 0.0012], 0.0004))
# the model decides; no human override within limits""",

    "dalio": """def risk_parity(vols):
    # dalio: each asset carries equal RISK, not equal capital
    inv = [1 / v for v in vols]
    total = sum(inv)
    return [round(w / total, 3) for w in inv]

print(risk_parity([0.15, 0.25, 0.05]))  # calm assets get more capital
print(sum(risk_parity([0.15, 0.25, 0.05])))  # weights sum to 1.0""",

    "crypto-market-maker": """def quote(mid, spread, inventory_skew):
    # skew quotes by inventory: sell what you hold too much of
    bid = mid - spread / 2 - inventory_skew
    ask = mid + spread / 2 - inventory_skew
    return {"bid": round(bid, 2), "ask": round(ask, 2)}

print(quote(100.0, 0.20, 0.05))    # long inventory -> quotes pushed down
print(quote(100.0, 0.20, -0.05))   # short inventory -> quotes pulled up""",

    "google-sre": """def budget_status(requests, errors, error_budget=0.001):
    # 99.9% SLO -> 0.1% error budget per window; spend it like currency
    rate = errors / requests if requests else 0.0
    return {"error_rate": round(rate, 5),
            "budget_remaining": round(error_budget - rate, 5),
            "deploy_allowed": rate < error_budget}

print(budget_status(1_000_000, 200))     # within budget: releases allowed
print(budget_status(1_000_000, 2_000))   # budget blown: freeze releases""",

    "hastings": """import random

def chaos_test(instances, kill_prob):
    # kill instances on purpose; the service must degrade, never die
    killed = [h for h in instances if random.random() < kill_prob]
    survivors = [h for h in instances if h not in killed]
    return {"killed": len(killed), "survivors": len(survivors),
            "degraded_not_down": len(survivors) > 0}

print(chaos_test(list(range(10)), 0.2))   # survivable by design, not by luck""",

    "hopper": """def moth_hunt(stages, failing_at):
    # the first stage whose output is wrong is where the moth lives
    for i, stage in enumerate(stages):
        if stage == failing_at:
            return f"moth in {stage} (stage {i + 1})"
    return "moth is in the input"

print(moth_hunt(["parse", "transform", "enrich", "render"], "transform"))""",

    "huang": """def bytes_moved(rows, cols, dtype_bytes):
    # name the data movement first: that is the real cost
    return rows * cols * dtype_bytes

def coalesced_sum(data, block):
    # walk memory in contiguous blocks, not one strided element at a time
    return sum(sum(data[i:i + block]) for i in range(0, len(data), block))

print("bytes moved:", bytes_moved(4096, 4096, 4))
print("sum ok:", coalesced_sum(list(range(1000)), block=64))""",

    "jobs": """def focus_scope(features, hard_cut):
    # say no: every feature earns its place or is cut
    kept = [f for f in features if f["value"] >= hard_cut]
    return {"kept": [f["name"] for f in kept],
            "cut": [f["name"] for f in features if f not in kept]}

features = [
    {"name": "search", "value": 9},
    {"name": "themes", "value": 2},
    {"name": "sync", "value": 8},
]
print(focus_scope(features, hard_cut=5))  # keep search + sync; themes is cut""",

    "knuth": """def power(base, exp):
    # invariant: result * base**exp == base**original at every step
    result = 1
    while exp:
        if exp % 2:
            result *= base
        base *= base
        exp //= 2
    return result

print(power(2, 10))  # 1024 — and the invariant is stated, not implied""",

    "meta-senior-dev": """def land_stack(stack, callers):
    # monorepo: change the API and every caller lands in the same commit
    updated = []
    for api in stack:
        touched = [c for c in callers if api in c]
        updated.append((api, len(touched)))
    return updated

callers = ["search/use_rank_v2", "feed/use_rank_v2", "ads/use_rank_v1"]
print(land_stack(["rank_v2"], callers))  # [('rank_v2', 2)] — no broken contract""",

    "military-general": """def campaign(terrain, forces, enemy, objective):
    # the strategic picture before any action: terrain, forces, enemy, plan, fallback
    risk = sum(enemy.values()) / max(1, sum(forces.values()))
    plan = "attack the flank" if risk < 1.2 else "hold and reinforce"
    return {"objective": objective, "terrain": terrain, "risk": round(risk, 2),
            "plan": plan, "fallback": "retreat to a prepared position"}

print(campaign("narrow pass", {"infantry": 50, "tanks": 10},
               {"mines": 20, "snipers": 5}, "secure the pass"))""",

    "neckbeard": """def parse_ints(text):
    # no regex, no classes, no framework. a loop. like god intended.
    out = []
    cur = ""
    for ch in text + ",":
        if ch.isdigit():
            cur += ch
        elif cur:
            out.append(int(cur))
            cur = ""
    return out

print(parse_ints("12 cats, 3 dogs, 99 problems"))  # [12, 3, 99]""",

    "fedora-hat-guy": """def big_chungus_buffer(data, chunk=3):
    # ok here we go, this is the tricky part — chunk it up, champ
    return [data[i:i + chunk] for i in range(0, len(data), chunk)]

print(big_chungus_buffer([1, 2, 3, 4, 5, 6, 7]))
# [[1, 2, 3], [4, 5, 6], [7]] — see? you've got this.""",

    "spacex-fsw": """def vote(a, b, c):
    # three computers, one answer: 2-of-3 majority wins, dissent is logged
    counts = {}
    for x in (a, b, c):
        counts[x] = counts.get(x, 0) + 1
    winner = max(counts, key=counts.get)
    return {"winner": winner, "agreement": counts[winner] >= 2}

print(vote(1.0, 1.0, 1.0))   # perfect agreement
print(vote(1.0, 1.0, 0.5))   # 2-of-3: the outlier is masked
print(vote(1.0, 0.5, 0.5))   # 2-of-3 the other way: logged and acted on""",

    "bezo": """def work_backward(customer_need, features):
    # start from the customer and work backward: cut what they never asked for
    return [f for f in features if f in customer_need]

print(work_backward("fast checkout",
                    ["fast checkout", "admin theming", "analytics"]))""",

    "miyamoto": """def multiple_problems(idea, problems_solved):
    return {"idea": idea, "problems_solved": problems_solved,
            "keep": len(problems_solved) >= 2}    # one idea, many wins

def fun_gate(playtest_score, budget):
    if playtest_score < 0.6:
        return {"action": "upend the tea table", "why": "fun failed the gate",
                "sunk_cost": f"{budget} spent, discarded anyway"}
    return {"action": "ship", "why": "fun passed with simple mockup art"}

print(multiple_problems("super mushroom", ["telegraph power", "health buffer",
                                           "low-res readable"]))
print(fun_gate(0.8, 40_000))""",
}


def swap_first_python_block(text: str, new_body: str) -> str:
    """Replace the first ```python ... ``` block in SKILL.md text."""
    start = text.find("```python")
    if start == -1:
        return None
    end = text.find("```", start + len("```python"))
    if end == -1:
        return None
    return text[:start] + "```python\n" + new_body + "\n```" + text[end + 3:]


def main():
    write = "--write" in sys.argv
    changed = []
    for name, body in sorted(EXAMPLES.items()):
        path = HERE / name / "SKILL.md"
        if not path.exists():
            print(f"  MISSING SKILL.md: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        new_text = swap_first_python_block(text, body)
        if new_text is None or new_text == text:
            print(f"  NO CHANGE: {name}")
            continue
        changed.append(name)
        if write:
            path.write_text(new_text, encoding="utf-8")
    print(f"{len(changed)} examples ready for swap: {', '.join(changed)}")
    if not write:
        print("dry-run: pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
