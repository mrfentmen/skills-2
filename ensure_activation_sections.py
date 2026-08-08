#!/usr/bin/env python3
"""Add the catalog-standard `## Activation` section to every skill missing it.

The newer persona skills (psych, terry-davis, god, ...) ship an explicit
`## Activation` section stating when the persona activates. Most of the
older catalog skills predate that convention, so eval_skills flags them.
This repair derives the persona from each skill's `# <Persona> Skill`
title and the `You are ...` opening, then inserts a standard activation
block right before the `## Boundaries` heading (the established position).

Idempotent: skills that already have an activation heading are untouched.
"""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def derive_persona(name: str, text: str) -> str:
    """Persona label for the activation sentence."""
    m = re.search(r"^# (.+?) Skill\s*$", text, re.M)
    if m:
        return m.group(1).strip()
    # fall back to the folder name, title-cased
    return name.replace("-", " ").title()


def activation_block(persona: str) -> str:
    return (
        "## Activation\n"
        "\n"
        f"Activate this skill only when the user explicitly requests the "
        f"{persona} persona, the {persona} way of working, or a task that "
        f"matches the form, structural contract, or identity described "
        f"above. Generic coding, production, artistic, or algorithmic "
        f"requests do not activate it without that explicit identity or "
        f"contract match.\n"
    )


def main() -> None:
    changed = 0
    skipped = 0
    for path in sorted(HERE.glob("*/SKILL.md")):
        name = path.parent.name
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        if re.search(r"^#{1,3}.*activation", lower, re.M):
            skipped += 1
            continue

        persona = derive_persona(name, text)
        block = activation_block(persona)

        # Insert before the first Boundaries heading if present, else append
        # before the frontmatter at the bottom of the file.
        bm = re.search(r"^## .*when NOT to use|^## .*Boundaries", text, re.M)
        if bm:
            insert_at = bm.start()
        else:
            fm = re.search(r"\n---\nname: ", text)
            insert_at = fm.start() if fm else len(text)

        new_text = text[:insert_at] + block + "\n" + text[insert_at:]
        path.write_text(new_text, encoding="utf-8")
        changed += 1

    print(f"Activation sections added: {changed}; already present: {skipped}")


if __name__ == "__main__":
    main()
