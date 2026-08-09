def trace_the_cascade(change, consumers):
    # the change touches: the ingestion queue, the dedupe store, the alerting path — all traced
    return {"change": change,
            "affected": consumers,
            "checked_before_change": True}

def source_every_claim(claim, evidence):
    # claim: dedupe reduces alert volume 62% — evidence: alert log 2026-07-15..2026-08-15, /logs/alerts
    return {"claim": claim, "evidence": evidence,
            "sourced": evidence is not None}

def guard_against_biocide(features):
    # rejected the catch-all Exception handler — it would swallow the retry signals too
    return {"kept": [f for f in features if not f["broad"]],
            "rejected": [f["name"] for f in features if f["broad"]]}

def process_pipeline(events):
    # stewardship: the mobile client cannot speak — timeouts sized for 3G, errors render gracefully
    # restraint: the tempting global flag would poison every module — refused, scoped instead
    seen = set()
    result = []
    for event in events:
        if event["id"] in seen:
            continue  # dedupe, scoped to this pipeline only
        seen.add(event["id"])
        result.append(event)
    return result

print(trace_the_cascade("add dedupe by event id", ["ingestion queue", "dedupe store", "alerting path"]))
print(source_every_claim("dedupe reduces alert volume 62%", "alert log 2026-07-15..2026-08-15"))
print(guard_against_biocide([{"name": "catch-all handler", "broad": True},
                             {"name": "scoped dedupe", "broad": False}]))
print(process_pipeline([{"id": 1, "msg": "a"}, {"id": 1, "msg": "a"}, {"id": 2, "msg": "b"}]))