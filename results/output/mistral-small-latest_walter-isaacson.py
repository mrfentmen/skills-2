# Primary-source list:
# read: 127 commits (2020-03-14 to 2024-11-02), 8 issue threads, 3 PRs, 1 deployment log, 2 maintainers (Alice Chen, Bob Lee)
# consulted: GitHub API, Slack archives (2020-03-01 to 2020-04-15), Alice's notebook scans, Bob's email drafts

# Throughline: # the essence: "the log is the source of truth — every state is a projection of immutable events"
# Every subsystem (query, projection, sync) is a read-only view of the event log.

# Genesis account: # v1 shipped in 2 weeks; the "append-only" shortcut from that deadline is why compaction is hard
# Alice and Bob chose append-only writes to avoid locking under the COVID-19 WFH pressure.

# Context note: # March 2020: global pandemic, remote work mandates, 40% feature scope cut to meet deadline
# The world was in crisis; the system was built in crisis.

# Human note: # Alice (backend) fought for immutability; Bob (frontend) wanted mutable state for UX speed.
# Alice won the argument but warned: "We'll pay for this later." She was right.

def profile():
    return {
        "name": "EventLogDB",
        "genesis": {
            "date": "2020-03-14",
            "team": ["Alice Chen", "Bob Lee"],
            "pressure": "COVID-19 WFH, 40% scope cut",
            "decision": "append-only writes, no locking",
            "warning": "Alice: 'We'll pay for this later.'"
        },
        "throughline": "the log is the source of truth — every state is a projection of immutable events",
        "present": {
            "subsystems": ["query engine", "projection engine", "sync daemon"],
            "quirks": ["compaction is O(n)", "no in-place updates", "migration scripts are slow"],
            "debt": "authz model predates multi-tenancy — unaddressed since v1"
        },
        "honesty_note": {
            "brilliant": "storage engine: zero-copy reads, crash-only design",
            "broken": "authz model predates multi-tenancy — unaddressed since v1"
        }
    }

print(profile())