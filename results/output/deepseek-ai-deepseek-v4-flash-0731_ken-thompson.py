import sys
import re

def filter_lines(stream, pattern):
    # (1) brute-force-first: simple regex scan, no state machines, no indexes
    rx = re.compile(pattern)
    for ln in stream:
        if rx.search(ln):
            yield ln.rstrip("\n")

def count_lines(stream):
    # one job: count lines. no cleverness, just a counter.
    n = 0
    for _ in stream:
        n += 1
    return n

# (2) trust decision: only stdlib (re, sys) — verified by CPython source, no third-party
#     dependencies, no compiler trust beyond the one we already run.
# (3) subtraction pass: threw out option parsing, config files, classes, error handling
#     beyond bare minimum. kept only pattern and stream. no flags, no modes.
# (4) small-tool decomposition: filter_lines does one thing (select), count_lines does
#     one thing (count). each file would be its own tool; here composed in one script.
# (5) universal text/byte streams: filter_lines yields strings, count_lines consumes
#     the same stream. pipe: filter -> count. no objects, no ceremony.

lines = [
    "alpha 42",
    "beta 7",
    "gamma 0",
    "alpha 99",
    "delta 3",
    "alpha 1",
]

# pipeline: filter_lines (grep) | count_lines (wc -l)
result = count_lines(filter_lines(iter(lines), r"alpha"))
print(result)  # 3