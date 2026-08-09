def drain_and_print(items, *, owns_items):
    if not isinstance(items, list):
        raise TypeError("owned list required")
    if not owns_items:
        copied = list(items)
        drain_and_print(copied, owns_items=True)
        return copied
    read = 0
    while read < len(items):
        print(items[read])
        read += 1
    del items[:]
    return items

owned = [1, 2, 3]
result = drain_and_print(owned, owns_items=True)
assert result is owned and owned == []
shared = [4, 5]
fallback = drain_and_print(shared, owns_items=False)
assert shared == [4, 5] and fallback == []
try:
    drain_and_print("abc", owns_items=True)
except TypeError as exc:
    assert str(exc) == "owned list required"
else:
    raise AssertionError("malformed buffer was mutated")
print({"owned": owned, "fallback": fallback})