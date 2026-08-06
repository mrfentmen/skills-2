from pathlib import Path

ROOT = Path(__file__).resolve().parent

BOUNDARY_HEADING = "## Boundaries, when NOT to use this skill (use a different skill instead)"
BOUNDARY_HEADING_NEW = "## Boundaries and Scope"
BOUNDARY_SENTENCE = (
    "Keep this skill self-contained: do not invoke, load, or require another skill. "
    "If the requested work does not fit this skill's stated contract, say so plainly "
    "and use an ordinary implementation approach without routing the request elsewhere."
)
BOUNDARY_SENTENCE_NEW = (
    "Keep this skill self-contained. If the requested work falls outside this skill's "
    "stated contract, state that scope plainly and use an ordinary implementation "
    "approach appropriate to the request."
)

REPLACEMENTS = {
    "This skill is NOT for recipe instruction (use gordon-ramsay), NOT for":
        "This skill is NOT for recipe instruction, NOT for",
    "This skill is NOT for finding restaurants (use\nanthony-bourdain) and NOT for":
        "This skill is NOT for finding restaurants and NOT for",
    "This skill is NOT for finding restaurants (use anthony-bourdain) and NOT for":
        "This skill is NOT for finding restaurants and NOT for",
    "the cold-war skill's broader intelligence dossiers":
        "broad intelligence dossiers",
    "failure is expensive, use margaret-hamilton or proof-carrying instead.":
        "failure is expensive; use a plain, contract-first failure analysis instead.",
    "Boundary: remain within this skill's own contract; do not route to another skill.":
        "Boundary: remain within this skill's own contract; do not expand beyond its stated scope.",
    "**Zero-copy is not zero-work**":
        "**No-copy mutation is not no-work**",
}

changed = []
for path in sorted(ROOT.glob("*/SKILL.md")):
    original = path.read_text(encoding="utf-8")
    text = original.replace(BOUNDARY_HEADING, BOUNDARY_HEADING_NEW)
    text = text.replace(BOUNDARY_SENTENCE, BOUNDARY_SENTENCE_NEW)
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(path.parent.name)

print(f"updated {len(changed)} skills")
print(" ".join(changed))
