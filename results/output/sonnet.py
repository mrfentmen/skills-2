primes = []                          # A: light
n = 2                                # B: bright
while len(primes) < 10:              # A: sight
    if all(n % d for d in range(2, int(n**0.5) + 1)):  # B: night
        primes.append(n)             # C: measure
    n += 1                           # D: treasure
assert len(primes) == 10             # C: measure
assert primes == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # D: treasure
print(primes)                        # E: art
scheme = "ABAB CDCD EFEF GG"         # F: start
assert len(scheme.split()) == 4      # E: art
assert len(primes) == 10             # F: start
print("first ten primes")            # G: clear
assert primes[0] == 2                # G: clear