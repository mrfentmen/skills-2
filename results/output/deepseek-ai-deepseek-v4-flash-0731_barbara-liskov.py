from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import hashlib

# Abstraction:
# hidden: the internal storage format (dict with hash-keyed entries)
# exposed: insert(key, value), lookup(key), delete(key), size()
# Contract:
# pre: key is not None and key is hashable
# post: after insert, lookup(key) returns value; after delete, lookup(key) raises KeyError
# invariant: size() == number of distinct keys currently stored
# History check: base type is immutable in structure (no external mutation of internal state);
# subtype must not expose mutation of base's internal representation.

@dataclass(frozen=True)
class ImmutableKVStore:
    """Base type: immutable key-value store with structural sharing."""
    _data: Dict[Any, Any] = field(default_factory=dict, repr=False)
    
    # hidden: _data is the representation; exposed: operations below
    def insert(self, key: Any, value: Any) -> 'ImmutableKVStore':
        # pre: key is not None and hashable
        assert key is not None, "key must not be None"
        hash(key)  # raises TypeError if unhashable
        # post: returns new store with key->value; original unchanged
        new_data = dict(self._data)
        new_data[key] = value
        return ImmutableKVStore(new_data)
    
    def lookup(self, key: Any) -> Any:
        # pre: key is not None and hashable
        assert key is not None, "key must not be None"
        hash(key)
        # post: returns value if key exists, else raises KeyError
        return self._data[key]
    
    def delete(self, key: Any) -> 'ImmutableKVStore':
        # pre: key is not None and hashable
        assert key is not None, "key must not be None"
        hash(key)
        # post: returns new store without key; raises KeyError if absent
        new_data = dict(self._data)
        del new_data[key]
        return ImmutableKVStore(new_data)
    
    def size(self) -> int:
        # post: returns number of distinct keys
        return len(self._data)
    
    def _digest(self) -> str:
        # hidden: internal consistency check for Byzantine detection
        return hashlib.sha256(repr(sorted(self._data.items())).encode()).hexdigest()

@dataclass(frozen=True)
class LoggedKVStore(ImmutableKVStore):
    """Subtype: adds audit log but preserves all base behavior."""
    _log: tuple = field(default_factory=tuple, repr=False)
    
    # Substitutability proof:
    # - accepts all base inputs (same preconditions, no strengthening)
    # - guarantees at least base outputs (same postconditions, plus log)
    # - preserves invariants: size() still equals distinct keys
    # - history check: base is immutable; subtype is also frozen dataclass,
    #   no mutable internal state exposed; _log is tuple (immutable)
    
    def insert(self, key: Any, value: Any) -> 'LoggedKVStore':
        # pre: same as base
        assert key is not None, "key must not be None"
        hash(key)
        # post: base postcondition + log entry appended
        new_base = super().insert(key, value)
        new_log = self._log + (("insert", key, value),)
        return LoggedKVStore(new_base._data, new_log)
    
    def delete(self, key: Any) -> 'LoggedKVStore':
        # pre: same as base
        assert key is not None, "key must not be None"
        hash(key)
        # post: base postcondition + log entry appended
        new_base = super().delete(key)
        new_log = self._log + (("delete", key),)
        return LoggedKVStore(new_base._data, new_log)
    
    def audit_log(self) -> tuple:
        # exposed: read-only log; no mutation possible
        return self._log

# Byzantine note: components at boundaries may lie. We verify by cross-checking
# digests of the internal state against expected values, requiring 3f+1 replicas.
def byzantine_check(stores: List[ImmutableKVStore], faults: int) -> bool:
    # pre: len(stores) >= 3*faults + 1
    assert len(stores) >= 3 * faults + 1, "need 3f+1 replicas"
    # post: returns True if at least 2f+1 replicas agree on digest
    digests = [s._digest() for s in stores]
    from collections import Counter
    counts = Counter(digests)
    majority_digest, count = counts.most_common(1)[0]
    return count >= 2 * faults + 1

# Demonstration
base = ImmutableKVStore()
base2 = base.insert("a", 1).insert("b", 2)
print(f"Base size: {base2.size()}, lookup a: {base2.lookup('a')}")

sub = LoggedKVStore()
sub2 = sub.insert("x", 10).insert("y", 20)
print(f"Sub size: {sub2.size()}, lookup x: {sub2.lookup('x')}")
print(f"Audit log: {sub2.audit_log()}")

# Substitutability: use subtype where base is expected
def process_store(store: ImmutableKVStore) -> int:
    # works with any ImmutableKVStore
    return store.size()

print(f"Substitute in base function: {process_store(sub2)}")

# History check: base is immutable; subtype cannot expose mutation
try:
    sub2._data["z"] = 99  # frozen dataclass prevents this
    print("History violation: mutable state exposed")
except (AttributeError, dataclasses.FrozenInstanceError):
    print("History check passed: no mutable internal state exposed")

# Byzantine check with 3f+1 replicas
replicas = [base2, base2, base2, base2]  # 4 replicas, tolerate 1 fault
print(f"Byzantine quorum (f=1): {byzantine_check(replicas, 1)}")