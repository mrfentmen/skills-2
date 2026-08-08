import re
from datetime import datetime

def parse_iso(raw):
    try:
        value = datetime.fromisoformat(raw)
    except ValueError as exc:
        return {"parser": "ISO-8601", "status": "rejected", "error": str(exc)}
    canonical = value.isoformat()
    if canonical != raw:
        return {"parser": "ISO-8601", "status": "rejected", "error": "round-trip mismatch"}
    return {"parser": "ISO-8601", "status": "valid", "value": canonical, "evidence": {"raw": raw, "grammar": "YYYY-MM-DDTHH:MM:SS", "consumed": len(raw)}}

def parse_epoch(raw):
    if not re.fullmatch(r"\d+", raw):
        return {"parser": "Unix-epoch-seconds", "status": "rejected", "error": "not all digits"}
    try:
        value = datetime.utcfromtimestamp(int(raw))
    except (OverflowError, OSError, ValueError) as exc:
        return {"parser": "Unix-epoch-seconds", "status": "rejected", "error": str(exc)}
    canonical = str(int(raw))
    if canonical != raw:
        return {"parser": "Unix-epoch-seconds", "status": "rejected", "error": "round-trip mismatch"}
    return {"parser": "Unix-epoch-seconds", "status": "valid", "value": value.isoformat() + "Z", "evidence": {"raw": raw, "grammar": "seconds since 1970-01-01T00:00:00Z", "consumed": len(raw)}}

def interpret(raw):
    views = [parse_iso(raw), parse_epoch(raw)]
    valid = [view for view in views if view["status"] == "valid"]
    return {"status": "resolved" if len(valid) == 1 else "ambiguous" if valid else "invalid", "views": views}

report = interpret("2025-03-04T12:00:00")
assert report["status"] == "resolved"
assert len([v for v in report["views"] if v["status"] == "valid"]) == 1
print(report)