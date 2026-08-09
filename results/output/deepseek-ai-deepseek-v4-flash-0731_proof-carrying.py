def produce_sorted(xs, input_id):
    if not xs:
        raise ValueError("empty input has no sorted result")
    result = sorted(xs)
    certificate = {
        "kind": "sorted-v1",
        "input_id": input_id,
        "length": len(xs),
        "multiset": sorted(xs),
        "result": result,
    }
    ok, reason = verify_sorted(xs, result, certificate, input_id)
    if not ok:
        raise AssertionError(reason)
    return result, certificate

def verify_sorted(xs, result, certificate, input_id):
    required = {"kind", "input_id", "length", "multiset", "result"}
    if set(certificate) != required or certificate["kind"] != "sorted-v1":
        return False, "unsupported certificate schema"
    if certificate["input_id"] != input_id or certificate["length"] != len(xs) or not xs:
        return False, "length mismatch or empty input"
    if result != certificate["result"]:
        return False, "result and certificate disagree"
    if len(result) != len(xs):
        return False, "result length mismatch"
    if any(result[i] > result[i + 1] for i in range(len(result) - 1)):
        return False, "result is not sorted"
    if certificate["multiset"] != sorted(xs):
        return False, "multiset witness does not match input"
    if result != certificate["multiset"]:
        return False, "result is not a permutation of input"
    return True, "accepted"

xs = [3, 1, 2]
result, certificate = produce_sorted(xs, "dataset-7")
ok, reason = verify_sorted(xs, result, certificate, "dataset-7")
assert ok and reason == "accepted"
tampered = [3, 2, 1]
ok, _ = verify_sorted(xs, tampered, certificate, "dataset-7")
assert not ok
bad_schema = dict(certificate, kind="sorted-v0")
ok, _ = verify_sorted(xs, result, bad_schema, "dataset-7")
assert not ok
assert not verify_sorted(xs, result, certificate, "stale-dataset")[0]
print({"result": result, "certificate": certificate, "status": "verified"})