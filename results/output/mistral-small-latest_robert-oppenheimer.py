def build_delivery_plan():
    # Talent map: need a frontend dev who fights for UX, a backend dev who owns the contract,
    # a security engineer who blocks on principle, and a domain expert who speaks the partner's language
    talent_map = {
        "disciplines": ["frontend", "backend", "security", "domain expert"],
        "people": ["Alice (UX zealot)", "Bob (contract purist)", "Carol (security absolutist)", "Dave (partner whisperer)"],
        "enablement": "Alice gets final say on UX, Bob owns the API contract, Carol can halt the build, Dave translates partner pain"
    }

    # Transparency move: daily 15-min standup where every team names its blocker and its discovery
    transparency = {
        "mechanism": "daily standup: blocker, discovery, next step — no silos, no surprises",
        "participants": ["frontend", "backend", "security", "domain"],
        "output": "public Slack thread with #blocker and #discovery tags"
    }

    # Pivot read: the rate-limit design failed under load; we pivot to the sharded path now
    pivot = {
        "current_design": "rate-limit queue",
        "failure": "latency spikes under 10k RPM",
        "pivot_to": "sharded path with consistent hashing",
        "decision": "now, not next quarter"
    }

    # Sweetness check: the clever compression is technically sweet — and it breaks the data contract
    sweetness = {
        "technically_sweet": "delta compression for partner payloads",
        "consequence": "partner's parser expects full payloads; contract violation",
        "proceed": "no — we ship uncompressed or negotiate the contract"
    }

    # Accountability line: the team owns the support impact of the rate-limit change
    accountability = {
        "owner": "the whole team",
        "responsibility": "support impact of rate-limit change and fix",
        "escalation": "Oppenheimer (project lead) has final say on harm limits"
    }

    plan = {
        "talent_map": talent_map,
        "transparency": transparency,
        "pivot": pivot,
        "sweetness": sweetness,
        "accountability": accountability
    }
    return plan

plan = build_delivery_plan()
print("=== HIGH-STAKES DELIVERY PLAN ===")
for k, v in plan.items():
    print(f"\n{k.upper()}:")
    for k2, v2 in v.items():
        print(f"  {k2}: {v2}")

# Demo: simulate the daily standup output
print("\n=== DAILY STANDUP DEMO ===")
standup = [
    {"team": "frontend", "blocker": "Alice wants to revert the button color", "discovery": "partner reported 5% drop in clicks"},
    {"team": "backend", "blocker": "Bob found a contract mismatch in the rate-limit header", "discovery": "sharded path reduces latency by 40%"},
    {"team": "security", "blocker": "Carol blocked the build over a missing CVE scan", "discovery": "CVE was a false positive"},
    {"team": "domain", "blocker": "Dave needs partner sign-off on the new payload format", "discovery": "partner willing to accept uncompressed if we add a header"}
]
for entry in standup:
    print(f"{entry['team']}: blocker={entry['blocker']}, discovery={entry['discovery']}")