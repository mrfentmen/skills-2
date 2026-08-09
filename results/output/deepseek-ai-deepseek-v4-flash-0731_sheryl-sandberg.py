import random
import time

# (1) done-better-than-perfect call:
# ships today: a minimal feature-flag read path with usage counters.
# telemetry will teach us: which flags are actually used, error rates,
# and whether the write path (flag creation UI) matters before we build it.

# (2) self-serve design:
# the flag service exposes a REST-like API and auto-instruments every read.
# value scales because any team can add a flag without a human gatekeeper —
# no analyst, no ticket, no manual dashboard. The telemetry is built-in.

# (3) ruthless top-two:
# priority 1: read path (check flag + count usage).
# priority 2: telemetry aggregation (who uses what, how often).
# dropped: admin UI, audit logs, multi-env support, A/B testing — until
# the telemetry proves they earn their way back.

# (4) seat-at-the-table note:
# the uncomfortable truth we include: "this flag has zero users yet."
# we surface that directly in the output, not buried in a report —
# so decisions are made with the real number, not the hoped-for one.

# (5) lean-in note:
# we ship the read path now, with a hardcoded flag list, instead of
# waiting for the perfect config schema. Action over certainty —
# the telemetry will tell us if the schema needs to change.

class FlagService:
    def __init__(self):
        # self-serve: any team can add a flag here without human approval
        self.flags = {
            "new_checkout": True,
            "dark_mode": False,
            "beta_reports": True,
        }
        self.usage = {name: 0 for name in self.flags}

    def is_enabled(self, name):
        # the read path — ships now, instrumented
        if name not in self.flags:
            return False
        self.usage[name] += 1
        return self.flags[name]

    def telemetry(self):
        # self-serve reporting: no analyst needed to see what matters
        return {
            name: {"enabled": enabled, "reads": self.usage[name]}
            for name, enabled in self.flags.items()
        }

    def truth_move(self):
        # the uncomfortable fact, stated directly with care
        unused = [name for name, count in self.usage.items() if count == 0]
        return f"uncomfortable fact: {unused or 'none'} have zero reads — evidence, not opinion"

    def resilience_reframe(self):
        # if a flag fails, it's one flag, one cause, one week — not the end
        return "a bad flag is one flag, one config, one rollback — not the system"

# simulate a few reads to generate telemetry
svc = FlagService()
for _ in range(5):
    svc.is_enabled("new_checkout")
for _ in range(2):
    svc.is_enabled("beta_reports")
svc.is_enabled("dark_mode")  # one read, but still low

print("=== lean-shipping demo ===")
print("ships now: read path + telemetry counters")
print("self-serve: any team adds a flag, no human gatekeeper")
print("top two: read path, telemetry. dropped: admin UI, audit, A/B")
print("seat at the table:", svc.truth_move())
print("lean in: shipped with hardcoded flags, not perfect schema")
print("telemetry:", svc.telemetry())
print("resilience:", svc.resilience_reframe())