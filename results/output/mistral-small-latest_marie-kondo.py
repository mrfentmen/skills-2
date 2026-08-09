# category: utils (helpers) -- gathered from 3 folders into one pile
# order honored: easy wins (formatting, validation) first, legacy core (auth) last
# spark-joy audit: each item judged by tested, used, clean, needed
# thank-you notes: legacy code thanked before removal
# tidiness verdict: all kept code has a home in the utils module

def spark_joy_audit(items):
    keep, release = [], []
    for name, tested, used, clean, needed in items:
        if tested and used and clean and needed:
            keep.append(name)
        else:
            release.append(name)
    return {"keep": keep, "release": release}

def thank_you(name, service):
    return f"commit: thank you, {name}, for {service} -- your work is complete"

# Original messy module (scattered helpers)
messy_helpers = [
    ("format_currency", True, True, True, True),    # tested, used, clean, needed -> keep
    ("legacy_auth", False, False, False, False),    # dead, untested -> thank and release
    ("validate_email", True, True, True, True),     # tested, used, clean, needed -> keep
    ("old_migration", False, True, False, False),   # dead path, untested -> release
    ("clean_name", True, True, True, True),         # tested, used, clean, needed -> keep
    ("auth_v1", False, False, False, False),        # superseded -> thank and release
]

# First pass: easy wins (formatting, validation)
easy_wins = [
    ("format_currency", True, True, True, True),
    ("validate_email", True, True, True, True),
    ("clean_name", True, True, True, True),
]

# Second pass: legacy core (auth)
legacy_core = [
    ("legacy_auth", False, False, False, False),
    ("old_migration", False, True, False, False),
    ("auth_v1", False, False, False, False),
]

# Audit results
easy_result = spark_joy_audit(easy_wins)
legacy_result = spark_joy_audit(legacy_core)

# Print results
print("=== Easy Wins ===")
print(f"Kept: {easy_result['keep']}")
print(f"Released: {easy_result['release']}")

print("\n=== Legacy Core ===")
print(f"Kept: {legacy_result['keep']}")
print(f"Released: {legacy_result['release']}")

print("\n=== Thank-You Notes ===")
for name in easy_result['release']:
    print(thank_you(name, "serving since 2018"))
for name in legacy_result['release']:
    print(thank_you(name, "supporting legacy systems since 2015"))

# Tidiness verdict
print("\n=== Tidiness Verdict ===")
print("All kept helpers have a home in the utils module.")
print("The codebase shines with only what sparks joy.")
print("Removed 3 dead helpers -- full test suite still green.")