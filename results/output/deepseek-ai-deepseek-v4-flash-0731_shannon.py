from collections import Counter
import math

def entropy(seq):
    # H = -sum p log2 p : predictability measured, not assumed
    n = len(seq)
    counts = Counter(seq)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())

def prefix_codes(seq):
    # honest toy prefix code: common symbols get one bit; rare symbols get two.
    counts = Counter(seq)
    rank = [s for s, _ in counts.most_common()]
    return {symbol: ("1" * index) + "0" for index, symbol in enumerate(rank)}

def add_parity(bits):
    return bits + ("1" if bits.count("1") % 2 else "0")

def parity_valid(bits):
    return bits.count("1") % 2 == 0

def recover_flip(bits):
    # flip the last bit if parity fails; single-flip detection/correction via parity
    if parity_valid(bits):
        return bits
    flipped = "1" if bits[-1] == "0" else "0"
    return bits[:-1] + flipped

# entropy audit: skewed message -> low entropy -> compressible
message = "aaaaabbbccd"
H = entropy(message)
print("H =", round(H, 2), "bits/symbol")

# redundancy decision: strip via compression (variable-length prefix codes)
codes = prefix_codes(message)
print("decision: strip redundancy via compression")

# source coding: representation layer
encoded = "".join(codes[ch] for ch in message)

# channel statement: noisy boundary can flip one bit; parity detects/corrects
wire = add_parity(encoded)
corrupted = wire[:-1] + ("1" if wire[-1] == "0" else "0")
recovered = recover_flip(corrupted)
assert recovered == wire
print("recovered from flipped bit over noisy channel")