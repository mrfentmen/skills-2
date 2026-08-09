#!/usr/bin/env python3
"""Guard: persona intros must never be rewritten — only added to.

The persona intro is the paragraph block between the `# <Persona> Skill`
title and the first `## ` heading. This check compares every SKILL.md
against the recorded baseline commit: the baseline intro must appear
verbatim inside the current intro (normalized whitespace). Prepending or
appending new identity lines is allowed; rewriting the original wording
is flagged.

Usage:  python3 check_intro_integrity.py [--baseline <commit>]
Default baseline: aa19e34 (Round 7 tip, includes the owner's intentional
intro edits to desert-island and jeffery-epstien made 2026-08-08 via the
GitHub web UI). Set BASELINE_COMMIT to override.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = sys.argv[sys.argv.index("--baseline") + 1] if "--baseline" in sys.argv \
    else "aa19e34"


def get_blob(ref: str, path: str) -> str:
    r = subprocess.run(["git", "show", f"{ref}:{path}"],
                       capture_output=True, text=True, cwd=HERE)
    return r.stdout if r.returncode == 0 else ""


def persona_para(blob: str) -> str:
    """The paragraph block from after '# Title' to the first '## ' heading."""
    lines = blob.splitlines()
    ti = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    if ti is None:
        return ""
    rest = "\n".join(lines[ti + 1:])
    idx = rest.find("\n## ")
    return rest[:idx] if idx != -1 else rest


def main() -> int:
    problems = []
    for path in sorted(HERE.glob("*/SKILL.md")):
        rel = f"{path.parent.name}/SKILL.md"
        old = persona_para(get_blob(BASELINE, rel))
        new = persona_para(path.read_text(encoding="utf-8"))
        if not old.strip():
            continue  # no baseline intro to protect (newly added skill)
        oi = " ".join(old.split())
        ni = " ".join(new.split())
        if oi not in ni:
            problems.append(rel)
    print(f"persona intros checked against {BASELINE}: "
          f"{sum(1 for p in HERE.glob('*/SKILL.md'))}")
    if problems:
        print("VIOLATIONS (intro rewritten):")
        for p in problems:
            print(f"  {p}")
        return 1
    print("intro integrity: PASS (no persona intro rewritten)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
