#!/usr/bin/env python3
"""
Curate real trigger phrases for skills in `skills 2/`.

The generator produced degenerate `Triggers on: "name, name"` clauses wherever
the source spec had no trigger list, which makes skill selection unreliable.
This script replaces those clauses with a curated list of real trigger phrases
for every skill, grounded in each skill's own description/persona. It updates
BOTH the SKILL.md frontmatter (the machine-readable layer) and the README
block (the human-readable catalog).

The SKILL.md frontmatter description is rebuilt deterministically from the
pristine README block description (the canonical verbatim spec), so repeated
runs are idempotent and cannot corrupt the YAML.

Usage:  python3 enrich_triggers.py            (dry-run: report what would change)
        python3 enrich_triggers.py --write    (apply changes)
"""

import re
import sys
from pathlib import Path
from generate_skills import fold

HERE = Path(__file__).resolve().parent

# name -> curated trigger phrases. Only skills whose triggers were missing or
# degenerate are listed; persona skills with real triggers are left alone.
TRIGGERS = {
    "fibonacci": ["fibonacci", "fibonacci sequence", "1 1 2 3 5 8 13",
                  "mathematically shaped code", "structurally grow",
                  "grow structurally", "tiny beginning", "golden ratio code"],
    "ouroboros": ["ouroboros", "quine", "self-referential", "self-reproducing",
                  "reads its own source", "reproduces itself",
                  "program uses its own output"],
    "noir": ["noir", "hardboiled detective", "detective story code",
             "cynical comments", "the missing record", "dirty cache"],
    "margaret-hamilton": ["margaret hamilton", "defensive code",
                          "validate every boundary", "fail safe",
                          "partial failure", "fault tolerant",
                          "handle malformed input"],
    "doppelganger": ["doppelganger", "compute twice", "two different strategies",
                     "compare the results", "compare at runtime", "two implementations",
                     "second opinion", "same computation twice"],
    "janitor": ["janitor", "cleanup", "resource management", "release path",
                "guaranteed cleanup", "leak free", "close every resource"],
    "oracle": ["oracle", "prediction", "gather evidence", "revise the prediction",
               "initial belief", "final judgment", "state your belief"],
    "schrodinger": ["schrodinger", "lazy evaluation", "lazy values", "defer",
                    "deferred computation", "unevaluated", "delay computation",
                    "last possible moment"],
    "casino": ["casino", "monte carlo", "random sampling", "probability",
               "confidence", "error margin", "randomized search",
               "estimate pi", "converge toward an answer"],
    "insomniac": ["insomniac", "non-blocking", "never sleep", "no sleeping",
                  "explicit polling", "event loop", "never block",
                  "poll instead of wait"],
    "vampire": ["vampire", "mutate in place", "drain the arguments",
                "zero allocation", "destructive ownership", "in place"],
    "blood-magic": ["blood magic", "blood sacrifice", "sacrifice code",
                    "destructive trade-off", "destroy something", "trades destruction"],
    "pepe-silvia": ["pepe silvia", "conspiracy code", "red string", "red string logic",
                    "schizo", "schizo comments", "corkboard", "conspiracy theorist",
                    "magic numbers"],
    "sovereign-citizen": ["sovereign citizen", "sovereign citizen code", "maritime law",
                          "maritime law logic", "refuse standard library",
                          "refuse standard lib",                          "does not consent", "reimplement operators",
                          "bitwise hacks", "refuse built in operators",
                          "from scratch", "reimplement from scratch",
                          "reimplement"],
    "y2k": ["y2k", "embedded engineer", "fixed width", "bounded buffers",
            "overflow handling", "rollover", "small integer types",
            "december 1999"],
    "floor-trader": ["floor trader", "live stream", "no rewind", "no lookahead",
                     "real-time decisions", "irreversible decision",
                     "online algorithm"],
    "hoarder": ["hoarder", "append only", "never delete", "delete nothing",
                "keep everything", "accumulate", "delete or overwrite nothing"],
    "trial-by-combat": ["trial by combat", "competing implementations", "fight",
                        "champion", "winner takes the state",
                        "deterministic rule"],
    "black-box": ["black box", "yes no questions", "yes no",
                  "yes no greater", "greater lesser equal", "interrogation",
                  "question only", "oracle questions", "interrogation alone"],
    "goldfish": ["goldfish", "two variables", "two variables only", "bit pack",
                 "memory amnesia", "extreme memory constraint", "forgetful"],
    "rorschach": ["rorschach", "ambiguous input", "multiple interpretations",
                  "heuristic parser", "polymorphic data", "inkblot",
                  "uncertain classification"],
    "lazarus": ["lazarus", "crash recovery", "checkpoint", "resurrect",
                "rebuild state", "event log", "snapshot", "restartable"],
    "redacted": ["redacted", "privacy", "minimize exposure", "sensitive values",
                 "data minimization", "refuse to retain", "secret handling"],
    "funeral": ["funeral", "used exactly once", "ownership", "linear logic",
                "destroy after use", "no alias", "transfer of data"],
    "counterpoint": ["counterpoint", "interleave", "two algorithms",
                     "interleaved execution", "neither finishes first",
                     "step by step"],
    "red-team": ["red team", "attack your own answer", "adversarial cases",
                 "repair the answer", "reject with evidence", "red teaming"],
    "dead-reckoning": ["dead reckoning", "single pass", "bounded memory",
                       "no random access", "left to right", "no rewinding",
                       "exactly once"],
    "blind": ["blind", "opaque input", "question only", "predicate",
              "blind oracle", "fixed set of questions"],
    "delta": ["delta", "diff", "minimal change", "change description",
              "synchronization", "apply the delta", "no full snapshot"],
    "proof-carrying": ["proof carrying", "certificate", "machine-checkable",
                       "verifier", "verify independently", "verified result"],
    "quiescent": ["quiescent", "quiet point", "atomic transition",
                  "no observers", "quiescence", "hot reload"],
    "zero-copy": ["zero copy", "no copies", "ownership", "slices", "views",
                  "move data without copying", "pass ownership"],
    "boiler-room-research": ["boiler room", "sales floor", "sales-floor",
                             "stock verdict", "hard verdict", "buy case",
                             "bear case", "catalyst", "trigger",
                             "invalidation", "investigate a stock",
                             "aggressive stock research"],
    "greybeard-after-midnight": ["greybeard", "2am", "ten year old system",
                                 "ten year old codebase", "legacy system",
                                 "smallest durable fix",
                                 "reproduce the problem", "incident repair"],
    "carmack-mode": ["carmack", "measure first", "bottleneck", "benchmark",
                     "cache behavior", "memory layout", "start from the hardware"],
    "cold-war": ["cold war", "dossier", "intelligence", "confirmed facts",
                 "weak signals", "misinformation", "unknowns",
                 "track each claim"],
    "quant": ["quant", "hypothesis", "metric", "backtest", "survivorship bias",
              "overfitting", "baseline", "hypothesis must survive data"],
    "war-room": ["war room", "production", "outage", "rollback",
                 "stop the bleeding", "incident", "impact"],
    "record-producer": ["record producer", "core loop", "first minute",
                        "pacing", "playtest", "player experience",
                        "earn attention", "friction"],
    "hostile-acquisition": ["hostile acquisition", "defeat", "switching costs",
                            "competitor analysis", "weak points",
                            "replacement path"],
    "boardroom-liar": ["boardroom", "pitch", "founder", "audit the claims",
                       "measurable behavior", "technical pitch",
                       "persuasive explanation", "where that story is false"],
    "desert-island": ["desert island", "offline", "no network", "no packages",
                      "no dependencies", "portable", "runnable offline"],
    "the-last-employee": ["last employee", "maintain for a decade",
                          "maintain it for a decade", "maintaining for a decade",
                          "only person maintaining", "boring interfaces",
                          "long-lived", "migration paths", "easy deletion",
                          "future maintainer"],
    "casino-owner": ["casino owner", "house", "expected value", "max loss",
                     "variance", "odds", "who has the edge"],
    "meta-senior-dev": ["meta senior dev", "facebook engineer", "monorepo",
                        "stacked diffs", "hack language", "buck", "move fast",
                        "senior tech dev at meta", "senior engineer at meta",
                        "meta engineer", "review my pr"],
    "azure-engineer": ["microsoft", "azure", "c#", ".net", "paved path",
                       "well-architected", "backward compatibility",
                       "backwards compatibility", "cloud engineer",
                       "cloud scale", "enterprise reliability", "c sharp"],
    "huang": ["jensen huang", "nvidia", "cuda", "gpu",
              "hardware-software co-design", "hardware software co-design",
              "memory layout", "data movement", "full-stack optimization"],
}

# folder name -> regex to match the heading name in README.md (differs for a few)
HEADING = {
    "boiler-room-research": r"boiler-room \(research\)",
}

INJECTED = re.compile(r"\*\*Triggers on:\*\* (?:\"[^\"]*\"\s*)+\.\n(?=This skill is NOT for)")

INJECTED_LINE = re.compile(r"^> .*\*\*Triggers on:\*\* .*$", re.M)


def quoted(phrases):
    return " ".join('"%s"' % p for p in phrases)


def readme_block_desc(name: str) -> str:
    """Extract the canonical description (the `> ...` lines) of a skill's
    README block, with any injected/legacy trigger clause stripped."""
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    heading = HEADING.get(name, re.escape(name))
    m = re.search(
        r"(#### \d+\.\s*" + heading + r"(?![\w-]).*?)(?=\n#### |\n## |\Z)",
        readme, re.S)
    if not m:
        return ""
    lines = []
    for line in m.group(1).splitlines():
        s = line.strip()
        if s.startswith("> "):
            s = s[2:]
            s = INJECTED_LINE.sub("", s)  # drop any injected trigger text
            lines.append(s.strip())
    desc = " ".join(lines)
    desc = re.sub(r"\*\*Triggers on(?: requests for)?:\*\*[^.]*\.\s*", "", desc)
    return re.sub(r"\s+", " ", desc).strip()


def build_skill_md(name: str, phrases: list):
    """Return (new_text, changed) for a rebuilt SKILL.md frontmatter."""
    path = HERE / name / "SKILL.md"
    if not path.exists():
        return None, False
    text = path.read_text(encoding="utf-8")
    base = readme_block_desc(name)
    if not base:
        return None, False
    new_desc = base + " Triggers on: " + quoted(phrases) + "."
    folded = fold(new_desc)
    m = re.match(r"^---\nname: ([^\n]+)\n", text)
    if not m:
        return None, False
    close = text.find("\n---", m.end())
    if close == -1:
        return None, False
    rest = text[close + 4:]
    new_text = "---\nname: %s\ndescription: >-\n  %s\n---\n%s" % (name, folded, rest)
    return new_text, new_text != text


def revert_readme_injections() -> int:
    """Remove the malformed inline trigger lines left by an earlier version."""
    path = HERE / "README.md"
    text = path.read_text(encoding="utf-8")
    new = INJECTED.sub("", text)
    if new != text:
        path.write_text(new, encoding="utf-8")
    return text.count("**Triggers on:**") - new.count("**Triggers on:**")


def inject_readme_trigger(name: str, phrases: list) -> bool:
    path = HERE / "README.md"
    text = path.read_text(encoding="utf-8")
    heading = HEADING.get(name, re.escape(name))
    m = re.search(
        r"(#### \d+\.\s*" + heading + r"(?![\w-]).*?)(?=\n#### |\n## |\Z)",
        text, re.S)
    if not m:
        return False
    block = m.group(1)
    if "**Triggers on:" in block:
        return False  # already has a real trigger list (persona skills)
    clean = block.rstrip()
    new_block = clean + "\n> **Triggers on:** " + quoted(phrases) + ".\n\n"
    text = text[: m.start(1)] + new_block + text[m.end(1):]
    path.write_text(text, encoding="utf-8")
    return True


def main():
    write = "--write" in sys.argv
    md_changed, rm_changed = [], []

    if write:
        n = revert_readme_injections()
        if n:
            print(f"reverted {n} malformed trigger lines in README")

    for name in sorted(TRIGGERS):
        phrases = TRIGGERS[name]
        new_text, changed = build_skill_md(name, phrases)
        if changed:
            md_changed.append(name)
        if write and new_text and changed:
            (HERE / name / "SKILL.md").write_text(new_text, encoding="utf-8")
        if write and inject_readme_trigger(name, phrases):
            rm_changed.append(name)

    print(f"skills in map: {len(TRIGGERS)}")
    print(f"SKILL.md updated: {len(md_changed)}  README updated: {len(rm_changed)}")
    if not write:
        print("dry-run: pass --write to apply")
    for n in md_changed:
        print(f"  MD  {n}")
    for n in rm_changed:
        print(f"  RM  {n}")


if __name__ == "__main__":
    sys.exit(main())
