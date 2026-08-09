LEGAL = {"yes", "no"}

def locate(query, lo=0, hi=100, budget=8):
    """Return the hidden integer using only yes/no answers."""
    transcript = []
    for _ in range(budget):
        if lo == hi:
            return lo, transcript
        mid = (lo + hi) // 2
        # Ask: "Is the hidden number <= mid?"
        answer = query(mid)
        if answer not in LEGAL:
            raise ValueError(f"invalid oracle answer: {answer!r}")
        transcript.append((mid, answer))
        if answer == "yes":
            hi = mid
        else:
            lo = mid + 1
        if lo > hi:
            raise ValueError("inconsistent oracle transcript")
    raise RuntimeError("query budget exhausted before determination")

def yes_no_oracle(hidden):
    # The solver never receives `hidden`; this closure is the boundary adapter.
    def ask(mid):
        return "yes" if hidden <= mid else "no"
    return ask

answer, transcript = locate(yes_no_oracle(37))
assert answer == 37
assert len(transcript) <= 7
print({"answer": answer, "queries": len(transcript)})