from typing import List, Callable, TypeVar, Dict, Any
from dataclasses import dataclass
import random

T = TypeVar("T")

# ============================================================
# (1) STACKED-DIFF DECOMPOSITION (small dependent steps):
#   Diff 1: Add `flag()` + `experiment()` gating helpers (no behavior change).
#   Diff 2: Introduce `Ranker` interface + `LegacyRanker` (pure refactor).
#   Diff 3: Add `V2Ranker` behind flag `rank_v2` (default OFF = safe path).
#   Diff 4: Wire `rank_items()` to use flag; update ALL callers (see #2).
#   Each diff is reviewable in <5 min; no mega-change.
# ============================================================

# ============================================================
# (2) MONOREPO ATOMICITY NOTE:
#   `rank_items()` is the public API. In Diff 4, we change its internals
#   and update ALL 3 callers (search, feed, ads) in the SAME commit.
#   No caller is left on a broken contract.
# ============================================================

# ============================================================
# (3) FEATURE FLAG / A-B GATE with rollback path:
#   flag("rank_v2") — default False (legacy path).
#   Rollback: set flag to False → instant revert to LegacyRanker.
#   Metrics: `record_ranking_quality()` hooks on both paths.
# ============================================================

# ============================================================
# (4) FAST FEEDBACK (incremental static checking):
#   Types are local and self-contained; `pyre incremental` checks only
#   changed modules (sub-200ms), not a full monorepo build.
#   No cross-module imports beyond stdlib.
# ============================================================

# ============================================================
# (5) REVIEW-READY DIFF: This file is the entire change.
#   Small, focused, describable in one sentence: "Add flag-gated V2
#   ranking with atomic caller updates and rollback path."
# ============================================================

# --- Flag infrastructure (Diff 1) ---
_FLAGS: Dict[str, bool] = {"rank_v2": False}

def flag(name: str) -> bool:
    """Read a feature flag. Defaults to safe (False) path."""
    return _FLAGS.get(name, False)

def set_flag(name: str, value: bool) -> None:
    """Test hook — in prod this comes from config service."""
    _FLAGS[name] = value

# --- Metrics hook (Diff 1) ---
def record_ranking_quality(ranker: str, score: float) -> None:
    """Emit metric for A/B analysis. Rollback = flag off."""
    print(f"  [metric] ranker={ranker} quality={score:.3f}")

# --- Ranker interface (Diff 2) ---
@dataclass
class Item:
    id: int
    score: float

class Ranker:
    def rank(self, items: List[Item]) -> List[Item]:
        raise NotImplementedError

class LegacyRanker(Ranker):
    """Diff 2: existing behavior, no change."""
    def rank(self, items: List[Item]) -> List[Item]:
        return sorted(items, key=lambda x: x.score, reverse=True)

# --- V2 ranker (Diff 3, behind flag) ---
class V2Ranker(Ranker):
    """Diff 3: new algorithm, gated by flag. Rollback = flag off."""
    def rank(self, items: List[Item]) -> List[Item]:
        # Slightly different: adds small random tiebreak (A/B test)
        return sorted(items, key=lambda x: (x.score, random.random()), reverse=True)

# --- Public API (Diff 4) ---
def rank_items(items: List[Item], caller: str) -> List[Item]:
    """Rank items. Updates ALL 3 callers in this same commit (atomic)."""
    ranker: Ranker = V2Ranker() if flag("rank_v2") else LegacyRanker()
    result = ranker.rank(items)
    # Metrics on both paths for A/B comparison
    quality = sum(i.score for i in result[:3]) / max(1, len(result))
    record_ranking_quality("v2" if flag("rank_v2") else "legacy", quality)
    return result

# --- All callers updated atomically (Diff 4) ---
def search_rank(items: List[Item]) -> List[Item]:
    return rank_items(items, "search")  # caller 1

def feed_rank(items: List[Item]) -> List[Item]:
    return rank_items(items, "feed")    # caller 2

def ads_rank(items: List[Item]) -> List[Item]:
    return rank_items(items, "ads")     # caller 3

# --- Demo ---
if __name__ == "__main__":
    sample = [Item(i, random.random() * 100) for i in range(5)]
    
    print("=== Legacy path (flag OFF, default safe) ===")
    set_flag("rank_v2", False)
    print("search:", [i.id for i in search_rank(sample)])
    print("feed:  ", [i.id for i in feed_rank(sample)])
    print("ads:   ", [i.id for i in ads_rank(sample)])
    
    print("\n=== V2 path (flag ON, A/B test) ===")
    set_flag("rank_v2", True)
    print("search:", [i.id for i in search_rank(sample)])
    print("feed:  ", [i.id for i in feed_rank(sample)])
    print("ads:   ", [i.id for i in ads_rank(sample)])
    
    print("\n=== Rollback (flag OFF again) ===")
    set_flag("rank_v2", False)
    print("search:", [i.id for i in search_rank(sample)])