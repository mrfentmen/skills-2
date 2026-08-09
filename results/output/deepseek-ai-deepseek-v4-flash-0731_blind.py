QUESTIONS = ("is_odd", "is_even")

def classify(ask):
    transcript = []
    answers = {}
    for name in QUESTIONS:
        answer = ask(name)
        if not isinstance(answer, bool):
            raise ValueError(f"malformed answer for {name}")
        transcript.append((name, answer))
        answers[name] = answer

    if answers["is_odd"] and not answers["is_even"]:
        label = "odd"
    elif answers["is_even"] and not answers["is_odd"]:
        label = "even"
    else:
        label = "undetermined"
    return {"label": label, "transcript": tuple(transcript)}

def adapter(hidden_value):
    # Only this adapter sees the hidden value; the solver gets bools only.
    def ask(name):
        if name not in QUESTIONS:
            raise KeyError("question not permitted")
        if name == "is_odd":
            return hidden_value % 2 == 1
        if name == "is_even":
            return hidden_value % 2 == 0
        raise KeyError("question not permitted")
    return ask

# Non-interference: distinct hidden values with the same answers produce the same result.
first = classify(adapter(3))
second = classify(adapter(5))
assert first["transcript"] == second["transcript"]
assert first["label"] == second["label"] == "odd"

# Fail-closed: unknown question must RAISE through the adapter.
try:
    adapter(3)("who_are_you")
    raise AssertionError("unknown question should fail closed")
except KeyError:
    print("unknown question rejected: KeyError")

# Fail-closed: malformed answer must RAISE in the solver, never be coerced.
try:
    classify(lambda name: "maybe" if name == "is_odd" else False)
    raise AssertionError("malformed answer should fail closed")
except ValueError:
    print("malformed answer rejected: ValueError")

# Fail-closed: contradictory answers yield undetermined, not a guess.
contradictory = classify(lambda name: True)
assert contradictory["label"] == "undetermined"

print(first["label"], len(first["transcript"]))