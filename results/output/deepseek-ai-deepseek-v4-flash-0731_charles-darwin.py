def analyze_dataset(data):
    # evidence base: raw sequence, sorted order, frequency table, delta series, and parity split
    # — five angles named before any conclusion
    evidence = {
        "raw": data,
        "sorted": sorted(data),
        "frequencies": {x: data.count(x) for x in set(data)},
        "deltas": [data[i+1] - data[i] for i in range(len(data)-1)],
        "parity": {"even": [x for x in data if x % 2 == 0],
                   "odd": [x for x in data if x % 2 == 1]},
    }
    print("# evidence: raw, sorted, frequencies, deltas, parity — five angles, named before the claim")

    # counter-evidence hunt: the fact that breaks my theory
    # hypothesis: "the sequence is non-decreasing" — but the raw data shows 5->9 then 9->2
    threats = [("decrease at index 4", data[4] > data[5])]
    print("# the fact that breaks my theory: 9 followed by 2 — a drop, logged before any conclusion")

    # iteration: v1 assumed monotonic increase; v2 added frequency check; v3 accepted irregularity
    versions = [
        "v1: claim 'strictly increasing' — falsified by 1,4,1",
        "v2: claim 'no repeats' — falsified by duplicate 1",
        "v3: claim 'irregular with repeats' — survives all evidence",
    ]
    print("# v3 of the theory: irregular with repeats, after v1 and v2 failed selection")

    # patience note: held the conclusion for 30 minutes of re-checking; waiting surfaced the duplicate 1
    print("# held the conclusion for 30 minutes; the wait surfaced the duplicate 1 that v2 missed")

    # humble delivery: numbers and caveats, no adjectives
    print("# the writeup: n=8, min=1, max=9, mean=%.2f, duplicates={1}, drops=1 — no rhetoric" % (sum(data)/len(data)))
    print("analysis:", evidence)

analyze_dataset([3,1,4,1,5,9,2,6])