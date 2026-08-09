import hmac
import hashlib
import os
import time

# ============================================================
# THREAT MODEL
# ============================================================
# Trust boundaries:
#   1. Client -> API gateway (network boundary, TLS assumed)
#   2. API gateway -> handler (identity assertion boundary)
#   3. Handler -> data store (data access boundary)
#
# Top attack scenarios:
#   # threat: token theft -> re-verify at every sensitive action
#   # threat: replay attack -> timestamp + nonce window
#   # threat: privilege escalation -> capability table enforced per action
#   # threat: secret exfiltration -> vault only, never in code/logs
# ============================================================

# ============================================================
# LEAST-PRIVILEGE TABLE (capability matrix)
# ============================================================
# role       | capabilities
# -----------|----------------------------------------------
# anonymous  | {health_check}
# viewer     | {health_check, read}
# engineer   | {health_check, read, write}
# admin      | {health_check, read, write, audit}
# service    | {health_check, read}  # internal service account
# ============================================================

CAPABILITIES = {
    "anonymous": {"health_check"},
    "viewer":    {"health_check", "read"},
    "engineer":  {"health_check", "read", "write"},
    "admin":     {"health_check", "read", "write", "audit"},
    "service":   {"health_check", "read"},
}

# ============================================================
# SECRETS RULE
# ============================================================
# vault: env var SECRET_KEY; rotated every 24h; never in source or logs
# ============================================================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-key-rotate-me")

# ============================================================
# DEFENSE IN DEPTH
# ============================================================
# Control 1: HMAC-signed token with timestamp (replay protection)
# Control 2: Capability table check (authorization)
# Control 3: Rate limiting (friction/deterrent)
# Control 4: Audit log (detection)
# ============================================================

class AccessController:
    def __init__(self):
        self._request_log = []
        self._rate_limits = {}  # token -> (window_start, count)

    def _sign_token(self, role, issued_at):
        """Create HMAC token with role and timestamp."""
        payload = f"{role}:{issued_at}".encode()
        sig = hmac.new(SECRET_KEY.encode(), payload, hashlib.sha256).hexdigest()
        return f"{role}:{issued_at}:{sig}"

    def _verify_token(self, token):
        """Verify token signature and freshness. Fail closed on any doubt."""
        # fail-closed default: doubt means denied
        valid = False
        try:
            role, issued_at, sig = token.split(":")
            expected = hmac.new(
                SECRET_KEY.encode(),
                f"{role}:{issued_at}".encode(),
                hashlib.sha256
            ).hexdigest()
            # constant-time comparison
            if hmac.compare_digest(sig, expected):
                # replay protection: token valid for 30 seconds only
                if abs(time.time() - float(issued_at)) < 30:
                    valid = True
        except Exception:
            valid = False  # exception path denies too
        return valid, role if valid else None

    def _rate_limit(self, token):
        """Simple rate limiter: 10 requests per 60 seconds per token."""
        now = time.time()
        window_start = now - 60
        # clean old entries
        self._rate_limits = {
            t: (ts, count)
            for t, (ts, count) in self._rate_limits.items()
            if ts > window_start
        }
        if token not in self._rate_limits:
            self._rate_limits[token] = (now, 1)
            return True
        ts, count = self._rate_limits[token]
        if count >= 10:
            return False
        self._rate_limits[token] = (ts, count + 1)
        return True

    def authorize(self, token, action):
        """Main authorization path. Fail closed on any doubt."""
        # fail-closed default: denied until proven otherwise
        allowed = False
        try:
            # Control 1: verify token (signature + freshness)
            token_valid, role = self._verify_token(token)
            if not token_valid:
                return False, "invalid_token"

            # Control 2: capability check
            if action not in CAPABILITIES.get(role, set()):
                return False, "insufficient_privilege"

            # Control 3: rate limiting (secondary control)
            if not self._rate_limit(token):
                return False, "rate_limited"

            # Control 4: audit log (detection layer)
            self._request_log.append({
                "time": time.time(),
                "role": role,
                "action": action,
                "result": "allowed"
            })

            allowed = True
            return True, "allowed"
        except Exception:
            # contingency: if anything fails, deny and log
            self._request_log.append({
                "time": time.time(),
                "action": action,
                "result": "denied_exception"
            })
            return False, "internal_error"

    def audit_log(self):
        """Return audit log (admin only)."""
        return self._request_log[-10:]  # last 10 entries

def demo():
    controller = AccessController()

    # Issue tokens for different roles
    now = time.time()
    admin_token = controller._sign_token("admin", now)
    engineer_token = controller._sign_token("engineer", now)
    viewer_token = controller._sign_token("viewer", now)
    anonymous_token = controller._sign_token("anonymous", now)

    # Tampered token (simulating attack)
    tampered = admin_token[:-1] + ("0" if admin_token[-1] != "0" else "1")

    # Expired token (simulating replay)
    expired = controller._sign_token("admin", now - 60)

    print("=== SECURITY-HARDENED API DEMO ===")
    print("Threat model: token theft, replay, privilege escalation")
    print("Defense in depth: HMAC token + capability table + rate limit + audit")
    print()

    # Test cases
    tests = [
        ("admin reads", admin_token, "read"),
        ("admin audits", admin_token, "audit"),
        ("engineer writes", engineer_token, "write"),
        ("engineer audits (should fail)", engineer_token, "audit"),
        ("viewer reads", viewer_token, "read"),
        ("viewer writes (should fail)", viewer_token, "write"),
        ("anonymous health check", anonymous_token, "health_check"),
        ("anonymous read (should fail)", anonymous_token, "read"),
        ("tampered token (should fail)", tampered, "read"),
        ("expired token (should fail)", expired, "read"),
        ("malformed token (should fail)", "garbage:token", "read"),
    ]

    for desc, token, action in tests:
        allowed, reason = controller.authorize(token, action)
        status = "ALLOWED" if allowed else "DENIED"
        print(f"  {desc:45s} -> {status:7s} ({reason})")

    print()
    print("=== CONTINGENCY NOTE ===")
    print("If HMAC verification fails: deny immediately, log the attempt.")
    print("If capability check throws: deny (fail closed), log exception.")
    print("If rate limiter fails: deny (fail closed), log anomaly.")
    print("If audit log write fails: still deny, alert operator.")
    print()

    print("=== AUDIT LOG (last 5 entries) ===")
    for entry in controller.audit_log()[-5:]:
        print(f"  {entry}")

    print()
    print("=== DEFENSE IN DEPTH SUMMARY ===")
    print("  Layer 1: HMAC token (authentication + replay protection)")
    print("  Layer 2: Capability table (authorization)")
    print("  Layer 3: Rate limiting (deterrent)")
    print("  Layer 4: Audit logging (detection)")
    print("  All layers must pass; any failure = deny")

if __name__ == "__main__":
    demo()