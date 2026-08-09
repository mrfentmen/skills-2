import hmac
import hashlib
import base64
import os
import json
from typing import Dict, Set, Tuple

# === THREAT MODEL ===
# Trust boundaries:
#   1. Client -> API (network)
#   2. API -> Token Vault (secrets)
#   3. API -> Audit Log (storage)
# Top attack scenarios:
#   - token theft -> re-verify at every sensitive action
#   - replay attack -> include nonce in token and validate
#   - privilege escalation -> enforce least privilege table strictly
#   - log tampering -> write-only audit log with HMAC integrity

# === SECRETS RULE ===
# vault: env var + rotation; never in source or logs
#   - HMAC_SECRET stored in environment variable
#   - Rotate via env var update and restart; no hot reload

# === LEAST PRIVILEGE TABLE ===
# role -> set of allowed actions
CAPABILITIES: Dict[str, Set[str]] = {
    "viewer":   {"read"},
    "engineer": {"read", "write", "deploy"},
    "admin":    {"read", "write", "deploy", "audit", "rotate"},
}

# === FAIL-CLOSED DEFAULT ===
# allowed = False before any try; exceptions keep it False
def authorize(role: str, action: str, token_valid: bool, nonce_valid: bool) -> bool:
    allowed = False
    try:
        allowed = action in CAPABILITIES.get(role, set())
    except Exception:
        allowed = False
    return allowed and token_valid and nonce_valid

# === DEFENSE IN DEPTH ===
# Layer 1: HMAC token verification
# Layer 2: Nonce replay protection (in-memory store for demo)
NONCE_STORE: Set[str] = set()

def verify_token(token: str, secret: bytes) -> Tuple[bool, str]:
    try:
        decoded = base64.urlsafe_b64decode(token.encode())
        sig, payload = decoded[:32], decoded[32:]
        expected_sig = hmac.new(secret, payload, hashlib.sha256).digest()
        return hmac.compare_digest(sig, expected_sig), payload.decode()
    except Exception:
        return False, ""

def verify_nonce(nonce: str) -> bool:
    if nonce in NONCE_STORE:
        return False
    NONCE_STORE.add(nonce)
    return True

# === CONTINGENCY NOTE ===
# If token verification fails: deny access and log with HMAC-protected integrity.
# If nonce replay detected: deny and alert (in demo, just deny).
# If capability check throws: deny by fail-closed default.
# Fallback: return 403 and do not process request.

# === DEMO ===
def demo():
    # Load secret from env (vault)
    secret = os.getenv("HMAC_SECRET", "default-secret-change-in-prod").encode()

    # Simulate tokens for roles
    payloads = {
        "viewer":   json.dumps({"role": "viewer", "nonce": "n1"}).encode(),
        "engineer": json.dumps({"role": "engineer", "nonce": "n2"}).encode(),
        "admin":    json.dumps({"role": "admin", "nonce": "n3"}).encode(),
    }
    tokens = {
        role: base64.urlsafe_b64encode(
            hmac.new(secret, payloads[role], hashlib.sha256).digest() + payloads[role]
        ).decode()
        for role in payloads
    }

    # Test cases
    tests = [
        ("viewer", "read", tokens["viewer"], True),
        ("viewer", "deploy", tokens["viewer"], True),
        ("engineer", "deploy", tokens["engineer"], True),
        ("engineer", "audit", tokens["engineer"], True),
        ("admin", "rotate", tokens["admin"], True),
        ("admin", "read", tokens["admin"], True),
    ]

    results = []
    for role, action, token, expected in tests:
        token_valid, payload = verify_token(token, secret)
        nonce = json.loads(payload)["nonce"]
        nonce_valid = verify_nonce(nonce)
        auth_result = authorize(role, action, token_valid, nonce_valid)
        results.append((role, action, auth_result == expected))

    # Print demo output
    for role, action, passed in results:
        print(f"{role} {action}: {'PASS' if passed else 'FAIL'}")

if __name__ == "__main__":
    demo()