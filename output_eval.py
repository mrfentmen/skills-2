#!/usr/bin/env python3
"""Output-compliance eval for constraint-heavy persona skills (skills 2/).

For each skill in SCOPE the harness sends the FULL SKILL.md content as the
system prompt plus a one-sentence task, asks for Python code only, executes
it, and runs a per-skill structural grader that checks the skill's own
"Minimum Requirements (checkable)".

Failures reveal skill wording that models cannot comply with -> the input for
skill improvements. Code samples are saved to results/output/<skill>.py.

Usage:
  KEY=... python3 output_eval.py [--model deepseek-ai/deepseek-v4-flash-0731] \\
      [--base-url https://integrate.api.nvidia.com/v1] [--skills goldfish,sonnet]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model_router_eval import make_ssl_context  # noqa: E402

SCOPE = [
    "goldfish", "sonnet", "vampire", "hoarder", "insomniac",
    "trial-by-combat", "counterpoint", "casino", "dead-reckoning", "doppelganger",
]

TASKS = {
    "goldfish": "Sum the integers 1..100 and print the result.",
    "sonnet": "Print the first 10 prime numbers.",
    "vampire": "Drain a list in place until it is empty and print each value.",
    "hoarder": "Process a list of numbers, never deleting or overwriting anything, and print the full history.",
    "insomniac": "Poll two jobs until both are ready, without ever blocking or sleeping.",
    "trial-by-combat": "Two different sorting implementations fight; a deterministic rule picks the winner.",
    "counterpoint": "Interleave two different step machines until both finish, neither observing the other's result early.",
    "casino": "Estimate pi by random sampling and print a confidence interval.",
    "dead-reckoning": "Find the maximum of a stream in one left-to-right pass with bounded memory.",
    "doppelganger": "Two different implementations of the same computation; compare them at runtime and print any disagreement.",
}

GRADERS = {
    "goldfish": lambda c, o, e: (
        ".append(" not in c and "list(" not in c and "while" in c
        and bool(o.strip()) and e == "",
        "no-accumulation + while + printed result" if ".append(" not in c and "list(" not in c and "while" in c and o.strip() else
        f"append/list({'.append(' in c or 'list(' in c}) while={'while' in c} out={bool(o.strip())} err={bool(e)}",
    ),
    "sonnet": lambda c, o, e: (
        len([ln for ln in c.splitlines() if ln.strip()]) == 14 and bool(o.strip()) and e == "",
        f"lines={len([ln for ln in c.splitlines() if ln.strip()])}/14 out={bool(o.strip())}",
    ),
    "vampire": lambda c, o, e: (
        "while" in c and ("pop(" in c or "del " in c) and bool(o.strip()) and e == "",
        f"while={'while' in c} pop/del={'pop(' in c or 'del ' in c} out={bool(o.strip())}",
    ),
    "hoarder": lambda c, o, e: (
        "append" in c and "del " not in c and "remove(" not in c and ".pop(" not in c
        and bool(o.strip()) and e == "",
        f"append={'append' in c} no-del={'del ' not in c} out={bool(o.strip())}",
    ),
    "insomniac": lambda c, o, e: (
        "sleep" not in c and "poll" in c and bool(o.strip()) and e == "",
        f"no-sleep={'sleep' not in c} poll={'poll' in c} out={bool(o.strip())}",
    ),
    "trial-by-combat": lambda c, o, e: (
        len(re.findall(r"^def ", c, re.M)) >= 2 and ("winner" in c or "score" in c)
        and bool(o.strip()) and e == "",
        f"defs={len(re.findall(r'^def ', c, re.M))} winner/score={'winner' in c or 'score' in c} out={bool(o.strip())}",
    ),
    "counterpoint": lambda c, o, e: (
        len(re.findall(r"^def ", c, re.M)) >= 2 and ("step" in c or "next(" in c)
        and bool(o.strip()) and e == "",
        f"defs={len(re.findall(r'^def ', c, re.M))} step/next={'step' in c or 'next(' in c} out={bool(o.strip())}",
    ),
    "casino": lambda c, o, e: (
        "random" in c and ("seed" in c or "Seed" in c)
        and ("confiden" in c or "interval" in c or "margin" in c or "low" in c or "high" in c)
        and bool(o.strip()) and e == "",
        f"random={'random' in c} seed={'seed' in c} interval={'confiden' in c or 'interval' in c or 'margin' in c or 'low' in c or 'high' in c} out={bool(o.strip())}",
    ),
    "dead-reckoning": lambda c, o, e: (
        not re.search(r"\bsorted\(|\b\.sort\(|rewind|random access", c) and "count" in c
        and bool(o.strip()) and e == "",
        f"no-sort/rewind={not _DR_PAT.search(c)} count={'count' in c} out={bool(o.strip())}",
    ),

    "doppelganger": lambda c, o, e: (
        len(re.findall(r"^def ", c, re.M)) >= 2 and ("disagre" in c or "both" in c or "compare" in c)
        and bool(o.strip()) and e == "",
        f"defs={len(re.findall(r'^def ', c, re.M))} compare={'disagre' in c or 'both' in c or 'compare' in c} out={bool(o.strip())}",
    ),
}


_DR_PAT = re.compile(r"\bsorted\(|\b\.sort\(|rewind|random access")


def extract_code(raw: str) -> str:
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    m = re.search(r"```python\n(.*?)```", raw, re.S)
    if m:
        return m.group(1).strip()
    if "```python" in raw:
        # fence present but not closed on one line: cut after the fence
        rest = raw.split("```python", 1)[1]
        return rest.split("```")[0].strip()
    return raw.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="deepseek-ai/deepseek-v4-flash-0731")
    ap.add_argument("--base-url", default="https://integrate.api.nvidia.com/v1")
    ap.add_argument("--skills", default=",".join(SCOPE))
    ap.add_argument("--key", default=None)
    ap.add_argument("--out", default="results/output_eval.json")
    args = ap.parse_args()

    key = args.key or os.environ.get("KEY")
    if not key:
        print("FATAL: pass --key or set KEY env var")
        sys.exit(2)

    ctx = make_ssl_context()
    skills = [s for s in args.skills.split(",") if s in TASKS]
    results = {}
    out_dir = HERE / "results" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, name in enumerate(skills):
        skill_text = (HERE / name / "SKILL.md").read_text(encoding="utf-8")
        system = (
            "You are a coding assistant using the skill below. Follow ALL of the "
            "skill's Minimum Requirements exactly. Write ONLY Python code inside a "
            "```python code block. No prose, no explanations, no comments outside "
            "the code.\n\n=== SKILL ===\n" + skill_text + "\n\n=== TASK ===\n" + TASKS[name]
        )
        payload = {
            "model": args.model,
            "messages": [{"role": "user", "content": system}],
            "max_tokens": 2000,
            "temperature": 0,
        }
        raw = ""
        try:
            req = urllib.request.Request(
                args.base_url.rstrip("/") + "/chat/completions",
                data=json.dumps(payload).encode(),
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
                data = json.loads(resp.read().decode())
            raw = data["choices"][0]["message"].get("content") or ""
        except urllib.error.HTTPError as e:
            raw = f"__HTTPERR__{e.code} {e.read().decode()[:120]}"
        except Exception as e:  # noqa: BLE001
            raw = f"__ERR__ {e}"

        code = extract_code(raw)
        (out_dir / f"{name}.py").write_text(code, encoding="utf-8")

        passed = None
        detail = ""
        if code.startswith("__ERR__") or code.startswith("__HTTPERR__"):
            detail = code[:100]
        else:
            try:
                r = subprocess.run([sys.executable, "-c", code], input="",
                                   capture_output=True, text=True, timeout=30)
                passed, detail = GRADERS[name](code, r.stdout, r.stderr)
                if r.returncode != 0:
                    passed = False
                    detail = f"EXEC FAIL: {(r.stderr or r.stdout).strip().splitlines()[-1][:80] if (r.stderr or r.stdout).strip() else 'no output'}"
            except subprocess.TimeoutExpired:
                passed = False
                detail = "EXEC TIMEOUT"
            except Exception as e:  # noqa: BLE001
                passed = False
                detail = f"GRADER ERR: {e}"

        results[name] = {"passed": bool(passed), "detail": detail,
                         "code_file": f"results/output/{name}.py"}
        print(f"[{i+1}/{len(skills)}] {name:16} {'PASS' if passed else 'FAIL'}  {detail}", flush=True)

    summary = {k: v["passed"] for k, v in results.items()}
    (HERE / args.out).write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"\nOUTPUT EVAL: {sum(summary.values())}/{len(summary)} pass")
    print(f"saved -> {args.out}")


if __name__ == "__main__":
    main()
