def parse_date(date_str):
    parts = date_str.split('-')
    if len(parts) != 3:
        raise ValueError("date must be YYYY-MM-DD")
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    if not (1 <= month <= 12):
        raise ValueError("month must be 1-12")
    if not (1 <= day <= 31):
        raise ValueError("day must be 1-31")
    return (year, month, day)

# A1: Input is a non-empty string; consequence if false: parser may crash or return wrong type
# A2: String format is exactly "YYYY-MM-DD"; consequence if false: parser may misalign parts
# A3: Year, month, day are valid integers; consequence if false: parser may coerce or crash
# A4: Month is between 1 and 12; consequence if false: invalid calendar date accepted
# A5: Day is between 1 and 31; consequence if false: invalid calendar date accepted
# A6: Day is valid for the given month/year; consequence if false: invalid calendar date accepted
# A7: No leading/trailing whitespace; consequence if false: parser may misalign parts

def adversarial_cases():
    # Derive cases from A1-A7
    return [
        "",           # empty string (A1)
        "2023",       # too few parts (A2)
        "2023-13-01", # month out of range (A4)
        "2023-02-30", # invalid day for month (A6)
        "2023-04-31", # invalid day for month (A6)
        "2023-00-01", # month out of range (A4)
        "2023-01-00", # day out of range (A5)
        "2023-01-32", # day out of range (A5)
        " 2023-01-01", # leading space (A7)
        "2023-01-01 ", # trailing space (A7)
        "2023-01-01\n", # trailing newline (A7)
        "2023-01-01\t", # trailing tab (A7)
        "2023-01-01-", # extra trailing dash (A2)
        "-2023-01-01", # leading dash (A2)
        "ab-cd-ef",    # non-integer parts (A3)
        "2023/01/01",  # wrong separator (A2)
        "2023.01.01",  # wrong separator (A2)
        "20230101",    # missing separators (A2)
        "2023-1-1",    # single-digit month/day (A2)
        "2023-01-1",   # single-digit day (A2)
        "2023-1-01",   # single-digit month (A2)
        "2023-01-01",  # valid case (sanity)
        "0000-01-01",  # year zero (A3)
        "99999-01-01", # year too large (A3)
        "2023-01-01 00:00:00", # extra time (A2)
    ]

def oracle(case):
    # Independent contract: accept only valid calendar dates in YYYY-MM-DD format
    if not isinstance(case, str):
        return ("error", "TypeError")
    parts = case.strip().split('-')
    if len(parts) != 3:
        return ("error", "ValueError")
    try:
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return ("error", "ValueError")
    if not (1 <= month <= 12):
        return ("error", "ValueError")
    if not (1 <= day <= 31):
        return ("error", "ValueError")
    # Check day validity per month/year
    if month in {4, 6, 9, 11} and day > 30:
        return ("error", "ValueError")
    if month == 2:
        if (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
            if day > 29:
                return ("error", "ValueError")
        else:
            if day > 28:
                return ("error", "ValueError")
    return ("ok", (year, month, day))

def attack():
    authorized_scope = "local parse_date function; no external systems"
    findings = []
    for case in adversarial_cases():
        expected = oracle(case)
        try:
            actual = ("ok", parse_date(case))
        except Exception as error:
            actual = ("error", type(error).__name__)
        if actual != expected:
            findings.append({
                "input": case,
                "expected": expected,
                "actual": actual,
                "violated": "A1-A7: input assumptions violated"
            })
    return {
        "authorized_scope": authorized_scope,
        "tested": len(adversarial_cases()),
        "findings": findings,
        "verdict": "REPAIR" if findings else "PASS"
    }

print(attack())