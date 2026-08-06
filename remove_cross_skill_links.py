from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
skill_names = sorted((p.parent.name for p in ROOT.glob("*/SKILL.md")), key=len, reverse=True)
name_alt = "|".join(re.escape(name) for name in skill_names)


def remove_boundary_sections(text: str) -> str:
    # Preserve the heading and replace routing bullets with a local boundary.
    pattern = r"(\n## Boundaries, when NOT to use this skill \(use a different skill instead\)\n).*?(?=\n## |\Z)"
    replacement = r"\1\nKeep this skill self-contained: do not invoke, load, or require another skill. If the requested work does not fit this skill's stated contract, say so plainly and use an ordinary implementation approach without routing the request elsewhere.\n"
    return re.sub(pattern, replacement, text, flags=re.S)


def remove_relation_blocks(text: str) -> str:
    # Relation labels are advisory linking, not skill behavior. Remove the
    # recommendation through the next sentence/section while preserving local prose.
    text = re.sub(r"(?:\*\*Relates to:\*\*|\bBuilds on:).*?(?=This skill is NOT|This skill is \*\*NOT|\n####|\n\n|\Z)", "", text, flags=re.S)
    text = re.sub(r"\*\*Relates\s*\n.*?(?=This skill is NOT|This skill is \*\*NOT|\n####|\n\n|\Z)", "", text, flags=re.S)
    return text


def restore_boundary(text: str) -> str:
    if "## Minimum Requirements (checkable)" not in text or "## Boundaries, when NOT to use this skill" in text:
        return text
    marker = "## Minimum Requirements (checkable)"
    boundary = ("## Boundaries, when NOT to use this skill\n\n"
                "Keep this skill self-contained: do not invoke, load, or require another skill. "
                "If the requested work does not fit this skill's stated contract, say so plainly "
                "and use an ordinary implementation approach without routing the request elsewhere.\n\n")
    return text.replace(marker, boundary + marker, 1)


def remove_skill_reference_lines(text: str) -> str:
    lines = []
    for line in text.splitlines():
        # Outside the catalog's identity table/headings, a backticked skill name
        # is a direct cross-skill reference. Remove the whole advisory line.
        if re.search(rf"`(?:{name_alt})`", line):
            if not line.startswith("| ") and not line.startswith("#### "):
                line = re.sub(rf"`(?:{name_alt})`", "the relevant contract", line)
        # These are direct routing/recommendation lines. Keep ordinary code arrows.
        if re.search(rf"->\s*(?:{name_alt})(?:\b|\s|$)", line):
            continue
        lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def clean_file(path: Path, is_readme: bool = False) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original
    if not is_readme:
        text = remove_boundary_sections(text)
    text = remove_relation_blocks(text)
    if not is_readme:
        text = remove_skill_reference_lines(text)
        text = re.sub(r"^.*Boundary:.*$", "Boundary: remain within this skill's own contract; do not route to another skill.", text, flags=re.M)
        text = restore_boundary(text)
    # Remove empty advisory headings/spacing left by the mechanical pass.
    text = re.sub(r"\n{3,}", "\n\n", text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


changed = 0
for path in sorted(ROOT.glob("*/SKILL.md")):
    changed += clean_file(path)
changed += clean_file(ROOT / "README.md", is_readme=True)
print(f"Changed {changed} files; removed cross-skill advisory links.")
