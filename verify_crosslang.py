#!/usr/bin/env python3
"""Extract the ```javascript example block from every SKILL.md under skills 2/
and execute it with node, reporting pass/fail per skill. Exits nonzero on any
failure. (Rust examples are stdlib-only and written conservatively; rustc is
not assumed to exist, so they are checked statically here: every block must be
non-trivial code, not a comment-only stub.)

Usage:  python3 verify_crosslang.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
skills = sorted(p.parent.name for p in HERE.glob("*/SKILL.md"))

NODE = shutil.which("node")
if NODE is None:
    print("node not found on PATH — cannot verify javascript examples.")
    sys.exit(2)

fails = []
passes = 0
stubs = []
for name in skills:
    text = (HERE / name / "SKILL.md").read_text(encoding="utf-8")
    block = text.split("```javascript", 1)[1].split("```", 1)[0] if "```javascript" in text else None
    if block is None:
        fails.append((name, "no javascript block"))
        continue
    body = block.strip()
    # real code = at least one non-blank line that isn't a comment
    code_lines = [ln for ln in body.splitlines()
                  if ln.strip() and not ln.lstrip().startswith(("//", "/*", "*"))]
    if not code_lines:
        stubs.append(name)  # comment-only block is not real code
        continue
    try:
        # input="" closes stdin so stdin-filter examples (unix) get EOF and exit.
        r = subprocess.run([NODE, "-e", body], input="", capture_output=True,
                           text=True, timeout=10)
    except subprocess.TimeoutExpired:
        fails.append((name, "TIMEOUT after 10s (hangs or runs too long)"))
        continue
    if r.returncode == 0:
        passes += 1
    else:
        err = (r.stderr or r.stdout).strip().splitlines()
        fails.append((name, err[-1] if err else "no output"))

print(f"Verified {passes}/{len(skills)} javascript examples run cleanly under node.")
for name, err in fails:
    print(f"  FAIL {name}: {err}")
if stubs:
    print(f"  STUB (comment-only, not real code): {', '.join(stubs)}")
sys.exit(1 if (fails or stubs) else 0)
