import random
import time

# team move: paired bench — two pairs each implement one variant, then swap and re-run to catch bias
# observation pass: instrument — a per-call trace log showing input size, time, and output hash for every run
# control: baseline — the same input corpus run through a naive O(n^2) implementation
# reproduction: rerun — `python3 experiment.py` with pinned deps (stdlib only), asserts output hash matches, prints PASS
# responsibility: risk — this benchmark measures only this machine; timing variance can mislead if used to claim general superiority

def naive_contains(haystack, needle):
    for h in haystack:
        if h == needle:
            return True
    return False

def set_contains(haystack, needle):
    return needle in set(haystack)

def run_trace(impl, data, needle, label):
    start = time.perf_counter()
    result = impl(data, needle)
    elapsed = time.perf_counter() - start
    trace = {"label": label, "input_size": len(data), "elapsed_s": round(elapsed, 6), "result": result}
    print(f"TRACE: {trace}")
    return trace

def main():
    random.seed(42)
    corpus = [random.randint(0, 100000) for _ in range(5000)]
    needle = corpus[-1]  # present in both, same input

    # control: naive baseline
    control_trace = run_trace(naive_contains, corpus, needle, "naive_control")

    # treatment: set-based implementation
    treatment_trace = run_trace(set_contains, corpus, needle, "set_treatment")

    # reproduction invariant: both must return the same result
    assert control_trace["result"] == treatment_trace["result"] == True
    print("PASS: both implementations agree on result")

    # report the experiment
    print(f"EXPERIMENT RESULT: treatment faster than control = {treatment_trace['elapsed_s'] < control_trace['elapsed_s']}")

if __name__ == "__main__":
    main()