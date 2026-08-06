#!/usr/bin/env python3
"""
skill_cli — use the skills 2/ catalog from a terminal.

Reads every <name>/SKILL.md in this folder and composes the persona prompt for
a skill from its real frontmatter (description + triggers), Activation, and
Minimum Requirements. No mock: everything printed comes from the actual files.

Usage:
    python3 skill_cli.py list                # show the whole catalog
    python3 skill_cli.py <name>              # one-shot: print the persona prompt
    python3 skill_cli.py <name> "task..."    # one-shot with a task to fold in
    python3 skill_cli.py                     # interactive loop (/skill <name>)
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML frontmatter parser that handles folded scalars (>-)."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data = {}
    current_key = None
    for line in m.group(1).splitlines():
        if line.startswith(" ") and current_key is not None:
            data[current_key] += " " + line.strip()
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            current_key = k.strip()
            if current_key:
                data[current_key] = v.strip()
            continue
        current_key = None
    for k in data:
        if data[k].startswith(">-") or data[k].startswith("|-"):
            data[k] = data[k][2:].strip()
    return data


def section(text: str, heading: str) -> str:
    """Return the text under a ## heading up to the next heading, or ''."""
    m = re.search(rf"^##\s+{re.escape(heading)}.*?\n(.*?)(?=^##|\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def load_skills() -> dict:
    skills = {}
    for sf in sorted(HERE.glob("*/SKILL.md")):
        text = sf.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        name = fm.get("name") or sf.parent.name
        skills[name] = {
            "path": sf,
            "description": fm.get("description", ""),
            "activation": section(text, "Activation"),
            "requirements": section(text, "Minimum Requirements"),
        }
    return skills


def find(skills: dict, query: str) -> list:
    q = query.strip().lower().replace("_", "-")
    exact = q if q.startswith("/") else q
    exact = exact.lstrip("/")
    if exact in skills:
        return [exact]
    # token overlap scoring: how many of the query's words appear in the name
    qwords = set(re.findall(r"[a-z0-9]+", q))
    scored = []
    for name in skills:
        nwords = set(re.findall(r"[a-z0-9]+", name))
        overlap = len(qwords & nwords)
        if overlap:
            scored.append((overlap, -abs(len(name) - len(qwords)), name))
    scored.sort(reverse=True)
    return [n for _, _, n in scored[:3]]


def compose(name: str, skill: dict, task: str = "") -> str:
    desc = skill["description"]
    # strip the trigger run from the description for the prompt body
    desc = re.sub(r"\s*Triggers on:.*$", "", desc, flags=re.S).strip()
    lines = [f"# /skill {name}", "", f"You are operating with the **{name}** skill.", ""]
    if desc:
        lines += ["## What this skill is", "", desc, ""]
    act = skill["activation"]
    if act:
        lines += ["## Activation", "", act, ""]
    reqs = skill["requirements"]
    if reqs:
        # keep only the checkable bullets
        bullets = [ln.strip() for ln in reqs.splitlines()
                   if ln.strip().startswith("-")]
        if bullets:
            lines += ["## Checkable requirements", ""] + [f"- {b[1:].strip()}"
                                                          for b in bullets] + [""]
    if task:
        lines += ["## Your task", "", task, ""]
    return "\n".join(lines)


def cmd_list(skills: dict) -> int:
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    rows = re.findall(
        r"^\|\s*(\d+)\s*\|\s*`([a-z0-9-]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
        readme, re.M)
    if rows:
        print(f"{'#':>3}  {'skill':24s} {'type':22s} {'persona':28s} essence")
        print("-" * 110)
        for num, name, typ, persona, essence in rows:
            if name in skills:
                print(f"{num:>3}  {name:24s} {typ[:22]:22s} {persona[:28]:28s} {essence.strip()}")
        return 0
    # fallback: names only
    for name in sorted(skills):
        print(name)
    return 0


def main() -> int:
    skills = load_skills()
    args = sys.argv[1:]

    if args and args[0] in ("list", "ls", "--list"):
        return cmd_list(skills)

    if args:
        query = args[0]
        task = " ".join(args[1:])
        matches = find(skills, query)
        if not matches:
            print(f"no skill matched '{query}' (try `python3 skill_cli.py list`)")
            return 1
        name = matches[0]
        if len(matches) > 1 and matches[0] != query.strip().lstrip("/"):
            print(f"(matched {', '.join(matches)}; using {name})")
        print(compose(name, skills[name], task))
        return 0

    # interactive loop
    print("skills 2/ CLI — type a skill name, or 'list' / 'quit'.")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not line:
            continue
        if line.lower() in ("quit", "exit", "q"):
            return 0
        if line.lower() in ("list", "ls"):
            cmd_list(skills)
            continue
        task = ""
        if " " in line and "=" in line:
            # e.g. "burglar find the leaks" — everything after the name is the task
            pass
        parts = line.split(None, 1)
        query = parts[0]
        if len(parts) > 1:
            task = parts[1]
        matches = find(skills, query)
        if not matches:
            print(f"no skill matched '{query}'")
            continue
        name = matches[0]
        print(compose(name, skills[name], task))


if __name__ == "__main__":
    sys.exit(main())
