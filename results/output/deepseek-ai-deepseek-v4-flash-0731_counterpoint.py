def bubble_voice(values):
    arr = list(values)
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        yield {"voice": "bubble", "step": i + 1, "state": arr[:]}
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
        arr[j + 1] = key
        yield {"voice": "insertion", "step": i, "state": arr[:]}
    return arr

def scheduler(values):
    voices = [bubble_voice(values), insertion_voice(values)]
    answers = [None, None]
    done = [False, False]
    trace = []
    seq = 0
    while not all(done):
        for idx, voice in enumerate(voices):
            if done[idx]:
                continue
            try:
                step = next(voice)
                step["seq"] = seq
                seq += 1
                trace.append(step)
            except StopIteration as fin:
                answers[idx] = fin.value
                done[idx] = True
    status = "converged" if answers[0] == answers[1] else "diverged"
    return {"answers": answers, "trace": trace, "status": status}

report = scheduler([5, 3, 8, 1, 9, 2])
assert report["status"] == "converged"
assert report["answers"][0] == [1, 2, 3, 5, 8, 9]
assert report["answers"][1] == [1, 2, 3, 5, 8, 9]
assert report["trace"][0]["voice"] == "bubble"
assert report["trace"][1]["voice"] == "insertion"
print({"status": report["status"], "steps": len(report["trace"])})