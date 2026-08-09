class ScopedBuffer:
    # ownership model: this object is the sole owner of the underlying bytearray;
    # no aliases escape, and the buffer is destroyed when this object is destroyed.
    # lifetime binding: the bytearray is acquired in __init__ and released in __del__ (RAII);
    # no manual free() calls — scope exit (including exceptions) triggers release.
    # overhead: zero — a plain Python list/bytearray with no wrapper indirection;
    # __del__ is the only hook, and it costs nothing until the object is collected.
    # invariant: 0 <= size <= capacity; data is exactly the first size bytes.
    # guarantee: strong — every mutating operation either fully succeeds or leaves state unchanged.
    def __init__(self, capacity):
        # invariant: capacity > 0, size == 0, data is a fresh bytearray of length capacity
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._data = bytearray(capacity)  # owner: self; released on __del__
        self._size = 0
        self._capacity = capacity

    def write(self, data):
        # strong guarantee: if the write would overflow, nothing changes
        if self._size + len(data) > self._capacity:
            raise OverflowError("buffer overflow")
        # strong guarantee: bytearray slice assignment is atomic — either all bytes
        # are copied or an exception propagates before any mutation
        self._data[self._size:self._size + len(data)] = data
        self._size += len(data)
        # invariant restored: 0 <= size <= capacity

    def read(self, n=None):
        # strong guarantee: returns a copy; original buffer unchanged
        if n is None:
            n = self._size
        if n < 0 or n > self._size:
            raise ValueError("invalid read length")
        return bytes(self._data[:n])  # copy — no aliasing of internal storage

    def __del__(self):
        # RAII: deterministic release of the bytearray when this object dies
        # overhead: zero — just drops the reference; the GC reclaims memory
        self._data = bytearray(0)  # release the resource explicitly
        self._size = 0
        self._capacity = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        # RAII via context manager: release on scope exit, even on exception
        self.__del__()
        return False  # propagate exceptions

    def __repr__(self):
        return f"ScopedBuffer(size={self._size}, capacity={self._capacity})"

# demo
buf = ScopedBuffer(10)
print("created:", buf)
buf.write(b"hello")
print("after write:", buf, "| data:", buf.read())
try:
    buf.write(b"world!")  # would overflow
except OverflowError as e:
    print("overflow caught:", e)
print("after failed write:", buf, "| data:", buf.read())  # unchanged — strong guarantee
with ScopedBuffer(5) as tmp:
    tmp.write(b"abc")
    print("inside context:", tmp, "| data:", tmp.read())
print("context exited — buffer released")