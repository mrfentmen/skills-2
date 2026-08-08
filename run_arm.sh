#!/usr/bin/env bash
# Run one model arm of the routing eval. Usage:
#   bash run_arm.sh <model> <key> <base-url> <out.json> [extra harness args...]
set -u
cd "/Users/del/Desktop/skills 2" || exit 1
MODEL="$1"; KEY="$2"; BASE="$3"; OUT="$4"; shift 4
KEY="$KEY" python3 model_router_eval.py \
  --model "$MODEL" --base-url "$BASE" --out "$OUT" "$@"
