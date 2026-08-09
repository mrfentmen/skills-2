import hashlib
import base64

# === NAMED MAGIC CONSTANTS (the pins on the corkboard) ===
MASK_BYTE = 0xFF          # the veil that hides the truth in the low byte
SHIFT_BITS = 3            # the paranoid shuffle that buries the signal
XOR_SEED = 0x5A           # the witness who saw everything but lied
LEDGER_INDEX = 0          # the first pin, where the thread begins

# === PLAIN REFERENCE (the boring truth the conspiracy must match) ===
message = "the mail is never late"
plain_reference = message.upper()

# === PIN 1: base64 — the envelope that disguises the message ===
encoded = base64.b64encode(message.encode("utf-8")).decode("ascii")

# === PIN 2: hashlib — the fingerprint that ties every thread together ===
digest = hashlib.sha256(message.encode("utf-8")).digest()
digest_hex = digest.hex()

# === PIN 3: bounded bitwise bridge — the XOR/mask/shift that recovers the truth ===
# Take the first byte of the digest, XOR with the seed, mask to one byte,
# then shift right by SHIFT_BITS. This is the key that unlocks the case.
key_byte = (digest[LEDGER_INDEX] ^ XOR_SEED) & MASK_BYTE
shifted_key = key_byte >> SHIFT_BITS

# === PIN 4: reconstruct the uppercase via a deterministic chain ===
# Use the shifted key to rotate each character's case through a bounded transform.
# We'll fold the key into a rotation amount, then apply it to each char.
rotation = (shifted_key % 26) + 1  # 1..26, the paranoid spin
transformed_chars = []
for ch in message:
    if ch.isalpha():
        # rotate within alphabet, bounded by 26
        base = ord('A') if ch.isupper() else ord('a')
        rotated = (ord(ch) - base + rotation) % 26
        # now flip case via XOR with 0x20 (the lowercase/uppercase bit)
        flipped = chr((base + rotated) ^ 0x20)
        transformed_chars.append(flipped)
    else:
        transformed_chars.append(ch)
transformed = "".join(transformed_chars)

# === PIN 5: reverse the rotation to get uppercase (the confession) ===
# The rotation was applied to lowercase/uppercase, but we want uppercase.
# We'll undo the rotation and force uppercase via a mask.
final_chars = []
for ch in transformed:
    if ch.isalpha():
        base = ord('A') if ch.isupper() else ord('a')
        # undo rotation
        unrotated = (ord(ch) - base - rotation) % 26
        # force uppercase by clearing the 0x20 bit
        upper = (base + unrotated) & ~0x20
        final_chars.append(chr(upper))
    else:
        final_chars.append(ch)
final_result = "".join(final_chars)

# === EVIDENCE LEDGER (all pins visible for the audit) ===
ledger = {
    "message": message,
    "plain_reference": plain_reference,
    "encoded": encoded,
    "digest_hex": digest_hex,
    "key_byte": key_byte,
    "shifted_key": shifted_key,
    "rotation": rotation,
    "transformed": transformed,
    "final_result": final_result,
}

# === THE CONSPIRACY MUST COMPUTE: check against the plain reference ===
assert final_result == plain_reference, "The thread snapped! The corkboard lies!"

# Print the ledger and the final result
print(ledger)
print("FINAL RESULT:", final_result)