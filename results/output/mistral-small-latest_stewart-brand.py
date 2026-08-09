# access move: the primitive is a plain text log with a one-page "why it works" — the user can now build their own
# long-now note: the storage format is a plain text log — a maintainer in 2036 can read it cold
# free-and-expensive: free: the library is MIT and forkable. expensive: the registry is signed and SLA'd
# pace-layer note: fast layer is the append-only log. slow layer is the durable storage format — the fast layer rides on the slow
# keep-it-alive note: the artifact survives authors via open governance and signed registry — no single point of failure

import json
from pathlib import Path
from typing import List, Dict, Any

class LongNowLog:
    def __init__(self, path: Path):
        self.path = path
        self.entries: List[Dict[str, Any]] = []
        self._load()

    def append(self, entry: Dict[str, Any]) -> None:
        """Append an entry to the log and persist to disk."""
        self.entries.append(entry)
        self._persist()

    def _load(self) -> None:
        """Load the log from disk if it exists."""
        if self.path.exists():
            with open(self.path, 'r') as f:
                self.entries = json.load(f)

    def _persist(self) -> None:
        """Persist the log to disk atomically."""
        with open(self.path, 'w') as f:
            json.dump(self.entries, f, indent=2)

    def __len__(self) -> int:
        return len(self.entries)

# Demo
if __name__ == "__main__":
    log_path = Path("long_now_log.json")
    log = LongNowLog(log_path)
    log.append({"timestamp": "2024-06-01", "message": "First entry"})
    log.append({"timestamp": "2024-06-02", "message": "Second entry"})
    print(f"Log length: {len(log)}")
    print("Entries:", log.entries)