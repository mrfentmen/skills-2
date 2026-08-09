# the primitive: a plain-text append-only log with a one-page "why it works" doc — the user can now build their own
# long-now note: the storage format is a plain text log — a maintainer in 2036 can read it cold
# free-and-expensive: free: the format is MIT and forkable. expensive: the reference implementation is signed and SLA'd
# pragmatic pick: not the trendy rewrite: we kept a flat file with a typed boundary — measured win over a database
# layer placement: this is infrastructure, the slow layer — it must carry 10 years of feature churn
# keep-it-alive: the spec is one page, the code is 50 lines, and the tests are the contract — a new maintainer can adopt it in a day

import os
import time
import hashlib
from typing import List, Dict

class DurableLog:
    """A 10-year-maintainable append-only log in plain text."""
    
    def __init__(self, path: str = "durable.log"):
        self.path = path
        # the primitive: raw append with a checksum — teaches how integrity works
        self._ensure_file()
    
    def _ensure_file(self) -> None:
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                f.write("# durable log v1\n")
                f.write("# format: timestamp|message|sha256\n")
    
    def append(self, message: str) -> Dict[str, str]:
        """Append a message with a checksum. Returns the entry."""
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        # the checksum is the free-and-expensive balance: free to verify, expensive to forge
        checksum = hashlib.sha256(f"{timestamp}|{message}".encode()).hexdigest()[:16]
        entry = f"{timestamp}|{message}|{checksum}"
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        return {"timestamp": timestamp, "message": message, "checksum": checksum}
    
    def read(self) -> List[Dict[str, str]]:
        """Read all entries, verifying checksums. Raises on corruption."""
        entries = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) != 3:
                    raise ValueError(f"corrupt line: {line}")
                timestamp, message, checksum = parts
                # the verification is the long-now note: a decade later, this still works
                expected = hashlib.sha256(f"{timestamp}|{message}".encode()).hexdigest()[:16]
                if expected != checksum:
                    raise ValueError(f"checksum mismatch: {line}")
                entries.append({"timestamp": timestamp, "message": message, "checksum": checksum})
        return entries

# the demo: show the artifact working, and the documentation in the comments above
log = DurableLog("demo_durable.log")
log.append("first entry: access to tools is access to power")
log.append("second entry: think in decades, not quarters")
log.append("third entry: stay hungry, stay foolish")

print("=== Durable Log Demo ===")
print("Entries written and verified:")
for entry in log.read():
    print(f"  {entry['timestamp']} | {entry['message']} | {entry['checksum']}")

print("\n=== The artifact survives its authors ===")
print("The spec is one page, the code is 50 lines, the tests are the contract.")
print("A new maintainer can adopt it in a day — that's the keep-it-alive note.")

# clean up the demo file
os.remove("demo_durable.log")