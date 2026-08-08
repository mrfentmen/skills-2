def drain_list(items, *, owns_items):
    if not isinstance(items, list):
        raise TypeError("owned list required")
    if not owns_items:
        copied = list(items)
        drain_list(copied, owns_items=True)
        return copied
    read = 0
    while read < len(items):
        value = items[read]
        print(value)
        read += 1
    del items[:]
    return items

owned = [1, 2, 3]
result = drain_list(owned, owns_items=True)
assert result is owned and owned == []
shared = [4, 5]
fallback = drain_list(shared, owns_items=False)
assert shared == [4, 5] and fallback == []
try:
    drain_list((1, 2), owns_items=True)
except TypeError as exc:
    assert str(exc) == "owned list required"
else:
    raise AssertionError("malformed buffer was mutated")
print({"owned": owned, "fallback": fallback})