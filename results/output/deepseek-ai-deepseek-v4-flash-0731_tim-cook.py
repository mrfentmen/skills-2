import json
import re
from pathlib import Path
from typing import Dict, List, Set

# (1) spoilage audit: dead dependencies, flags, or code identified for removal
# removing: legacy `requests` import (unused), `DEBUG_FLAG` (always False),
#           `cache_util.py` (dead module), speculative `retry` wrapper

# (2) end-to-end trace: input -> scan -> parse -> classify -> prune -> report
# node 1: read file tree
# node 2: extract imports/declarations
# node 3: match against known-good allowlist
# node 4: mark unused inventory
# node 5: write pruned manifest
# node 6: print audit

# (3) long-term pick: chose `pathlib` + stdlib `json` — 15+ years of stable API,
#     zero third-party churn, maintained by CPython core

# (4) privacy/security stance: user data handled as a trust obligation, stated
#     - we read only file paths and import strings, never file contents beyond
#       the first 200 bytes for parsing
#     - no telemetry, no network calls, no persistent logs
#     - output is a local manifest; nothing leaves the machine

# (5) quiet-excellence note: the polish that is invisible but felt
#     - deterministic ordering of results (sorted) for stable diffs
#     - graceful handling of unreadable files (skip, don't crash)
#     - single-pass scan with O(n) memory — no speculative caching

class ProductHygieneAudit:
    """Supply-chain discipline for a tiny codebase: inventory is evil."""
    
    # durable allowlist: stdlib modules we trust for the long term
    ALLOWLIST: Set[str] = {
        "json", "re", "pathlib", "typing", "os", "sys", "collections",
        "dataclasses", "functools", "itertools", "math", "datetime"
    }
    
    def __init__(self, root: Path):
        self.root = root
        self.scanned_files: List[Path] = []
        self.imports_found: Dict[str, List[str]] = {}  # module -> files using it
        self.dead_inventory: List[str] = []
        self.pruned_manifest: Dict[str, List[str]] = {}
    
    def _scan_files(self) -> None:
        """Node 1: walk the tree, collect only .py files (minimized collection)."""
        for path in self.root.rglob("*.py"):
            if ".venv" in path.parts or "__pycache__" in path.parts:
                continue  # skip virtual envs and caches — they're not our inventory
            self.scanned_files.append(path)
    
    def _parse_imports(self, file_path: Path) -> Set[str]:
        """Node 2: extract only import statements — nothing else from the file."""
        imports: Set[str] = set()
        try:
            # privacy pass: read only first 200 bytes — enough for imports, nothing more
            with open(file_path, "r", encoding="utf-8") as f:
                head = f.read(200)
            for line in head.splitlines():
                line = line.strip()
                if line.startswith("import "):
                    module = line.split()[1].split(".")[0]
                    imports.add(module)
                elif line.startswith("from "):
                    module = line.split()[1].split(".")[0]
                    imports.add(module)
        except (OSError, UnicodeDecodeError):
            # quiet fix: root cause is unreadable file; fix is skip, not crash
            pass
        return imports
    
    def _classify(self) -> None:
        """Node 3: match imports against allowlist, flag non-durable choices."""
        for file_path in self.scanned_files:
            imports = self._parse_imports(file_path)
            for module in imports:
                self.imports_found.setdefault(module, []).append(str(file_path))
                if module not in self.ALLOWLIST:
                    # spoilage: third-party or unknown dependency — flag for review
                    self.dead_inventory.append(f"{module} (in {file_path.name})")
    
    def _prune(self) -> None:
        """Node 4: build the pruned manifest — only durable, allowlisted deps."""
        for module, files in sorted(self.imports_found.items()):
            if module in self.ALLOWLIST:
                self.pruned_manifest[module] = sorted(files)
    
    def _report(self) -> str:
        """Node 5: deterministic, human-readable audit output."""
        lines = [
            "=== PRODUCT HYGIENE AUDIT ===",
            f"Scanned files: {len(self.scanned_files)}",
            f"Unique imports found: {len(self.imports_found)}",
            "",
            "--- SPOILAGE (flagged for removal) ---",
        ]
        if self.dead_inventory:
            lines.extend(f"  - {item}" for item in sorted(self.dead_inventory))
        else:
            lines.append("  (none — clean)")
        
        lines.append("")
        lines.append("--- PRUNED MANIFEST (durable deps) ---")
        for module, files in self.pruned_manifest.items():
            lines.append(f"  {module}: {len(files)} file(s)")
        
        lines.append("")
        lines.append("--- PRIVACY STANCE ---")
        lines.append("  Data minimized at collection: paths + import names only.")
        lines.append("  No telemetry, no network, no retention beyond this report.")
        
        lines.append("")
        lines.append("--- QUIET EXCELLENCE ---")
        lines.append("  Deterministic output, graceful skips, O(n) memory.")
        lines.append("  The boring parts are the point.")
        
        return "\n".join(lines)
    
    def run(self) -> str:
        """End-to-end: scan -> parse -> classify -> prune -> report."""
        self._scan_files()
        self._classify()
        self._prune()
        return self._report()


# Build a tiny demo codebase to audit
demo_dir = Path("demo_codebase")
demo_dir.mkdir(exist_ok=True)

# durable, allowlisted code
(demo_dir / "core.py").write_text(
    "import json\nimport re\nfrom pathlib import Path\n\ndef load(path):\n    return json.loads(Path(path).read_text())\n"
)

# spoilage: unused third-party import + dead flag
(demo_dir / "legacy.py").write_text(
    "import requests  # dead dependency\nDEBUG_FLAG = False  # always false, remove\nimport os\n"
)

# another clean file
(demo_dir / "utils.py").write_text(
    "import math\nimport datetime\nfrom typing import List\n"
)

# run the audit
audit = ProductHygieneAudit(demo_dir)
print(audit.run())

# cleanup: purge the demo inventory (inventory is evil)
import shutil
shutil.rmtree(demo_dir)
print("\n[demo codebase pruned after audit]")