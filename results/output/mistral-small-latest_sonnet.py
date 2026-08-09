primes = []                  # A: light
n = 2                        # B: bright
while len(primes) < 10:      # A: sight
    is_prime = True          # B: night
    for p in primes:         # C: measure
        if p * p > n:        # D: treasure
            break            # C: measure
        if n % p == 0:       # D: treasure
            is_prime = False # E: art
            break            # F: start
    if is_prime:             # E: art
        primes.append(n)     # F: start
    n += 1                   # G: clear
print(primes)                # G: clear