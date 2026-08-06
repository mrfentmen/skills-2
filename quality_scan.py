#!/usr/bin/env python3
"""Depth scan for every SKILL.md in skills 2/.

Ranks skills by content quality so improvement passes can target the weakest
first. Scores are objective and mechanical:

  +2  frontmatter name + description present
  +2  description > 400 chars (specific, not a one-liner)
  +2  boundaries section with at least 2 bullets
  +2  >= 4 checkable minimum requirements
  +2  activation present
  +2  core principles with >= 4 numbered items
  +2  style guidelines with >= 3 bullets
  +4  a real python example block whose code has a print() and no 'pass' body
  +2  example self-contained: imports used are stdlib-only, no undefined
      obvious names (heuristic: no 'TODO' / 'Fake' / 'placeholder')
  +1  javascript example with actual code (not only a comment line)
  +1  rust example with actual code
  +2  a safety section

Max score = 24. Writes QUALITY_REPORT.md sorted weakest-first.

Usage: python3 quality_scan.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def score_skill(name: str) -> tuple[int, list[str]]:
    text = (HERE / name / "SKILL.md").read_text(encoding="utf-8")
    lower = text.lower()
    got = []

    if re.search(r"^---\nname: \S+\ndescription:", text, re.M):
        got.append("frontmatter")
    else:
        return _finish(name, got)

    m = re.search(r"^description: >-\n(.*?)^---", text, re.S | re.M)
    desc = m.group(1) if m else ""
    if len(desc.strip()) > 400:
        got.append("rich description")

    boundaries = re.search(r"#+.*when not to use.*?\n(.*?)(\n#+|\Z)", lower, re.S)
    if boundaries and sum(1 for ln in boundaries.group(1).splitlines()
                          if ln.strip().startswith("-")) >= 2:
        got.append("boundaries")

    req = re.search(r"#+.*minimum requirements.*?\n(.*?)(\n#+|\Z)", lower, re.S)
    if req and sum(1 for ln in req.group(1).splitlines()
                   if ln.strip().startswith("-")) >= 4:
        got.append(">=4 requirements")

    if re.search(r"#+.*activation", lower):
        got.append("activation")

    princ = re.search(r"#+.*core principles.*?\n(.*?)(\n#+|\Z)", lower, re.S)
    if princ and sum(1 for ln in princ.group(1).splitlines()
                     if re.match(r"\s*\d+\.", ln)) >= 4:
        got.append(">=4 principles")

    style = re.search(r"#+.*style.*?\n(.*?)(\n#+|\Z)", lower, re.S)
    if style and sum(1 for ln in style.group(1).splitlines()
                     if ln.strip().startswith("-")) >= 3:
        got.append("style bullets")

    code = 0
    py = re.search(r"```python\n(.*?)```", text, re.S)
    if py and "print(" in py.group(1) and not re.search(r"\n\s+pass\b", py.group(1)):
        got.append("real python example")
        code += 1
    if py and not re.search(r"TODO|Fake|placeholder", py.group(1), re.I):
        got.append("no placeholder markers")
        code += 1

    for lang in ("javascript", "rust"):
        b = re.search(rf"```{lang}\n(.*?)```", text, re.S)
        if not b:
            continue
        body = b.group(1).strip()
        # real code = at least one non-blank line that isn't a comment
        code_lines = [ln for ln in body.splitlines()
                      if ln.strip() and not ln.lstrip().startswith(("//", "/*", "*"))]
        if code_lines:
            got.append(f"{lang} code")

    if re.search(r"#+.*safety", lower):
        got.append("safety")

    score = {
        "frontmatter": 2, "rich description": 2, "boundaries": 2,
        ">=4 requirements": 2, "activation": 2, ">=4 principles": 2,
        "style bullets": 2, "real python example": 4, "no placeholder markers": 2,
        "javascript code": 1, "rust code": 1, "safety": 2,
    }
    return sum(score.get(g, 0) for g in got), got


def _finish(name, got):
    return 2, got + ["frontmatter only"]


def main():
    skills = sorted(p.parent.name for p in HERE.glob("*/SKILL.md"))
    rows = [(score_skill(n)[0], n) for n in skills]
    rows.sort()

    rep = ["# Skills 2 — Quality (depth) scan\n",
           f"Scored **{len(rows)}** skills, max 24.\n",
           "| Score | Skill |", "|---:|---|"]
    for score, name in rows:
        rep.append(f"| {score} | `{name}` |")
    rep.append("")
    weakest = [n for s, n in rows if s <= 12]
    rep.append(f"**Weakest (score <= 12, improvement candidates):** {', '.join(weakest) or 'none'}")

    (HERE / "QUALITY_REPORT.md").write_text("\n".join(rep), encoding="utf-8")
    print(f"Scored {len(rows)} skills.")
    print(f"  mean: {sum(s for s, _ in rows) / len(rows):.1f} / 24")
    print(f"  weakest (<=12): {weakest or 'none'}")
    print(f"  report: QUALITY_REPORT.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
