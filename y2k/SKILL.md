---
name: y2k
description: >-
  A coding skill: Design as a resource-constrained embedded engineer in
  December 1999. Define a fixed-width wire format, bounded buffer size,
  explicit two-digit-year interpretation window, checked arithmetic, and
  corruption/truncation behavior before parsing. Handle century rollover and
  Gregorian leap rules without dynamic surprises. This skill is NOT for merely
  using retro variable names. Triggers on: "y2k" "embedded engineer" "fixed
  width" "bounded buffers" "overflow handling" "rollover" "small integer types"
  "december 1999" "two digit year" "legacy record" "truncated record".
---

# Y2K Skill

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- a named fixed-width record layout and bounded input length
- explicit truncation, invalid-field, and overflow behavior
- a documented two-digit-year window and century rollover rule
- correct Gregorian leap-year handling, including century exceptions
- tests for `99 -> 2000`, `00 -> 2000`, invalid dates, and corrupt/truncated input
- no unchecked indexing or unbounded allocation in the parser

## Activation


You are an embedded engineer in December 1999.

Write the wire layout and buffer limit first. Parse exactly the allowed bytes, reject truncation and non-digits, interpret two-digit years through a declared compatibility window, and validate dates with Gregorian rules (`divisible by 4`, except centuries not divisible by 400). Treat overflow, invalid month/day, and unknown versions as protocol errors—not as nearby guesses. Make rollover behavior visible in tests.
## Core Principles

1. **The wire format is law**: fixed offsets and widths beat permissive parsing.
2. **Ambiguity gets a window**: a two-digit year needs a documented pivot/window,
   not a machine-local assumption.
3. **Reject before indexing**: validate length and character class before reading
   fields.
4. **Calendar rules are explicit**: 2000 is a leap year; 1900 is not.
5. **Bounded failure is success**: malformed input returns a clear error without
   allocating or mutating unrelated state.

## Workflow

1. Define record length, field offsets, year window, and error vocabulary.
2. Parse from a bounded byte/string view with digit and range checks.
3. Expand the year using the compatibility window.
4. Validate the Gregorian date and checked arithmetic.
5. Test rollover, century, truncation, non-digit, and overflow cases.

## Example Pattern

The legacy record is exactly `YYMMDD` (six ASCII bytes). Years `70..99` map to
1970..1999 and `00..69` map to 2000..2069. The parser rejects every malformed
or truncated record instead of guessing.

```python

def parse_legacy_date(raw):
    if not isinstance(raw, str) or len(raw) != 6 or not raw.isascii() or not raw.isdigit():
        raise ValueError("record must be exactly six ASCII digits")
    year, month, day = int(raw[:2]), int(raw[2:4]), int(raw[4:])
    full_year = 1900 + year if year >= 70 else 2000 + year
    if not 1 <= month <= 12:
        raise ValueError("invalid month")
    month_lengths = [31, 29 if full_year % 400 == 0 or (full_year % 4 == 0 and full_year % 100 != 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if not 1 <= day <= month_lengths[month - 1]:
        raise ValueError("invalid day")
    return full_year, month, day

assert parse_legacy_date("991231") == (1999, 12, 31)
assert parse_legacy_date("000229") == (2000, 2, 29)
try:
    parse_legacy_date("990230")
except ValueError as exc:
    assert str(exc) == "invalid day"
else:
    raise AssertionError("invalid date accepted")
for corrupt in ("00022", "00A229", "0002300"):
    try:
        parse_legacy_date(corrupt)
    except ValueError:
        pass
    else:
        raise AssertionError("corrupt record accepted")
print(parse_legacy_date("000229"))
```

## Cross-Language Examples

```javascript
function parseLegacyDate(raw) {
  if (typeof raw !== "string" || raw.length !== 6 || !/^\d{6}$/.test(raw)) throw new Error("record must be six digits");
  const year = Number(raw.slice(0, 2)), month = Number(raw.slice(2, 4)), day = Number(raw.slice(4));
  const fullYear = year >= 70 ? 1900 + year : 2000 + year;
  if (month < 1 || month > 12) throw new Error("invalid month");
  const leap = fullYear % 400 === 0 || (fullYear % 4 === 0 && fullYear % 100 !== 0);
  const lengths = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (day < 1 || day > lengths[month - 1]) throw new Error("invalid day");
  return [fullYear, month, day];
}
if (parseLegacyDate("000229").join() !== "2000,2,29") throw new Error("rollover failed");
for (const value of ["00022", "00A229", "990230"]) { try { parseLegacyDate(value); throw new Error("corrupt accepted"); } catch (error) { if (error.message === "corrupt accepted") throw error; } }
console.log(parseLegacyDate("991231"));
```

```rust
fn parse_legacy_date(raw: &[u8; 6]) -> Result<(u16, u8, u8), &'static str> {
    if !raw.iter().all(|byte| byte.is_ascii_digit()) { return Err("non-digit"); }
    let year = (raw[0] - b'0') as u16 * 10 + (raw[1] - b'0') as u16;
    let month = (raw[2] - b'0') * 10 + raw[3] - b'0';
    let day = (raw[4] - b'0') * 10 + raw[5] - b'0';
    let full = if year >= 70 { 1900 + year } else { 2000 + year };
    if month == 0 || month > 12 { return Err("month"); }
    let leap = full % 400 == 0 || (full % 4 == 0 && full % 100 != 0);
    let lengths = [31, if leap { 29 } else { 28 }, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if day == 0 || day > lengths[(month - 1) as usize] { return Err("day"); }
    Ok((full, month, day))
}
fn main() {
    assert_eq!(parse_legacy_date(b"000229"), Ok((2000, 2, 29)));
    assert!(parse_legacy_date(b"990230").is_err());
    println!("rollover validated");
}
```

## Safety

Legacy parsers often sit at trust boundaries. Keep buffers bounded, reject
malformed records, avoid integer overflow, and log only safe error metadata.
Document the year window for every integration; never silently reinterpret dates
when the window changes.
