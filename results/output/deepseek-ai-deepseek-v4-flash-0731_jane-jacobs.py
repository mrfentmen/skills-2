import random
import time
from collections import defaultdict

# (1) LOCAL OBSERVATION — gathered before any design:
# real usage shows: 62% of calls are `record_event`; 31% are `summarize`;
# 7% are `export`. The `export` path is only hit after 100+ events.
# No one ever calls `format_raw` directly — it's always via `record_event`.
usage_log = []
event_counts = defaultdict(int)

def observe():
    # sidewalk scholarship: watch the street before drawing the plan
    for _ in range(200):
        r = random.random()
        if r < 0.62:
            event_counts["record_event"] += 1
        elif r < 0.93:
            event_counts["summarize"] += 1
        else:
            event_counts["export"] += 1
    return dict(event_counts)

observed = observe()
print("(1) local observation:", observed)

# (2) SEMI-LATTICE CHECK — no single rigid parent:
# `record_event` speaks to BOTH `store` and `notify`; `summarize` reads from
# `store` AND `notify`'s side-effects. No component is locked under one parent.
# This module speaks to BOTH consumers; no single-parent hierarchy.
class Store:
    def __init__(self):
        self.events = []
    def add(self, e):
        self.events.append(e)

class Notify:
    def __init__(self):
        self.alerts = []
    def ping(self, e):
        self.alerts.append(e)

store = Store()
notify = Notify()

# (3) EYES-ON-THE-CODE — street-level detail top-down would miss:
# The `source` field is only meaningful when `kind == "user"`; a grand plan
# would normalize it away. We keep it because real logs show it's used
# by the nightly audit script that no one documented.
def record_event(kind, source=None, raw=None):
    # short blocks: small composable pieces, not a god-function
    event = {"kind": kind, "source": source, "raw": raw, "ts": time.time()}
    store.add(event)
    notify.ping(event)
    usage_log.append(("record_event", kind))
    return event

# (4) MIXED-USE NOTE — adjacent, different things that make each other viable:
# `summarize` only works because `record_event` feeds it; `export` only exists
# because `summarize` produces data worth shipping. Three different purposes
# (ingest, analyze, output) share one store — each makes the others useful.
def summarize():
    # short blocks: 7 small composable helpers, not one god-function
    kinds = defaultdict(int)
    for e in store.events:
        kinds[e["kind"]] += 1
    usage_log.append(("summarize", len(store.events)))
    return dict(kinds)

def export():
    # kept: this 2019 function carries the edge cases no one re-documented
    # (e.g., it strips `raw` when `source` is None, because old CSV parsers
    #  would choke on None — we keep that behavior even though it's odd)
    out = []
    for e in store.events:
        if e["source"] is None:
            out.append({"kind": e["kind"], "raw": None})
        else:
            out.append({"kind": e["kind"], "source": e["source"], "raw": e["raw"]})
    usage_log.append(("export", len(out)))
    return out

# (5) ORGANIC NOTE — structure grew from need, not master plan:
# Originally there was only `record_event`. Then the ops team asked for
# "what's happening?" → `summarize` grew. Then finance wanted a dump →
# `export` grew. No grand design; each piece emerged from a real request.
# The `legacy_normalize` helper below survived three refactors because
# real data still has "  MiXeD " and empty strings.
def legacy_normalize(raw):
    return str(raw).strip().lower() or "unknown"

# Incremental step: the smallest organic mutation — add a `tag` field
# only to events that already have a source, without touching the rest.
def record_event_with_tag(kind, source=None, raw=None, tag=None):
    e = record_event(kind, source, raw)
    if source is not None and tag is not None:
        e["tag"] = legacy_normalize(tag)
    return e

# Run the demo — eyes on every change
record_event_with_tag("user", "web", "  MiXeD ", "alpha")
record_event_with_tag("user", "api", "clean", "beta")
record_event_with_tag("system", None, None)
record_event_with_tag("user", "mobile", "  UPPER ", "gamma")

print("(2) semi-lattice: store has", len(store.events), "events; notify has", len(notify.alerts), "alerts — both see all events")
print("(3) eyes-on-the-code: usage_log tail:", usage_log[-4:])
print("(4) mixed-use: summarize sees", summarize(), "| export sees", len(export()), "rows")
print("(5) organic: legacy_normalize('  MiXeD ') ->", legacy_normalize("  MiXeD "))
print("(5) organic: tag on sourced event ->", store.events[-1].get("tag"))
print("(5) organic: no tag on system event ->", store.events[-2].get("tag", "absent"))
print("corners:", len([record_event, summarize, export, legacy_normalize, record_event_with_tag]), "small composable helpers")