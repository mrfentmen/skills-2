#!/usr/bin/env bash
# Skills-2 catalog CI gate.
#
# Runs the full quality battery against all 180 skills and fails RED on any
# check that regresses. Mirrors the main skills repo's run_current_ci.sh
# pattern: every check must exit 0, output is streamed, and the final line
# reports the gate verdict.
#
# Checks:
#   1. check_intro_integrity.py  - persona intros must never be rewritten
#   2. eval_skills.py            - 8-dimension static audit (>= 0.75)
#   3. identity_audit.py         - every skill opens with "You are", README link
#   4. verify_examples.py        - every Python example executes cleanly
#   5. verify_crosslang.py       - every JS example executes cleanly (node)
#   6. benchmark_prompts.py      - routing hit@1/hit@3 + adversarial precision
#   7. quality_scan.py           - depth score; wrapped to fail if any <= 12
#   8. verify_rust_static.py     - Rust blocks structurally clean
#   9. enforce_skill_self_containment.py - no cross-skill dependencies
#
# Usage:  bash run_ci.sh
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE" || exit 1

FAILED=0
STEP=0

run_check() {
  STEP=$((STEP + 1))
  local name="$1"
  shift
  echo "==> [$STEP/9] $name"
  if "$@"; then
    echo "    PASS: $name"
  else
    echo "    FAIL: $name"
    FAILED=1
  fi
}

run_check "intro integrity (persona intros add-only)" python3 check_intro_integrity.py
run_check "static skill audit (8 dimensions, min 0.75)" python3 eval_skills.py --min 0.75
run_check "identity audit (You-are openings + README links)" python3 identity_audit.py
run_check "python examples execute" python3 verify_examples.py
run_check "javascript examples execute (node)" python3 verify_crosslang.py
run_check "routing benchmark (hit@1/hit@3 + adversarial)" python3 benchmark_prompts.py

# quality_scan.py reports but always exits 0; wrap it with a real threshold.
STEP=$((STEP + 1))
echo "==> [$STEP/9] quality depth (mean /24, no skill <= 12)"
QUALITY_OUT="$(python3 quality_scan.py)"
QUALITY_STATUS=$?
echo "$QUALITY_OUT"
if [ "$QUALITY_STATUS" -ne 0 ]; then
  echo "    FAIL: quality_scan exited nonzero"
  FAILED=1
elif printf '%s\n' "$QUALITY_OUT" | grep -q "weakest (<=12): none"; then
  echo "    PASS: quality depth (no skill <= 12)"
else
  echo "    FAIL: quality depth - at least one skill scored <= 12"
  FAILED=1
fi

run_check "rust blocks static audit" python3 verify_rust_static.py
run_check "skill self-containment" python3 enforce_skill_self_containment.py

echo
if [ "$FAILED" -eq 0 ]; then
  echo "SKILLS-2 CI GATE: ALL GREEN (9/9)"
  exit 0
else
  echo "SKILLS-2 CI GATE: FAILED - see FAIL lines above"
  exit 1
fi
