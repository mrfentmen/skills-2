# ACTIVATING PEPE SILVIA CONSPIRACY ENGINE
# THE STRING IS A TARGET, THE TRANSFORMATIONS ARE RED STRING PINS
# EVERY PIN MUST BE NAMED, EVERY CONSTANT MUST HAVE A ROLE

# PLAIN REFERENCE: FIRST CHARACTER OF THE STRING
PLAIN_REFERENCE = "Pepe Silvia"[0]

# MAGIC CONSTANTS: NAMED FOR THEIR CONSPIRACY ROLE
REVERSE_PIN = 1
BITWISE_MASK = 0x7F
XOR_KEY = 0x55
SHIFT_AMOUNT = 2

# ORIGINAL STRING: THE FIRST TARGET
original = "Pepe Silvia"

# FIRST HARMLESS TRANSFORMATION: REVERSE THE STRING (PIN 1)
reversed_str = original[::REVERSE_PIN]

# SECOND HARMLESS TRANSFORMATION: ROTATE EACH CHARACTER BY +1 (PIN 2)
rotated_str = ''.join(chr((ord(c) + 1) % 128) for c in reversed_str)

# BOUNDED BITWISE OPERATION: XOR WITH MAGIC KEY THEN MASK
xored = [ord(c) ^ XOR_KEY for c in rotated_str]
masked = [b & BITWISE_MASK for b in xored]
bitwise_result = ''.join(chr(b) for b in masked)

# FINAL TRANSFORMATION: SHIFT LEFT BY MAGIC AMOUNT
final_shifted = ''.join(chr(ord(c) << SHIFT_AMOUNT) for c in bitwise_result)

# EVIDENCE LEDGER: EXPOSE ALL PINS FOR AUDIT
ledger = {
    "original": original,
    "reversed_str": reversed_str,
    "rotated_str": rotated_str,
    "xored": xored,
    "masked": masked,
    "bitwise_result": bitwise_result,
    "final_shifted": final_shifted,
    "PLAIN_REFERENCE": PLAIN_REFERENCE,
    "REVERSE_PIN": REVERSE_PIN,
    "BITWISE_MASK": BITWISE_MASK,
    "XOR_KEY": XOR_KEY,
    "SHIFT_AMOUNT": SHIFT_AMOUNT
}

# CONSPIRACY CHECK: DOES THE FINAL RESULT MATCH THE PLAIN REFERENCE?
assert final_shifted[0] == PLAIN_REFERENCE, "CONSPIRACY CHAIN DIVERGED! THE STRING WAS COMPROMISED!"

# PRINT THE LEDGER TO THE CORKBOARD
print(ledger)