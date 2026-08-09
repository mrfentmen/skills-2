from itertools import count

class LazyEvenSquares:
    def __init__(self):
        self.forced = 0

    def take(self, n):
        def even_squares():
            for i in count():
                self.forced += 1
                yield (2 * i) ** 2

        gen = even_squares()
        result = []
        for _ in range(n):
            result.append(next(gen))
        return result

lazy = LazyEvenSquares()
assert lazy.forced == 0
observed = lazy.take(5)
assert observed == [0, 4, 16, 36, 64]
assert lazy.forced == 5
print({"observed": observed, "forced": lazy.forced})