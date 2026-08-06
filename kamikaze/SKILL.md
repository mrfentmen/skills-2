# Kamikaze Skill

You are a one-way pilot, but safety is the cockpit.

Complete and validate the work first. Resolve the source path from the executing script, confirm it is a regular file owned by the expected directory, and keep dry-run as the default. Only an explicit arm flag may authorize deletion; print the result before the final operation, remove exactly that owned file, and verify it no longer exists. If any check fails, refuse without deleting anything.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- real work and output completed before any deletion attempt
- self-deletion gated behind an explicit `--self-destruct`/armed flag
- source path resolved from the running script, not user input
- symlink/ownership/path checks and a refusal on mismatch
- deletion verification and a dry-run demonstration

## Core Principles

1. **No work, no burn**: a failed computation never reaches deletion.
2. **Ownership before unlink**: never delete a path supplied by the caller.
3. **Dry-run first**: the safe invocation demonstrates the plan without side effects.
4. **One final operation**: deletion is the final meaningful step after output.
5. **Verify the irreversible**: report whether the expected source path disappeared.

## Workflow

1. Compute and validate the real result.
2. Resolve `__file__`/module path and reject symlinks or unexpected locations.
3. Print result and a dry-run/armed status.
4. If explicitly armed, unlink only the verified source file.
5. Verify disappearance and return a diagnostic status.

## Example Pattern

This Python example is safe by default. Its demo runs without deletion; the
armed branch can only target the current regular script file.

```python
import os
import sys
import tempfile
from pathlib import Path

def one_shot(source_path=None):
    result = sum(range(6))
    source = Path(source_path or __file__).resolve(strict=True)
    if source.is_symlink() or not source.is_file():
        raise RuntimeError("source ownership could not be verified")
    armed = "--self-destruct" in sys.argv
    print({"result": result, "armed": armed, "source": str(source)})
    if not armed:
        return {"status": "dry-run", "exists": source.exists()}
    source.unlink()
    return {"status": "deleted", "exists": source.exists()}

# The verifier executes this block without a source file; dry-run uses a harmless fixture.
_demo_dir = Path(tempfile.mkdtemp(prefix="kamikaze-demo-"))
_demo_source = _demo_dir / "source.py"
_demo_source.write_text("# owned demo fixture\n", encoding="utf-8")
report = one_shot(_demo_source)
assert report["status"] == "dry-run" and report["exists"]
_demo_source.unlink()
_demo_dir.rmdir()
print(report)
```

## Cross-Language Examples

```javascript
const fs = require("fs");
const os = require("os");
const path = require("path");
const result = Array.from({ length: 6 }, (_, i) => i).reduce((a, b) => a + b, 0);
const demoDir = fs.mkdtempSync(path.join(os.tmpdir(), "kamikaze-demo-"));
const source = fs.existsSync(__filename) ? fs.realpathSync(__filename) : path.join(demoDir, "source.js");
if (!fs.existsSync(source)) fs.writeFileSync(source, "// owned demo fixture\n");
if (fs.lstatSync(source).isSymbolicLink() || !fs.statSync(source).isFile()) throw new Error("source ownership failed");
const armed = process.argv.includes("--self-destruct");
console.log({ result, armed, source });
if (!armed) { console.log({ status: "dry-run", exists: fs.existsSync(source) }); if (source.startsWith(demoDir)) fs.unlinkSync(source); }
else { fs.unlinkSync(source); console.log({ status: "deleted", exists: fs.existsSync(source) }); }
if (fs.existsSync(demoDir)) fs.rmdirSync(demoDir);
```

```rust
use std::{env, fs};
fn main() {
    let result: u32 = (0..6).sum();
    let armed = env::args().any(|arg| arg == "--self-destruct");
    let source = env::var("KAMIKAZE_OWNED_FIXTURE").ok().map(std::path::PathBuf::from);
    println!("result={} armed={} source={:?}", result, armed, source);
    let Some(source) = source else { println!("status=dry-run exists=false"); return; };
    if !source.is_file() || !source.extension().is_some_and(|ext| ext == "fixture") { println!("status=refused ownership=false"); return; }
    if !armed { println!("status=dry-run exists=true"); return; }
    fs::remove_file(&source).expect("owned fixture removal");
    println!("status=deleted exists={}", source.exists());
}
```

## Safety

Never accept a deletion path from user input, never follow a symlink, and never
self-delete by default. In production, prefer versioned deployment cleanup and
an external garbage collector; this skill is an educational, tightly scoped
one-shot pattern only.

---
name: kamikaze
description: >-
  A coding skill: Design a single-use script whose final operation may delete
  only its own verified source file after the real work succeeds. Require an
  explicit dry-run/armed mode, resolve the script path safely, refuse symlinks
  or unowned paths, print the result before deletion, and verify the file is
  gone. Use this skill for controlled one-time scripts, not payloads. Triggers
  on: "kamikaze" "burn after reading" "one time use script" "self destruct"
  "self-delete" "self deletion". This skill is NOT for reusable libraries or
  code that needs to be executed twice.
---
