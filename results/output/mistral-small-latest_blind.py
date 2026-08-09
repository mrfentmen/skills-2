QUESTIONS = ("is_even",)

def classify_parity(ask):
    transcript = []
    answers = {}
    for name in QUESTIONS:
        answer = ask(name)
        if not isinstance(answer, bool):
            raise ValueError(f"malformed answer for {name}")
        transcript.append((name, answer))
        answers[name] = answer

    if answers["is_even"]:
        label = "even"
    else:
        label = "odd"
    return {"label": label, "transcript": tuple(transcript)}

def adapter(value):
    def ask(name):
        if name not in QUESTIONS:
            raise KeyError("question not permitted")
        if name == "is_even":
            return value % 2 == 0
        raise KeyError("question not permitted")
    return ask

first = classify_parity(adapter(4))
second = classify_parity(adapter(4))
assert first["transcript"] == second["transcript"]
assert first["label"] == second["label"] == "even"

try:
    adapter(3)("who_are_you")
    raise AssertionError("unknown question should fail closed")
except KeyError:
    pass

try:
    classify_parity(lambda name: "maybe" if name == "is_even" else False)
    raise AssertionError("malformed answer should fail closed")
except ValueError:
    pass

print(first["label"], len(first["transcript"]))