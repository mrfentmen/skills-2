#!/usr/bin/env python3
"""Extract the ```python example block from every SKILL.md under skills 2/ and
execute it, reporting pass/fail per skill. Exits nonzero on any failure."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
skills = sorted(p.parent.name for p in HERE.glob("*/SKILL.md"))

fails = []
passes = 0
for name in skills:
    text = (HERE / name / "SKILL.md").read_text(encoding="utf-8")
    if "```python" not in text:
        fails.append((name, "no python example block"))
        continue
    block = text.split("```python", 1)[1].split("```", 1)[0]
    # input="" closes stdin so stdin-filter examples (unix) get EOF and exit.
    # NOTE: stdin-reading examples are smoke-tested on EMPTY input (they must
    # terminate and exit 0), not pipeline-tested with real data -- that's the
    # verifier's job elsewhere. Don't remove the input="" or the unix example hangs.
    r = subprocess.run([sys.executable, "-c", block], input="", capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        passes += 1
    else:
        fails.append((name, (r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else "no output"))

print(f"Verified {passes}/{len(skills)} examples run cleanly.")
for name, err in fails:
    print(f"  FAIL {name}: {err}")
print("SKILL_MD_COUNT:", len(skills))
sys.exit(1 if fails else 0)
