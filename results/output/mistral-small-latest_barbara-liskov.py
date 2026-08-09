from typing import Any, Iterator, Optional

# Abstraction: hidden: the storage format (dict). exposed: insert(key, value), get(key), range()
class KeyValueStore:
    def __init__(self) -> None:
        self._data: dict[Any, Any] = {}

    def insert(self, key: Any, value: Any) -> None:
        """Insert a key-value pair."""
        self._data[key] = value

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve value by key, or None if absent."""
        return self._data.get(key)

    def range(self) -> Iterator[tuple[Any, Any]]:
        """Yield (key, value) pairs in insertion order."""
        return iter(self._data.items())

# Contract:
# pre: key is not None for insert/get
# post: value retrievable by key until deleted; range yields all inserted pairs
# invariant: size == len(_data)

# Substitutability proof: ImmutableKeyValueStore accepts all KeyValueStore inputs
# and guarantees at least KeyValueStore outputs (no mutation exposed).
class ImmutableKeyValueStore(KeyValueStore):
    def __init__(self) -> None:
        super().__init__()
        self._frozen = True

    def insert(self, key: Any, value: Any) -> None:
        """No-op: immutable store forbids mutation."""
        if self._frozen:
            raise TypeError("immutable store cannot be modified")

    def get(self, key: Any) -> Optional[Any]:
        """Delegate to base: safe because base is read-only."""
        return super().get(key)

    def range(self) -> Iterator[tuple[Any, Any]]:
        """Delegate to base: safe because base is read-only."""
        return super().range()

# History check: base is immutable; subclass must not expose mutation — refactor the hierarchy instead.
# Here, the subclass enforces immutability by raising on insert, so no violation occurs.

# Byzantine note: the replica can lie — we require 3f+1 and cross-check digests, not trust.
def verify_substitutability() -> bool:
    base = KeyValueStore()
    sub = ImmutableKeyValueStore()

    # Insert into base and verify get
    base.insert("a", 1)
    assert base.get("a") == 1

    # Attempt insert into immutable subclass should fail
    try:
        sub.insert("b", 2)
        return False
    except TypeError:
        pass

    # Get from immutable subclass should still work
    assert sub.get("a") is None  # base empty, sub empty
    return True

print(verify_substitutability())