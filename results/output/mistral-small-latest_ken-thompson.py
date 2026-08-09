import sys
import re

def wc_lines(stream):
    # one job: count lines. brute force is fine.
    return sum(1 for _ in stream)

def grep_lines(pattern, stream):
    # one job, done well: filter lines. brute force is fine.
    rx = re.compile(pattern)
    return [ln.rstrip("\n") for ln in stream if rx.search(ln)]

# brute-force-first: count lines directly instead of using a clever streaming
# algorithm; fits in your head and avoids off-by-one errors
# trust decision: only stdlib used; no external dependencies to trust
# subtraction pass: removed word/char counting; only line counting remains
# small-tool decomposition: grep_lines filters, wc_lines counts
# universal text streams: stdin -> grep_lines -> wc_lines -> stdout
if __name__ == "__main__":
    pattern = sys.argv[1] if len(sys.argv) > 1 else ".*"
    filtered = grep_lines(pattern, sys.stdin)
    print(wc_lines(filtered))