LEGAL = {"yes", "no"}

def locate_yes_no(query, lo=0, hi=100, budget=8):
    """Return the hidden integer using only 'yes'/'no' answers where 'yes' means hidden >= guess."""
    transcript = []
    for _ in range(budget):
        if lo == hi:
            return lo, transcript
        candidate = (lo + hi + 1) // 2
        answer = query(candidate)
        if answer not in LEGAL:
            raise ValueError(f"invalid oracle answer: {answer!r}")
        transcript.append((candidate, answer))
        if answer == "yes":
            lo = candidate
        else:
            hi = candidate - 1
        if lo > hi:
            raise ValueError("inconsistent oracle transcript")
    raise RuntimeError("query budget exhausted before determination")

def yes_no_oracle(hidden):
    def ask(candidate):
        return "yes" if hidden >= candidate else "no"
    return ask

answer, transcript = locate_yes_no(yes_no_oracle(37))
assert answer == 37
assert len(transcript) <= 8
print({"answer": answer, "queries": len(transcript)})