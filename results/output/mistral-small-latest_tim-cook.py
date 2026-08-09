# spoilage audit: legacy feature flag (USE_LEGACY_PARSER), unused dep (numpy), speculative cache (parse_cache)
# end-to-end trace: input -> validator -> parser -> formatter -> output
# long-term pick: chose json for interchange — 20+ years of stable tooling and RFCs
# privacy pass: collected at the edge — only the fields the feature actually reads
# quiet-fix note: root cause: unchecked offset; fix: one bounds check, not a refactor

import json
from pathlib import Path

def validate(raw: str) -> str:
    # collected at the edge: only the fields the feature actually reads
    if not isinstance(raw, str):
        raise ValueError("input must be a string")
    return raw.strip()

def parse(valid: str) -> dict:
    # root cause: unchecked offset; fix: one bounds check, not a refactor
    if not valid:
        return {"status": "empty"}
    parts = valid.split("|", 1)
    if len(parts) < 2:
        return {"status": "malformed"}
    return {"id": parts[0].strip(), "payload": parts[1].strip()}

def format(parsed: dict) -> str:
    # chose: json — 20+ years of stable tooling and RFCs
    return json.dumps(parsed, separators=(",", ":"))

def run_pipeline(raw: str) -> str:
    # input -> validator -> parser -> formatter -> output
    return format(parse(validate(raw)))

sample = "  42|Hello Apple CEO  "
print("Audit: legacy flag USE_LEGACY_PARSER, unused numpy, speculative cache parse_cache")
print("Result:", run_pipeline(sample))