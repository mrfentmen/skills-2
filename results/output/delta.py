# base_version=3; patch applies only to version 3
# insert operation: (insert, index, value) with precondition index in [0, len(base)]
# apply copies the base; caller's state remains untouched on failure
# reconstructed == target; otherwise reject the patch
# patch bytes >= snapshot bytes -> send snapshot instead
# version mismatch -> reject and request a fresh base

def make_insert_delta(base_version, index, value):
    return {"base_version": base_version, "operations": [("insert", index, value)]}

def apply_delta(base, patch, current_version):
    if patch["base_version"] != current_version:
        raise ValueError("stale base: request a fresh snapshot")
    result = list(base)  # copy; caller's base remains untouched
    for operation in patch["operations"]:
        kind, index, value = operation
        if kind != "insert":
            raise ValueError(f"unknown operation: {kind}")
        if not (0 <= index <= len(result)):
            raise ValueError(f"insert index out of range: {index}")
        result.insert(index, value)
    return result

def choose_patch_or_snapshot(new_state, patch):
    patch_size = len(repr(patch).encode("utf-8"))
    snapshot_size = len(repr(new_state).encode("utf-8"))
    return ("patch", patch) if patch_size < snapshot_size else ("snapshot", new_state)

base = ["a", "b", "c"]
target = ["a", "x", "b", "c"]
patch = make_insert_delta(base_version=3, index=1, value="x")
rebuilt = apply_delta(base, patch, current_version=3)
assert rebuilt == target
assert base == ["a", "b", "c"]  # apply was isolated
payload_kind, payload = choose_patch_or_snapshot(target, patch)
print("payload:", payload_kind, "patch_bytes:", len(repr(patch).encode("utf-8")),
      "snapshot_bytes:", len(repr(target).encode("utf-8")))
try:
    apply_delta(base, patch, current_version=2)
except ValueError as error:
    print("stale patch rejected:", error)
print("operations:", patch["operations"], "exact:", rebuilt == target)