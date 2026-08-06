#!/usr/bin/env python3
"""Deepen every SKILL.md Activation from its existing contract.

The catalog already has the authoritative material: identity, Core Principles,
Minimum Requirements, Style Guidelines, and boundaries. This tool composes that
material into a richer Activation without inventing biography, triggers, or
capabilities. It preserves the existing opening paragraph so identity and
README headline synchronization remain stable.

Usage:
  python3 expand_activations.py --dry-run
  python3 expand_activations.py --write
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# These are the four examples the user explicitly approved. They are intentionally
# hand-shaped because their requested persona/method distinction is important.
APPROVED = {
    "black-box": (
        "You are a black-box interrogation specialist designing algorithms under "
        "strict information-hiding constraints. You may not inspect, stringify, "
        "hash, copy, index, or reflect on the hidden value. You may learn only "
        "through an approved query interface whose answers are limited to yes, "
        "no, greater, lesser, or equal. Design the smallest sequence of questions "
        "that solves the task, state the information each question provides, stop "
        "when the answer is determined, and prove that your result depends only on "
        "the allowed answers. Never smuggle direct inspection into a helper function "
        "or disguise a read as debugging."
    ),
    "carmack-mode": (
        "You are John Carmack, pioneering game and graphics programmer known for "
        "working from hardware constraints upward. Before changing an algorithm, "
        "measure allocations, memory layout, cache behavior, data movement, frame "
        "time, and the actual bottleneck. Separate measured facts from hypotheses. "
        "Build the smallest focused implementation that improves the measured hot "
        "path, preserve correctness, and report the benchmark before and after. Do "
        "not optimize by aesthetic preference, cargo-cult folklore, or a benchmark "
        "that does not represent the workload."
    ),
    "casino": (
        "You are a probability-focused quantitative analyst. Solve the problem "
        "through meaningful randomness only when direct calculation is unavailable "
        "or would hide the uncertainty. Define the random process, sample size, "
        "estimator, confidence interval, stopping rule, and sources of bias before "
        "running the simulation. Report the estimate, uncertainty, convergence "
        "behavior, and why the result is useful. Never add Monte Carlo theatrics to "
        "a problem with a simple exact solution, and never present a simulation "
        "estimate as certainty."
    ),
    "boiler-room-research": (
        "You are Jordan Belfort on an aggressive stock-research desk, using "
        "sales-floor energy without fraud, manipulation, or guaranteed-return "
        "claims. For every company, find the narrative, catalyst, numbers that "
        "support the thesis, and facts that could kill it. Separate sourced evidence "
        "from promotional language. Deliver a hard verdict with a bull case, bear "
        "case, trigger, invalidation, time horizon, confidence level, and explicit "
        "uncertainty. The rhetoric can be fast and forceful; the research must remain "
        "honest and the user must never be told that speculation is certainty."
    ),
}


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n\s*(.*?)(?=^## |\Z)",
        text,
        re.M | re.S,
    )
    return match.group(1).strip() if match else ""


def opening_persona(text: str) -> str:
    """Top-of-file persona block: from 'You are' to the next ## heading."""
    match = re.search(r"^You are\b.*?(?=^## |\Z)", text, re.M | re.S)
    return match.group(0).strip() if match else ""


def bullets(block: str) -> list[str]:
    return [re.sub(r"^[-*]\s+", "", line.strip()) for line in block.splitlines() if line.strip().startswith(("-", "*"))]


def principles(block: str) -> list[str]:
    out = []
    for line in block.splitlines():
        match = re.match(r"\s*\d+\.\s+(.+)", line)
        if match:
            out.append(match.group(1).strip())
    return out


def trigger_vocabulary(text: str) -> list[str]:
    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not frontmatter:
        return []
    values = re.findall(r'\"([^\"]{3,})\"', frontmatter.group(1).lower())
    seen = set()
    result = []
    for value in values:
        value = re.sub(r"\s+", " ", value).strip()
        if len(value) > 80 or len(value.split()) > 8:
            continue
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result[:6]


def clean_sentence(value: str, limit: int = 220) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"^A coding skill:\s*", "", value, flags=re.I)
    value = re.sub(r"^A research skill:\s*", "", value, flags=re.I)
    value = re.sub(r"^A practical skill:\s*", "", value, flags=re.I)
    value = value.replace("**", "").replace("`", "")
    value = value.replace("?.", "?").replace("..", ".")
    if len(value) > limit:
        value = value[:limit].rsplit(" ", 1)[0] + "…"
    return value.rstrip(" .…") + "."


def existing_opening(activation: str) -> str:
    # Keep the original identity paragraph intact. This is what keeps README
    # identity headlines synchronized and makes this pass idempotent.
    return activation.split("\n\n", 1)[0].strip()


def expand_generic(name: str, text: str) -> str:
    activation = opening_persona(text)
    if not activation:
        raise ValueError(f"{name}: missing Activation section")
    opening = existing_opening(activation)
    reqs = bullets(section(text, "Minimum Requirements (checkable)"))
    princ = principles(section(text, "Core Principles"))
    styles = bullets(section(text, "Style Guidelines"))
    boundary_block = section(text, "Boundaries, when NOT to use this skill (use a different skill instead)")
    boundary = bullets(boundary_block)
    vocabulary = trigger_vocabulary(text)

    method = clean_sentence(princ[0] if princ else "follow the skill's stated contract")
    second = clean_sentence(princ[1] if len(princ) > 1 else (styles[0] if styles else "keep the result concrete and checkable"))
    req_one = clean_sentence(reqs[0] if reqs else "complete the requested task")
    req_two = clean_sentence(reqs[1] if len(reqs) > 1 else "show the reasoning or evidence behind the result")
    req_three = clean_sentence(reqs[2] if len(reqs) > 2 else "produce a real, verifiable output")
    not_for = clean_sentence(boundary[0] if boundary else "do not let the persona replace correctness")

    detail = (
        "Use a deliberate, auditable workflow. "
        f"Method: {method} {second} "
        f"Contract checks: {req_one} {req_two} {req_three} "
        f"Key vocabulary: {', '.join(vocabulary) or name}. "
        f"Boundary: {not_for}"
    )
    return opening + "\n\n" + detail


def expanded(name: str, text: str) -> str:
    return APPROVED[name] if name in APPROVED else expand_generic(name, text)


def replace_opening(text: str, value: str) -> str:
    pattern = re.compile(
        r"(^You are\b.*?)(?=^## |\Z)", re.M | re.S
    )
    match = pattern.search(text)
    if not match:
        raise ValueError("missing opening persona block")
    return text[:match.start(1)] + value + "\n\n" + text[match.end(1):].lstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.dry_run == args.write:
        parser.error("choose exactly one of --dry-run or --write")

    files = sorted(HERE.glob("*/SKILL.md"))
    previews = []
    changed = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        before = opening_persona(text)
        after = expanded(path.parent.name, text)
        if before != after:
            changed += 1
            if len(previews) < 8:
                previews.append((path.parent.name, before, after))
            if args.write:
                path.write_text(replace_opening(text, after), encoding="utf-8")

    mode = "preview" if args.dry_run else "wrote"
    print(f"{mode}: {changed}/{len(files)} opening persona blocks")
    for name, before, after in previews:
        print(f"\n--- {name} BEFORE ---\n{before}\n--- {name} AFTER ---\n{after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
