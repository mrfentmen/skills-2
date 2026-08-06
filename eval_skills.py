#!/usr/bin/env python3
"""
Static skill audit for `skills 2/`.

Scores every <skill>/SKILL.md on checkable dimensions (mirrors the sibling
repo's static_skill_audit.py approach). Writes EVAL_REPORT.md in this folder
and prints a summary. Exits nonzero if any skill scores below AUDIT_MIN_SCORE.

Usage:  python3 eval_skills.py [--min 0.75]
"""

import re
import sys
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT_MIN_SCORE = 0.75

DIMENSIONS = [
    "frontmatter",      # name: + description: present
    "triggers",         # description includes trigger phrases
    "boundaries",       # "when NOT to use" / "not for" section present
    "requirements",     # "Minimum Requirements (checkable)" with bullets
    "activation",       # persona / activation section present
    "principles",       # core principles section present
    "style",            # style guidelines section present
    "cross_language",   # cross-language examples section present
]


def parse_frontmatter(text: str):
    """Minimal YAML frontmatter parser that handles folded scalars (>-)."""
    m = re.search(r"(?:^|\n)---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data = {}
    current_key = None
    for line in m.group(1).splitlines():
        if line.startswith(" ") and current_key is not None:
            # continuation of the previous (folded) value
            data[current_key] += " " + line.strip()
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            current_key = k.strip()
            if current_key:
                data[current_key] = v.strip()
            continue
        current_key = None
    # tidy folded values (collapse repeated whitespace)
    for k in data:
        if data[k].startswith(">-") or data[k].startswith("|-"):
            data[k] = data[k][2:].strip()
    return data


def readme_triggers_missing(readme: str, name: str, skill_text: str):
    """Quoted trigger phrases in this skill's README block that are absent from
    the SKILL.md description (case-insensitive). Returns a list of phrases."""
    m = re.search(r"^#### \d+\.\s*" + re.escape(name) + r"\b(.*?)(?=^#### |^## |\Z)",
                  readme, re.S | re.M)
    if not m:
        return []
    block = m.group(1)
    # Only phrases inside the "Triggers on:" run count as triggers. The run is
    # delimited by the marker line(s); prose quotes elsewhere in the block
    # (e.g. the persona line or spec quotes) are ignored, so we must scan the
    # WHOLE block — trigger lines may legally appear after the "This skill is
    # NOT" clause.
    phrases = []
    in_run = False
    for line in block.splitlines():
        if re.search(r"riggers?\s+on:", line, re.I):
            in_run = True
        elif in_run and (not line.startswith(">") and not line.startswith(" ")
                         or "Relates to:" in line or "This skill is NOT" in line):
            # the run ends at a new heading, a paragraph break, or a marker
            # line that carries prose (Relates-to / NOT-for clauses)
            in_run = False
        if in_run:
            for t in re.findall(r'"([^"]{3,})"', line):
                # skip prose quotes that bleed in (they carry markdown markers
                # or the 'Triggers on' marker itself and are never real triggers)
                if "**" in t or "Triggers" in t or "Relates" in t:
                    continue
                phrases.append(t)
    if not phrases:
        return []
    desc = parse_frontmatter(skill_text).get("description", "").lower()
    return [t for t in phrases if t.lower() not in desc]


def audit(path: Path):
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    scores = {}

    fm = parse_frontmatter(text)
    scores["frontmatter"] = 1.0 if (fm.get("name") and fm.get("description")) else 0.0

    desc = fm.get("description", "")
    trigger_words = ["trigger", "triggers"]
    scores["triggers"] = 1.0 if any(t in desc.lower() for t in trigger_words) else 0.0

    # boundaries: a "not for" / "when NOT to use" section
    scores["boundaries"] = 1.0 if (
        "not to use" in lower or "not for" in lower
    ) else 0.0

    # requirements: bullets *inside* the Minimum Requirements section
    req_m = re.search(r"#+\s*minimum requirements.*?\n(.*?)(\n#+|\Z)", lower, re.S)
    if req_m:
        req_section = req_m.group(1)
        has_bullets = any(line.strip().startswith("-") for line in req_section.splitlines())
        scores["requirements"] = 1.0 if has_bullets else 0.0
    else:
        scores["requirements"] = 0.0

    scores["activation"] = 1.0 if re.search(r"#+.*activation", lower) else 0.0
    scores["principles"] = 1.0 if re.search(r"#+.*core principles", lower) else 0.0
    scores["style"] = 1.0 if re.search(r"#+.*style", lower) else 0.0
    scores["cross_language"] = 1.0 if re.search(r"#+.*cross.language", lower) else 0.0

    total = sum(scores.values()) / len(DIMENSIONS)
    return total, scores


def main():
    min_score = AUDIT_MIN_SCORE
    if "--min" in sys.argv:
        idx = sys.argv.index("--min")
        if idx + 1 < len(sys.argv):
            min_score = float(sys.argv[idx + 1])
        else:
            print("--min requires a value (e.g. --min 0.75)")
            return 2

    skill_files = sorted(HERE.glob("*/SKILL.md"))
    if not skill_files:
        print("No SKILL.md files found under skills 2/.")
        return 1

    results = []
    for sf in skill_files:
        total, scores = audit(sf)
        results.append((sf.parent.name, total, scores))

    # consistency pass: every skill folder appears in README.md, and the
    # frontmatter `name` matches its folder name.
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    problems = []
    drift_warnings = []
    for name, total, scores in results:
        if f"`{name}`" not in readme:
            problems.append(f"{name}: SKILL.md exists but is not referenced in README.md")
        if scores["frontmatter"] == 1.0:
            text = (HERE / name / "SKILL.md").read_text(encoding="utf-8")
            fm_name = parse_frontmatter(text).get("name")
            if fm_name != name:
                problems.append(f"{name}: frontmatter name '{fm_name}' != folder '{name}'")
        # trigger parity: every quoted trigger in the README block for this
        # skill should also appear in its SKILL.md description (catches drift
        # when only one of the two files is edited). Warnings only.
        missing = readme_triggers_missing(readme, name, text)
        for t in missing:
            drift_warnings.append(f"{name}: README trigger '{t}' not in SKILL.md description")

    # report
    report = ["# Skills 2 — Eval Report\n"]
    report.append(f"Audited **{len(results)}** SKILL.md files · min score **{min_score}**\n")
    report.append("| Skill | Overall | " + " | ".join(d.title() for d in DIMENSIONS) + " |")
    report.append("|---|---|" + "---|" * len(DIMENSIONS))
    for name, total, scores in results:
        cells = [f"{d.title()}: {scores[d]:.0%}" for d in DIMENSIONS]
        report.append(f"| {name} | **{total:.0%}** | " + " | ".join(cells) + " |")
    report.append("")

    failed = [r for r in results if r[1] < min_score]
    report.append(f"**Passed:** {len(results) - len(failed)}/{len(results)}")
    if failed:
        report.append("**Failed (below threshold):** " + ", ".join(r[0] for r in failed))
    report.append("")

    report.append("## Consistency checks")
    if problems:
        report.append("Problems found:")
        for p in problems:
            report.append(f"- {p}")
    else:
        report.append("All SKILL.md folders referenced in README; frontmatter names match folder names.")
    if drift_warnings:
        report.append("Trigger parity warnings (README vs SKILL.md, non-fatal):")
        for w in drift_warnings:
            report.append(f"- {w}")
    else:
        report.append("No trigger parity drift between README and SKILL.md files.")
    report.append("")

    (HERE / "EVAL_REPORT.md").write_text("\n".join(report), encoding="utf-8")

    # json for machine consumption
    (HERE / "EVAL_RESULTS.json").write_text(
        json.dumps(
            {name: {"overall": total, **scores} for name, total, scores in results},
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Audited {len(results)} skills. Passed: {len(results)-len(failed)}. Failed: {len(failed)}")
    for name, total, scores in results:
        mark = "PASS" if total >= min_score else "FAIL"
        print(f"  [{mark}] {name}: {total:.0%}")
    for name, total, scores in failed:
        missing = [d for d in DIMENSIONS if scores[d] == 0.0]
        print(f"    -> {name} missing: {', '.join(missing)}")
    if problems:
        print("Consistency problems:")
        for p in problems:
            print(f"  ! {p}")
    if drift_warnings:
        print(f"Trigger parity warnings: {len(drift_warnings)}")
        for w in drift_warnings[:10]:
            print(f"  ~ {w}")

    return 1 if (failed or problems) else 0


if __name__ == "__main__":
    sys.exit(main())
