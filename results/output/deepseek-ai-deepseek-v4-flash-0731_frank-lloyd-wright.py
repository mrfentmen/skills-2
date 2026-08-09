class StreamBed:
    # the schema is the behavior: one aggregate, not a table plus an orphan service
    # grows from the site: the sqlite file is the constraint — the store is the file, native, not bolted on
    def __init__(self, path=":memory:"):
        import sqlite3
        self._conn = sqlite3.connect(path)
        self._conn.execute("CREATE TABLE IF NOT EXISTS flow (id INTEGER PRIMARY KEY, v REAL)")
        self._conn.commit()
        # removed: the connection pool, the ORM, the migration framework — three layers where one file was enough
        # the box destroyed: the storage wall became a callable — callers see a function, never the cursor
        self.put = self._put
        self.get = self._get

    def _put(self, v):
        self._conn.execute("INSERT INTO flow (v) VALUES (?)", (v,))
        self._conn.commit()
        return v

    def _get(self, n=1):
        cur = self._conn.execute("SELECT v FROM flow ORDER BY id DESC LIMIT ?", (n,))
        return [r[0] for r in cur.fetchall()]

    # self-healing loop borrowed from a tide pool: retry with backoff, no central brain
    def pump(self, v, retries=3):
        for i in range(retries):
            try:
                return self.put(v)
            except Exception:
                import time
                time.sleep(0.1 * (i + 1))
        raise RuntimeError("tide pool dry")

    def close(self):
        self._conn.close()

# the whole and the parts determine each other: the store's shape is its behavior
bed = StreamBed()
bed.pump(1.5)
bed.pump(2.5)
print(bed.get(2))  # [2.5, 1.5] — the interface is the wall, opened
bed.close()