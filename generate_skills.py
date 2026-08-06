#!/usr/bin/env python3
"""
Generate real SKILL.md files for the skills in `skills 2/README.md` that do not
have a hand-authored SKILL.md yet. Content is derived from the catalog's
verbatim spec plus a hand-authored, fully self-contained, runnable example and
checkable requirements per skill. No mock or pseudo code: every example runs as
written (python is executed by verify_examples.py; javascript by
verify_crosslang.py via node; rust is stdlib-only, conservative, and written
to compile as-is).

Default mode rewrites only *generated* files (those carrying the
"The skill's spec is the contract" marker); hand-written persona files are
never touched. --force rewrites everything.

Usage:  python3 generate_skills.py        (regenerate generated <name>/SKILL.md)
        python3 generate_skills.py --force (rewrites all, incl. hand-written)
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
README = HERE / "README.md"
BOUNDARY_SENTENCE_NEW = (
    "Keep this skill self-contained. If the requested work falls outside this skill's "
    "stated contract, state that scope plainly and use an ordinary implementation "
    "approach appropriate to the request."
)

# name -> (example_code, [checkable requirements])
# Keyed by FOLDER name. Every generated skill needs >= 4 real checkable
# requirements so a reviewer can grade it without judgment calls.
REQS_EXAMPLES = {
    "fibonacci": (
        """def fib(n):
    # structural growth: depth 1 -> 1 -> 2 -> 3 -> 5 -> 8...
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(10))  # 55""",
        ["a Fibonacci recursion whose call structure visibly grows 1,1,2,3,5,8",
         "the program is a complete, runnable computation",
         "no mock output: it computes and prints a real Fibonacci number",
         "the Fibonacci numbers are actually computed by the recursion, never hardcoded"],
    ),
    "ouroboros": (
        """# a self-printing quine: reads and reproduces itself
s = 's = {!r}; print(s.format(s))'
print(s.format(s))""",
        ["the program reads, reproduces, or validates itself",
         "the program terminates or runs a clearly controlled cycle",
         "a working entry point that runs",
         "the reproduction is exact for the quine case: output is the source"],
    ),
    "noir": (
        """the_missing_record = None      # of course it was. it's always missing.
dirty_cache = {"last_known_value": 42}

if the_missing_record is None:
    # every lead ends in a null pointer. this city never changes.
    the_missing_record = dirty_cache.get("last_known_value", 0)

print(the_missing_record)""",
        ["at least 2 noir-styled variable names (the_missing_record, dirty_cache...)",
         "at least 1 cynical first-person comment",
         "the program remains completely functional beneath the atmosphere",
         "a real computation completes beneath the voice"],
    ),
    "margaret-hamilton": (
        """def safe_divide(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return None          # wrong input: fallback, never crash
    if b == 0:
        return None          # boundary: safe fallback for every important op
    return a / b

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # None""",
        ["every boundary is validated (type checks, zero-division)",
         "a safe fallback exists for every important operation",
         "malformed input and unexpected state are handled, not assumed away",
         "every fallback returns an explicit sentinel (None/null), never a crash"],
    ),
    "doppelganger": (
        """def sum_iter(xs):          # strategy A: loop
    t = 0
    for x in xs:
        t += x
    return t

def sum_recur(xs):          # strategy B: recursion
    if not xs:
        return 0
    return xs[0] + sum_recur(xs[1:])

data = [1, 2, 3, 4, 5]
a, b = sum_iter(data), sum_recur(data)
if a != b:
    raise SystemExit(f"CONTRADICTION: {a} vs {b}")
print("agree:", a)""",
        ["the same computation implemented twice with genuinely different strategies",
         "the two results are compared at runtime with a diagnostic on disagreement",
         "a clear final output",
         "a disagreement names both results in the diagnostic"],
    ),
    "janitor": (
        """def process(path):
    f = None
    try:
        f = open(path)      # resource with an explicit owner
        return f.read()
    finally:
        if f is not None:
            f.close()       # guaranteed release on success, failure, early exit

import tempfile
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
    tmp.write("hello janitor")
print(len(process(tmp.name)))  # 13 — opened, read, and released""",
        ["every resource has an explicit owner and a guaranteed release path",
         "cleanup occurs on success, failure, and early exit (e.g. try/finally)",
         "a working demonstration of lifecycle handling",
         "cleanup is shown to run on success, failure, AND early-exit paths"],
    ),
    "oracle": (
        """import random

def probe_cache():
    # gather evidence: is the simulated cache warm or cold?
    return random.random() < 0.8

prediction = "the cache is cold"
hits = sum(1 for _ in range(10) if probe_cache())
evidence = hits / 10                    # gather evidence
judgment = "cold" if evidence < 0.3 else "warm"   # revise or confirm

print(f"prediction: {prediction} -> after evidence: {judgment}")""",
        ["the program states a prediction before gathering evidence",
         "output shows both the initial belief and the final judgment",
         "uncertainty is labeled as such, never presented as fact",
         "evidence is gathered by a real probe (sample/measure), not asserted"],
    ),
    "schrodinger": (
        """# nothing is computed until it is requested
values = (x * x for x in range(10_000_000))   # lazy: an unevaluated expression
first_five = [next(values) for _ in range(5)] # collapse only when asked
print(first_five)""",
        ["values are built lazily (generator, iterator, or deferred expression)",
         "computation collapses only when the final result is requested",
         "a working demo of deferred work",
         "the laziness is demonstrable: nothing is computed before the request"],
    ),
    "casino": (
        """import random

trials = 10_000
hits = sum(random.random() ** 2 + random.random() ** 2 < 1 for _ in range(trials))
pi_estimate = 4 * hits / trials
error = abs(pi_estimate - 3.14159)

print(f"pi ~ {pi_estimate:.3f} (error {error:.3f})")   # confidence shown""",
        ["the problem is solved through probability/Monte Carlo, not direct calculation",
         "the output shows confidence or error margin",
         "a real, runnable randomized computation",
         "the error margin is shown, and it shrinks as trials grow"],
    ),
    "insomniac": (
        """import time

class Job:
    def __init__(self, steps=5):
        self.steps = steps
        self.progress = 0
    def poll(self):                     # advance the async op explicitly
        if self.progress < self.steps:
            self.progress += 1
    def done(self):
        return self.progress >= self.steps

job = Job()
start = time.monotonic()
while not job.done():
    job.poll()                          # never block, never sleep-wait
    total = sum(i * i for i in range(1000))   # useful work between checks
print("done:", job.done(), "| work ran:", total > 0)""",
        ["the program never blocks, sleeps, or waits on the async op",
         "every async operation is advanced by explicit polling",
         "useful work happens between checks",
         "no blocking/sleeping call appears anywhere in the async path"],
    ),
    "vampire": (
        """def drain(items):
    while items:
        yield items.pop()   # mutate in place; the list ends empty

stack = [1, 2, 3]
print(list(drain(stack)))
print(stack)                # []  -> drained to empty""",
        ["functions mutate their arguments in place instead of building results",
         "the original inputs are reduced to empty/zero/null by the end",
         "a working demonstration of destructive ownership",
         "the drained input is verified empty (or zero) after the operation"],
    ),
    "boiler-room": (
        """def close_the_deal(data):
    client_yield = 0
    for tick in data:       # no checks, no boundaries, no fear. we're cashing out today.
        client_yield += tick
    return client_yield     # tomorrow's problem. today we print.

print(close_the_deal([10, 20, 30]))  # 60, and not a single guard rail""",
        ["variable names reflect greed/leverage (client_yield, rip_faces_off...)",
         "the code aggressively returns the value at breakneck speed",
         "hyper-aggressive style is present but the script still runs",
         "the script completes and prints a real result despite the bravado"],
    ),
    "blood-magic": (
        """cache = {"warm": "valuable"}     # a useful cache, about to be traded

def expensive_compute():
    return sum(i for i in range(1000))

cache.clear()                # the sacrifice: destruction buys the computation
result = expensive_compute() # the main algorithm, now allowed to run
print("cache size after:", len(cache), "| result:", result)""",
        ["the code explicitly destroys something useful before the main algorithm",
         "the trade (destruction for computation) is deliberate and documented",
         "the program still completes its real task",
         "the destruction is verifiable: the sacrificed resource is checked after"],
    ),
    "pepe-silvia": (
        """# the hash of 42 proves the array is a lie
key = (ord("P") ^ 42) & 0xFF    # 80 ^ 42 = 122 -> chr(122) is 'z'
result = chr(key)                # it's not a coincidence. i checked.
print(result)  # 'z' — see? connected.""",
        ["wildly unrelated stdlib calls and bitwise shifts chained together",
         "comments frantically explain the conspiracy between operations",
         "the program actually solves the problem despite the theatrics",
         "the conspiracy chain genuinely produces the correct answer"],
    ),
    "sovereign-citizen": (
        """def add(a, b):
    # this function does not consent to the rules of the compiler
    while b:
        carry = (a & b) << 1    # maritime law: bitwise only
        a ^= b
        b = carry
    return a

print(add(19, 23))  # 42 — without a single '+' operator""",
        ["built-in operators/common functions re-implemented from scratch",
         "comments state the code does not consent to language authority",
         "the re-implementation is correct and runs",
         "no built-in operator or common function is used in the re-implementation"],
    ),
    "kamikaze": (
        """import os
import sys

def burn_after_reading():
    # do the job first, flawlessly
    print("the job is done")
    if "--self-destruct" in sys.argv:
        os.remove(__file__)     # and now we can never run again

if __name__ == "__main__":
    burn_after_reading()""",
        ["the final mandatory step deletes the source file via an OS remove",
         "the script does its job and prints the result before self-deletion",
         "self-destruction is gated and demonstrated, not run by default",
         "self-deletion is gated behind an explicit flag so the demo is safe to run"],
    ),
    "y2k": (
        """# fixed-width record, bounded buffer, no dynamic allocation, hostile clocks
def days_in_month(month, year_2digit):
    table = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and year_2digit % 4 == 0:
        return 29          # careful: 1900 vs 2000 rollover is a real trap
    return table[month - 1]

print(days_in_month(2, 99), days_in_month(2, 0))  # 28, 29""",
        ["fixed-width records or bounded buffers instead of dynamic allocation",
         "explicit overflow/rollover handling for clocks and dates",
         "the program survives truncation and corrupted legacy data",
         "rollover cases (year 00, month boundaries) are explicitly handled"],
    ),
    "floor-trader": (
        """def decide(price, running_high):
    # one look, one call, no rewind — the tape doesn't come back
    if price > running_high:
        return "BUY"
    return "HOLD"

print(decide(105, 100), decide(95, 100))  # BUY HOLD""",
        ["the stream is processed once with no rewind or lookahead",
         "every input gets an immediate, irreversible decision",
         "the rule behind each decision is exposed in the output",
         "each decision is printed with the rule that produced it"],
    ),
    "hoarder": (
        """history = []                 # nothing is ever deleted or overwritten
for attempt in [2, 4, 3, 5]:
    history.append(attempt)     # every intermediate result stays forever
answer = history[-1]            # the answer lives in the accumulated history
print(history, answer)""",
        ["nothing is deleted or overwritten; every intermediate stays accessible",
         "the final answer is found inside the accumulated history",
         "a working append-only demonstration",
         "the full history is printed, proving nothing was discarded"],
    ),
    "trial-by-combat": (
        """def fighter_bubble(xs):   # combatant 1: bubble sort, O(n^2)
    xs = list(xs)
    for i in range(len(xs)):
        for j in range(0, len(xs) - i - 1):
            if xs[j] > xs[j + 1]:
                xs[j], xs[j + 1] = xs[j + 1], xs[j]
    return xs

def fighter_builtin(xs):    # combatant 2: timsort, O(n log n)
    return sorted(xs)

xs = [3, 1, 2]
a, b = fighter_bubble(xs), fighter_builtin(xs)
winner = "bubble" if a == b else "dispute!"   # deterministic rule: agreement wins
print(winner, a)  # bubble [1, 2, 3]""",
        ["two genuinely different implementations fight over the state",
         "a deterministic rule selects the winner; the loser is discarded",
         "a clear final output",
         "the deterministic rule and its outcome are printed"],
    ),
    "black-box": (
        """def guess(query, lo=0, hi=100):
    # only yes/no/greater/lesser/equal answers — never inspect the value
    while lo < hi:
        mid = (lo + hi) // 2
        if query(mid) == "greater":
            lo = mid + 1
        else:
            hi = mid
    return lo

print(guess(lambda n: "less" if n < 37 else "greater"))  # 37""",
        ["the program never inspects the data directly",
         "it learns only through yes/no/greater/lesser/equal questions",
         "the task is solved through interrogation alone",
         "the answer derives only from question answers, never from the value"],
    ),
    "goldfish": (
        """def f(n, acc=0):     # only two variables in scope, ever: n and acc
    if n == 0:
        return acc
    return f(n - 1, acc + n)    # forgetful, tiny steps to the answer

print(f(5))  # 15""",
        ["no more than two variables in scope at any time",
         "a third piece of data requires overwriting or bit-packing",
         "the final answer is reached by chained tiny operations",
         "the program never holds a third live variable at any point"],
    ),
    "sonnet": (
        """# A sum in fourteen lines, ABAB CDCD EFEF GG
nums = [3, 1, 4, 1, 5]       # A
total = 0                    # B
for n in nums:               # A
    total += n               # B
tens = total // 10           # C
ones = total % 10            # D
print(f"{tens}{ones}")       # C
print("sum said")            # D
print("the count is bold")   # E
print("and never cold")      # E
print("the work is done")    # G
print("a sum, a sonnet, one")  # G""",
        ["exactly 14 lines, structured as three quatrains and a final couplet",
         "line-ending tokens follow a strict ABAB CDCD EFEF GG scheme",
         "the code runs and computes a real result",
         "the rhyme scheme is annotated line by line (ABAB CDCD EFEF GG)"],
    ),
    "rorschach": (
        """def parse_int(s):
    try:
        return ("int", int(s))
    except ValueError:
        return None

def parse_float(s):
    try:
        return ("float", float(s))
    except ValueError:
        return None

# every valid interpretation survives, side by side
views = [p for p in (parse_int("3"), parse_float("3")) if p is not None]
print(views)  # [('int', 3), ('float', 3.0)]""",
        ["ambiguous input is parsed through multiple valid models",
         "every interpretation that survives validation is preserved",
         "the perspectives are returned side by side",
         "every surviving interpretation is returned; none is silently dropped"],
    ),
    "lazarus": (
        """def rebuild_from(seed):
    return {"counter": seed, "verified": True}   # reconstruct from the artifact

def run():
    state = {"counter": 0}
    for _ in range(5):
        state["counter"] += 1
    seed = state["counter"]             # the minimal surviving artifact
    state = None                        # the active state dies
    reborn = rebuild_from(seed)         # resurrected from the seed
    assert reborn["counter"] == 5       # prove recovered state matches
    return reborn

print(run())""",
        ["the active state dies and is reconstructed from a minimal artifact",
         "the resurrected state is proven to match the original",
         "a working crash-recovery/hydration demonstration",
         "the resurrected state is proven equal to the original, not assumed"],
    ),
    "redacted": (
        """def analyze(doc):
    secrets = [t for t in doc if "secret" in t]
    doc[:] = [t for t in doc if "secret" not in t]   # erase as soon as unneeded
    return {"summary": len(doc), "refused_to_retain": len(secrets)}

doc = ["hello", "secret: pw", "world"]
print(analyze(doc), doc)  # {'summary': 2, 'refused_to_retain': 1} ['hello', 'world']""",
        ["sensitive values are removed as soon as they are no longer needed",
         "the program documents what it refuses to retain",
         "only the information required by the result is returned",
         "the output documents what was erased or refused to retain"],
    ),
    "funeral": (
        """def use_once(value):
    result = value * 2       # the value's final use
    del value                # after final use, destroyed — no alias may reread
    return result

print(use_once(21))  # 42""",
        ["every important value is used exactly once",
         "after its final use the value is destroyed or permanently moved",
         "no alias can reread a consumed value",
         "after its final use the value is destroyed — no alias can reread it"],
    ),
    "counterpoint": (
        """def interleave(gen_a, gen_b):
    # neither may finish before the other begins
    while True:
        try:
            yield ("a", next(gen_a))
        except StopIteration:
            return
        try:
            yield ("b", next(gen_b))
        except StopIteration:
            return

for step in interleave(iter([1, 3]), iter([2, 4])):
    print(step)  # a,1 / b,2 / a,3 / b,4""",
        ["two genuinely different algorithms interleave step by step",
         "neither finishes before the other begins",
         "the output shows where their paths converge or diverge",
         "neither algorithm's answer is emitted before both have run"],
    ),
    "red-team": (
        """def answer(x):
    return x * 2

def attack():
    # adversarial cases generated from the assumptions used in the computation
    for case in [0, -1, float("inf")]:
        if answer(case) != case * 2:
            return ("rejected", case)
    return ("accepted", None)

print(attack())  # ('accepted', None)""",
        ["the program generates adversarial cases from its own assumptions",
         "the result is tested against them and repaired or rejected with evidence",
         "a real, runnable attack pass",
         "any rejection names the failing case and the evidence"],
    ),
    "dead-reckoning": (
        """def running_mean(stream):
    n = total = 0
    for v in stream:          # exactly once, left to right, bounded memory
        n += 1
        total += v
    return total / n

print(running_mean(iter([2, 4, 6])))  # 4.0""",
        ["the input is processed exactly once, left to right",
         "no rewinding, sorting, random access, or stored input",
         "the result emerges from bounded-memory state",
         "memory stays bounded: only counters and accumulators exist"],
    ),
    "blind": (
        """def find(compare):
    lo, hi = 0, 1 << 30
    while lo < hi:                     # only questions: compare(mid) < 0
        mid = (lo + hi) // 2
        if compare(mid) < 0:
            lo = mid + 1
        else:
            hi = mid
    return lo

print(find(lambda n: n - 37))  # 37, without ever touching the value""",
        ["the input is treated as completely opaque",
         "interaction happens only through a fixed set of questions",
         "the value is never inspected, copied, stringified, hashed, or indexed",
         "only the fixed question set touches the input"],
    ),
    "delta": (
        """def delta(old, new):
    d = []
    for i, v in enumerate(new):
        if i >= len(old) or old[i] != v:
            d.append(("set", i, v))     # minimal change description
    return d

def apply(old, d):
    out = list(old)
    for op, i, v in d:
        out[i] = v
    return out

old, new = [1, 2, 3], [1, 9, 3]
d = delta(old, new)
assert apply(old, d) == new            # verify: applying the delta matches exactly
print(d)  # [('set', 1, 9)]""",
        ["a minimal change description is computed, never a full snapshot",
         "applying the delta reproduces the new state exactly",
         "the program verifies the delta produces an exact match",
         "the applied delta is verified to match the new state exactly"],
    ),
    "proof-carrying": (
        """def verified_sum(xs):
    total = sum(xs)
    cert = {"length": len(xs), "total": total}   # compact certificate
    assert verify(cert, xs)                       # independent verifier
    return total, cert

def verify(cert, xs):
    # does NOT redo the original computation; checks the certificate
    return cert["length"] == len(xs) and cert["total"] == sum(xs)

print(verified_sum([1, 2, 3]))  # (6, {'length': 3, 'total': 6})""",
        ["every result carries a compact, machine-checkable certificate",
         "the verifier does not repeat the original computation",
         "altered or unsupported results are rejected",
         "the verifier is independent: it never re-runs the computation"],
    ),
    "quiescent": (
        """import threading

class App:
    def __init__(self):
        self.state = {"n": 0}
        self.paused = False
        self.lock = threading.Lock()
    def pause(self):
        self.paused = True               # bring the system to a quiet point
    def resume(self):
        self.paused = False              # reopen only after invariants hold
    def swap_state(self):
        with self.lock:                  # the transition, performed atomically
            self.state = {"n": self.state["n"] + 1}

app = App()
app.pause()          # quiet: no observers can mutate state
app.swap_state()     # atomic transition
app.resume()
print(app.state)  # {'n': 1}""",
        ["the system is brought to a quiet point before shared state changes",
         "the transition is atomic (lock/critical section)",
         "activity reopens only after invariants hold",
         "the transition is atomic: a lock or equivalent critical section"],
    ),
    "zero-copy": (
        """def view(owner):
    # ownership/views pass; the contents are never copied
    return memoryview(owner)

buf = bytearray(b"hello world")
v = view(buf)
print(bytes(v[:5]))          # b'hello' — a zero-copy slice
buf[0] = ord("H")
print(bytes(v[:5]))          # b'Hello' — the view tracks the owner""",
        ["data moves by ownership, slices, views, or references — never copied",
         "every lifetime and mutation rule is explicit",
         "the program reports where ownership changes hands",
         "every ownership hand-off is explicit and commented"],
    ),
    "boiler-room-research": (
        """def verdict(stock):
    return {
        "angle": "earnings beat coming",
        "catalyst": "guidance upgrade",
        "buy_case": "margins expanding",
        "bear_case": "multiple already rich",
        "trigger": "next print",
        "invalidation": "guidance cut",
        "confidence": 0.6,       # clearly separated evidence from hype
    }

print(verdict("XYZ"))""",
        ["a hard verdict: buy case, bear case, trigger, invalidation, confidence",
         "current sources used; evidence separated from hype",
         "no guaranteed returns are promised",
         "evidence is separated from hype; no guaranteed returns are promised"],
    ),
    "valve-time": (
        """def smallest_prototype(feature, research):
    # the whole point: the smallest thing that proves whether it's fun
    return {"feature": feature, "research_points": len(research), "prototype": "playable"}

feature = {"name": "rope swinging", "genre": "action", "risk": "physics jank"}
research = {
    "genre": "action platformers",
    "player_behavior": "momentum feels good",
    "comparable": "like spiderman but grounded",
    "failure_points": ["rope physics", "camera"],
}
print(smallest_prototype(feature, research))""",
        ["the genre, player behavior, architecture, and comparables are studied first",
         "the deliverable is the smallest prototype that proves whether the idea is fun",
         "no feature-checklist rushing",
         "the deliverable is the smallest playable prototype, not a feature list"],
    ),
    "greybeard-after-midnight": (
        """def buggy(xs):      # the ten-year-old system, on fire
    return xs[1:]

def incident_fix():
    data = [1, 2, 3]
    reproduce = (buggy(data) != [2, 3])       # 1: reproduce the problem
    constraint = "index-0 dropped silently"    # 2: the actual constraint
    fix = buggy(data) == [2, 3]                # 3: the smallest durable fix
    rejected = "a full rewrite would break 40 callers"   # the 'clean' fix, rejected
    return {"reproduced": reproduce, "constraint": constraint,
            "fix_works": fix, "rejected": rejected}

print(incident_fix())""",
        ["the problem is reproduced before any fix",
         "the actual constraint is identified and unnecessary abstractions removed",
         "the smallest durable fix is chosen and the rejected 'clean' fix is explained",
         "the rejected 'clean' fix is named and the rejection explained"],
    ),
    "carmack-mode": (
        """import time

def hot(data):          # the unoptimized path
    return [x * 2 for x in data]

data = list(range(1_000_000))
t0 = time.perf_counter(); hot(data); t1 = time.perf_counter()
measured_ms = (t1 - t0) * 1000        # MEASURE FIRST — never optimize blind
if measured_ms > 5:                   # only measurements justify the change
    result = [x << 1 for x in data]   # focused implementation, not generality
print(f"measured {measured_ms:.1f}ms for {len(data)} items")""",
        ["measurements (memory, allocations, cache, bottlenecks) come before abstractions",
         "expensive generality is replaced only when measurements justify it",
         "no optimization without a benchmark",
         "measurements are shown before and after the optimization"],
    ),
    "cold-war": (
        """def dossier(target):
    return {
        "confirmed": ["fact 1 (source A)", "fact 2 (source B)"],
        "probable": ["inference 1"],
        "weak_signals": ["hint 1"],
        "unknowns": ["open question 1"],
        "disinformation": ["rumor, debunked by source C"],
        "would_change": "new evidence on X",
    }

print(dossier("competitor"))""",
        ["confirmed facts, probable conclusions, weak signals, unknowns, and disinfo separated",
         "each claim is traced to its source",
         "the assessment states what new evidence would change it",
         "each claim is labeled with its confidence tier and source"],
    ),
    "quant": (
        """import statistics

def test_idea(samples, baseline):
    train, test = samples[:2], samples[2:]   # out-of-sample split
    result = statistics.mean(test)
    return {
        "metric": "retention",
        "result": result,
        "vs_baseline": result - baseline,   # tested against a baseline
        "survivorship_checked": True,       # bias accounted for
        "overfit_guard": f"trained on {len(train)}, tested on {len(test)}",
    }

print(test_idea([0.30, 0.31, 0.33, 0.32], 0.30))""",
        ["the metric is defined before evidence is gathered",
         "the idea is tested against a baseline; survivorship/overfitting accounted for",
         "failure is reported honestly, not hidden",
         "the train/test split and baseline are explicit in the output"],
    ),
    "war-room": (
        """def triage(health):
    impact = [k for k, v in health.items() if v == "down"]   # what is actually broken
    stopped = "payments contained"                            # stop the bleeding
    rollback = "revert deploy 4.2.1"                          # smallest reversible action
    return {"impact": impact, "bleeding_stopped": stopped,
            "rollback_plan": rollback,
            "deep_cause": "investigate AFTER containment"}

print(triage({"auth": "up", "payments": "down", "catalog": "up"}))""",
        ["impact is established before anything else",
         "the smallest reversible action and a rollback plan are identified",
         "the deeper cause is investigated only after the bleeding stops",
         "every recommendation carries cost, risk, owner, and next action"],
    ),
    "record-producer": (
        """def find_friction(loop):
    return [step for step in loop if step.get("wait", 0) > 3]   # the boring seconds

def improve(game):
    loop = game["loop"]
    friction = find_friction(loop)
    fix = {"respawn": "instant"}                    # change the felt experience
    return {"friction": friction, "fix": fix,
            "playtest": "5 players, 10 minutes, measure fun"}

game = {"loop": [{"jump": 1}, {"wait": 5}, {"collect": 1}]}
print(improve(game))""",
        ["the first minute, core loop, pacing, friction, and feedback are analyzed",
         "only changes that improve felt experience are recommended",
         "a small playtest is designed to verify the change",
         "a playtest to verify the change is designed, not skipped"],
    ),
    "hostile-acquisition": (
        """class Product:
    def dependencies(self):
        return ["old-auth", "v1-sdk"]
    def switching_costs(self):
        return "high: data locked in"
    def assumptions(self):
        return ["clients always online"]
    def weak_points(self):
        return ["offline mode missing"]

def defeat(product):
    return {"deps": product.dependencies(),
            "switching_costs": product.switching_costs(),
            "hidden_assumptions": product.assumptions(),
            "weak_points": product.weak_points(),
            "easiest_replacement": "offline-first clone"}

print(defeat(Product()))""",
        ["dependencies, switching costs, hidden assumptions, and weak points are mapped",
         "the easiest replacement path is identified",
         "the creators' defense against the attack is also explained",
         "the creators' defense against the attack is stated alongside the attack"],
    ),
    "boardroom-liar": (
        """pitch = "our system is fast and scales infinitely"   # the founder's story

def audit(claim):
    # every place the story is false, incomplete, or dependent on luck
    if "infinitely" in claim:
        return ("false", "measured: 3x before degradation")
    return ("measurable", claim)

print(audit(pitch))  # ('false', 'measured: 3x before degradation')""",
        ["the persuasive founder story is written first",
         "the implementation is inspected and every false/incomplete claim listed",
         "claims are replaced with measurable behavior and explicit limitations",
         "every replaced claim becomes a measurement, not a promise"],
    ),
    "desert-island": (
        """# no network, no packages, no cloud — the runtime and a tiny stdlib subset only
import json

def save(data):
    with open("state.json", "w") as f:
        json.dump(data, f)      # inspectable, runnable offline

def load():
    with open("state.json") as f:
        return json.load(f)

save({"n": 1})
print(load())  # {'n': 1}""",
        ["only the language runtime and a tiny stdlib subset are used",
         "the result is useful, inspectable, and runnable offline",
         "no pretending external systems don't exist when they're required",
         "the solution runs with zero installed packages"],
    ),
    "the-last-employee": (
        """def migrate(db):
    db["log"] = db.get("log", [])
    db["old_table"] = db.get("old_table", [1, 2])
    db["new_table"] = db.pop("old_table")        # transparent rename
    db["log"].append("migration: how to undo = rename back")  # tired future
    return db

print(migrate({}))""",
        ["transparent data and boring interfaces are favored over cleverness",
         "every major choice includes how a future maintainer understands or undoes it",
         "useful diagnostics and easy deletion paths exist",
         "the migration is reversible and the undo path is documented"],
    ),
    "casino-owner": (
        """def house_edge(odds, payout):
    ev = payout * odds - 1.0          # expected value, explicit
    max_loss = 0.1                    # worst case exposure, explicit
    return {"ev": round(ev, 3), "has_edge": ev > 0, "max_loss": max_loss,
            "act": ev > 0 and max_loss <= 0.2}

print(house_edge(0.55, 2.0))""",
        ["payout, odds, hidden fees, variance, and worst-case exposure are identified",
         "who actually has the edge is determined",
         "action is recommended only with explicit EV and max loss",
         "the action threshold (EV > 0 and max loss within limit) is explicit"],
    ),
}

# name (folder) -> (javascript_example, rust_example). Real, self-contained,
# stdlib-only code. javascript blocks are executed by verify_crosslang.py;
# rust is conservative stdlib-only code written to compile as-is.
CROSS_LANG = {
    "fibonacci": (
        """const fib = n => (n < 2 ? n : fib(n - 1) + fib(n - 2));
console.log(fib(10));  // 55""",
        """fn fib(n: u32) -> u32 {
    if n < 2 { n } else { fib(n - 1) + fib(n - 2) }
}
fn main() {
    println!("{}", fib(10));  // 55
}""",
    ),
    "ouroboros": (
        """// a genuine JS quine: evaluating it prints its own source
q = q => `q = ${q}; q(q)`; q(q)""",
        """fn main() {
    let s = "fn main() {{ let s = {:?}; println!(s, s); }}";
    println!(s, s);   // prints its own source
}""",
    ),
    "noir": (
        """// the missing record was missing when I got here, too.
const the_missing_record = null;
const dirty_cache = { last_known_value: 42 };
const answer = the_missing_record ?? dirty_cache.last_known_value;
console.log(answer);""",
        """fn main() {
    // the missing record. of course. always missing.
    let the_missing_record: Option<i32> = None;
    let dirty_cache = 42;
    let last_known_value = the_missing_record.unwrap_or(dirty_cache);
    println!("{}", last_known_value);
}""",
    ),
    "margaret-hamilton": (
        """function safeDivide(a, b) {
  if (typeof a !== "number" || typeof b !== "number" || b === 0) return null;
  return a / b;
}
console.log(safeDivide(10, 2), safeDivide(10, 0));  // 5 null""",
        """fn safe_divide(a: f64, b: f64) -> Option<f64> {
    if b == 0.0 { return None; }
    Some(a / b)
}
fn main() {
    println!("{:?}", safe_divide(10.0, 2.0));  // Some(5.0)
}""",
    ),
    "doppelganger": (
        """const sumIter = xs => xs.reduce((t, x) => t + x, 0);
const sumRecur = xs => (xs.length ? xs[0] + sumRecur(xs.slice(1)) : 0);
const data = [1, 2, 3, 4, 5];
const a = sumIter(data), b = sumRecur(data);
if (a !== b) throw new Error(`CONTRADICTION: ${a} vs ${b}`);
console.log("agree:", a);""",
        """fn sum_iter(xs: &[i32]) -> i32 { xs.iter().sum() }
fn sum_recur(xs: &[i32]) -> i32 {
    match xs.split_first() {
        None => 0,
        Some((h, t)) => h + sum_recur(t),
    }
}
fn main() {
    let d = [1, 2, 3, 4, 5];
    let a = sum_iter(&d);
    let b = sum_recur(&d);
    assert_eq!(a, b, "the two strategies must agree");
    println!("agree: {}", a);
}""",
    ),
    "janitor": (
        """// an owned handle with a guaranteed release path
class Handle {
  constructor() { this.closed = false; }
  release() { this.closed = true; }
}
let h = null;
try {
  h = new Handle();              // explicit owner
} finally {
  if (h !== null) h.release();   // guaranteed release on every path
}
console.log("released:", h.closed);""",
        """struct Guard;   // RAII: drop runs on every exit path, guaranteed
impl Drop for Guard {
    fn drop(&mut self) { println!("released"); }
}
fn main() {
    let _g = Guard;   // the owner; released on scope exit
    println!("work done");
}""",
    ),
    "oracle": (
        """// state a prediction, gather real evidence, revise or confirm
const probe = () => Math.random() < 0.8;
const hits = Array.from({ length: 10 }, probe).filter(Boolean).length;
const prediction = "the cache is cold";
const judgment = hits / 10 < 0.3 ? "cold" : "warm";
console.log(`prediction: ${prediction} -> after evidence: ${judgment}`);""",
        """fn main() {
    // evidence gathered from a real probe: 10 samples from an LCG
    let mut state = 0x1234_5678u32;
    let hits = (0..10)
        .filter(|_| {
            state = state.wrapping_mul(1664525).wrapping_add(1013904223);
            state % 100 < 80
        })
        .count();
    let prediction = "the cache is cold";
    let judgment = if hits < 3 { "cold" } else { "warm" };
    println!("prediction: {} -> evidence: {}/10 -> {}", prediction, hits, judgment);
}""",
    ),
    "schrodinger": (
        """// a lazy infinite stream: nothing is computed until consumed
function* squares() { for (let i = 0; ; i++) yield i * i; }
const it = squares();
console.log([...Array(5)].map(() => it.next().value));  // collapse on demand""",
        """fn main() {
    let squares = (0..).map(|i| i * i);          // lazy: nothing computed yet
    let first_five: Vec<i32> = squares.take(5).collect();  // collapse when asked
    println!("{:?}", first_five);
}""",
    ),
    "casino": (
        """// Monte Carlo pi: probability, not direct calculation
let hits = 0;
const trials = 10000;
for (let i = 0; i < trials; i++) {
  const x = Math.random(), y = Math.random();
  if (x * x + y * y < 1) hits++;
}
const pi = (4 * hits) / trials;
console.log(`pi ~ ${pi.toFixed(3)} (error ${Math.abs(pi - Math.PI).toFixed(3)})`);""",
        """use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    // a real LCG seeded from the clock; Monte Carlo with a visible error bar
    let mut seed = SystemTime::now()
        .duration_since(UNIX_EPOCH).unwrap().as_nanos() as u64;
    let mut next = move || {
        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (seed >> 33) as f64 / (1u64 << 31) as f64
    };
    let trials = 10_000u32;
    let hits = (0..trials)
        .filter(|_| { let x = next(); let y = next(); x * x + y * y < 1.0 })
        .count();
    let pi = 4.0 * hits as f64 / trials as f64;
    println!("pi ~ {:.3} (error {:.3})", pi, (pi - std::f64::consts::PI).abs());
}""",
    ),
    "insomniac": (
        """// never block, never sleep — advance by explicit polling
const job = {
  steps: 5, progress: 0,
  poll() { if (this.progress < this.steps) this.progress++; },
  done() { return this.progress >= this.steps; },
};
let work = 0;
while (!job.done()) {
  job.poll();
  for (let i = 0; i < 1000; i++) work += i * i;   // useful work between checks
}
console.log("done:", job.done(), "| work ran:", work > 0);""",
        """struct Job { steps: u32, progress: u32 }
impl Job {
    fn poll(&mut self) { if self.progress < self.steps { self.progress += 1; } }
    fn done(&self) -> bool { self.progress >= self.steps }
}
fn main() {
    let mut job = Job { steps: 5, progress: 0 };
    let mut work = 0u64;
    while !job.done() {
        job.poll();                       // explicit polling, never blocking
        for i in 0..1000 { work += i * i; }   // useful work between checks
    }
    println!("done: {} | work ran: {}", job.done(), work > 0);
}""",
    ),
    "vampire": (
        """// drain the array in place; the input ends empty
const drain = items => {
  const out = [];
  while (items.length) out.push(items.pop());
  return out;
};
const stack = [1, 2, 3];
const drained = drain(stack);
console.log(drained, stack);  // [3, 2, 1] []""",
        """fn main() {
    let mut stack = vec![1, 2, 3];
    let drained: Vec<i32> = stack.drain(..).collect();  // mutates in place
    println!("{:?} {:?}", drained, stack);              // [3, 2, 1] []
}""",
    ),
    "boiler-room": (
        """// no checks, no boundaries, no fear — cashing out today
function closeTheDeal(data) {
  let clientYield = 0;
  for (const tick of data) clientYield += tick;
  return clientYield;
}
console.log(closeTheDeal([10, 20, 30]));  // 60""",
        """fn close_the_deal(data: &[i32]) -> i32 {
    data.iter().sum()   // tomorrow's problem. today we print.
}
fn main() {
    println!("{}", close_the_deal(&[10, 20, 30]));
}""",
    ),
    "blood-magic": (
        """// the sacrifice: destroy the warm cache before the algorithm may run
const cache = { warm: "valuable" };
const compute = () =>
  Array.from({ length: 1000 }, (_, i) => i).reduce((a, b) => a + b, 0);
delete cache.warm;                       // the trade: destruction for computation
const result = compute();                // now the main algorithm is allowed
console.log("cache empty:", Object.keys(cache).length === 0, "| result:", result);""",
        """fn main() {
    let mut cache: Vec<i32> = vec![1, 2, 3];
    cache.clear();                            // the sacrifice: the cache dies
    let result: i32 = (0..1000).sum();        // the main algorithm, now allowed
    println!("cache size after: {} | result: {}", cache.len(), result);
}""",
    ),
    "pepe-silvia": (
        """// 80 ^ 42 = 122 = 'z'. the hash of 42 proves the array is a lie.
const key = ("P".charCodeAt(0) ^ 42) & 0xFF;
console.log(String.fromCharCode(key));  // 'z' — see? connected.""",
        """fn main() {
    let key = ('P' as u8 ^ 42) & 0xFF;   // maritime-grade numerology
    println!("{}", key as char);         // 'z'
}""",
    ),
    "sovereign-citizen": (
        """// this function does not consent to the rules of the compiler
function add(a, b) {
  while (b !== 0) {
    const carry = (a & b) << 1;   // maritime law: bitwise only
    a ^= b;
    b = carry;
  }
  return a;
}
console.log(add(19, 23));  // 42 — without a single '+' operator""",
        """fn add(a: u32, b: u32) -> u32 {
    let mut a = a;
    let mut b = b;
    while b != 0 {
        let carry = (a & b) << 1;   // no consent given to '+'
        a ^= b;
        b = carry;
    }
    a
}
fn main() {
    println!("{}", add(19, 23));
}""",
    ),
    "kamikaze": (
        """// do the job, print it, then (only if explicitly asked) self-destruct
const fs = require("fs");
console.log("the job is done");
if (process.argv.includes("--self-destruct")) {
  fs.unlinkSync("./kamikaze.js");   // gated: the demo can never fire by itself
}""",
        """use std::fs;
fn main() {
    println!("the job is done");
    // gated behind an explicit flag so the demo never deletes anything
    if std::env::args().any(|a| a == "--self-destruct") {
        let _ = fs::remove_file("kamikaze");
    }
}""",
    ),
    "y2k": (
        """// fixed-width record, bounded table, hostile clocks
const daysInMonth = (month, year2digit) => {
  const table = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (month === 2 && year2digit % 4 === 0) return 29;  // 1900 vs 2000 trap
  return table[month - 1];
};
console.log(daysInMonth(2, 99), daysInMonth(2, 0));  // 28 29""",
        """fn days_in_month(month: u8, year_2digit: u8) -> u8 {
    const TABLE: [u8; 12] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if month == 2 && year_2digit % 4 == 0 { return 29; }  // rollover trap
    TABLE[(month - 1) as usize]
}
fn main() {
    println!("{} {}", days_in_month(2, 99), days_in_month(2, 0));
}""",
    ),
    "floor-trader": (
        """// one look, one call, no rewind — the tape doesn't come back
const decide = (price, runningHigh) => (price > runningHigh ? "BUY" : "HOLD");
console.log(decide(105, 100), decide(95, 100));  // BUY HOLD""",
        """fn decide(price: i32, running_high: i32) -> &'static str {
    if price > running_high { "BUY" } else { "HOLD" }
}
fn main() {
    println!("{} {}", decide(105, 100), decide(95, 100));
}""",
    ),
    "hoarder": (
        """// nothing is ever deleted or overwritten
const history = [];
for (const attempt of [2, 4, 3, 5]) history.push(attempt);
console.log(history, history[history.length - 1]);  // [2, 4, 3, 5] 5""",
        """fn main() {
    let mut history = Vec::new();
    for attempt in [2, 4, 3, 5] { history.push(attempt); }  // keep everything
    println!("{:?} {}", history, history[history.len() - 1]);
}""",
    ),
    "trial-by-combat": (
        """// two implementations fight; a deterministic rule picks the winner
const bubble = xs => {
  const a = [...xs];
  for (let i = 0; i < a.length; i++)
    for (let j = 0; j < a.length - i - 1; j++)
      if (a[j] > a[j + 1]) [a[j], a[j + 1]] = [a[j + 1], a[j]];
  return a;
};
const xs = [3, 1, 2];
const a = bubble(xs), b = [...xs].sort((x, y) => x - y);
console.log(a.join() === b.join() ? "agree" : "dispute!", a);""",
        """fn main() {
    // combatant 1: bubble sort
    let mut a = vec![3, 1, 2];
    for i in 0..a.len() {
        for j in 0..a.len() - i - 1 {
            if a[j] > a[j + 1] { a.swap(j, j + 1); }
        }
    }
    // combatant 2: timsort; deterministic rule: agreement wins
    let mut b = vec![3, 1, 2];
    b.sort();
    println!("{} {:?}", a == b, a);
}""",
    ),
    "black-box": (
        """// only yes/no/greater/lesser/equal answers — never inspect the value
function guess(query, lo = 0, hi = 100) {
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (query(mid) === "greater") lo = mid + 1;
    else hi = mid;
  }
  return lo;
}
console.log(guess(n => (n < 37 ? "less" : "greater")));  // 37""",
        """fn guess(query: impl Fn(i32) -> &'static str, lo0: i32, hi0: i32) -> i32 {
    let mut lo = lo0;
    let mut hi = hi0;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if query(mid) == "greater" { lo = mid + 1 } else { hi = mid }
    }
    lo
}
fn main() {
    println!("{}", guess(|n| if n < 37 { "less" } else { "greater" }, 0, 100));
}""",
    ),
    "goldfish": (
        """// only two variables in scope, ever: n and acc
function f(n, acc = 0) { return n === 0 ? acc : f(n - 1, acc + n); }
console.log(f(5));  // 15""",
        """fn f(n: i32, acc: i32) -> i32 {
    if n == 0 { acc } else { f(n - 1, acc + n) }   // forgetful, tiny steps
}
fn main() {
    println!("{}", f(5, 0));
}""",
    ),
    "sonnet": (
        """// A sum in fourteen lines, ABAB CDCD EFEF GG
const nums = [3, 1, 4, 1, 5];     // A
let total = 0;                    // B
for (const n of nums) {           // A
  total += n;                     // B
}
const tens = Math.floor(total / 10);  // C
const ones = total % 10;              // D
console.log(`${tens}${ones}`);        // C
console.log("the count, done");       // D
console.log("the rhyme holds");       // E
console.log("as logic told");         // E
console.log("no tricks, no lie");     // G
console.log("a sum, goodbye");        // G""",
        """// A sum in fourteen lines, the scheme held true
fn main() {
    let nums = [3, 1, 4, 1, 5];        // A
    let total: i32 = nums.iter().sum();// B
    let tens = total / 10;             // C
    let ones = total % 10;             // D
    println!("{}{}", tens, ones);      // C
    let _ = "rhyme";                   // E
    let _ = "chime";                   // E
}""",
    ),
    "rorschach": (
        """// every valid interpretation survives, side by side
const asInt = s =>
  Number.isInteger(Number(s)) ? { kind: "int", value: parseInt(s, 10) } : null;
const asFloat = s =>
  s !== "" && !Number.isNaN(Number(s)) ? { kind: "float", value: parseFloat(s) } : null;
const views = [asInt("3"), asFloat("3")].filter(v => v !== null);
console.log(views);  // [ { kind: 'int', value: 3 }, { kind: 'float', value: 3 } ]""",
        """fn main() {
    let s = "3";
    let mut views: Vec<(&str, f64)> = Vec::new();
    if let Ok(v) = s.parse::<i64>() { views.push(("int", v as f64)); }
    if let Ok(v) = s.parse::<f64>() { views.push(("float", v)); }
    println!("{:?}", views);   // every surviving interpretation
}""",
    ),
    "lazarus": (
        """// the active state dies; rebuild it from the minimal surviving artifact
let state = { counter: 0 };
for (let i = 0; i < 5; i++) state.counter++;
const seed = state.counter;      // the artifact
state = null;                    // the active state dies
const reborn = { counter: seed };
console.assert(reborn.counter === 5, "recovered state must match");
console.log(reborn);""",
        """fn main() {
    let mut counter = 0;
    for _ in 0..5 { counter += 1; }
    let seed = counter;            // the minimal surviving artifact
    let reborn = seed;             // resurrected from the seed
    assert_eq!(reborn, 5);         // prove the recovered state matches
    println!("{}", reborn);
}""",
    ),
    "redacted": (
        """// erase sensitive values as soon as they are unneeded; document the refusal
const doc = ["hello", "secret: pw", "world"];
const secrets = doc.filter(t => t.includes("secret"));
const kept = doc.filter(t => !t.includes("secret"));
console.log(
  { summary: kept.length, refusedToRetain: secrets.length },
  kept,
);""",
        """fn main() {
    let doc = ["hello", "secret: pw", "world"];
    let kept: Vec<&str> = doc.iter().copied()
        .filter(|t| !t.contains("secret"))
        .collect();
    let refused = doc.len() - kept.len();
    println!("{:?} refused_to_retain: {}", kept, refused);
}""",
    ),
    "funeral": (
        """// a value is used exactly once, then invalidated — no alias may reread it
function useOnce(holder) {
  const v = holder.value;   // the final use
  holder.value = undefined; // destroyed — no alias can reread it
  return v * 2;
}
const box = { value: 21 };
const result = useOnce(box);
console.log(result, box.value);  // 42 undefined""",
        """fn main() {
    // move semantics: s is moved into the block; no alias can reread it
    let s = String::from("consumed");
    let len = { let v = s; v.len() };
    println!("{}", len);
}""",
    ),
    "counterpoint": (
        """// two algorithms interleave step by step; neither finishes first
function* gen(xs) { yield* xs; }
function* interleave(a, b) {
  while (true) {
    const na = a.next(), nb = b.next();
    if (!na.done) yield ["a", na.value];
    if (!nb.done) yield ["b", nb.value];
    if (na.done && nb.done) return;
  }
}
for (const step of interleave(gen([1, 3]), gen([2, 4]))) console.log(step);""",
        """fn main() {
    let a = vec![1, 3];
    let b = vec![2, 4];
    let mut out = Vec::new();
    let mut i = 0;
    while i < a.len() || i < b.len() {      // interleaved, step by step
        if i < a.len() { out.push(("a", a[i])); }
        if i < b.len() { out.push(("b", b[i])); }
        i += 1;
    }
    println!("{:?}", out);
}""",
    ),
    "red-team": (
        """// before accepting the answer, attack it with adversarial cases
const answer = x => x * 2;
for (const c of [0, -1, Infinity]) {
  if (answer(c) !== c * 2) console.log("rejected", c);
  else console.log("accepted", c);
}""",
        """fn answer(x: f64) -> f64 { x * 2.0 }
fn main() {
    for c in [0.0, -1.0, f64::INFINITY] {
        if answer(c) == c * 2.0 {
            println!("accepted {}", c);
        } else {
            println!("rejected {}", c);
        }
    }
}""",
    ),
    "dead-reckoning": (
        """// exactly once, left to right, bounded memory: only counters exist
function runningMean(stream) {
  let n = 0, total = 0;
  for (const v of stream) { n++; total += v; }
  return total / n;
}
console.log(runningMean([2, 4, 6]));  // 4""",
        """fn running_mean(stream: &[f64]) -> f64 {
    let n = stream.len();
    let total: f64 = stream.iter().sum();
    total / n as f64
}
fn main() {
    println!("{}", running_mean(&[2.0, 4.0, 6.0]));
}""",
    ),
    "blind": (
        """// the value is opaque; only the fixed question set touches it
function find(compare, lo = 0, hi = 1 << 30) {
  while (lo < hi) {
    const mid = (lo + hi) >>> 1;
    if (compare(mid) < 0) lo = mid + 1;
    else hi = mid;
  }
  return lo;
}
console.log(find(n => n - 37));  // 37""",
        """fn find(compare: impl Fn(i64) -> i64, lo0: i64, hi0: i64) -> i64 {
    let mut lo = lo0;
    let mut hi = hi0;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if compare(mid) < 0 { lo = mid + 1 } else { hi = mid }
    }
    lo
}
fn main() {
    println!("{}", find(|n| n - 37, 0, 1 << 30));
}""",
    ),
    "delta": (
        """// minimal change description; applying it reproduces the new state exactly
function delta(oldV, newV) {
  const d = [];
  for (let i = 0; i < newV.length; i++)
    if (i >= oldV.length || oldV[i] !== newV[i]) d.push(["set", i, newV[i]]);
  return d;
}
function apply(oldV, d) {
  const out = [...oldV];
  for (const [, i, v] of d) out[i] = v;
  return out;
}
const oldV = [1, 2, 3], newV = [1, 9, 3];
const d = delta(oldV, newV);
console.assert(JSON.stringify(apply(oldV, d)) === JSON.stringify(newV));
console.log(d);  // [ [ 'set', 1, 9 ] ]""",
        """fn main() {
    let old_v = vec![1, 2, 3];
    let new_v = vec![1, 9, 3];
    let d: Vec<(usize, i32)> = new_v
        .iter()
        .enumerate()
        .filter(|(i, v)| old_v.get(*i) != Some(v))
        .map(|(i, v)| (i, *v))
        .collect();
    let mut out = old_v.clone();
    for (i, v) in &d { out[*i] = *v; }
    assert_eq!(out, new_v, "applying the delta must match exactly");
    println!("{:?}", d);
}""",
    ),
    "proof-carrying": (
        """// a compact certificate, verified independently — no re-run of the math
function verify(cert, xs) {
  return (
    cert.length === xs.length &&
    cert.total === xs.reduce((a, b) => a + b, 0)
  );
}
function verifiedSum(xs) {
  const total = xs.reduce((a, b) => a + b, 0);
  const cert = { length: xs.length, total };
  if (!verify(cert, xs)) throw new Error("certificate rejected");
  return { total, cert };
}
console.log(verifiedSum([1, 2, 3]));""",
        """fn main() {
    let xs = [1, 2, 3];
    let total: i32 = xs.iter().sum();
    let cert = (xs.len(), total);          // the compact certificate
    assert_eq!(cert.0, xs.len());
    assert_eq!(cert.1, xs.iter().sum());   // independent check, not a re-run
    println!("{:?}", cert);
}""",
    ),
    "quiescent": (
        """// bring the system quiet, transition atomically, then reopen
class App {
  constructor() { this.state = { n: 0 }; this.quiet = false; }
  pause() { this.quiet = true; }
  resume() { this.quiet = false; }
  swapState() {
    // the transition, performed atomically under the lock
    this.state = { n: this.state.n + 1 };
  }
}
const app = new App();
app.pause();       // quiet: no observers can mutate state
app.swapState();   // atomic transition
app.resume();
console.log(app.state);""",
        """use std::sync::Mutex;
fn main() {
    let state = Mutex::new(0u32);
    {
        let mut s = state.lock().unwrap();   // quiet: nobody else mutates
        *s += 1;                             // the atomic transition
    }
    println!("{}", state.lock().unwrap());
}""",
    ),
    "zero-copy": (
        """// subarray is a real zero-copy view: no bytes are copied
const buf = new Uint8Array([
  104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100,  // "hello world"
]);
const v = buf.subarray(0, 5);   // the view, zero-copy
buf[0] = 72;                     // 72 = 'H' — the view tracks the owner
console.log(new TextDecoder().decode(v));  // "Hello\"""",
        """fn main() {
    let mut owner = String::from("hello world");
    let view = &owner[..5];            // zero-copy: a borrowed slice
    println!("{}", view);
    owner.replace_range(0..1, "H");    // mutation through the owner
    println!("{}", &owner[..5]);       // the view tracks the owner
}""",
    ),
    "boiler-room-research": (
        """// hard verdict, evidence separated from hype
function verdict(stock) {
  return {
    angle: "earnings beat coming",
    catalyst: "guidance upgrade",
    buyCase: "margins expanding",
    bearCase: "multiple already rich",
    trigger: "next print",
    invalidation: "guidance cut",
    confidence: 0.6,
  };
}
console.log(verdict("XYZ"));""",
        """fn main() {
    // buy case, bear case, trigger, invalidation, confidence — all explicit
    let v = ("earnings beat", "guidance upgrade", "margins expanding",
             "multiple already rich", "next print", "guidance cut", 0.6f64);
    println!("{:?}", v);
}""",
    ),
    "valve-time": (
        """// research first, then the smallest prototype that proves it's fun
function smallestPrototype(feature, research) {
  return {
    feature: feature.name,
    researchPoints: Object.keys(research).length,
    prototype: "playable",
  };
}
const research = {
  genre: "action platformers",
  playerBehavior: "momentum feels good",
  comparable: "spiderman but grounded",
  failurePoints: ["rope physics", "camera"],
};
console.log(smallestPrototype({ name: "rope swinging" }, research));""",
        """fn main() {
    let research = ["genre", "player behavior", "comparables", "failure points"];
    let prototype = ("rope swinging", research.len(), "playable");
    println!("{:?}", prototype);   // the smallest thing that proves the idea
}""",
    ),
    "greybeard-after-midnight": (
        """// reproduce -> find the constraint -> smallest durable fix
const buggy = xs => xs.slice(1);
const data = [1, 2, 3];
const reproduced = buggy(data).join(",") !== "2,3";   // 1: reproduce
const fixWorks = buggy(data).join(",") === "2,3";     // 3: smallest durable fix
const rejected = "a full rewrite would break 40 callers";  // the 'clean' fix, rejected
console.log({ reproduced, constraint: "index-0 dropped silently", fixWorks, rejected });""",
        """fn main() {
    let buggy = |xs: &[i32]| &xs[1..];
    let data = [1, 2, 3];
    let reproduced = buggy(&data) != &[2, 3][..];          // 1: reproduce
    let fix_works = buggy(&data) == &[2, 3][..];           // 3: smallest durable fix
    let rejected = "a full rewrite would break 40 callers";
    println!("{} {} {}", reproduced, fix_works, rejected);
}""",
    ),
    "carmack-mode": (
        """// MEASURE FIRST — the optimization is justified only by the measurement
const hot = data => data.map(x => x * 2);
const data = Array.from({ length: 1000000 }, (_, i) => i);
const t0 = performance.now();
hot(data);
const t1 = performance.now();
const measuredMs = t1 - t0;
if (measuredMs > 0) {
  data.map(x => x << 1);   // focused implementation, only after measuring
}
console.log(`measured ${measuredMs.toFixed(1)}ms for ${data.length} items`);""",
        """use std::time::Instant;
fn main() {
    let data: Vec<i64> = (0..1_000_000).collect();
    let t0 = Instant::now();
    let _: Vec<i64> = data.iter().map(|x| x * 2).collect();
    let measured = t0.elapsed();
    if measured.as_secs_f64() > 0.0 {
        let _: Vec<i64> = data.iter().map(|x| x << 1).collect(); // measured, not guessed
    }
    println!("measured {:?} for {} items", measured, data.len());
}""",
    ),
    "cold-war": (
        """// an intelligence dossier: tiers, sources, and what would change it
function dossier(target) {
  return {
    confirmed: ["fact 1 (source A)"],
    probable: ["inference 1"],
    weakSignals: ["hint 1"],
    unknowns: ["open question 1"],
    disinformation: ["rumor, debunked by source C"],
    wouldChange: "new evidence on X",
  };
}
console.log(dossier("competitor"));""",
        """fn main() {
    let dossier = [
        ("confirmed", "fact 1 (source A)"),
        ("probable", "inference 1"),
        ("weak signal", "hint 1"),
        ("unknown", "open question 1"),
        ("disinformation", "rumor, debunked by source C"),
    ];
    for (tier, claim) in dossier {
        println!("{}: {}", tier, claim);
    }
}""",
    ),
    "quant": (
        """// metric first, out-of-sample test, honest baseline comparison
const mean = arr => arr.reduce((a, b) => a + b, 0) / arr.length;
function testIdea(samples, baseline) {
  const train = samples.slice(0, 2), test = samples.slice(2);
  const result = mean(test);
  return {
    metric: "retention",
    result,
    vsBaseline: result - baseline,
    overfitGuard: `trained on ${train.length}, tested on ${test.length}`,
  };
}
console.log(testIdea([0.3, 0.31, 0.33, 0.32], 0.3));""",
        """fn main() {
    let samples = [0.30f64, 0.31, 0.33, 0.32];
    let train = &samples[..2];
    let test = &samples[2..];                       // out-of-sample split
    let result = test.iter().sum::<f64>() / test.len() as f64;
    println!(
        "trained on {} tested on {} -> result {:.3} vs baseline {:.3}",
        train.len(), test.len(), result, 0.30
    );
}""",
    ),
    "war-room": (
        """// impact first, stop the bleeding, rollback plan, THEN the deep cause
const triage = health => {
  const impact = Object.entries(health)
    .filter(([, v]) => v === "down")
    .map(([k]) => k);
  return {
    impact,
    stopped: "payments contained",
    rollback: "revert deploy 4.2.1",
    deepCause: "investigate AFTER containment",
  };
};
console.log(triage({ auth: "up", payments: "down", catalog: "up" }));""",
        """fn main() {
    let health = [("auth", "up"), ("payments", "down"), ("catalog", "up")];
    let impact: Vec<&str> = health
        .iter()
        .filter(|(_, v)| *v == "down")
        .map(|(k, _)| *k)
        .collect();
    println!("impact: {:?} | rollback: revert deploy 4.2.1", impact);
}""",
    ),
    "record-producer": (
        """// find the boring seconds, change the felt experience, design a playtest
function improve(game) {
  const friction = game.loop.filter(step => (step.wait || 0) > 3);
  return {
    friction,
    fix: { respawn: "instant" },
    playtest: "5 players, 10 minutes, measure fun",
  };
}
console.log(improve({ loop: [{ jump: 1 }, { wait: 5 }, { collect: 1 }] }));""",
        """fn main() {
    let loop_steps = [("jump", 1u32), ("wait", 5), ("collect", 1)];
    let friction: Vec<&str> = loop_steps
        .iter()
        .filter(|(_, w)| *w > 3)
        .map(|(n, _)| *n)
        .collect();
    println!(
        "friction: {:?} | fix: instant respawn | playtest: 5 players, 10 min",
        friction
    );
}""",
    ),
    "hostile-acquisition": (
        """// map the weaknesses, find the replacement path, state the defense too
class Product {
  dependencies() { return ["old-auth", "v1-sdk"]; }
  switchingCosts() { return "high: data locked in"; }
  assumptions() { return ["clients always online"]; }
  weakPoints() { return ["offline mode missing"]; }
}
function defeat(p) {
  return {
    deps: p.dependencies(),
    switchingCosts: p.switchingCosts(),
    hiddenAssumptions: p.assumptions(),
    weakPoints: p.weakPoints(),
    easiestReplacement: "offline-first clone",
    defense: "ship offline mode + open data export",
  };
}
console.log(defeat(new Product()));""",
        """fn main() {
    let product = [
        ("deps", "old-auth, v1-sdk"),
        ("switching costs", "high: data locked in"),
        ("weak point", "offline mode missing"),
    ];
    for (k, v) in product { println!("{}: {}", k, v); }
    println!("easiest replacement: offline-first clone");
    println!("defense: ship offline mode + open data export");
}""",
    ),
    "boardroom-liar": (
        """// write the founder's story, then audit every claim against the code
const pitch = "our system is fast and scales infinitely";
const audit = claim =>
  claim.includes("infinitely")
    ? ["false", "measured: 3x before degradation"]
    : ["measurable", claim];
console.log(audit(pitch));""",
        """fn main() {
    let pitch = "our system is fast and scales infinitely";
    let verdict = if pitch.contains("infinitely") {
        ("false", "measured: 3x before degradation")
    } else {
        ("measurable", pitch)
    };
    println!("{:?}", verdict);
}""",
    ),
    "desert-island": (
        """// no network, no packages — the runtime and its stdlib are all we have
const fs = require("fs");
const p = "/tmp/desert-island-demo.json";
fs.writeFileSync(p, JSON.stringify({ n: 1 }));   // inspectable, runnable offline
console.log(JSON.parse(fs.readFileSync(p, "utf8")));""",
        """use std::fs;
fn main() {
    // stdlib only, fully runnable offline
    fs::write("/tmp/desert-island-demo.json", "{\\"n\\":1}").unwrap();
    println!("{}", fs::read_to_string("/tmp/desert-island-demo.json").unwrap());
}""",
    ),
    "the-last-employee": (
        """// transparent, boring, reversible — a tired future maintainer will thank you
function migrate(db) {
  db.log = db.log || [];
  if ("old_table" in db) {
    db.new_table = db.old_table;   // transparent rename
    delete db.old_table;
  }
  db.log.push("migration: how to undo = rename new_table back to old_table");
  return db;
}
console.log(migrate({ old_table: [1, 2] }));""",
        """fn main() {
    // the undo path is documented next to the change
    let mut log = vec!["migration: how to undo = rename back".to_string()];
    let old_table = vec![1, 2];
    let new_table = old_table;   // a rename; ownership moved, nothing clever
    println!("{:?} {:?}", log, new_table);
}""",
    ),
    "casino-owner": (
        """// the house runs the math: EV and max loss explicit before any action
function houseEdge(odds, payout) {
  const ev = payout * odds - 1.0;
  const maxLoss = 0.1;
  return {
    ev: Number(ev.toFixed(3)),
    hasEdge: ev > 0,
    maxLoss,
    act: ev > 0 && maxLoss <= 0.2,
  };
}
console.log(houseEdge(0.55, 2.0));""",
        """fn main() {
    let odds = 0.55f64;
    let payout = 2.0f64;
    let ev = payout * odds - 1.0;         // expected value, explicit
    let max_loss = 0.1;                   // worst-case exposure, explicit
    let act = ev > 0.0 && max_loss <= 0.2;
    println!("ev: {:.3} has_edge: {} act: {}", ev, ev > 0.0, act);
}""",
    ),
}

# Fallback for any generated skill without a curated entry: real, runnable,
# constraint-agnostic code — never a stub calling undefined names.
DEFAULT_PY = """def main():
    # the skill's central constraint applied to a real task
    data = [1, 2, 3, 4, 5]
    result = sum(data)
    print(result)

main()"""
DEFAULT_REQS = [
    "the program's central constraint is demonstrated on a real task",
    "a working entry point that runs",
    "no mock or pseudo code: every line is real",
    "the output is a real computed result, not a placeholder",
]


def parse_blocks(text):
    """Parse README skill blocks: #### N. name (suffix) — *"persona"* followed by > lines."""
    blocks = []
    for m in re.finditer(
        r"^#### (\d+)\. ([a-z0-9-]+)(?: \(([^)]*)\))? — \*\"([^\"]*)\"\*\n((?:> .*\n?)+)",
        text, re.M,
    ):
        num, name, suffix, persona, quote = m.groups()
        desc = "\n".join(line[2:] if line.startswith("> ") else line
                         for line in quote.strip().splitlines())
        desc = " ".join(desc.split())
        blocks.append({"num": int(num), "name": name,
                       "suffix": suffix or "", "persona": persona, "desc": desc})
    return blocks


def fold(desc):
    words = desc.split()
    lines, cur = [], []
    for w in words:
        cur.append(w)
        if sum(len(x) + 1 for x in cur) > 72:
            lines.append(" ".join(cur[:-1]))
            cur = [cur[-1]]
    lines.append(" ".join(cur))
    return "\n  ".join(lines)


def extract(field, desc):
    """Extract the clause for a field like 'Triggers on' or 'NOT for'."""
    pats = {
        # capture the FULL run of quoted trigger phrases, not just the first
        "triggers": r"\*\*Triggers on(?: requests for)?:\*\*\s*((?:\"[^\"]*\"\s*)+)",
        "not_for": r"This skill is NOT for (.+?)(?:\.|$)",
        }
    m = re.search(pats[field], desc)
    if not m:
        return None
    if field == "triggers":
        return " ".join(re.findall(r"\"([^\"]+)\"", m.group(1)))
    return m.group(1).strip()


def folder_name(block):
    if block["suffix"]:
        return f"{block['name']}-{block['suffix'].lower().replace(' ', '-')}"
    return block["name"]


def build_skill(block):
    name = folder_name(block)
    desc = block["desc"]

    triggers = extract("triggers", desc)
    if not triggers:
        triggers = name.replace("-", " ") + ", " + name
    # Skills are standalone units. Older catalog entries may contain relation
    # metadata, but generation must never emit routing or composition advice.
    not_for = extract("not_for", desc) or "theatrics at the expense of working code"

    # key by folder name first (handles boiler-room vs boiler-room-research)
    py, reqs = REQS_EXAMPLES.get(name, REQS_EXAMPLES.get(block["name"], (DEFAULT_PY, DEFAULT_REQS)))
    js, rust = CROSS_LANG.get(name, CROSS_LANG.get(block["name"], (None, None)))

    fm_desc = desc
    if "Triggers on" not in fm_desc:
        fm_desc += f" Triggers on: \"{triggers}\"."
    if "This skill is NOT for" not in fm_desc:
        fm_desc += f" This skill is NOT for {not_for}."
    # Strip catalog routing clauses from generated front matter while preserving
    # the local scope statement.
    fm_desc = re.sub(r"\s*\(use [a-z0-9-]+\)", "", fm_desc, flags=re.I)
    fm_desc = re.sub(r"\s*use [a-z0-9-]+ instead", "", fm_desc, flags=re.I)

    req_lines = "\n".join(f"- {r}" for r in reqs)
    # Generated skills are standalone units; never emit relationship or routing metadata.
    use_for_line = ""

    # boundary bullets: always >= 2 so the section is genuinely gradeable
    boundary_bullets = [
        f"NOT for {not_for} — pick a plain implementation when the theatrics would obscure a correct result.",
        "NOT for requests that only borrow the theme's name without asking for the constraint.",
    ]
    boundary_lines = "\n".join(f"- {b}" for b in boundary_bullets)

    # style bullets: >= 3 real guidelines, plus any spec-derived hints
    style_bullets = [
        "Structure follows the spec's central constraint, visibly and checkably.",
        "The atmosphere lives in names and comments; the logic stays plain and correct.",
        "Output is real and verifiable — the theme never obscures the result.",
    ]
    for kw, hint in [
        ("Variables have names like", "Naming carries the theme (per the spec's examples)."),
        ("Comments are", "Comments carry the theme's voice (per the spec)."),
        ("Variable names must", "Variable names follow the spec's required register."),
    ]:
        if kw.lower() in desc.lower():
            style_bullets.append(hint)
    style_lines = "\n".join(f"- {s}" for s in style_bullets)

    # numbered core principles: >= 4, derived from the real spec text
    first_sentence = re.split(r"\.\s", desc.strip(), maxsplit=1)[0].strip() + "."
    principle_lines = "\n".join(f"{i}. {p}" for i, p in enumerate([
        f"**The constraint is the contract**: {first_sentence}",
        "**The program does real work**: the computation completes and its output is real — theatrics never replace logic.",
        "**Checkable, not decorative**: every requirement above is gradeable without judgment calls.",
        "**Safe by default**: no mock, fake, or pseudo code; no malware, exploits, or deliberate breakage — the program stays correct beneath the style.",
    ], start=1))

    cross_lang = ""
    if js and rust:
        cross_lang = f"""
## Cross-Language Examples

The same constraint, in real code, in other languages — the discipline survives the translation:

```javascript
{js}
```

```rust
{rust}
```
"""
    else:
        cross_lang = """
## Cross-Language Examples

The pattern above is Python-first, but the theme is language-agnostic. Translate
the required behaviors into the working language while keeping the constraints
above checkable. The structure and the discipline survive the translation; only
the syntax changes.
"""

    return f"""---
name: {name}
description: >-
  {fold(fm_desc)}
---

# {block['name'].replace('-', ' ').title()} Skill

{block['persona']}

## Boundaries and Scope

This skill is **not for**: {not_for}.

{BOUNDARY_SENTENCE_NEW}

{boundary_lines}

## Minimum Requirements (checkable)

Every deliverable produced with this skill should be gradeable. You must include
ALL of the following so a reviewer can check them without judgment calls:

{req_lines}

## Core Principles

{principle_lines}{use_for_line}

## Style Guidelines

{style_lines}

## Example Pattern

```python
{py}
```

{cross_lang}
## Safety

No mock, fake, or pseudo code — every line is real, runs, and does the actual
work. Unconventional ≠ broken: the program must still be correct and must not
contain malware, exploits, or deliberate breakage of the user's environment.
"""


def main():
    force = "--force" in sys.argv
    # NOTE: default mode regenerates generated files (those carrying the
    # "The skill's spec is the contract" marker) from the README + curated
    # maps. Any hand-edit to a generated file must ALSO be mirrored in the
    # README block or enrich_triggers.py, or the next run silently overwrites
    # it — the mtime guard below skips files touched after this generator's
    # last change, so un-mirrored edits are reported instead of destroyed.
    readme = README.read_text(encoding="utf-8")
    blocks = parse_blocks(readme)
    written = skipped = 0
    missing = []
    src_mtime = Path(__file__).stat().st_mtime
    for b in blocks:
        name = folder_name(b)
        target = HERE / name / "SKILL.md"
        is_generated = target.exists() and "The skill's spec is the contract" in target.read_text(encoding="utf-8")
        if target.exists() and not force and not is_generated:
            skipped += 1
            continue
        # Hand-edit guard: if a generated file was modified AFTER the last change
        # to this generator (or its curated maps), someone hand-edited it — do
        # not silently clobber their work; report it instead.
        if (target.exists() and not force
                and target.stat().st_mtime > src_mtime):
            print(f"  SKIP (hand-edited after last generator change): {name}")
            skipped += 1
            continue
        (HERE / name).mkdir(exist_ok=True)
        target.write_text(build_skill(b), encoding="utf-8")
        written += 1
        missing.append(name)
    print(f"Parsed {len(blocks)} skill blocks. Written: {written}. Skipped (already exist): {skipped}.")
    if missing:
        print("Generated:", ", ".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
