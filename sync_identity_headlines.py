#!/usr/bin/env python3
"""Synchronize every README skill headline with its Activation identity."""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def activation(text):
    match = re.search(r"^## Activation\s*\n\s*(.*?)(?=^## |\Z)", text, re.M | re.S)
    return " ".join(match.group(1).split()) if match else ""


def first_sentence(text):
    """Return the first sentence while handling initials such as J. Robert."""
    for match in re.finditer(r"[.!?]\s+(?=[A-Z#])", text):
        punctuation = match.start()
        before = text[:punctuation]
        token = before[before.rfind(" ") + 1:]
        if punctuation and len(token) == 1 and token.isupper():
            continue
        return text[:match.start() + 1]
    return text


def folder_for_heading(display_name):
    candidates = [display_name]
    if display_name.endswith(" (research)"):
        candidates.insert(0, display_name[:-len(" (research)")] + "-research")
    for candidate in candidates:
        if (HERE / candidate / "SKILL.md").exists():
            return candidate
    return None


readme = HERE / "README.md"
text = readme.read_text(encoding="utf-8")
headings = re.compile(r'^(####\s+\d+\.\s+)([^ —]+(?:\s+\(research\))?)(\s+—\s+\*)"([^"]*)"(\*\s*)$', re.M)
seen = set()
changed = []
missing = []

def replace(match):
    prefix, display, middle, old_quote, suffix = match.groups()
    name = folder_for_heading(display)
    if name is None:
        return match.group(0)
    seen.add(name)
    skill_text = (HERE / name / "SKILL.md").read_text(encoding="utf-8")
    identity = first_sentence(activation(skill_text))
    if not identity:
        missing.append(name)
        return match.group(0)
    if old_quote != identity:
        changed.append(name)
    return f'{prefix}{display}{middle}"{identity}"{suffix}'

text = headings.sub(replace, text)
all_skills = {p.parent.name for p in HERE.glob("*/SKILL.md")}
missing.extend(sorted(all_skills - seen))
readme.write_text(text, encoding="utf-8")
print(f"headlines synchronized: {len(set(changed))}")
print("missing or unparsed README headings:", sorted(set(missing)) or "none")
if missing:
    raise SystemExit(1)
