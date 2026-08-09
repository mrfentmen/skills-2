"""
Transparent User Store with Versioned Migration
===============================================

Data Model
----------
- Namespace: `user_store`
  - `users`: dict mapping user_id (str) to user record (dict)
  - `schema_version`: int indicating current schema version
  - `maintenance_log`: list of dicts recording migration events

Interface
---------
- migrate(store: dict) -> dict: idempotent migration to latest schema
- rollback(store: dict) -> dict: revert to previous schema version
- delete_owned(store: dict) -> dict: remove only user_store-owned data
- get_user(store: dict, user_id: str) -> dict | None: read user record
- put_user(store: dict, user_id: str, record: dict) -> dict: write user record

Decision Records
----------------
1. Schema Versioning
   Reason: Enable reversible migrations and future-proofing
   Owner: platform
   Rollback: Use rollback() to revert to previous schema
   Removal Condition: When all consumers use v2 and no rollback needed

2. Namespace Isolation
   Reason: Prevent collision with unrelated data
   Owner: platform
   Rollback: N/A (structural)
   Removal Condition: When user_store is decommissioned entirely

3. Maintenance Log
   Reason: Provide audit trail for diagnostics
   Owner: platform
   Rollback: Log entries remain; no functional impact
   Removal Condition: After 365 days of inactivity

4. User Record Format
   Reason: Simple, extensible structure
   Owner: platform
   Rollback: N/A (data migration handled by schema version)
   Removal Condition: When user_store is deleted

Migration Path
--------------
v0 -> v1: Initial schema with flat user records
v1 -> v2: Add email index for faster lookups
"""

def migrate(store):
    """
    Idempotent migration to latest schema version.
    Preserves existing data and emits diagnostics.
    """
    log = store.setdefault("maintenance_log", [])
    version = store.get("schema_version", 0)

    # Migration v0 -> v1: Initial schema
    if version < 1:
        if "users" not in store:
            store["users"] = {}
        store["schema_version"] = 1
        log.append({
            "event": "migrated_v0_v1",
            "undo": "delete users key and set schema_version=0",
            "diagnostics": "Initial schema created"
        })

    # Migration v1 -> v2: Add email index
    if version < 2:
        if "users" in store and not any("email_index" in k for k in store):
            store["email_index"] = {}
            for uid, record in store["users"].items():
                if "email" in record:
                    store["email_index"][record["email"]] = uid
            store["schema_version"] = 2
            log.append({
                "event": "migrated_v1_v2",
                "undo": "delete email_index and set schema_version=1",
                "diagnostics": "Email index created"
            })

    return {
        "status": "ok",
        "schema_version": store.get("schema_version", 0),
        "diagnostics": log[-1:] if log else [{"event": "no_migration", "diagnostics": "Already at latest version"}]
    }

def rollback(store):
    """
    Revert to previous schema version.
    Preserves data structure compatibility.
    """
    version = store.get("schema_version", 0)

    # Rollback v2 -> v1: Remove email index
    if version == 2 and "email_index" in store:
        del store["email_index"]
        store["schema_version"] = 1
        store.setdefault("maintenance_log", []).append({
            "event": "rolled_back_v2_v1",
            "undo": "re-run migrate() to restore v2",
            "diagnostics": "Email index removed"
        })

    # Rollback v1 -> v0: Remove users container
    elif version == 1 and "users" in store:
        del store["users"]
        store["schema_version"] = 0
        store.setdefault("maintenance_log", []).append({
            "event": "rolled_back_v1_v0",
            "undo": "re-run migrate() to restore v1",
            "diagnostics": "Users container removed"
        })

    return store

def delete_owned(store):
    """
    Remove only user_store-owned data.
    Preserves unrelated keys in the store.
    """
    removed = False
    if "users" in store:
        del store["users"]
        removed = True
    if "email_index" in store:
        del store["email_index"]
        removed = True
    if "schema_version" in store:
        del store["schema_version"]
        removed = True
    if "maintenance_log" in store:
        del store["maintenance_log"]
        removed = True

    store.setdefault("maintenance_log", []).append({
        "event": "deleted_owned",
        "undo": "restore from backup",
        "diagnostics": "user_store data removed"
    })

    return {
        "status": "deleted",
        "removed": removed,
        "remaining_keys": [k for k in store if not k.startswith("user_store_")]
    }

def get_user(store, user_id):
    """Read user record by ID with diagnostics."""
    if "users" not in store:
        return {"status": "error", "diagnostics": "users container missing"}
    record = store["users"].get(user_id)
    if record is None:
        return {"status": "not_found", "diagnostics": f"user {user_id} not found"}
    return {"status": "ok", "record": record}

def put_user(store, user_id, record):
    """Write user record with diagnostics."""
    if "users" not in store:
        store["users"] = {}
    store["users"][user_id] = record
    if "email" in record and "email_index" in store:
        store["email_index"][record["email"]] = user_id
    return {"status": "ok", "user_id": user_id, "diagnostics": "user stored"}

# Demo
if __name__ == "__main__":
    # Initial state: empty store with unrelated data
    store = {
        "unrelated_config": {"theme": "dark"},
        "user_store_backup": None
    }

    # Run migration twice to test idempotency
    print("=== Initial Migration ===")
    result1 = migrate(store)
    print(result1)

    print("\n=== Second Migration (idempotency) ===")
    result2 = migrate(store)
    print(result2)

    # Add some users
    print("\n=== Adding Users ===")
    put_user(store, "u1", {"name": "Alice", "email": "alice@example.com"})
    put_user(store, "u2", {"name": "Bob", "email": "bob@example.com"})
    print(get_user(store, "u1"))
    print(get_user(store, "u99"))

    # Test rollback
    print("\n=== Rollback to v1 ===")
    rollback(store)
    print(f"Schema after rollback: {store.get('schema_version')}")
    print(f"Users preserved: {'users' in store}")
    print(f"Email index removed: {'email_index' not in store}")

    # Re-migrate to v2
    print("\n=== Re-migrate to v2 ===")
    migrate(store)
    print(f"Schema after re-migration: {store.get('schema_version')}")
    print(f"Email index restored: {'email_index' in store}")

    # Test deletion
    print("\n=== Deleting Owned Data ===")
    deletion = delete_owned(store)
    print(deletion)
    print(f"Remaining keys: {deletion['remaining_keys']}")
    print(f"Unrelated data preserved: {store['unrelated_config']}")

    # Final diagnostics
    print("\n=== Final Store State ===")
    print(store)