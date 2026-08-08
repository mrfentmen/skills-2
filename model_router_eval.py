#!/usr/bin/env python3
"""Real-model routing benchmark for `skills 2/`.

Measures how well a real LLM can route a user request to the correct skill
using ONLY the catalog (frontmatter name + description) - which is exactly
what agent skill-loaders see at trigger time. This is the live complement to
the mechanical benchmark_prompts.py.

For each prompt the model is asked to name the single best-matching skill id
(or NONE). hit@1 = gold skill chosen. Per-skill misses reveal descriptions
that are too vague for real routers -> the raw material for buzzword/trigger
edits.

Progress is written to --out incrementally, so interrupted runs keep results
and can be resumed by passing the remaining --prompt-ids.

Usage (key via env, never committed):
  KEY=... python3 model_router_eval.py \\
      --model nvidia/nemotron-3-super-120b-a12b \\
      --base-url https://integrate.api.nvidia.com/v1 \\
      --out results/nemotron.json
  KEY=... python3 model_router_eval.py --model llama-3.3-70b-versatile \\
      --base-url https://api.groq.com/openai/v1 --compact \\
      --out results/groq-llama.json

Exit code 0 always (results are data, not a gate).
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from benchmark_prompts import SUITE, parse_frontmatter  # noqa: E402

# Curated prompt ids: finance personas, tech personas, coding-forms,
# safety/verification, CS greats, odd/creative, shorthand repeats.
DEFAULT_IDS = [
    0, 4, 7, 8, 9, 10, 13, 14, 15, 19, 20, 22, 23, 25, 26, 27,
    28, 30, 32, 39, 40, 41, 45, 48, 49, 50, 52, 56, 57, 58, 62, 65,
    69, 71, 75, 76, 78, 82, 83, 89, 93, 95, 97, 101, 103, 113, 119,
    127, 271, 272, 273, 275, 277, 278, 282, 285,
]

_SYSTEM_CAS = [
    "/etc/ssl/cert.pem",
    "/etc/ssl/certs/ca-certificates.crt",
    "/etc/pki/tls/certs/ca-bundle.crt",
    "/System/Library/OpenSSL/certs/cacert.pem",
    "/usr/local/etc/openssl/cert.pem",
    "/opt/homebrew/etc/openssl/cert.pem",
]


def make_ssl_context() -> ssl.SSLContext:
    """Best-effort verified SSL; last-resort unverified (local eval harness)."""
    for cafile in _SYSTEM_CAS:
        if Path(cafile).exists():
            return ssl.create_default_context(cafile=cafile)
    try:
        import certifi  # type: ignore

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001
        print("WARNING: no CA bundle found; using unverified SSL (local eval only)",
              flush=True)
        return ssl._create_unverified_context()  # noqa: S323


def build_catalog(compact: bool):
    """Return [(folder_name, description)] sorted, optionally truncated."""
    skills = []
    for p in sorted(HERE.glob("*/SKILL.md")):
        name = p.parent.name
        desc = parse_frontmatter(p.read_text(encoding="utf-8")).get("description", "")
        desc = " ".join(desc.split())
        if compact and len(desc) > 170:
            desc = desc[:170].rsplit(" ", 1)[0] + " ..."
        skills.append((name, desc))
    return skills


def call(base_url: str, key: str, model: str, system: str, user: str,
         retries: int = 2, timeout: int = 90,
         ctx: ssl.SSLContext | None = None) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": 48,
        "temperature": 0,
    }
    url = base_url.rstrip("/") + "/chat/completions"
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode(),
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                data = json.loads(resp.read().decode())
            msg = data["choices"][0]["message"]
            content = msg.get("content") or msg.get("reasoning_content") or ""
            return str(content).strip()
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:200]
            if e.code in (429, 500, 502, 503):
                time.sleep(3 * (attempt + 1))
                continue
            return f"__HTTPERR__{e.code} {body}"
        except Exception as e:  # noqa: BLE001
            if attempt < retries:
                time.sleep(3 * (attempt + 1))
                continue
            return f"__ERR__ {e}"
    return "__ERR__ retries exhausted"


def parse_decision(text: str, ids: set) -> str:
    # strip markdown fences and  tags if present
    text = re.sub(r"```(?:json)?", "", text)
    text = re.sub(r"</?thought>|</?reasoning>|</?analysis>", "", text)
    m = re.search(r'"id"\s*:\s*"([^"]+)"', text)
    if m:
        return m.group(1).strip()
    if "NONE" in text.upper():
        return "NONE"
    toks = re.findall(r"[A-Za-z0-9\-_]+", text.lower())
    for t in toks:
        if t in ids:
            return t
    return "UNPARSEABLE"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--key", default=None, help="defaults to $KEY")
    ap.add_argument("--prompt-ids", type=str, default=",".join(map(str, DEFAULT_IDS)))
    ap.add_argument("--compact", action="store_true",
                    help="truncate descriptions (small-context/TPM providers)")
    ap.add_argument("--sleep", type=float, default=0.0,
                    help="extra seconds between requests")
    ap.add_argument("--timeout", type=int, default=90,
                    help="per-request timeout in seconds")
    args = ap.parse_args()

    key = args.key or os.environ.get("KEY")
    if not key:
        print("FATAL: pass --key or set KEY env var")
        sys.exit(2)

    ctx = make_ssl_context()
    ids = [int(x) for x in args.prompt_ids.split(",") if x.strip() != ""]
    catalog = build_catalog(args.compact)
    idset = {n for n, _ in catalog}

    lines = [f"{n}: {d}" for n, d in catalog]
    system = (
        "You are a skill router for a coding assistant. Below is the catalog of "
        "available skills. A user will send a coding request. Respond with ONLY a "
        "JSON object of the form {\"id\": \"<skill-folder-name>\"} naming the single "
        "best-matching skill, or {\"id\": \"NONE\"} if no skill is a good match. "
        "Pick the skill whose persona, style, or constraints the request most "
        "strongly invokes. Respond with ONLY the JSON object. No explanations, no prose, no markdown.\n\nCATALOG:\n" + "\n".join(lines)
    )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    results = []

    for i, idx in enumerate(ids):
        prompt, gold = SUITE[idx]
        raw = call(args.base_url, key, args.model, system, prompt,
                   timeout=args.timeout, ctx=ctx)
        decision = parse_decision(raw, idset)
        hit = decision in [g.strip().lower() for g in gold]
        results.append({
            "idx": idx, "prompt": prompt, "gold": gold,
            "decision": decision, "raw": raw[:140], "hit": hit,
        })
        payload = {
            "model": args.model, "base_url": args.base_url, "n": len(ids),
            "done": i + 1,
            "hit1": round(sum(1 for r in results if r["hit"]) / len(results), 4),
            "results": results,
        }
        out.write_text(json.dumps(payload, indent=1), encoding="utf-8")
        print(f"[{i+1}/{len(ids)}] idx={idx} gold={gold[0]:22} -> {decision:24} "
              f"{'HIT' if hit else 'MISS'}", flush=True)
        if args.sleep:
            time.sleep(args.sleep)

    hits = sum(1 for r in results if r["hit"])
    print(f"\nMODEL {args.model}: hit@1 = {hits}/{len(results)} = "
          f"{round(hits / len(results), 4) if results else 0.0}", flush=True)
    print(f"saved -> {out}", flush=True)


if __name__ == "__main__":
    main()
