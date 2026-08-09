def drain_list_in_place(items, *, owns_items):
    if not isinstance(items, list):
        raise TypeError("owned list required")
    if not owns_items:
        copied = list(items)
        drain_list_in_place(copied, owns_items=True)
        return copied
    while items:
        value = items.pop(0)
        print(value)
    return items

owned = [1, 2, 3]
result = drain_list_in_place(owned, owns_items=True)
assert result == [] and owned == []
shared = [4, 5, 6]
fallback = drain_list_in_place(shared, owns_items=False)
assert shared == [4, 5, 6] and fallback == []
try:
    drain_list_in_place((1, 2), owns_items=True)
except TypeError as exc:
    assert str(exc) == "owned list required"
else:
    raise AssertionError("malformed buffer was mutated")