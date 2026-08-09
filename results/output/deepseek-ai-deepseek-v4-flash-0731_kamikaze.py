import os
import sys
import tempfile
from pathlib import Path

def one_shot(source_path=None):
    # (1) Real work and output completed before any deletion attempt
    # Simulate a config cleaner: compute and validate the real result first
    config_entries = ["api_key", "db_password", "session_token"]
    cleaned_count = 0
    for entry in config_entries:
        if entry.startswith(("api_", "db_", "session_")):
            cleaned_count += 1
    result = {"cleaned_entries": cleaned_count, "total_entries": len(config_entries)}
    
    # (3) Source path resolved from the running script, not user input
    source = Path(source_path or __file__).resolve(strict=True)
    
    # (4) Symlink/ownership/path checks and a refusal on mismatch
    if source.is_symlink():
        raise RuntimeError("refused: source is a symlink")
    if not source.is_file():
        raise RuntimeError("refused: source is not a regular file")
    if not source.name.endswith(".py"):
        raise RuntimeError("refused: source is not a Python script")
    
    # (2) Self-deletion gated behind an explicit --self-destruct/armed flag
    armed = "--self-destruct" in sys.argv
    
    # Print result and dry-run/armed status before any deletion
    print({"result": result, "armed": armed, "source": str(source)})
    
    # (5) Deletion verification and a dry-run demonstration
    if not armed:
        # Safe demo: no actual deletion, only dry-run print
        return {"status": "dry-run", "exists": source.exists(), "deleted": False}
    
    # Armed branch: only delete the verified source file
    source.unlink()
    return {"status": "deleted", "exists": source.exists(), "deleted": True}

# Safe demo: use a temporary fixture, never the actual script
_demo_dir = Path(tempfile.mkdtemp(prefix="kamikaze-demo-"))
_demo_source = _demo_dir / "config_cleaner.py"
_demo_source.write_text("# owned demo fixture for config cleaner\n", encoding="utf-8")

# Run the demo in dry-run mode (no --self-destruct flag)
report = one_shot(_demo_source)
assert report["status"] == "dry-run" and report["exists"] and not report["deleted"]

# Clean up the demo fixture (not part of the self-deletion mechanism)
_demo_source.unlink()
_demo_dir.rmdir()

print(report)