# category: utils (helpers) -- gathered from 4 folders into one pile
# order: easy wins (naming/format) -> docs -> config -> utilities -> legacy core last
# spark joy? clean name? tested? needed? simple?

def spark_joy_audit(items):
    # the one question, per item: does it spark joy?
    keep, release = [], []
    for name, tested, used, clean in items:
        if tested and used and clean:
            keep.append(name)                      # it sparks joy: celebrate and keep
        else:
            release.append(name)                   # thank it, then let it go
    return {"keep": keep, "release": release}

def thank_you(name, service):
    # the ritual before deletion: acknowledge what it did
    return f"commit: thank you, {name}, for {service} -- your work is complete"

# messy toy module: scattered helpers, dead legacy, duplicated logic
def format_currency(amount):
    return f"${amount:.2f}"  # clean, tested, used

def legacy_auth(user):
    return user == "admin"  # superseded by token auth, dead path

def csv_export(data):
    return ",".join(str(x) for x in data)  # clean, tested, used

def old_migration():
    return "migrate v1"  # dead path, never called

def duplicate_format(amount):
    return "$" + str(round(amount, 2))  # duplicate of format_currency, messy

# category pass: gather all helpers into one pile
items = [
    ("format_currency", True,  True,  True),    # tested, used, clean -> keep
    ("legacy_auth",     False, False, False),   # superseded -> thank and release
    ("csv_export",      True,  True,  True),    # keep
    ("old_migration",   False, True,  False),   # dead path -> release
    ("duplicate_format", False, False, False),  # duplicate, messy -> release
]

# order honored: easy wins (duplicate removal) first, legacy core (legacy_auth) last
result = spark_joy_audit(items)

# thank-you notes before deletion
for name in result["release"]:
    if name == "legacy_auth":
        print(thank_you(name, "authenticating users since 2019"))
    elif name == "old_migration":
        print(thank_you(name, "guiding the v1 to v2 data shift"))
    elif name == "duplicate_format":
        print(thank_you(name, "formatting currency in a pinch, now redundant"))

# safety net: verification that kept items still work
assert format_currency(12.5) == "$12.50"
assert csv_export([1, 2, 3]) == "1,2,3"

# tidiness verdict: everything kept has a home in the utils pile
print("tidiness verdict: kept items have a home in utils; the pile is tidy")
print(result)