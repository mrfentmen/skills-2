def make_list_delta(old_list, new_list, base_version):
    # Identify insertions by position and value
    operations = []
    old_index = 0
    new_index = 0
    while old_index < len(old_list) and new_index < len(new_list):
        if old_list[old_index] == new_list[new_index]:
            old_index += 1
            new_index += 1
        else:
            # Insertion detected at new_index
            operations.append(("insert", new_index, new_list[new_index]))
            new_index += 1
    # Remaining items in new_list are insertions at the end
    while new_index < len(new_list):
        operations.append(("insert", new_index, new_list[new_index]))
        new_index += 1
    return {"base_version": base_version, "operations": operations}

def apply_list_delta(base, patch, current_version):
    if patch["base_version"] != current_version:
        raise ValueError("stale base: request a fresh snapshot")
    result = list(base)  # Copy the base to avoid mutation
    for operation in patch["operations"]:
        kind, index, value = operation
        if kind == "insert":
            if index > len(result):
                raise ValueError(f"insert index out of bounds: {index}")
            result.insert(index, value)
        else:
            raise ValueError(f"unknown operation: {kind}")
    return result

# Example usage
old = [1, 2, 4]
new = [1, 2, 3, 4]
patch = make_list_delta(old, new, base_version=1)
rebuilt = apply_list_delta(old, patch, current_version=1)
assert rebuilt == new
assert old == [1, 2, 4]  # Caller's base remains untouched
print("operations:", patch["operations"], "reconstructed:", rebuilt == new)