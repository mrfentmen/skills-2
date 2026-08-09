class RingBuffer:
    """Fixed-size ring buffer. The obvious structure: a preallocated list and
    two indices. No cleverness, no wraparound math hidden in a class — the
    indices do the work and the size check is the only branch."""

    def __init__(self, capacity):
        # capacity must be positive; a zero-size buffer is a footgun
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.buf = [None] * capacity
        self.head = 0  # next write position
        self.tail = 0  # next read position
        self.size = 0  # number of valid elements
        self.capacity = capacity

    def push(self, item):
        """Add item, overwriting oldest if full. Returns the evicted item or None."""
        evicted = None
        if self.size == self.capacity:
            # full: overwrite the oldest, which is at tail
            evicted = self.buf[self.tail]
            self.tail = (self.tail + 1) % self.capacity
        else:
            self.size += 1
        self.buf[self.head] = item
        self.head = (self.head + 1) % self.capacity
        return evicted

    def pop(self):
        """Remove and return oldest item, or None if empty."""
        if self.size == 0:
            return None
        item = self.buf[self.tail]
        self.buf[self.tail] = None  # drop reference, helps GC
        self.tail = (self.tail + 1) % self.capacity
        self.size -= 1
        return item

    def __len__(self):
        return self.size

    def __iter__(self):
        # iterate in FIFO order without mutating; simple slice copy
        # is the obvious structure — no index juggling in the loop
        for i in range(self.size):
            yield self.buf[(self.tail + i) % self.capacity]


def main():
    # demo: push 5 into a 3-slot buffer, then drain
    rb = RingBuffer(3)
    for i in range(5):
        evicted = rb.push(i)
        if evicted is not None:
            print(f"push {i} evicted {evicted}")
        else:
            print(f"push {i}")

    print("contents:", list(rb))
    print("pop order:", [rb.pop() for _ in range(len(rb))])
    print("pop empty:", rb.pop())  # None, not an error

    # backward-compatibility: existing callers that only used push/pop/len
    # still work; __iter__ is additive, no behavior changed
    rb2 = RingBuffer(2)
    rb2.push("a")
    rb2.push("b")
    assert len(rb2) == 2
    assert rb2.pop() == "a"
    assert rb2.pop() == "b"
    assert rb2.pop() is None
    print("compat check passed")


if __name__ == "__main__":
    main()