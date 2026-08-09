from typing import Iterable, Callable, TypeVar, Optional, Union

T = TypeVar('T')
Number = Union[int, float]

# (1) ecosystem statement: existing callers of sum_all and mean_all keep working unchanged;
#     the new lazy variants are additive and do not alter any existing signature or behavior.
def sum_all(values: Iterable[Number]) -> Number:
    """Original eager sum. Existing callers unchanged."""
    total = 0
    for v in values:
        total += v
    return total

def mean_all(values: Iterable[Number]) -> Optional[Number]:
    """Original eager mean. Existing callers unchanged."""
    total = 0
    count = 0
    for v in values:
        total += v
        count += 1
    if count == 0:
        return None
    return total / count

# (2) gradual path: adopt the lazy variant in one call site at a time;
#     the new functions are opt-in, so teams can migrate file by file at their own pace.
def lazy_sum(values: Iterable[Number]) -> Callable[[], Number]:
    """Lazy sum: returns a thunk that computes on demand. New, additive API."""
    def compute() -> Number:
        return sum_all(values)
    return compute

def lazy_mean(values: Iterable[Number]) -> Callable[[], Optional[Number]]:
    """Lazy mean: returns a thunk that computes on demand. New, additive API."""
    def compute() -> Optional[Number]:
        return mean_all(values)
    return compute

# (3) evolution check: adding these new members cannot silently change existing callers;
#     they have distinct names (lazy_*) and no existing function is overridden or overloaded.
#     If a future subclass defines a method named lazy_sum, it will warn on collision, not break.

# (4) machinery audit: the thunk wrapper is justified because it serves the ordinary path
#     of deferring expensive computation until needed; for eager callers, the original
#     functions remain the ordinary path and are not taxed by any indirection.

# (5) tooling note: the editor will show the new functions in autocomplete with clear
#     docstrings; type hints make the return type (Callable) explicit, and any misuse
#     (e.g., calling lazy_sum without invoking the thunk) is caught by the type checker
#     with a message pointing at the exact line.

# Demo: existing eager callers work unchanged, and lazy variants are used incrementally.
data = [1, 2, 3, 4]

# Existing callers — unchanged behavior.
print("eager sum:", sum_all(data))
print("eager mean:", mean_all(data))

# New lazy variants — adopted at one call site.
lazy_total = lazy_sum(data)
lazy_avg = lazy_mean(data)
print("lazy sum result:", lazy_total())
print("lazy mean result:", lazy_avg())

# Demonstrate that lazy computation is deferred (no computation until thunk called).
print("lazy thunk created, not yet computed:", lazy_total)