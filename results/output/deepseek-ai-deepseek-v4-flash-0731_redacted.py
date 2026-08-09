def compute_and_redact(records):
    # Retention table:
    #   value -> required for sum only, then cleared
    #   secret -> never retained, never logged, never returned
    total = 0
    for record in records:
        value = record.get("value", 0)
        secret = record.get("secret")
        total += value
        # Last use of secret: only existence check, then immediate discard
        _ = bool(secret)
        record.clear()
        record.update({"redacted": True})

    result = {
        "total": total,
        "refused_to_retain": ["secret", "raw_record"],
        "cleanup_boundary": "after per-record aggregation",
        "erasure_limit": "container cleared; secure memory wiping not guaranteed",
    }
    assert all("secret" not in record and "value" not in record for record in records)
    return result

records = [
    {"value": 10, "secret": "s3cr3t-a"},
    {"value": 20, "secret": "s3cr3t-b"},
]
report = compute_and_redact(records)
assert report["total"] == 30
assert records == [{"redacted": True}, {"redacted": True}]
assert "s3cr3t" not in repr(report)
print(report)