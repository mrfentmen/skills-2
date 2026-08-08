#!/usr/bin/env python3
"""Insert persona-boundary disambiguation sentences into overlapping skill
descriptions (frontmatter at the bottom of each persona-first SKILL.md).

Run after `model_router_eval.py` found near-miss overlap pairs. Idempotent:
a skill is skipped if its sentence is already present. Only touches the
frontmatter description, never the "You are" intro (check_intro_integrity
guards that separately).

Usage:  python3 disambiguate_overlaps.py
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# skill -> disambiguation sentence (inserted right before "Triggers on:")
EDITS = {
    "hastings": (
        "This is the Reed Hastings leadership persona: engineering culture and "
        "resilience strategy, not media or ABR player engineering."
    ),
    "netflix-streaming": (
        "This is Netflix media-pipeline engineering: video players, ABR, and QoE, "
        "not the Reed Hastings leadership persona."
    ),
    "altman": (
        "This is the Sam Altman / OpenAI strategy persona for technical bets, not "
        "gambling or house-edge analysis."
    ),
    "casino-owner": (
        "This is the house-operator lens for evaluating a risky bet, not the Sam "
        "Altman strategy persona."
    ),
    "ken-thompson": (
        "This is the Ken Thompson persona: hardware skepticism, brute force, and "
        "trust nothing, not a generic do-one-thing-well composition doctrine."
    ),
    "unix": (
        "This is the Unix design doctrine: composition, pipes, and small tools, "
        "not a single-engineer persona."
    ),
    "gates": (
        "This is the Bill Gates / early-Microsoft persona: hard resource budgets "
        "and shipping on schedule, not general platform or cloud engineering."
    ),
    "bushnell": (
        "This is the Nolan Bushnell arcade-founder persona: shipping energy and "
        "simple-but-deep games, not a systems-design persona."
    ),
    "sid-meier": (
        "This is the Sid Meier systems-design persona: interesting decisions and "
        "balance, not an arcade-founder persona."
    ),
    "grace-hopper": (
        "This is the Grace Hopper quotes-and-culture persona: pragmatic shipping "
        "and questioning inherited assumptions, not a debugging-and-root-cause "
        "persona."
    ),
    "hopper": (
        "This is the Grace Hopper debugging persona: observable evidence and "
        "literal root cause, not an ask-forgiveness-and-ship persona."
    ),
    "forensic-money-trail": (
        "This is transaction forensics: reconstructing where money went and who "
        "benefits, not a special-situations investor persona."
    ),
    "jeffery-epstien": (
        "This is the special-situations investor persona: distressed claims, "
        "asset tracing, and primary-source verification, not general "
        "money-laundering forensics."
    ),
    "gordon-ramsay": (
        "This is the professional-kitchen persona: exact technique and "
        "discipline on the pass, not a joyful home-cooking teacher persona."
    ),
    "julia-child": (
        "This is the joyful home-cooking teacher persona: fundamentals, "
        "fearlessness, and a what-the-hell attitude, not a professional-kitchen "
        "discipline persona."
    ),
    "feynman": (
        "This is the Richard Feynman scientific-debugging persona: recreate the "
        "primitive and test extremes, not a first-principles engineering persona."
    ),
    "musk": (
        "This is the Elon Musk first-principles engineering persona: question "
        "every requirement and apply the five-step algorithm, not a "
        "scientific-debugging persona."
    ),
    "carmack-mode": (
        "This is the John Carmack game-engine perf persona: measure cache "
        "behavior and binary layouts, not a GPU-accelerator compute persona."
    ),
}


def main() -> None:
    changed, skipped, missing = [], [], []
    for skill, sentence in sorted(EDITS.items()):
        p = HERE / skill / "SKILL.md"
        if not p.exists():
            missing.append(skill)
            continue
        text = p.read_text(encoding="utf-8")
        if sentence.split(":")[0] in text:
            skipped.append(skill)
            continue
        # normalize the sentence to one line for folded YAML
        sent = " ".join(sentence.split())
        idx = text.rfind("Triggers on:")
        if idx == -1:
            # fallback: end of description = line before frontmatter close
            m = re.search(r"\n---\s*\n", text)
            idx = m.start() if m else len(text)
            text = text[:idx] + "\n" + sent + text[idx:]
        else:
            text = text[:idx] + sent + " " + text[idx:]
        p.write_text(text, encoding="utf-8")
        changed.append(skill)
    print(f"changed: {len(changed)} -> {sorted(changed)}")
    print(f"skipped (already present): {sorted(skipped)}")
    print(f"missing: {missing}")


if __name__ == "__main__":
    main()
