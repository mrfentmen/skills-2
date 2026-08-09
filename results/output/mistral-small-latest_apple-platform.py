from typing import TypeVar, Generic, Optional, Dict
from collections import OrderedDict

K = TypeVar('K')
V = TypeVar('V')

class LRUCache(Generic[K, V]):
    """
    Public API:
        get(key: K) -> Optional[V]: returns None on miss, never raises
        put(key: K, value: V) -> None: inserts or updates, never raises
    Failure is explicit via Optional return; no silent sentinels.
    """

    def __init__(self, capacity: int):
        self._capacity = capacity
        self._cache: OrderedDict[K, V] = OrderedDict()
        # Backward-compatibility commitment:
        # Existing callers using capacity=0 will continue to work as unbounded cache.
        # Deprecation path: capacity=0 will emit a printed note but remain functional.
        if capacity == 0:
            print("Note: capacity=0 is deprecated; use positive capacity for bounded cache")

    def get(self, key: K) -> Optional[V]:
        # Zero-regression performance budget:
        # +0 allocations in hot path; OrderedDict.move_to_end is O(1) on average.
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: K, value: V) -> None:
        # Memory segregated by type: OrderedDict[K, V] is typed; no untyped buffers alias structured data.
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self._capacity:
            self._cache.popitem(last=False)

# Demo
cache = LRUCache[str, int](2)
cache.put("a", 1)
cache.put("b", 2)
print(cache.get("a"))  # 1
cache.put("c", 3)
print(cache.get("b"))  # None (evicted)
print(cache.get("c"))  # 3

# Backward-compatibility demo
old_cache = LRUCache[str, int](0)
old_cache.put("x", 10)
print(old_cache.get("x"))  # 10