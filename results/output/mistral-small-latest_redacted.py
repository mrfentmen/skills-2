def compute_with_redaction(records):
    # Retention table:
    # required_output -> aggregate of sensitive_intermediate; sensitive_intermediate -> never retain
    # forbidden_retain -> raw_secret, raw_record
    aggregate_sum = 0
    for record in records:
        # Purpose: compute aggregate using sensitive_intermediate
        raw_secret = record.get("secret")
        sensitive_intermediate = int(raw_secret) * 2 if raw_secret is not None else 0
        aggregate_sum += sensitive_intermediate

        # Last use boundary: clear mutable sensitive field immediately after use
        record.clear()
        record.update({"redacted": True})

    result = {
        "aggregate_sum": aggregate_sum,
        "refused_to_retain": ["raw_secret", "raw_record"],
        "cleanup_boundary": "after per-record sensitive_intermediate computation",
        "erasure_limit": "container cleared; secure memory wiping not guaranteed",
    }
    assert all("secret" not in record for record in records)
    return result

records = [
    {"secret": "10", "other": "a"},
    {"secret": "20", "other": "b"},
]
report = compute_with_redaction(records)
assert report["aggregate_sum"] == 60
assert records == [{"redacted": True}, {"redacted": True}]
assert "10" not in repr(report) and "20" not in repr(report)
print(report)