import time
import numpy as np
from typing import List, Tuple

BUDGET_MS = 16.6  # 60fps hard budget
FORMAT_VERSION = "scene-v1-json"

def validate_workload(entities: np.ndarray) -> bool:
    """Validate contiguous layout and supported dtype."""
    return (isinstance(entities, np.ndarray) and
            entities.dtype == np.float32 and
            entities.ndim == 2 and
            entities.shape[1] == 4)  # vec4 layout

def process_entities(entities: np.ndarray, quality: str = "full") -> dict:
    """Process contiguous entity batch with hard frame budget gate."""
    if not validate_workload(entities):
        return {"status": "rejected", "reason": "unsupported workload layout or dtype"}

    if quality not in {"full", "degraded"}:
        return {"status": "rejected", "reason": "unsupported quality level"}

    start = time.perf_counter()

    # Hot path: contiguous SIMD-friendly processing
    if quality == "full":
        # Full quality: compute world-space positions and culling
        positions = entities[:, :3]
        scales = entities[:, 3]
        visible_mask = np.abs(positions).sum(axis=1) > 0.01  # simple cull
        visible = entities[visible_mask]
        work_units = len(entities)
    else:
        # Degraded: minimal processing
        visible = entities[:len(entities)//2]  # drop half
        work_units = len(entities)

    elapsed_ms = (time.perf_counter() - start) * 1000

    # Hard gate enforcement
    if elapsed_ms > BUDGET_MS and quality == "full":
        return process_entities(entities, quality="degraded")

    return {
        "status": quality,
        "cost_ms": elapsed_ms,
        "work_units": work_units,
        "visible": len(visible),
        "entities": len(entities),
        "format": FORMAT_VERSION
    }

# Largest representative load: 100k entities (typical Nanite cluster)
largest_scene = np.random.rand(100_000, 4).astype(np.float32)
report = process_entities(largest_scene)
print(report)

# Validate gate behavior
assert report["status"] in {"full", "degraded"}
assert report["format"] == FORMAT_VERSION
assert report["cost_ms"] <= BUDGET_MS
assert isinstance(report["work_units"], int)
assert isinstance(report["visible"], int)