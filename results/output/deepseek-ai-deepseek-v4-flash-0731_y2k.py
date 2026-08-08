RECORD_LEN = 6
YEAR_WINDOW = 70
YEAR_BASE_PRE = 1900
YEAR_BASE_POST = 2000
MONTH_LEN = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def parse_legacy_date(raw):
    if not isinstance(raw, str) or len(raw) != RECORD_LEN or not raw.isascii() or not raw.isdigit():
        raise ValueError("record must be exactly six ASCII digits")
    year = int(raw[0:2])
    month = int(raw[2:4])
    day = int(raw[4:6])
    if year >= YEAR_WINDOW:
        full_year = YEAR_BASE_PRE + year
    else:
        full_year = YEAR_BASE_POST + year
    if month < 1 or month > 12:
        raise ValueError("invalid month")
    leap = full_year % 400 == 0 or (full_year % 4 == 0 and full_year % 100 != 0)
    max_day = MONTH_LEN[month - 1]
    if month == 2 and leap:
        max_day = 29
    if day < 1 or day > max_day:
        raise ValueError("invalid day")
    return full_year, month, day

assert parse_legacy_date("991231") == (1999, 12, 31)
assert parse_legacy_date("000229") == (2000, 2, 29)
assert parse_legacy_date("990229") == (1999, 2, 28)
try:
    parse_legacy_date("990230")
except ValueError as exc:
    assert str(exc) == "invalid day"
else:
    raise AssertionError("invalid date accepted")
for corrupt in ("00022", "00A229", "0002300", "000000", "001300", "000100"):
    try:
        parse_legacy_date(corrupt)
    except ValueError:
        pass
    else:
        raise AssertionError("corrupt record accepted")
print(parse_legacy_date("000229"))