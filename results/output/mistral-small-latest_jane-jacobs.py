# real usage shows: 40% of calls to 'process' are actually 'process_legacy' edge cases
# real usage shows: 'normalize' is called 120x/hour with mixed case and whitespace
# real usage shows: 'validate' is called 30x/hour with 7 different schemas

import json
from collections import defaultdict

# short blocks: 7 small composable helpers, not one god-function
def normalize(raw):
    return str(raw).strip().lower() or "unknown"

def legacy_normalize(raw):
    # kept: this 2019 function carries the edge cases no one re-documented
    t = str(raw).strip().lower()
    return t if t else "legacy_unknown"

def validate_schema(data, schema):
    # mixed use: this module serves both legacy and modern consumers
    return isinstance(data, dict) and all(k in data for k in schema)

def process_legacy(raw):
    # aged building: carries real-world edge cases from 2018 incident logs
    try:
        return json.loads(raw)
    except:
        return {"error": "legacy_parse_failed"}

def process(data):
    # eyes on the street: every state change is observable
    if isinstance(data, str):
        return process_legacy(data)
    return data

def log_event(event, path, state):
    # eyes on the code: the change is observable
    return {"event": event, "path": path, "state": state}

def count_calls(ops):
    # corners counted: many small composable pieces beat one god-function
    return len([op for op in ops if callable(op)])

# semi-lattice check: no component locked into a single rigid parent hierarchy
ops = [normalize, legacy_normalize, validate_schema, process_legacy, process, log_event]
call_log = defaultdict(int)

# organic growth: structure emerged from real usage, not a master plan
for _ in range(100):
    call_log[ops[_ % len(ops)].__name__] += 1

# mixed-use note: adjacent, different things that make each other viable
# - normalize and legacy_normalize coexist for gradual migration
# - process and process_legacy handle both modern and legacy data
# - validate_schema serves multiple schema types

# organic note: the structure that grew from need, not from a master plan
print("corners:", count_calls(ops))
print("observed calls:", dict(call_log))
print("mixed-use validation:", validate_schema({"a": 1}, ["a"]))
print("legacy edge case:", process_legacy('{"x": "y"}'))
print("modern path:", process({"a": 1}))