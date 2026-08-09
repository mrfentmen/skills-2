def step_plan(steps):
    # schritt für schritt: each step verifiable and reversible before the next
    return [{"step": s, "reversible": True, "verify": f"check {s} before continuing"}
            for s in steps]

def decide(capable, right):
    # am i doing something because it is right, or simply because it is possible?
    return {"capable": capable, "right": right,
            "action": "do it" if (capable and right) else "do not"}

# (1) measurement: the fact — current table has 1.2M rows, 3% nulls in `user_id`,
#     and the new schema requires 100% non-null. The decision rests on that 3%,
#     not on a guess about data quality.
measurement = {
    "rows": 1_200_000,
    "null_user_id_pct": 3.0,
    "fact": "3% nulls = 36,000 rows must be resolved before cutover, or the constraint fails"
}

# (2) step plan: small, atomic, reversible steps, each verified before the next
steps = step_plan([
    "read-only snapshot of source table",
    "add nullable new column with backfill in batches of 10k",
    "validate row counts and nulls after each batch",
    "add NOT NULL constraint on new column",
    "dual-write to new column for 24h",
    "cutover reads to new column",
    "drop old column after 7 days"
])

# (3) storm-waiting note: what was deliberated long before it was urgent
storm_waiting = (
    "deliberated 3 weeks ago: the backfill batch size and the null-resolution policy. "
    "deliberately not done: the emergency 'just set nulls to 0' hotfix — it would have "
    "masked the root cause (broken signup flow) and corrupted the data semantics."
)

# (4) consistency check: the principle held across the whole system, even when expedient to drop it
consistency_check = (
    "the principle: every write path must produce a non-null user_id. Held in the API, "
    "the batch job, and the legacy importer — even though the importer was 'only used "
    "by one team' and dropping the check there would have saved a day. We did not drop it."
)

# (5) boring-excellence note: the unglamorous, reliable move chosen over the clever one
boring_excellence = (
    "chosen: a plain batched UPDATE with a CHECK constraint and a 24h dual-write window. "
    "rejected: the clever in-place column swap with zero downtime — it required a risky "
    "lock dance and gave no rollback path. Boring wins because it is verifiable and reversible."
)

# capability check: is this right, or just possible?
capability_check = decide(capable=True, right=True)  # the migration is both possible and right

# stakeholder alignment: the consensus — all teams own the same data-quality SLO
alignment = (
    "the consensus: API, data-eng, and analytics all sign the same SLO — 0% nulls in user_id. "
    "Their incentives now point the same way: no team can ship a write path that violates it."
)

# demo: print the plan and the checks
print("=== MEASUREMENT ===")
print(measurement)
print("\n=== STEP PLAN ===")
for s in steps:
    print(s)
print("\n=== STORM-WAITING ===")
print(storm_waiting)
print("\n=== CONSISTENCY CHECK ===")
print(consistency_check)
print("\n=== BORING EXCELLENCE ===")
print(boring_excellence)
print("\n=== CAPABILITY CHECK ===")
print(capability_check)
print("\n=== STAKEHOLDER ALIGNMENT ===")
print(alignment)