#!/usr/bin/env python3
"""Validate the standalone contract for the no-bullshit skill."""
from pathlib import Path
import re
import sys

SKILL = 'no-bullshit'
SIGNATURES = ['inspect', 'evidence', 'verify']
root = Path(__file__).resolve().parents[1]
text = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
errors = []
if not re.search(r"^---\s*$.*?^---\s*$", text, re.MULTILINE | re.DOTALL):
    errors.append("missing frontmatter")
if not re.search(r"(?m)^name:\s*" + re.escape(SKILL) + r"\s*$", text):
    errors.append("frontmatter name mismatch")
for heading in ("Activation", "Minimum Requirements", "Cross-Language Examples", "Bundled Helpers"):
    if "## " + heading not in text:
        errors.append("missing heading: ## " + heading)
markers = (
    "shared" + "/", "evals" + "-infra" + "/", "-" + "workspace",
    "load the " + "skill", "use the " + "skill", "select another " + "skill",
)
lower = text.lower()
for marker in markers:
    if marker.lower() in lower:
        errors.append("forbidden dependency marker: " + marker)
for signature in SIGNATURES:
    if signature.lower() not in lower:
        errors.append("missing skill signature: " + signature)
if errors:
    print("FAIL " + SKILL + " contract")
    for error in errors:
        print("- " + error)
    raise SystemExit(1)
print("PASS " + SKILL + " contract")
