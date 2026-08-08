#!/usr/bin/env python3
"""Add a `## Style Guidelines` section to every skill missing one.

The catalog convention is that every skill carries a `## Style Guidelines`
section with persona-specific bullets. Skills missing it (36 at last audit)
get one derived from their own `## Core Principles`: each principle's bolded
title becomes a style directive ("Write code that embodies X: ..."), plus a
closing bullet that keeps examples real and runnable (the catalog's
no-vibes rule). If a skill has no Core Principles section, a minimal
voice-based set is used.

Idempotent: skills that already have a style heading are untouched.
"""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def extract_principle_titles(text: str) -> list[str]:
    m = re.search(r"^## Core Principles\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    if not m:
        return []
    titles = []
    for line in m.group(1).splitlines():
        mm = re.search(r"^\s*\d+\.\s+\*\*(.+?)\*\*", line)
        if mm:
            titles.append(mm.group(1).strip().rstrip("."))
    return titles


def style_block(name: str, titles: list[str]) -> str:
    lines = []
    if titles:
        for t in titles[:4]:
            lines.append(f"- Write code that embodies **{t}**; make the "
                         f"principle visible in structure and comments, not "
                         f"just claimed.")
        lines.append("- Keep every example real and runnable: no mock, fake, "
                     "or pseudo code; comments state the intent, not a "
                     "fantasy.")
    else:
        lines = [
            f"- Write in the voice of the {name.replace('-', ' ').title()} "
            f"persona: direct, consistent, and grounded in the contract.",
            f"- Name the {name.replace('-', ' ').title()} contract in comments "
            f"and code so the persona is checkable, not just claimed.",
            "- Keep every example real and runnable: no mock, fake, or pseudo "
            "code.",
        ]
    return "## Style Guidelines\n\n" + "\n".join(lines) + "\n"


def main() -> None:
    changed = 0
    skipped = 0
    for path in sorted(HERE.glob("*/SKILL.md")):
        name = path.parent.name
        text = path.read_text(encoding="utf-8")
        if re.search(r"^#{1,3}.*style", text, re.M | re.I):
            skipped += 1
            continue

        titles = extract_principle_titles(text)
        block = style_block(name, titles)

        # Insert before Cross-Language Examples, else before the bottom
        # frontmatter block, else append.
        cm = re.search(r"^## Cross-Language Examples", text, re.M)
        if cm:
            insert_at = cm.start()
        else:
            fm = re.search(r"\n---\nname: ", text)
            insert_at = fm.start() if fm else len(text)

        new_text = text[:insert_at] + block + "\n" + text[insert_at:]
        path.write_text(new_text, encoding="utf-8")
        changed += 1

    print(f"Style Guidelines added: {changed}; already present: {skipped}")


if __name__ == "__main__":
    main()
