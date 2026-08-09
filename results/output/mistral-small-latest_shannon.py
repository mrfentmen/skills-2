from collections import Counter
import math

def entropy(seq):
    n = len(seq)
    counts = Counter(seq)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())

def prefix_codes(seq):
    counts = Counter(seq)
    rank = [s for s, _ in counts.most_common()]
    return {symbol: ("1" * index) + "0" for index, symbol in enumerate(rank)}

def add_parity(bits):
    return bits + ("1" if bits.count("1") % 2 else "0")

def parity_valid(bits):
    return bits.count("1") % 2 == 0

# Reduction step: strip to essentials — a short, skewed message
message = "hello world"
print("original:", message)

# Entropy audit: measure predictability
H = entropy(message)
print("H =", round(H, 2), "bits/symbol")

# Redundancy decision: strip via compression (source coding)
codes = prefix_codes(message)
compressed = "".join(codes[ch] for ch in message)
print("compressed:", compressed)

# Channel statement: noisy boundary — one bit may flip
noisy = compressed[:-1] + ("1" if compressed[-1] == "0" else "0")

# Add redundancy back for error detection (channel coding)
on_wire = add_parity(noisy)
print("on the wire:", on_wire)

# Recovery: detect corruption and correct if possible
if not parity_valid(on_wire):
    print("corruption detected")
else:
    print("no corruption detected")