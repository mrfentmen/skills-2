def produce_sorted_pair(xs):
    """
    Claim: The result is a sorted pair of the two largest distinct values in xs.
    Witness fields:
      - kind: schema version ("sorted-pair-v1")
      - input_length: length of xs at time of signing
      - input_digest: SHA-256 digest of xs (immutable content binding)
      - first: largest value
      - second: second largest value
    Guarantee: first >= second, both appear in xs, and no value in xs exceeds first.
    """
    if len(xs) < 2:
        raise ValueError("input must contain at least two elements")

    # Producer computes the two largest distinct values
    unique = sorted(set(xs), reverse=True)
    first, second = unique[0], unique[1]

    # Canonical digest of the input content
    import hashlib
    digest = hashlib.sha256(bytes(str(xs), 'utf-8')).hexdigest()

    result = {"first": first, "second": second}
    certificate = {
        "kind": "sorted-pair-v1",
        "input_length": len(xs),
        "input_digest": digest,
        "first": first,
        "second": second,
    }
    ok, reason = verify_sorted_pair(xs, result, certificate)
    if not ok:
        raise AssertionError(f"certificate rejected: {reason}")
    return result, certificate

def verify_sorted_pair(xs, result, certificate):
    """
    Independent verifier: checks witness against input and certificate fields.
    Does NOT recompute the two largest values; instead validates the witness.
    """
    required = {"kind", "input_length", "input_digest", "first", "second"}
    if set(certificate) != required or certificate["kind"] != "sorted-pair-v1":
        return False, "unsupported certificate schema"

    if certificate["input_length"] != len(xs):
        return False, "input length mismatch"

    # Recompute digest to ensure content binding
    import hashlib
    digest = hashlib.sha256(bytes(str(xs), 'utf-8')).hexdigest()
    if certificate["input_digest"] != digest:
        return False, "input content altered"

    first = certificate["first"]
    second = certificate["second"]

    if result != {"first": first, "second": second}:
        return False, "result does not match certificate"

    if first < second:
        return False, "first must be >= second"

    if first not in xs or second not in xs:
        return False, "claimed values not present in input"

    if any(v > first for v in xs):
        return False, "witness violates maximality"

    return True, "accepted"

# Valid case
xs = [3, 1, 4, 1, 5, 9, 2, 6]
result, certificate = produce_sorted_pair(xs)
ok, reason = verify_sorted_pair(xs, result, certificate)
assert ok and reason == "accepted"

# Tampered result
tampered_result = {"first": 9, "second": 7}
ok, _ = verify_sorted_pair(xs, tampered_result, certificate)
assert not ok

# Tampered certificate (wrong digest)
import hashlib
tampered_digest = hashlib.sha256(bytes(str(xs[:-1] + [0]), 'utf-8')).hexdigest()
tampered_cert = dict(certificate, input_digest=tampered_digest)
ok, _ = verify_sorted_pair(xs, result, tampered_cert)
assert not ok

# Unsupported schema version
unsupported_cert = dict(certificate, kind="sorted-pair-v0")
ok, _ = verify_sorted_pair(xs, result, unsupported_cert)
assert not ok

# Altered input length
bad_length_cert = dict(certificate, input_length=len(xs) + 1)
ok, _ = verify_sorted_pair(xs, result, bad_length_cert)
assert not ok

print({"result": result, "certificate": certificate, "status": "verified"})