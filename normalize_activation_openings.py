from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def first_nonblank(lines):
    return next((i for i, line in enumerate(lines) if line.strip()), None)


def readme_identity_map():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    return {
        match.group(1): match.group(2)
        for match in re.finditer(
            r'^####\s+\d+\.\s+(.+?)\s+—\s+\*"(.*?)"\*$',
            readme,
            re.M,
        )
    }


identities = readme_identity_map()
changed = 0
for path in sorted(ROOT.glob("*/SKILL.md")):
    name = path.parent.name
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(^You are\b.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        raise ValueError(f"Missing opening persona: {path}")

    body = match.group(1)
    lines = body.splitlines()
    index = first_nonblank(lines)
    if index is None:
        raise ValueError(f"Empty Activation: {path}")
    first = lines[index].strip()

    # Already normalized: do nothing. This makes reruns safe and preserves
    # intentional paragraph formatting after the identity line.
    if first.startswith("You are ") and first.endswith("."):
        continue

    identity = identities.get(name)
    if not identity or not identity.startswith("You are ") or not identity.endswith("."):
        raise ValueError(f"Cannot derive a complete identity for {name!r}")

    # Replace only the first nonblank line. The README headline is the source
    # of truth for the complete identity sentence, including abbreviations.
    lines[index] = identity
    updated_body = "\n".join(lines) + ("\n" if body.endswith("\n") else "")
    updated = text[:match.start(1)] + updated_body + text[match.end(1):]
    path.write_text(updated, encoding="utf-8")
    changed += 1

print(f"Normalized {changed} Activation openings; existing compliant files were unchanged.")
