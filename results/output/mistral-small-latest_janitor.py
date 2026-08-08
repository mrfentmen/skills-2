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
        resource.close()

def main():
    outcomes = []
    for mode in ["success", "failure", "early"]:
        ledger = []
        try:
            result = run(mode, ledger)
            outcomes.append((mode, "success", result, ledger))
        except Exception as exc:
            outcomes.append((mode, "exception", exc, ledger))

    for mode, status, payload, ledger in outcomes:
        print(f"{mode}: {status} -> {payload}")
        print(f"  ledger: {ledger}")

    expected_ledgers = {
        "success": [("acquire", "success"), ("release", "success")],
        "failure": [("acquire", "failure"), ("release", "failure")],
        "early": [("acquire", "early"), ("release", "early")]
    }
    for mode, _, _, ledger in outcomes:
        assert ledger == expected_ledgers[mode], f"ledger mismatch for {mode}: {ledger}"

    # Cleanup failure path
    ledger = []
    primary_error = None
    cleanup_error = None
    try:
        try:
            raise ValueError("work failed")
        finally:
            try:
                Resource("cleanup-failure", ledger).close()
            except OSError as exc:
                cleanup_error = str(exc)
    except ValueError as exc:
        primary_error = str(exc)

    print(f"cleanup-failure: primary={primary_error}, cleanup={cleanup_error}")
    print(f"  ledger: {ledger}")
    assert primary_error == "work failed"
    assert cleanup_error == "release failed"
    assert ledger == [("acquire", "cleanup-failure")]

if __name__ == "__main__":
    main()