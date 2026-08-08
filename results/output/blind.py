QUESTIONS = ("is_even", "is_positive", "is_zero")

def solve_parity(ask):
    transcript = []
    answers = {}
    for name in QUESTIONS:
        answer = ask(name)
        if not isinstance(answer, bool):
            raise ValueError(f"malformed answer for {name}")
        transcript.append((name, answer))
        answers[name] = answer

    if answers["is_zero"]:
        label = "even"
    elif answers["is_even"]:
        label = "even"
    else:
        label = "odd"
    return {"label": label, "transcript": tuple(transcript)}

def adapter(hidden_value):
    # Only this adapter sees the hidden value; solver gets bools only.
    def ask(name):
        if name not in QUESTIONS:
            raise KeyError("question not permitted")
        if name == "is_even":
            return hidden_value % 2 == 0
        if name == "is_positive":
            return hidden_value > 0
        return hidden_value == 0
    return ask

# Non-interference: two distinct hidden values with same answers produce same result.
first = solve_parity(adapter(4))
second = solve_parity(adapter(8))
assert first["transcript"] == second["transcript"]
assert first["label"] == second["label"] == "even"

# Fail-closed: unknown question rejected.
try:
    solve_parity(lambda name: True if name == "not_allowed" else False)
except KeyError:
    pass
else:
    raise AssertionError("unknown question should fail closed")

# Malformed answer rejected.
try:
    solve_parity(lambda name: "yes" if name == "is_even" else False)
except ValueError:
    pass
else:
    raise AssertionError("malformed answer should fail closed")

print(first["label"], len(first["transcript"]))