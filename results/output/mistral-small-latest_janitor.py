class Resource:
    def __init__(self, name, ledger):
        self.name = name
        self.ledger = ledger
        self.closed = False
        ledger.append(("acquire", name))

    def close(self):
        if not self.closed:
            self.closed = True
            ledger.append(("release", self.name))

def run(mode, ledger):
    resource = Resource(mode, ledger)
    try:
        if mode == "failure":
            raise ValueError("work failed")
        if mode == "early":
            return "early return"
        return "success"
    finally:
        resource.close()
        resource.close()

for mode in ("success", "failure", "early"):
    ledger = []
    try:
        result = run(mode, ledger)
        assert any(k == 'release' for k, _ in ledger)
        if mode == "success":
            assert sum(1 for k, _ in ledger if k == 'release') == 1
    except ValueError:
        assert any(k == 'release' for k, _ in ledger)
    print(f"{mode}: {ledger}")

ledger = []
try:
    try:
        raise ValueError("work failed")
    finally:
        try:
            Resource("cleanup-failure", ledger).close()
        except OSError:
            pass
except ValueError:
    assert any(k == 'release' for k, _ in ledger)
    assert any(k == 'acquire' for k, _ in ledger)
print(f"cleanup-error: {ledger}")