#!/usr/bin/env python3
"""Extend every skill's first 'You are' line with vivid detail + buzzwords.

Appends the continuation from intro_line_extensions.json directly onto the
first line that starts with 'You are', preserving the original words as a
prefix (the owner's goldfish/neckbeard run-on style). Special-case anchors
insert inside the line for the few files whose first line ends mid-sentence
(no-bullshit, psych).

Usage:  python3 enrich_intro_lines.py [--dry-run]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRY = "--dry-run" in sys.argv

# skills whose first 'You are' line ends mid-sentence: insert after this anchor
INSERT_AFTER = {
    "no-bullshit": "writes code that actually works.",
    "psych": "psychedelic programmer.",
}


def main() -> int:
    ext = json.loads((HERE / "intro_line_extensions.json").read_text(encoding="utf-8"))
    skills = sorted(p.parent.name for p in HERE.glob("*/SKILL.md"))

    missing = [s for s in skills if s not in ext]
    extra = [k for k in ext if k not in skills]
    if missing:
        print(f"MISSING ENTRY for {len(missing)}: {', '.join(missing[:10])}")
    if extra:
        print(f"EXTRA KEYS: {', '.join(extra[:10])}")

    done = skip = broken = 0
    for name in skills:
        p = HERE / name / "SKILL.md"
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
        idx = next((i for i, l in enumerate(lines)
                    if l.strip().lower().startswith("you are")), None)
        if idx is None:
            broken += 1
            print(f"NO YOU-ARE LINE: {name}")
            continue
        line = lines[idx]
        cont = ext.get(name)
        if not cont:
            continue
        if cont.strip() in line:
            skip += 1
            continue

        anchor = INSERT_AFTER.get(name)
        if anchor:
            pos = line.find(anchor)
            if pos == -1:
                broken += 1
                print(f"ANCHOR NOT FOUND: {name}")
                continue
            cut = pos + len(anchor)
            new_line = line[:cut] + cont + line[cut:]
        else:
            stripped = line.rstrip("\n")
            # strip trailing whitespace and a single trailing period
            body = stripped.rstrip()
            if body.endswith("."):
                body = body[:-1]
            new_line = body + cont + ("\n" if stripped.endswith("\n") else "")

        if not DRY:
            lines[idx] = new_line
            p.write_text("".join(lines), encoding="utf-8")
        done += 1

    print(f"extended={done} already={skip} broken={broken} "
          f"(dry-run={DRY}) of {len(skills)} skills")
    return 1 if missing or broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
