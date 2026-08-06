#!/usr/bin/env python3
"""Audit Activation identity frames and README headline consistency."""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def activation(text):
    match = re.search(r"^You are\b.*?(?=^## |\Z)", text, re.M | re.S)
    return " ".join(match.group(0).split()) if match else ""


def headings(readme):
    return {
        m.group(1): m.group(2)
        for m in re.finditer(
            r'^####\s+\d+\.\s+(.+?)\s+—\s+\*"(.*?)"\*$',
            readme, re.M
        )
    }


def main():
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    heading_map = headings(readme)
    normalized = dict(heading_map)
    if "boiler-room (research)" in normalized:
        normalized["boiler-room-research"] = normalized["boiler-room (research)"]
    problems = []
    files = sorted(HERE.glob("*/SKILL.md"))
    for path in files:
        name = path.parent.name
        text = path.read_text(encoding="utf-8")
        act = activation(text)
        if not act.startswith("You are "):
            problems.append((name, "Activation must start with 'You are'"))
        if name not in normalized:
            problems.append((name, "missing README heading"))
        # A heading must at least reproduce the complete first sentence of the
        # Activation block. Full paragraph sync is handled by the sync script.
        if name in normalized:
            first = re.split(r"(?<!\b[A-Z])(?<=[.!?])\s+", act, maxsplit=1)[0]
            if first not in normalized[name]:
                problems.append((name, "README headline does not contain Activation identity"))
    print(f"skills: {len(files)}")
    print(f"README headings: {len(heading_map)}")
    print(f"explicit You-are openings: {len(files) - sum(1 for p in problems if 'Activation' in p[1])}")
    print(f"problems: {len(problems)}")
    for name, message in problems:
        print(f"REPAIR\t{name}\t{message}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
