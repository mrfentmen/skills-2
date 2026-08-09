# Simple ring buffer: the obvious structure is a fixed-size list with head/tail indices
# Good taste simplification: no clever modulo tricks; use bitmask for power-of-two sizes
# Backward compatibility: existing callers see the same interface (append, pop, peek)
# No unexplained magic: every line is justified; no silent failures

class RingBuffer:
    def __init__(self, size):
        if size <= 0 or (size & (size - 1)) != 0:
            raise ValueError("size must be a positive power of two")
        self.buf = [None] * size
        self.head = 0
        self.tail = 0
        self.mask = size - 1  # bitmask for power-of-two size

    def append(self, item):
        self.buf[self.tail & self.mask] = item
        self.tail += 1

    def pop(self):
        if self.head == self.tail:
            raise IndexError("pop from empty buffer")
        item = self.buf[self.head & self.mask]
        self.head += 1
        return item

    def peek(self):
        if self.head == self.tail:
            raise IndexError("peek from empty buffer")
        return self.buf[self.head & self.mask]

    def __len__(self):
        return self.tail - self.head

# Working entry point: demo the ring buffer with a power-of-two size
if __name__ == "__main__":
    rb = RingBuffer(4)
    rb.append(1)
    rb.append(2)
    rb.append(3)
    print("peek:", rb.peek())  # 1
    print("pop:", rb.pop())    # 1
    print("len:", len(rb))     # 2
    rb.append(4)
    rb.append(5)
    print("len after append:", len(rb))  # 4
    print("pop:", rb.pop())    # 2
    print("pop:", rb.pop())    # 3
    print("pop:", rb.pop())    # 4
    print("pop:", rb.pop())    # 5
    try:
        rb.pop()
    except IndexError as e:
        print("expected error:", e)  # pop from empty buffer