def make_list_insert_delta(base_version, index, item):
    return {
        "base_version": base_version,
        "operations": [("insert", index, item)],
    }

def apply_list_insert_delta(base, patch, current_version):
    if patch["base_version"] != current_version:
        raise ValueError("stale base: request a fresh snapshot")
    result = list(base)
    for operation in patch["operations"]:
        kind, index, item = operation
        if kind != "insert":
            raise ValueError(f"unknown operation: {kind}")
        if not (0 <= index <= len(result)):
            raise ValueError(f"insert index out of range: {index}")
        result.insert(index, item)
    return result

base = ["a", "b", "c"]
patch = make_list_insert_delta(base_version=3, index=1, item="X")
rebuilt = apply_list_insert_delta(base, patch, current_version=3)
assert rebuilt == ["a", "X", "b", "c"]
assert base == ["a", "b", "c"]
try:
    apply_list_insert_delta(base, patch, current_version=2)
except ValueError as error:
    print("stale patch rejected:", error)
print("reconstructed:", rebuilt, "exact:", rebuilt == ["a", "X", "b", "c"])