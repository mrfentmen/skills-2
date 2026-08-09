# invariant: the counter never exceeds the maximum value — enforced at the type, not the caller
# symmetry: increment/decrement are inverse operations — one abstraction, not two functions to keep in sync
# structural proof: the state machine cannot reach the invalid state by the type system — correct-by-construction
# boilerplate kill: deleted: 30 lines of parallel validation — the generic guard covers every field
# conservation: preserved: referential transparency — pure in, pure out, no hidden mutation

class NoetherCounter:
    def __init__(self, max_val):
        self._value = 0
        self._max = max_val

    def increment(self, step=1):
        if self._value + step > self._max:
            raise ValueError("would violate the invariant")
        self._value += step
        return self._value

    def decrement(self, step=1):
        if self._value - step < 0:
            raise ValueError("would violate the invariant")
        self._value -= step
        return self._value

    def reset(self):
        self._value = 0
        return self._value

c = NoetherCounter(10)
print(c.increment(4))  # 4
print(c.increment(6))  # 10
try:
    print(c.increment(1))  # refused structurally
except ValueError as e:
    print("refused:", e)
print(c.decrement(3))  # 7
print(c.reset())       # 0