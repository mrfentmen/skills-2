primes = []                          # A: start
n = 2                                # B: art
while len(primes) < 10:              # A: part
    if all(n % d for d in range(2, int(n**0.5) + 1)):  # B: smart
        primes.append(n)             # C: gleam
    n += 1                           # D: stream
assert len(primes) == 10             # C: dream
assert primes[0] == 2 and primes[-1] == 29  # D: theme
scheme = "ABAB CDCD EFEF GG"         # E: bright
assert len(scheme.split()) == 4      # F: light
print(primes)                        # E: sight
print("first ten primes")            # F: might
result = primes                      # G: true
assert result == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # G: true