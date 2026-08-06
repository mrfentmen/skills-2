#!/usr/bin/env python3
"""
Static audit of every skill's SKILL.md. Scores 8 objective dimensions so we
can measure improvement across the enhancement pass:

  1. valid_frontmatter   - name + description present
  2. description_rich    - description >= 200 chars (trigger-ability)
  3. code_examples       - contains at least one code block
  4. language_coverage   - distinct languages/``` tags seen (expect >= 2 after item 5)
  5. theme_self_consistency - SKILL.md mentions its own theme keywords (from evals)
  6. success_criteria    - has an explicit checkable "requirements" section
  7. boundaries          - has a "not for / use X instead" boundary line
  8. bundled_scripts     - references shared/ helpers or has scripts/ dir
  9. no_mock_code        - explicitly bans mock / fake / pseudo code (real
                          runnable output only, in the checkable section)

Works in BOTH layouts:
  - monorepo:  skills/<name>/SKILL.md  (scans all skill dirs)
  - single:    SKILL.md at the repo root (a per-skill repo, e.g. a GitHub
               Actions check where the repo IS one skill)

Usage:
  python3 evals-infra/static_skill_audit.py [--json]
  python3 evals-infra/static_skill_audit.py --min-score 0.75   # exit 1 below
  (--min-score can be combined with --json)
"""
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
# Layout-aware repo root (disambiguated by the script's directory name):
#   monorepo:       <root>/evals-infra/static_skill_audit.py   -> parent
#   per-skill repo: <root>/.github/scripts/static_skill_audit.py -> parent.parent
if SCRIPT_DIR.name == "scripts" and (SCRIPT_DIR.parent.parent / "SKILL.md").exists():
    BASE = SCRIPT_DIR.parent.parent
else:
    BASE = SCRIPT_DIR.parent

THEME_KEYWORDS = {
    "terry-davis": ["god", "temple", "holy", "divine", "sacred", "goto", "asm"],
    "psych": ["psychedelic", "fractal", "trippy", "consciousness", "mind-bending", "hallucinat"],
    "no-bullshit": ["bullshit", "reality", "inspect", "verify", "honest", "production"],
    "smoker": ["smoke", "verify", "test", "inspect", "pretend", "checked"],
    "retro-computing": ["sprite", "chip", "memory", "palette", "sid", "8-bit", "commodore", "dos", "pixel"],
    "mathematical-elegance": ["proof", "elegant", "theorem", "invariant", "mathematical", "elegance"],
    "minimalist-zen": ["zen", "minimal", "breath", "meditat", "empty", "stillness", "simplicity"],
    "artistic-creative": ["generative", "art", "beautiful", "aesthetic", "canvas", "palette", "render"],
    "quantum-computing": ["qubit", "superposition", "entangle", "amplitude", "hadamard", "quantum", "measure"],
    "esoteric-programming": ["brainfuck", "befunge", "malbolge", "golf", "quine", "obfusc", "esolang"],
    "biomimicry": ["evolution", "selection", "mutation", "crossover", "swarm", "flock", "pheromone", "organism"],
    "glitch-art": ["glitch", "pixel", "sort", "corrupt", "scanline", "datamosh", "artifact", "noise"],
    "steampunk": ["gear", "brass", "steam", "victorian", "babbage", "clockwork", "analytical", "copper"],
    "cosmic-horror": ["sanity", "madness", "eldritch", "cosmic", "abyss", "lovecraft", "dread", "unknowable"],
    "renaissance": ["golden", "ratio", "proportion", "perspective", "vitruvian", "da vinci", "classical", "fibonacci"],
    "zen-calligraphy": ["brush", "ink", "stroke", "haiku", "zen", "breath", "wabi", "sumi", "garden"],
    "haiku": ["haiku", "5-7-5", "token", "kigo", "dense", "turn", "moment", "three lines", "no boilerplate"],
    "tanka": ["tanka", "5-7-5-7-7", "expand", "reflection", "five lines", "second view", "deeper"],
    "senryu": ["senryu", "human", "humor", "funny", "quirk", "punchline", "people"],
    "lunes": ["lunes", "5-3-5", "punch", "short middle", "american", "strike"],
    "haibun": ["haibun", "prose", "narrative", "story", "walk", "journey", "ending"],
    "sedoka": ["sedoka", "stanza", "mirror", "response", "question", "echo"],
    "katauta": ["katauta", "5-7-7", "half", "addressed", "fragment", "falling"],
    "gogyohka": ["gogyohka", "five-line", "free", "breath", "phrase", "meter"],
    "monoku": ["monoku", "one-line", "single line", "breath", "extreme", "semicolon"],
    "sijo": ["sijo", "twist", "volta", "korean", "surprise", "reframe"],
    "choka": ["choka", "couplet", "alternating", "long", "verse", "meter"],
    "dodoitsu": ["dodoitsu", "folk", "7-7-7-5", "landing", "four lines", "settle"],
    "renga": ["renga", "stanza", "linked", "pivot", "hokku", "chain"],
}

LANG_MARKERS = {
    "python": ["```python", "```py"],
    "javascript/typescript": ["```javascript", "```js", "```typescript", "```ts", "```node"],
    "rust": ["```rust"],
    "c/c++": ["```c\n", "```cpp", "```c++"],
    "go": ["```go"],
    "bash": ["```bash", "```sh"],
}


def audit_skill(skill: str, path: Path | None = None) -> dict:
    path = path or (BASE / skill / "SKILL.md")
    result = {"skill": skill, "checks": {}, "langs": []}
    if not path.exists():
        result["checks"] = {"missing": True}
        return result
    text = path.read_text(errors="ignore")
    lower = text.lower()

    m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    fm = m.group(1) if m else ""
    has_name = bool(re.search(r"(?m)^name\s*:", fm))
    has_desc = bool(re.search(r"(?m)^description\s*:", fm))
    result["checks"]["valid_frontmatter"] = has_name and has_desc

    desc_parts, in_desc = [], False
    for line in fm.split("\n"):
        stripped = line.strip()
        if stripped.startswith("description:"):
            in_desc = True
            continue
        if in_desc:
            if line.startswith("  ") or stripped == "":
                desc_parts.append(stripped)
            else:
                break
    desc_text = " ".join(p for p in desc_parts if p)
    result["checks"]["description_rich"] = len(desc_text) >= 200

    blocks = re.findall(r"```(\w+)", text)
    result["langs"] = sorted(set(blocks))
    result["checks"]["code_examples"] = len(blocks) > 0
    covered = {lang for lang, markers in LANG_MARKERS.items()
               if any(mk in lower for mk in markers)}
    result["checks"]["language_coverage"] = len(covered) >= 2

    kws = THEME_KEYWORDS.get(skill, [])
    hit = sum(1 for k in kws if k in lower)
    result["checks"]["theme_self_consistency"] = hit >= 3
    result["theme_hits"] = hit

    result["checks"]["success_criteria"] = any(
        s in lower for s in ["checkable", "success criteria", "required elements",
                             "minimum requirements", "you must include"])
    result["checks"]["boundaries"] = any(
        s in lower for s in ["not for", "use instead", "if you want", "does not cover",
                             "better fit", "instead use", "see the"])
    result["checks"]["bundled_scripts"] = ("shared/" in lower
                                           or (BASE / skill / "scripts").exists())
    # 9. no_mock_code: the skill must explicitly forbid mock / fake / pseudo
    # output. The canonical phrasing lives in the Minimum Requirements
    # section of every SKILL.md. Scoped to that section so an incidental
    # phrase elsewhere (e.g. "no pseudo-random" in a generative-art skill,
    # "mock" as a testing keyword) cannot satisfy it by accident.
    req_sec = ""
    m_sec = re.search(r"## Minimum Requirements[^\n]*\n(.*?)(?=^## |\Z)",
                      text, re.DOTALL | re.MULTILINE)
    if m_sec:
        req_sec = m_sec.group(1).lower()
    # The rule bans MOCK CODE, so the terms must attach to 'code' (or use
    # the canonical phrasing); "no pseudo-random numbers" or "no fake data"
    # must NOT satisfy it.
    result["checks"]["no_mock_code"] = bool(re.search(
        r"mock, fake, or pseudo|no mock code|no fake code|no pseudo code|never present fake",
        req_sec))
    return result


def score(result: dict) -> float:
    checks = result.get("checks", {})
    if "missing" in checks:
        return 0.0
    passed = sum(1 for v in checks.values() if v)
    return passed / len(checks)


def main() -> None:
    single = (BASE / "SKILL.md").exists()
    if single:
        # per-skill repo: SKILL.md at the root, repo name = skill name
        skills = [BASE.name]
    else:
        skills = [p.parent.name for p in sorted(BASE.glob("*/SKILL.md"))
                  if not p.parent.name.endswith("-workspace")]
    results = [audit_skill(s, BASE / "SKILL.md" if single else None) for s in skills]
    for r in results:
        r["score"] = round(score(r), 2)
    results.sort(key=lambda r: r["skill"])
    overall = round(sum(r["score"] for r in results) / len(results), 2)

    (BASE / "SKILL_AUDIT.json").write_text(
        json.dumps({"overall": overall, "skills": results}, indent=2))

    # quality gate: "bad quality doesn't ship" (runs in EVERY mode, incl.
    # --json, so a combined invocation still gates and still writes the file)
    if "--min-score" in sys.argv:
        min_score = float(sys.argv[sys.argv.index("--min-score") + 1])
        worst = min(r["score"] for r in results)
        if worst < min_score:
            worst_name = min(results, key=lambda r: r["score"])["skill"]
            print(f"\nGATE FAILED: {worst_name} scored {worst:.2f} < "
                  f"required {min_score:.2f}, not shipping")
            sys.exit(1)
        print(f"GATE PASSED: all skills >= {min_score:.2f}")

    if "--json" in sys.argv:
        print(json.dumps({"overall": overall, "skills": results}, indent=2))
        return

    print(f"{'skill':<24}{'score':>6}  detail")
    print("-" * 90)
    for r in results:
        fails = [k for k, v in r["checks"].items() if not v]
        detail = f"LANGS:{','.join(r.get('langs', []))[:60]}" if r.get("langs") else "no code"
        extra = f"  | FAIL: {', '.join(fails)}" if fails else ""
        print(f"{r['skill']:<24}{r['score']:.2f}  {detail}{extra}")
    print("-" * 90)
    print(f"{'OVERALL':<24}{overall:.2f}")


if __name__ == "__main__":
    main()
