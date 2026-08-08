def produce_maximum(xs, input_id):
    if not xs:
        raise ValueError("empty input has no maximum")
    index, value = 0, xs[0]
    for candidate_index in range(1, len(xs)):
        if xs[candidate_index] > value:
            index, value = candidate_index, xs[candidate_index]
    result = {"value": value, "index": index}
    certificate = {
        "kind": "maximum-v1",
        "input_id": input_id,
        "length": len(xs),
        "index": index,
        "value": value,
    }
    ok, reason = verify_maximum(xs, result, certificate, input_id)
    if not ok:
        raise AssertionError(reason)
    return result, certificate

def verify_maximum(xs, result, certificate, input_id):
    # Independent witness check: no max(), sorting, or producer call.
    required = {"kind", "input_id", "length", "index", "value"}
    if set(certificate) != required or certificate["kind"] != "maximum-v1":
        return False, "unsupported certificate schema"
    if certificate["input_id"] != input_id or certificate["length"] != len(xs) or not xs:
        return False, "length mismatch or empty input"
    index = certificate["index"]
    value = certificate["value"]
    if not isinstance(index, int) or not 0 <= index < len(xs):
        return False, "index out of range"
    if result != {"value": value, "index": index}:
        return False, "result and certificate disagree"
    if xs[index] != value:
        return False, "witness does not point at claimed value"
    if any(other > value for position, other in enumerate(xs) if position != index):
        return False, "witness is not maximal"
    return True, "accepted"

xs = [4, 9, 2, 9, 1]
result, certificate = produce_maximum(xs, "dataset-7")
ok, reason = verify_maximum(xs, result, certificate, "dataset-7")
assert ok and reason == "accepted"
# Mutation, unsupported schema, and a stale version are rejected without rerunning the producer.
tampered = {"value": 99, "index": certificate["index"]}
ok, _ = verify_maximum(xs, tampered, certificate, "dataset-7")
assert not ok
bad_schema = dict(certificate, kind="maximum-v0")
ok, _ = verify_maximum(xs, result, bad_schema, "dataset-7")
assert not verify_maximum(xs, result, certificate, "stale-dataset")[0]
assert not ok
print({"result": result, "certificate": certificate, "status": "verified"})