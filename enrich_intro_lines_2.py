#!/usr/bin/env python3
"""Pass-2 intro enrichment: append a buzzword-rich continuation to each
persona's first "You are" line. Append-only and idempotent - the original
text (and pass-1 extensions) are always preserved as a prefix.

Usage:
    python3 enrich_intro_lines_2.py            # apply
    python3 enrich_intro_lines_2.py --dry-run  # preview only
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    dry = "--dry-run" in sys.argv
    ext = json.loads((HERE / "intro_line_extensions_2.json").read_text(encoding="utf-8"))

    skills = sorted(p.parent.name for p in HERE.glob("*/SKILL.md"))
    missing = [s for s in skills if s not in ext]
    extra = [s for s in ext if s not in skills]
    if missing:
        print(f"WARNING: {len(missing)} skills missing an extension: {', '.join(missing)}")
    if extra:
        print(f"NOTE: {len(extra)} extensions with no matching skill: {', '.join(extra)}")

    applied = 0
    for name in skills:
        if name not in ext:
            continue
        add = ext[name]
        p = HERE / name / "SKILL.md"
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
        idx = next((i for i, l in enumerate(lines)
                    if l.strip().lower().startswith("you are")), None)
        if idx is None:
            print(f"SKIP {name}: no 'You are' line found")
            continue
        if add.strip() in lines[idx]:
            continue  # already applied
        new = lines[idx].rstrip("\n") + add + "\n"
        print(f"{name}: {lines[idx].strip()[:80]}... +{len(add.split())}w")
        if not dry:
            lines[idx] = new
            p.write_text("".join(lines), encoding="utf-8")
        applied += 1

    print(f"\n{'DRY-RUN: ' if dry else ''}{applied}/{len(skills)} skills would be / were enriched")


if __name__ == "__main__":
    main()
