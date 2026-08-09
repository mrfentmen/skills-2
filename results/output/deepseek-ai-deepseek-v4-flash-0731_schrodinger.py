class LazyEvenSquares:
    def __init__(self):
        self.forced = 0
        self._cache = []
        self._memoized = True

    def take(self, n):
        if self._memoized:
            start = len(self._cache)
            for _ in range(start, n):
                self.forced += 1
                number = len(self._cache)
                value = (2 * number) ** 2
                self._cache.append(value)
                yield value
        else:
            produced = 0
            number = 0
            while produced < n:
                self.forced += 1
                value = (2 * number) ** 2
                number += 1
                produced += 1
                yield value

lazy = LazyEvenSquares()
assert lazy.forced == 0
observed = list(lazy.take(5))
assert observed == [0, 4, 16, 36, 64]
assert lazy.forced == 5
print({"observed": observed, "forced": lazy.forced})