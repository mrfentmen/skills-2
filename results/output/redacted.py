def compute_and_redact(records):
    # Retention table:
    # value -> aggregate only; secret -> count only, then clear; raw -> never keep.
    total = 0
    secret_count = 0
    for record in records:
        value = record.get("value", 0)
        secret = record.get("secret")
        total += value
        secret_count += bool(secret)
        record.clear()                 # last use of all raw fields
        record.update({"redacted": True})

    result = {
        "total": total,
        "secret_count": secret_count,
        "refused_to_retain": ["secret", "raw_record"],
        "cleanup_boundary": "after per-record aggregation",
        "erasure_limit": "container cleared; secure memory wiping not guaranteed",
    }
    assert all("secret" not in record and "value" not in record for record in records)
    return result

records = [
    {"value": 10, "secret": "s3cr3t-a"},
    {"value": 20, "secret": ""},
]
report = compute_and_redact(records)
assert report["total"] == 30
assert report["secret_count"] == 1
assert records == [{"redacted": True}, {"redacted": True}]
assert "s3cr3t-a" not in repr(report)
print(report)