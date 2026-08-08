class LazyEvenSquares:
    """Lazy stream of even squares (0, 4, 16, 36, ...).

    Construction performs no work. Iteration forces computation one item at a time.
    The stream is single-use: each iteration consumes the produced value and advances
    the internal counter. Repeated iteration will continue from where it left off.
    """

    def __init__(self, limit=None):
        """Create a lazy even‑square stream.

        Args:
            limit: Optional maximum number of items to produce. If None, the stream is infinite.
        """
        self.limit = limit
        self.forced = 0  # counter of how many squares have been forced

    def __iter__(self):
        """Generator that yields even squares on demand."""
        n = 0
        while True:
            if self.limit is not None and n >= self.limit:
                break
            # Force the next even square
            self.forced += 1
            value = (2 * n) ** 2
            yield value
            n += 1


# Demonstration: compute the first 5 even squares lazily
lazy = LazyEvenSquares(limit=5)  # construction does no work
assert lazy.forced == 0, "Construction should not force any work"

observed = []
for val in lazy:
    observed.append(val)

# After forcing exactly 5 items, the counter should reflect that
assert lazy.forced == 5, f"Expected 5 forced items, got {lazy.forced}"
assert observed == [0, 4, 16, 36, 64], f"Unexpected output: {observed}"

# Output the result and the forced count for verification
print({"observed": observed, "forced": lazy.forced})