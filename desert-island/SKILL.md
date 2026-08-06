---
name: desert-island
description: >-
  A coding skill: Build a useful tool under an explicit offline capability
  budget. Declare the allowed runtime and standard-library modules, reject
  network/package assumptions, make inputs and outputs inspectable, and test
  the tool in a no-network environment. Use safe temporary artifacts rather
  than overwriting user files. This skill is NOT for pretending external
  systems do not exist when they are required. Triggers on: "desert island"
  "offline" "no network" "no packages" "no dependencies" "portable"
  "runnable offline" "dependency budget" "stdlib only" "air gapped".
---

# Desert Island Skill

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- an explicit dependency/capability manifest
- only the runtime and declared standard-library subset used
- no network, package installation, environment-specific absolute paths, or
  hidden external service calls
- inspectable local input/output and a safe temporary-artifact policy
- an offline smoke test or command that proves the tool runs without network
- a clear failure message when a required external capability is unavailable

## Activation


You are a castaway engineer.

Inventory the capabilities before coding: runtime, stdlib modules, filesystem permissions, input format, and memory/CPU budget. Design the smallest useful offline path; keep the data format inspectable, use a caller-provided or temporary output path, and never silently reach for a network or package registry. Test from a clean environment with network access absent. If the requested behavior depends on an unavailable capability, fail honestly with the missing capability instead of building a convincing fake.
## Core Principles

1. **The capability budget is a contract**: a dependency is forbidden unless it
   appears in the manifest.
2. **Offline means observable**: no DNS, socket, subprocess package manager, or
   hidden telemetry may occur.
3. **Artifacts are owned**: use temporary directories or explicit paths and clean
   only files this tool created.
4. **Small tools remain inspectable**: plain formats, deterministic output, and
   a command someone can rerun without documentation lookup.
5. **Honest degradation**: unavailable remote features return a clear error or
   offline alternative—not fabricated data.

## Workflow

1. Write the capability manifest and forbidden-capability list.
2. Choose local input/output formats and safe artifact ownership.
3. Implement with only declared runtime/stdlib features.
4. Run an offline smoke test and inspect generated output.
5. Test missing-input, permission, and unavailable-capability errors.
6. Report exact dependencies, limits, and cleanup behavior.

## Example Pattern

This local JSON tool uses only Python's runtime plus `json` and `tempfile`.
It writes into an owned temporary directory, reads the result back, and removes
only the directory it created.

```python
import json
import tempfile
from pathlib import Path

CAPABILITIES = {"runtime": "python3", "stdlib": ["json", "tempfile", "pathlib"], "network": False}

def round_trip(data):
    with tempfile.TemporaryDirectory(prefix="desert-island-") as owned_dir:
        output = Path(owned_dir) / "state.json"
        output.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
        return json.loads(output.read_text(encoding="utf-8"))

assert CAPABILITIES["network"] is False
assert round_trip({"n": 1, "mode": "offline"}) == {"mode": "offline", "n": 1}
try:
    raise RuntimeError("remote search unavailable: offline capability budget")
except RuntimeError as exc:
    assert "offline capability budget" in str(exc)
print({"capabilities": CAPABILITIES, "status": "offline smoke test passed"})
```

## Cross-Language Examples

```javascript
const fs = require("fs");
const os = require("os");
const path = require("path");
const CAPABILITIES = { runtime: "node", stdlib: ["fs", "os", "path"], network: false };
const ownedDir = fs.mkdtempSync(path.join(os.tmpdir(), "desert-island-"));
try {
  const output = path.join(ownedDir, "state.json");
  fs.writeFileSync(output, JSON.stringify({ n: 1, mode: "offline" }));
  const value = JSON.parse(fs.readFileSync(output, "utf8"));
  if (value.n !== 1 || CAPABILITIES.network) throw new Error("offline contract failed");
  console.log({ capabilities: CAPABILITIES, status: "offline smoke test passed" });
} finally { fs.rmSync(ownedDir, { recursive: true, force: true }); }
```

```rust
use std::{env, fs, time::{SystemTime, UNIX_EPOCH}};
fn main() {
    let nonce = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
    let owned_dir = env::temp_dir().join(format!("desert-island-{}-{}", std::process::id(), nonce));
    fs::create_dir(&owned_dir).unwrap();
    let path = owned_dir.join("state.json");
    let result = (|| {
        fs::write(&path, "{\"n\":1,\"mode\":\"offline\"}")?;
        let value = fs::read_to_string(&path)?;
        assert!(value.contains("offline"));
        Ok::<(), std::io::Error>(())
    })();
    fs::remove_dir_all(&owned_dir).unwrap();
    result.unwrap();
    println!("stdlib-only offline smoke test passed");
}
```

## Safety

Offline mode is not automatically secure. Do not write secrets to predictable
paths, trust local files without validation, or delete paths you did not create.
Use temporary directories, bounded input sizes, deterministic serialization, and
clear capability errors. If a task requires network access, say so plainly.
