import os
import sys
from pathlib import Path

# Real work: compute a small result before any deletion attempt
demo_result = len([x for x in range(10) if x % 2 == 0])

# Deterministic target path resolved from a constant, never __file__ or argv
TARGET_PATH = Path("/tmp/kamikaze-demo-config.txt")

# Ensure the demo fixture exists for the dry-run
if not TARGET_PATH.exists():
    TARGET_PATH.write_text("demo config line 1\ndemo config line 2\n", encoding="utf-8")

# Symlink/ownership/path checks
if TARGET_PATH.is_symlink():
    raise RuntimeError("target is a symlink")
if not TARGET_PATH.is_file():
    raise RuntimeError("target is not a regular file")

# Armed flag simulation (safe demo: no actual deletion)
armed = "--self-destruct" in sys.argv

# Print result and dry-run/armed status
print({
    "result": demo_result,
    "armed": armed,
    "target": str(TARGET_PATH),
    "exists": TARGET_PATH.exists()
})

# Dry-run demonstration: no deletion, only status print
if not armed:
    print({"status": "dry-run", "exists": TARGET_PATH.exists()})
else:
    # Final operation: deletion only when explicitly armed
    TARGET_PATH.unlink()
    print({"status": "deleted", "exists": TARGET_PATH.exists()})

# Cleanup demo fixture if it was created
if TARGET_PATH.exists() and not TARGET_PATH.is_symlink():
    TARGET_PATH.unlink()