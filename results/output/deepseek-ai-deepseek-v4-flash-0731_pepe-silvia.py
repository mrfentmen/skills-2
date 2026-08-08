MASK = 0xFF
SHIFT = 1
SEED = 0x5A
message = "conspiracy"
plain_reference = message[0]

# Pin 1: reverse the string (harmless stdlib transformation)
backwards = message[::-1]

# Pin 2: re-reverse to restore original (second harmless stdlib transformation)
restored = "".join(reversed(backwards))

# Pin 3: hex-encode the restored string (third stdlib transformation)
hex_pin = restored.encode("utf-8").hex()

# Pin 4: fold a bounded checksum from the hex bytes
checksum = sum(byte for byte in bytes.fromhex(hex_pin)) & MASK

# Pin 5: bounded bitwise bridge — XOR with checksum, then XOR back, shift right
key = ((ord(restored[0]) ^ checksum) ^ checksum) >> SHIFT

# Pin 6: recover first char via shift-left and OR with LSB
recovered = chr((key << SHIFT) | (ord(restored[0]) & 1))

# Evidence ledger — every pin visible
ledger = {
    "backwards": backwards,
    "restored": restored,
    "hex_pin": hex_pin,
    "checksum": checksum,
    "key": key,
    "recovered": recovered,
    "plain_reference": plain_reference,
}

# The corkboard must not lie — compare against plain reference
assert recovered == plain_reference, "conspiracy chain diverged!"

print(ledger)