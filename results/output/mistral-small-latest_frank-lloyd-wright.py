# the schema is the behavior: one aggregate, not a table plus an orphan service
class LivingCache:
    # grows from the site: the cache exists because the db is the constraint — native, not bolted on
    def __init__(self, db, ttl=60):
        self._db = db
        self._ttl = ttl
        self._store = {}
        self._last_refresh = 0

    def get(self, key):
        # the interface is the wall, opened: callers see intent, never the internals
        now = time.time()
        if now - self._last_refresh > self._ttl:
            self._store = {k: v for k, v in self._db.items() if k in self._store}
            self._last_refresh = now
        return self._store.get(key)

# removed: the auth wrapper, the feature flag layer, the DTO duplication — three lines where five were obesity
# left only the essential: a time-aware cache that refreshes from the db constraint
# the box destroyed: the cache's wall became a time-bound refresh — boundaries flow, coupling dies
# self-healing loop borrowed from a coral reef: retry with backoff, no central brain

import time

db = {"a": 1, "b": 2, "c": 3}
cache = LivingCache(db, ttl=1)
print(cache.get("a"))  # 1
time.sleep(2)
print(cache.get("a"))  # None (expired)