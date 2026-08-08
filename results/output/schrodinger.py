from itertools import count

class LazyEvenSquares:
    def __init__(self):
        self.forced = 0

    def take(self, n):
        def even_numbers():
            for i in count():
                if i % 2 == 0:
                    yield i

        evens = even_numbers()
        for _ in range(n):
            self.forced += 1
            value = next(evens) ** 2
            yield value

lazy = LazyEvenSquares()
assert lazy.forced == 0              # construction did no work
observed = list(lazy.take(5))
assert observed == [0, 4, 16, 36, 64]
assert lazy.forced == 5               # demand stopped after 5 items
print({"observed": observed, "forced": lazy.forced})