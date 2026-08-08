#!/usr/bin/env python3
"""Audit Activation identity frames and README headline consistency."""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def activation(text):
    match = re.search(r"^You are\b.*?(?=^## |\Z)", text, re.M | re.S)
    return " ".join(match.group(0).split()) if match else ""


def linked_names(readme):
    """Skill folder names referenced by a README table link (`[name](./name)`)."""
    names = set()
    for m in re.finditer(r"\[`?([^`\]]+)`?\]\(\./([^)]+)\)", readme):
        label, target = m.group(1).strip(), m.group(2).strip().rstrip("/")
        names.add(target)
        names.add(label)
    return names


def main():
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    linked = linked_names(readme)
    problems = []
    files = sorted(HERE.glob("*/SKILL.md"))
    for path in files:
        name = path.parent.name
        text = path.read_text(encoding="utf-8")
        act = activation(text)
        if not act.startswith("You are "):
            problems.append((name, "opening must start with 'You are'"))
        if name not in linked:
            problems.append((name, "missing README table link"))
    print(f"skills: {len(files)}")
    print(f"explicit You-are openings: {sum(1 for p in files if activation(p.read_text(encoding='utf-8')).startswith('You are '))}")
    print(f"README table links: {len(linked)}")
    print(f"problems: {len(problems)}")
    for name, message in problems:
        print(f"REPAIR\t{name}\t{message}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
