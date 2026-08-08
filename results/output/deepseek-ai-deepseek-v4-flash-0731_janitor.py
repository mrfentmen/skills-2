class Resource:
    def __init__(self, name, ledger):
        self.name = name
        self.ledger = ledger
        self.closed = False
        ledger.append(("acquire", name))

    def close(self):
        if not self.closed:
            self.closed = True
            self.ledger.append(("release", self.name))


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
        resource.close()  # idempotent: no second release event


for mode in ["success", "failure", "early"]:
    ledger = []
    try:
        result = run(mode, ledger)
        print(f"{mode}: result={result}, ledger={ledger}")
    except ValueError as exc:
        print(f"{mode}: exception={exc}, ledger={ledger}")
    assert ledger == [("acquire", mode), ("release", mode)]

print("All paths verified: no leaks, no double releases")