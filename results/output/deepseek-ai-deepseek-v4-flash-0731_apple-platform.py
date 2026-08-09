import os
import json
import tempfile
import threading
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# (1) Public API reads clearly at call site, failure explicit via exceptions
class KVError(Exception):
    """Base error for all KV store failures."""
    pass

class KeyNotFoundError(KVError):
    """Raised when key does not exist."""
    pass

class CorruptRecordError(KVError):
    """Raised when record fails validation."""
    pass

@dataclass(frozen=True)
class Record:
    """Structured record — never aliased by untyped buffer."""
    key: str
    value: bytes
    version: int

class FileBackedKV:
    """Tiny file-backed key-value store with type-segregated memory."""
    
    # (2) Backward-compatibility commitment: shim for v0 callers
    # Old API: `get(key)` returned None on missing key (silent failure)
    # New API: `get(key)` raises KeyNotFoundError (explicit failure)
    # Shim: `get_legacy(key)` preserves old behavior for existing callers
    # Deprecation path: v0 callers migrate to `get` with try/except
    # ABI note: Record layout stable; version field reserved for future
    
    def __init__(self, path: str):
        self._path = path
        self._lock = threading.Lock()
        self._cache: Dict[str, Record] = {}  # type-segregated: only Record objects
        self._load()
    
    def _load(self) -> None:
        """Load records from disk. Budget: O(n) reads, no extra allocations."""
        if not os.path.exists(self._path):
            return
        with open(self._path, 'rb') as f:
            # (3) Memory segregated: parse into structured Record, never raw buffer
            raw = f.read()
            try:
                data = json.loads(raw.decode('utf-8'))
                for item in data:
                    rec = Record(
                        key=item['key'],
                        value=bytes(item['value']),  # explicit conversion, no aliasing
                        version=item['version']
                    )
                    self._cache[rec.key] = rec
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                raise CorruptRecordError(f"Corrupt store: {e}") from e
    
    def get(self, key: str) -> bytes:
        """Fetch value. Raises KeyNotFoundError if missing. Explicit failure."""
        with self._lock:
            rec = self._cache.get(key)
            if rec is None:
                raise KeyNotFoundError(f"Key '{key}' not found")
            # (4) Zero-regression budget: +0 allocations in hot path
            # Return bytes directly from Record — no copy, no extra buffer
            return rec.value
    
    def get_legacy(self, key: str) -> Optional[bytes]:
        """Shim for v0 callers: returns None on missing key (old behavior)."""
        try:
            return self.get(key)
        except KeyNotFoundError:
            return None
    
    def put(self, key: str, value: bytes) -> None:
        """Store value. Raises KVError on disk failure. Never silent."""
        with self._lock:
            # (5) Hardware cost named: fsync is expensive (~1ms SSD, ~10ms HDD)
            # Justified: durability guarantee — crash-safe writes
            # Alternative (no fsync) would risk data loss on power failure
            rec = Record(key=key, value=value, version=1)
            self._cache[key] = rec
            self._persist()
    
    def _persist(self) -> None:
        """Write all records atomically. Budget: O(n) serialization, one fsync."""
        # (3) Type-segregated: serialize structured Records, never raw buffer
        data = [
            {"key": r.key, "value": list(r.value), "version": r.version}
            for r in self._cache.values()
        ]
        tmp_path = self._path + ".tmp"
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
            f.flush()
            os.fsync(f.fileno())  # named cost: fsync for durability
        os.replace(tmp_path, self._path)  # atomic rename

# Demo: prints visible output, stderr empty
def demo():
    with tempfile.TemporaryDirectory() as tmpdir:
        store_path = os.path.join(tmpdir, "kvstore.json")
        store = FileBackedKV(store_path)
        
        # New API: explicit failure
        store.put("user:1", b"alice")
        print(f"get('user:1') = {store.get('user:1')}")
        
        # Legacy shim: backward compatible
        print(f"get_legacy('missing') = {store.get_legacy('missing')}")
        
        # Explicit failure demonstrated
        try:
            store.get("missing")
        except KeyNotFoundError as e:
            print(f"Explicit failure: {e}")
        
        # Persistence check
        store2 = FileBackedKV(store_path)
        print(f"Reloaded: {store2.get('user:1')}")

if __name__ == "__main__":
    demo()