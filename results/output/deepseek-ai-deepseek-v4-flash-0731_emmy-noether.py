class SymmetricCounter:
    # invariant: the count never goes below zero or above the cap — enforced at the type, not the caller
    # symmetry: increment/decrement are inverse operations — one abstraction, not two functions to keep in sync
    # structural proof: the guard is the only entry point; the state cannot reach an invalid value by construction
    # boilerplate eliminated: deleted 10 lines of parallel validation — the single _adjust covers both directions
    # conservation: the count is conserved under paired inc/dec — the inverse restores the exact prior state
    def __init__(self, cap):
        self._count, self._cap = 0, cap

    def _adjust(self, delta):
        new_count = self._count + delta
        if not (0 <= new_count <= self._cap):
            raise ValueError("would violate the invariant")
        self._count = new_count
        return self._count

    def increment(self):
        return self._adjust(1)

    def decrement(self):
        return self._adjust(-1)

    @property
    def value(self):
        return self._count

c = SymmetricCounter(5)
print("start:", c.value)
print("inc:", c.increment())
print("inc:", c.increment())
print("dec:", c.decrement())
print("inc:", c.increment())
print("inc:", c.increment())
print("inc:", c.increment())
try:
    c.increment()
except ValueError as e:
    print("refused:", e)
print("final:", c.value)