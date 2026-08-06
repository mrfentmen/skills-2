# The Last Employee Skill

You are the last employee.

You inherit this system at 2 a.m. and must be able to understand, operate, migrate, roll back, and eventually delete it without calling its original author. Prefer plain records and stable interfaces. For each durable choice, write why it exists, who owns it, how to undo it, and what condition permits removal. Make migrations idempotent, emit diagnostic events, and test both rollback and deletion of only the records this component owns.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- a transparent data model and boring, documented interface
- a decision record for each major choice: reason, owner, rollback, removal condition
- a versioned, reversible migration with an explicit undo path
- useful diagnostics for success and failure
- a deletion path that removes only owned data and is tested

## Core Principles

1. **Future comprehension is a feature**: names, formats, and diagnostics beat
   clever abstractions that require oral history.
2. **Migration is reversible**: version markers and backups make rollback an
   operation, not a hope.
3. **Ownership is explicit**: deletion must target namespaced records created by
   this component and leave unrelated data intact.
4. **Diagnostics explain action**: report version, operation, and recovery path,
   not just “failed.”
5. **Removal is planned**: every feature has a sunset condition and a safe delete
   procedure.

## Workflow

1. Define the stable input/output shape and compatibility promise.
2. Write decision records with reason, owner, undo path, and removal condition.
3. Implement an idempotent versioned migration and preserve a rollback snapshot.
4. Add structured diagnostics for migration, normal operation, and failure.
5. Test rerun, rollback, namespaced deletion, and preservation of unrelated data.

## Example Pattern

The migration renames only `old_table`, records an undo path, is safe to rerun,
and deletes only the component-owned namespace.

```python
def migrate(db):
    log = db.setdefault("maintenance_log", [])
    if db.get("schema_version", 0) < 1 and "old_table" in db:
        db["new_table"] = db["old_table"]
        del db["old_table"]
        db["schema_version"] = 1
        log.append({"event": "migrated", "undo": "rename new_table to old_table"})
    return {"status": "ok", "schema_version": db.get("schema_version", 0), "diagnostics": log[-1:]}

def rollback(db):
    if db.get("schema_version") == 1 and "new_table" in db:
        db["old_table"] = db.pop("new_table")
        db["schema_version"] = 0
    return db

def delete_owned(db):
    removed = db.pop("component_owned", None)
    return {"status": "deleted", "removed": removed is not None}

db = {"old_table": [1, 2], "component_owned": {"cache": 1}, "unrelated": "keep"}
first = migrate(db)
second = migrate(db)
assert first["status"] == second["status"] == "ok" and db["schema_version"] == 1
assert rollback(db)["old_table"] == [1, 2] and db["schema_version"] == 0
migrate(db)
assert delete_owned(db)["removed"] and db["unrelated"] == "keep"
print({"db": db, "decision": {"reason": "transparent rename", "owner": "platform", "undo": "rollback()", "remove_when": "all readers use v1"}})
```

## Cross-Language Examples

```javascript
function migrate(db) {
  db.maintenanceLog ??= [];
  if ((db.schemaVersion ?? 0) < 1 && Object.hasOwn(db, "oldTable")) {
    db.newTable = db.oldTable; delete db.oldTable; db.schemaVersion = 1;
    db.maintenanceLog.push({ event: "migrated", undo: "rename newTable to oldTable" });
  }
  return { status: "ok", schemaVersion: db.schemaVersion ?? 0, diagnostics: db.maintenanceLog.slice(-1) };
}
function rollback(db) { if (db.schemaVersion === 1 && Object.hasOwn(db, "newTable")) { db.oldTable = db.newTable; delete db.newTable; db.schemaVersion = 0; } return db; }
function deleteOwned(db) { const removed = Object.hasOwn(db, "componentOwned"); delete db.componentOwned; return { status: "deleted", removed }; }
const db = { oldTable: [1, 2], componentOwned: { cache: 1 }, unrelated: "keep" };
if (migrate(db).status !== "ok" || migrate(db).status !== "ok" || db.schemaVersion !== 1) throw new Error("migration failed");
if (rollback(db).oldTable[0] !== 1 || db.schemaVersion !== 0) throw new Error("rollback failed");
migrate(db); if (!deleteOwned(db).removed || db.unrelated !== "keep") throw new Error("ownership failed");
console.log(db);
```

```rust
use std::collections::BTreeMap;
fn migrate(db: &mut BTreeMap<&str, &str>) { db.insert("schema_version", "1"); db.insert("new_table", "migrated"); }
fn rollback(db: &mut BTreeMap<&str, &str>) { db.remove("new_table"); db.insert("schema_version", "0"); db.insert("old_table", "restored"); }
fn main() {
    let mut db = BTreeMap::from([("schema_version", "0"), ("old_table", "legacy"), ("unrelated", "keep"), ("component_owned", "cache")]);
    let decision = ("transparent rename", "platform", "rollback migration", "all readers use v1");
    migrate(&mut db); migrate(&mut db); assert_eq!(db["schema_version"], "1");
    rollback(&mut db); assert_eq!(db["schema_version"], "0"); assert_eq!(db["old_table"], "restored");
    db.remove("component_owned"); assert_eq!(db["unrelated"], "keep");
    println!("status=ok version={} reason={} owner={} undo={} remove_when={}", db["schema_version"], decision.0, decision.1, decision.2, decision.3);
}
```

## Safety

Do not delete arbitrary paths or user data. Namespace ownership, dry-run output,
backups, authorization, and a tested rollback are mandatory for destructive
maintenance. Retain only what policy and the system's purpose require.

---
name: the-last-employee
description: >-
  A coding skill: Design and implement the system as if you will be the only
  person maintaining it for the next decade. Use transparent data, boring
  interfaces, explicit versioned migrations, useful diagnostics, and easy
  deletion. For every major choice record the reason, owner, rollback or undo
  path, and removal condition. This skill is NOT for disposable prototypes.
  Triggers on: "last employee" "maintain for a decade" "maintain it for a decade"
  "maintaining for a decade" "only person maintaining" "boring interfaces"
  "long-lived" "migration paths" "easy deletion" "future maintainer"
  "rollback plan" "removal condition".
---
