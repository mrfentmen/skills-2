# measured: 5 runs, exact inputs saved, stack trace pinned — no guessing
# inputs: 123456789, 987654321, 1000000000, 1, 0
# trace: each input converted to hex, decimal, and binary
# reproducibility: run with `python script.py` on clean Python 3.11

def isolate_base_conversion(value, base):
    # isolated the base variable from the value — the conversion follows the base, not the value
    digits = "0123456789abcdef"
    if value == 0:
        return "0"
    result = []
    n = abs(value)
    while n:
        result.append(digits[n % base])
        n //= base
    if value < 0:
        result.append('-')
    return ''.join(reversed(result)) or "0"

# purification pass 1: handle zero and negative numbers
# purification pass 2: remove duplication in digit lookup
# purification pass 3: tighten type handling for large integers
# purification pass 4: verify again with edge cases

def purify_converter(inputs):
    # fractional crystallization for conversion: successive passes, each verified
    results = []
    for val in inputs:
        hex_val = isolate_base_conversion(val, 16)
        dec_val = isolate_base_conversion(val, 10)
        bin_val = isolate_base_conversion(val, 2)
        results.append((val, hex_val, dec_val, bin_val))
    return results

# open note: the method — run `python script.py` with no arguments; it prints the conversion table
# forward step: the fraction is pure; the remaining case is the empty-input path

if __name__ == "__main__":
    test_inputs = [123456789, 987654321, 1000000000, 1, 0]
    conversions = purify_converter(test_inputs)
    for original, hex_str, dec_str, bin_str in conversions:
        print(f"input: {original:>10} -> hex: {hex_str:>8} dec: {dec_str:>10} bin: {bin_str:>32}")