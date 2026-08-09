def migrate(db):
    log = db.setdefault("maintenance_log", [])
    if db.get("schema_version", 0) < 1 and "old_users" in db:
        db["users"] = db["old_users"]
        del db["old_users"]
        db["schema_version"] = 1
        log.append({"event": "migrated", "undo": "rename users to old_users"})
    return {"status": "ok", "schema_version": db.get("schema_version", 0), "diagnostics": log[-1:]}

def rollback(db):
    if db.get("schema_version") == 1 and "users" in db:
        db["old_users"] = db.pop("users")
        db["schema_version"] = 0
    return db

def delete_owned(db):
    removed = db.pop("component_owned", None)
    return {"status": "deleted", "removed": removed is not None}

db = {"old_users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], "component_owned": {"cache": 1}, "unrelated": "keep"}
first = migrate(db)
second = migrate(db)
assert first["status"] == second["status"] == "ok" and db["schema_version"] == 1
assert rollback(db)["old_users"] == [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}] and db["schema_version"] == 0
migrate(db)
assert delete_owned(db)["removed"] and db["unrelated"] == "keep"
print({"db": db, "decision": {"reason": "transparent rename", "owner": "platform", "undo": "rollback()", "remove_when": "all readers use v1"}})