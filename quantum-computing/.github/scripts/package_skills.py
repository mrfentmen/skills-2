#!/usr/bin/env python3
"""
Package skill(s) into a distributable .skill file (zip containing the
skill directory) under dist/.

Works in BOTH layouts:
  - monorepo: packages every skill dir -> dist/<name>.skill
  - single:   SKILL.md at the repo root (a per-skill repo, e.g. a GitHub
              Actions repackage) -> dist/<repo-name>.skill

Usage:  python3 package_skills.py [--target .agents/skills]
"""
import sys
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
# Layout-aware repo root (disambiguated by the script's directory name):
#   monorepo:       <root>/package_skills.py                     -> parent
#   per-skill repo: <root>/.github/scripts/package_skills.py     -> parent.parent
if SCRIPT_DIR.name == "scripts" and (SCRIPT_DIR.parent.parent / "SKILL.md").exists():
    BASE = SCRIPT_DIR.parent.parent
elif any(d.is_dir() and (d / "SKILL.md").exists()
         for d in SCRIPT_DIR.iterdir()):
    BASE = SCRIPT_DIR  # the script lives at the monorepo root itself
else:
    BASE = SCRIPT_DIR.parent
if (BASE / "SKILL.md").exists():
    SKILL_DIRS = [BASE]  # per-skill repo mode
else:
    SKILL_DIRS = sorted(
        d for d in BASE.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
        and not d.name.endswith("-workspace")
    )


EXCLUDE_DIR_PARTS = {".github", "dist", "__pycache__"}


def package(skill_dir: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"{skill_dir.name}.skill"
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(skill_dir.rglob("*")):
            rel = f.relative_to(skill_dir)
            if not f.is_file() or f.name.endswith((".backup", ".backup2", ".pyc")):
                continue
            if rel.name == "SKILL_AUDIT.json":
                continue
            if any(part in EXCLUDE_DIR_PARTS for part in rel.parts):
                continue  # CI machinery + build output never ships in the skill
            zf.write(f, arcname=f"{skill_dir.name}/{rel}")
    return dest


def main() -> None:
    target = "dist"
    if len(sys.argv) > 1 and sys.argv[1] == "--target":
        target = sys.argv[2]
    out_dir = BASE / target
    for d in SKILL_DIRS:
        dest = package(d, out_dir)
        print(f"packaged {d.name} -> {dest.relative_to(BASE)}")
    print(f"Packaged {len(SKILL_DIRS)} skills into {out_dir.relative_to(BASE)}/")


if __name__ == "__main__":
    main()
