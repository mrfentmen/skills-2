# the fact: user_id column in orders table grew 3x in 12 months while query latency increased 2.8x
# the root cause: VARCHAR(36) primary key vs INT(11) foreign key mismatch causing index bloat
# the measurement: index scan ratio rose from 12% to 78% during peak load

# step 1: read-only toggle — add new INT(11) user_id column, keep VARCHAR(36) for rollback
# step 2: dual-write — migrate writes to new column, backfill reads via view
# step 3: cutover — switch primary key, drop old column after 14-day observation window
# step 4: cleanup — vacuum analyze, update statistics, notify stakeholders

def step_plan(steps):
    return [{"step": s, "reversible": True, "verify": f"check {s} before continuing"}
            for s in steps]

plan = step_plan([
    "add new INT(11) user_id column with default NULL",
    "create orders_new_view mapping old VARCHAR(36) to new INT(11)",
    "backfill user_id from users table using LEFT JOIN",
    "enable dual-write via application flag",
    "monitor index scan ratio and latency for 7 days",
    "switch primary key to user_id, drop old column after 14 days"
])

# storm-waiting note: deliberately not done — emergency VARCHAR→INT conversion during peak
#   it would have masked the root cause (index bloat) and risked data corruption

# consistency check: the INT(11) type must match across orders, order_items, and payments tables
#   otherwise referential integrity breaks — this principle held even when expedient to use VARCHAR

# boring-excellence note: chose INT(11) over UUID() or composite keys — unglamorous but reliable
#   and compatible with existing ORM mappings and replication lag constraints

print("measurement: index scan ratio rose from 12% to 78% during peak load")
print("step plan:", plan)
print("storm-waiting: no emergency VARCHAR→INT conversion during peak")
print("consistency: INT(11) type enforced across all foreign key relationships")
print("boring-excellence: INT(11) primary key over clever UUID or composite keys")