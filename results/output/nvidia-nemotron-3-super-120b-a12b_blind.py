# Blind parity solver: determines if a hidden integer is even or odd
# using only a fixed set of permitted questions and primitive boolean answers.

# --- Question allowlist (capability boundary) ---
QUESTIONS = ("is_even",)  # only this question may be asked of the hidden value

def parity(ask):
    """
    Solver that receives only question names and primitive answers.
    It never sees the hidden value; its output is a pure function of the answer transcript.
    """
    transcript = []
    answers = {}
    for name in QUESTIONS:
        answer = ask(name)
        if not isinstance(answer, bool):
            raise ValueError(f"malformed answer for {name}")
        transcript.append((name, answer))
        answers[name] = answer

    # Deterministic mapping from answers to result
    label = "even" if answers["is_even"] else "odd"
    return {"label": label, "transcript": tuple(transcript)}

def adapter(hidden):
    """
    Adapter that knows the hidden integer and exposes it only via the allowed questions.
    The solver never receives the hidden object; it receives only bools.
    """
    def ask(name):
        if name not in QUESTIONS:
            raise KeyError("question not permitted")
        if name == "is_even":
            return (hidden % 2 == 0)
        # unreachable due to allowlist check, but kept for completeness
        raise KeyError("question not permitted")
    return ask

# --- Demonstration and non-interference test ---
if __name__ == "__main__":
    # Two distinct hidden values that yield the same answer transcript (both even)
    first_hidden = 4
    second_hidden = 6

    first = parity(adapter(first_hidden))
    second = parity(adapter(second_hidden))

    # Non-interference: same transcript and same label
    assert first["transcript"] == second["transcript"], "Transcripts differ for same answers"
    assert first["label"] == second["label"] == "even", "Labels differ for same answers"

    # Fail-closed: unknown question must raise through the adapter
    try:
        adapter(first_hidden)("unknown_question")
        raise AssertionError("unknown question should fail closed")
    except KeyError:
        pass  # expected

    # Fail-closed: malformed answer must raise in the solver
    try:
        parity(lambda name: "maybe" if name == "is_even" else False)
        raise AssertionError("malformed answer should fail closed")
    except ValueError:
        pass  # expected

    # Output result and transcript length as required
    print(first["label"], len(first["transcript"]))