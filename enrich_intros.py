#!/usr/bin/env python3
"""Append-only intro enrichment for all 180 skills.

Inserts the curated paragraph from intro_enrichments.json at the END of the
persona block (right before the first '## ' heading). Never rewrites or edits
existing text, so the intro-integrity baseline stays a verbatim substring.

Usage:  python3 enrich_intros.py [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRY = "--dry-run" in sys.argv


def main() -> int:
    enrich = json.loads((HERE / "intro_enrichments.json").read_text(encoding="utf-8"))
    skills = sorted(p.parent.name for p in HERE.glob("*/SKILL.md"))

    missing = [s for s in skills if s not in enrich]
    extra = [k for k in enrich if k not in skills]
    if missing:
        print(f"MISSING ENTRY for {len(missing)} skills: {', '.join(missing[:10])}")
    if extra:
        print(f"EXTRA KEYS not in folder: {', '.join(extra[:10])}")

    done = skip = no_heading = 0
    for name in skills:
        p = HERE / name / "SKILL.md"
        text = p.read_text(encoding="utf-8")
        para = enrich.get(name)
        if not para:
            continue
        if para in text:
            skip += 1
            continue
        m = re.search(r"\n## ", text)
        if not m:
            no_heading += 1
            print(f"NO HEADING: {name}")
            continue
        idx = m.start()
        new = text[:idx] + "\n\n" + para + text[idx:]
        if not DRY:
            p.write_text(new, encoding="utf-8")
        done += 1

    print(f"enriched={done} already={skip} no_heading={no_heading} "
          f"(dry-run={DRY}) of {len(skills)} skills")
    return 1 if missing or no_heading else 0


if __name__ == "__main__":
    raise SystemExit(main())
