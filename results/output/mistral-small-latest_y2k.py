# Wire layout: fixed-width record of exactly 6 ASCII bytes in YYMMDD format
# Buffer limit: 6 bytes; truncation or overflow is a protocol error
# Year window: 70..99 -> 1970..1999; 00..69 -> 2000..2069
# Gregorian leap rule: divisible by 4, except centuries not divisible by 400

def parse_y2k_date(raw: bytes) -> tuple[int, int, int]:
    """
    Parse a fixed-width 6-byte YYMMDD record.
    Raises ValueError on truncation, non-digit, invalid month/day, or overflow.
    """
    if not isinstance(raw, bytes):
        raise ValueError("record must be bytes")
    if len(raw) != 6:
        raise ValueError("record must be exactly 6 bytes")
    if not all(b >= 0x30 and b <= 0x39 for b in raw):
        raise ValueError("record must contain only ASCII digits")

    yy = (raw[0] - 0x30) * 10 + (raw[1] - 0x30)
    mm = (raw[2] - 0x30) * 10 + (raw[3] - 0x30)
    dd = (raw[4] - 0x30) * 10 + (raw[5] - 0x30)

    full_year = 1900 + yy if yy >= 70 else 2000 + yy

    if not (1 <= mm <= 12):
        raise ValueError("invalid month")

    def is_leap(y: int) -> bool:
        return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)

    month_lengths = [
        31,
        29 if is_leap(full_year) else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ]

    if not (1 <= dd <= month_lengths[mm - 1]):
        raise ValueError("invalid day")

    return full_year, mm, dd

# Tests
assert parse_y2k_date(b"991231") == (1999, 12, 31)
assert parse_y2k_date(b"000229") == (2000, 2, 29)
assert parse_y2k_date(b"000101") == (2000, 1, 1)
assert parse_y2k_date(b"691231") == (2069, 12, 31)
assert parse_y2k_date(b"700101") == (1970, 1, 1)

try:
    parse_y2k_date(b"990230")
except ValueError as e:
    assert str(e) == "invalid day"
else:
    raise AssertionError("invalid date accepted")

for corrupt in (b"00022", b"00A229", b"0002300", b"990000", b"991301"):
    try:
        parse_y2k_date(corrupt)
    except ValueError:
        pass
    else:
        raise AssertionError("corrupt record accepted")

print(parse_y2k_date(b"000229"))