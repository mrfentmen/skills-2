# Meta Senior Dev Stacked Diff: Refactor `safe_divide` utility with feature flag
# 1. Stacked-diff decomposition:
#    diff1: Introduce feature flag `safe_divide_v2` (default False)
#    diff2: Add new `safe_divide_v2` implementation with overflow guard
#    diff3: Migrate all 5 callers to v2 in one atomic commit
# 2. Monorepo atomicity: All 5 callers updated in diff3 (no broken contract)
# 3. Feature flag: `safe_divide_v2` gated; rollback path: flip flag to False
# 4. Fast feedback: Type hints + mypy incremental checks (sub-200ms)
# 5. Review-ready diff: <5 min review per diff; focused change per step

from typing import Optional
from dataclasses import dataclass

@dataclass
class Flags:
    safe_divide_v2: bool = False

def safe_divide(a: int, b: int, flags: Flags) -> Optional[float]:
    if flags.safe_divide_v2:
        # v2: guard against overflow and division by zero
        if b == 0:
            return None
        if a == -2**31 and b == -1:
            return None  # overflow guard
        return a / b
    else:
        # legacy: only guard against division by zero
        if b == 0:
            return None
        return a / b

# Updates all 5 callers in the same commit (monorepo atomicity)
def caller1(a: int, b: int, flags: Flags) -> Optional[float]:
    return safe_divide(a, b, flags)

def caller2(a: int, b: int, flags: Flags) -> Optional[float]:
    return safe_divide(a, b, flags)

def caller3(a: int, b: int, flags: Flags) -> Optional[float]:
    return safe_divide(a, b, flags)

def caller4(a: int, b: int, flags: Flags) -> Optional[float]:
    return safe_divide(a, b, flags)

def caller5(a: int, b: int, flags: Flags) -> Optional[float]:
    return safe_divide(a, b, flags)

# Demo output
if __name__ == "__main__":
    flags = Flags(safe_divide_v2=True)
    print(safe_divide(10, 2, flags))  # 5.0
    print(safe_divide(10, 0, flags))  # None
    print(safe_divide(-2147483648, -1, flags))  # None (overflow guard)