RECORD_LEN = 6
YEAR_WINDOW_START = 70
YEAR_WINDOW_CENTURY = 1900
YEAR_WINDOW_ALT_CENTURY = 2000
MONTH_LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def is_leap(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)

def parse_legacy_date(raw):
    if not isinstance(raw, str) or len(raw) != RECORD_LEN or not raw.isascii() or not raw.isdigit():
        raise ValueError("record must be exactly six ASCII digits")
    year, month, day = int(raw[:2]), int(raw[2:4]), int(raw[4:])
    full_year = YEAR_WINDOW_CENTURY + year if year >= YEAR_WINDOW_START else YEAR_WINDOW_ALT_CENTURY + year
    if not 1 <= month <= 12:
        raise ValueError("invalid month")
    month_lengths = list(MONTH_LENGTHS)
    month_lengths[1] = 29 if is_leap(full_year) else 28
    if not 1 <= day <= month_lengths[month - 1]:
        raise ValueError("invalid day")
    return full_year, month, day

assert parse_legacy_date("991231") == (1999, 12, 31)
assert parse_legacy_date("000229") == (2000, 2, 29)
assert parse_legacy_date("990228") == (1999, 2, 28)
assert parse_legacy_date("000101") == (2000, 1, 1)
assert parse_legacy_date("691231") == (2069, 12, 31)
assert parse_legacy_date("700101") == (1970, 1, 1)

for corrupt in ("00022", "00A229", "0002300", "990230", "001301", "000000", "991332"):
    try:
        parse_legacy_date(corrupt)
    except ValueError as exc:
        print(f"rejected {corrupt!r}: {exc}")
    else:
        raise AssertionError(f"corrupt record accepted: {corrupt!r}")

print(parse_legacy_date("000229"))