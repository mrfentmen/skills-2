from datetime import datetime

# Legacy date formatter drops the year when the input is a string with a 4-digit year
def legacy_format_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%m/%d")  # legacy shortcut: silently drops the year

# Reproduction: smallest input that fails
sample = "2023-01-15"
expected = "01/15/2023"
observed = legacy_format_date(sample)

# Assert reproduction fails before fix
assert observed != expected, {"observed": observed, "expected": expected}

# The violated invariant: the formatter must preserve the full date including year
constraint = "date formatter must preserve year, month, and day"

# Smallest durable fix: include the year in the output format
def fixed_format_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%m/%d/%Y")

# Regression check: original failing case must now pass
repaired = fixed_format_date(sample)
assert repaired == expected, {"repaired": repaired, "expected": expected}

# Rejected rewrite: using a full date object serialization
# Reason: introduces unnecessary complexity and potential timezone issues
# Evidence: the legacy caller expects a specific string format; changing to object serialization
# would break downstream consumers without adding value for this simple case
rejected_rewrite = "full_date_object_serialization"
rejection_reason = "unnecessary complexity; breaks string format contract"

# Report findings
report = {
    "reproduced": True,
    "smallest_input": sample,
    "observed": observed,
    "expected": expected,
    "constraint": constraint,
    "fix": "include year in output format",
    "rejected": rejected_rewrite,
    "rejection_reason": rejection_reason,
    "unknowns": "none for this input contract"
}

print("Reproduction output:", observed)
print("Fixed output:", repaired)
print("Report:", report)