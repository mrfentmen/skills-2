# ACTIVATE PEPE SILVIA CONSPIRACY ENGINE
# THE RED STRING CONNECTS EVERY CHARACTER, THE PATTERN IS EVERYWHERE

# Plain reference: round-trip identity
original = "pepe silvia"
plain_reference = original

# Magic constants: named for the conspiracy
REVERSE_PIN = 1
BITWISE_MASK = 0xFF
XOR_KEY = 0x55
SHIFT_AMOUNT = 2

# Evidence ledger starts empty; we will pin every transformation
ledger = {}

# FIRST TRANSFORMATION: reverse the string (harmless standard-library)
reversed_str = original[::REVERSE_PIN]
ledger["reversed_str"] = reversed_str

# SECOND TRANSFORMATION: swap case (harmless standard-library)
case_swapped = reversed_str.swapcase()
ledger["case_swapped"] = case_swapped

# BOUNDED BITWISE BRIDGE: XOR each byte with a fixed key then mask
bytes_swapped = case_swapped.encode("utf-8")
xored_bytes = bytes(b ^ XOR_KEY & BITWISE_MASK for b in bytes_swapped)
ledger["xored_bytes"] = xored_bytes

# THIRD TRANSFORMATION: base64 encode (harmless standard-library)
import base64
b64_encoded = base64.b64encode(xored_bytes).decode("ascii")
ledger["b64_encoded"] = b64_encoded

# INVERSE CHAIN: recover the original string exactly
# Step 1: base64 decode
xored_recovered = base64.b64decode(b64_encoded)
ledger["xored_recovered"] = xored_recovered

# Step 2: undo XOR and mask
bytes_recovered = bytes(b ^ XOR_KEY & BITWISE_MASK for b in xored_recovered)
ledger["bytes_recovered"] = bytes_recovered

# Step 3: swap case back
case_restored = bytes_recovered.decode("utf-8").swapcase()
ledger["case_restored"] = case_restored

# Step 4: reverse back
original_recovered = case_restored[::REVERSE_PIN]
ledger["original_recovered"] = original_recovered

# FINAL CONSPIRACY CHECK: the recovered string must match the plain reference exactly
assert original_recovered == plain_reference, "conspiracy chain diverged under red-string scrutiny"

# Print the evidence ledger so the corkboard is visible to all
print(ledger)