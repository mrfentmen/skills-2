def bubble_voice(values):
    arr = list(values)
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
            yield {"voice": "bubble", "step": f"pass={i}, compare={j}"}
        if not swapped:
            break
    return arr

def insertion_voice(values):
    arr = list(values)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            yield {"voice": "insertion", "step": f"shift={i}, pos={j+1}"}
        arr[j + 1] = key
        yield {"voice": "insertion", "step": f"insert={i}"}
    return arr

def counterpoint(values):
    voices = [bubble_voice(values), insertion_voice(values)]
    answers = [None, None]
    done = [False, False]
    trace = []
    while not all(done):
        for idx, voice in enumerate(voices):
            if done[idx]:
                continue
            try:
                trace.append(next(voice))
            except StopIteration as finished:
                answers[idx] = finished.value
                done[idx] = True
    status = "converged" if answers[0] == answers[1] else "diverged"
    return {"answers": answers, "trace": trace, "status": status}

report = counterpoint([5, 3, 8, 1, 9, 2])
assert report["status"] == "converged"
assert report["answers"][0] == [1, 2, 3, 5, 8, 9]
assert report["answers"][1] == [1, 2, 3, 5, 8, 9]
assert report["trace"][0]["voice"] == "bubble"
assert report["trace"][1]["voice"] == "insertion"
print({"status": report["status"], "steps": len(report["trace"])})