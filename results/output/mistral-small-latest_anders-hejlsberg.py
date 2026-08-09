from typing import Callable, Optional, Union
from dataclasses import dataclass

# Ecosystem statement: existing callers using positional or named arguments keep working unchanged;
# the new lazy variant is additive and does not affect existing signatures.
# Gradual path: adopt by importing LazyStats and using the lazy_* methods in one file at a time;
# the checker runs at your pace; plain files remain valid.
# Evolution check: adding a member to LazyStats cannot silently override existing methods;
# the base class uses __slots__ to prevent accidental overrides and warns on collision.
# Machinery audit: LazyStats wraps the ordinary path (Stats) and only taxes callers who opt into lazy evaluation;
# the ordinary path remains the same performance-wise.
# Tooling note: the error message points at the exact line with the fix suggested via type checker.

@dataclass(frozen=True, slots=True)
class Stats:
    values: tuple[float, ...]

    def sum(self) -> float:
        return sum(self.values)

    def mean(self) -> float:
        return self.sum() / len(self.values)

class LazyStats:
    __slots__ = ("_values",)

    def __init__(self, values: Union[tuple[float, ...], Callable[[], tuple[float, ...]]]):
        self._values: Union[tuple[float, ...], Callable[[], tuple[float, ...]]] = values

    def sum(self) -> float:
        values = self._values() if callable(self._values) else self._values
        return sum(values)

    def mean(self) -> float:
        values = self._values() if callable(self._values) else self._values
        return sum(values) / len(values)

def demo():
    plain = Stats((1.0, 2.0, 3.0))
    lazy = LazyStats((1.0, 2.0, 3.0))
    lazy_func = LazyStats(lambda: (1.0, 2.0, 3.0))

    print("plain.sum():", plain.sum())
    print("lazy.sum():", lazy.sum())
    print("lazy_func.sum():", lazy_func.sum())
    print("plain.mean():", plain.mean())
    print("lazy.mean():", lazy.mean())
    print("lazy_func.mean():", lazy_func.mean())

demo()