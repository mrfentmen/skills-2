import datetime
import re

def parse_date(s):
    # A1: input is a string of form YYYY-MM-DD; consequence if false: regex may crash or coerce
    # A2: year is 4 digits, month 1-12, day 1-31; consequence: invalid dates accepted
    # A3: no leading/trailing whitespace; consequence: regex fails or matches wrong
    # A4: no timezone or extra characters; consequence: silent truncation
    # A5: input is not None; consequence: AttributeError
    # A6: memory is sufficient for string length; consequence: DoS on huge input
    if s is None:
        raise TypeError("input must be a string")
    if not isinstance(s, str):
        raise TypeError("input must be a string")
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if not m:
        raise ValueError("invalid format")
    y, mo, d = map(int, m.groups())
    # A7: month/day are zero-padded; consequence: "2024-1-1" rejected
    # A8: calendar is Gregorian proleptic; consequence: year 0000 or negative rejected
    return datetime.date(y, mo, d)

def oracle(s):
    # Independent contract: accept only exact "YYYY-MM-DD" with real calendar dates, reject bools, None, non-str, whitespace, extra chars, huge strings
    if s is None or not isinstance(s, str) or isinstance(s, bool):
        return ("error", "TypeError")
    if len(s) > 20:  # resource cap for test
        return ("error", "ValueError")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return ("error", "ValueError")
    y, mo, d = map(int, s.split("-"))
    try:
        datetime.date(y, mo, d)
        return ("ok", str(datetime.date(y, mo, d)))
    except ValueError:
        return ("error", "ValueError")

def adversarial_cases():
    # Generated from assumptions:
    # A1: non-string, None, bool, bytes
    # A2: month 00, 13, day 00, 32, leap year 2023-02-29, 2024-02-29
    # A3: leading/trailing spaces, tabs, newline
    # A4: extra suffix "T00:00", prefix "X", timezone "+00:00"
    # A5: None
    # A6: "1"*1000000 (huge)
    # A7: "2024-1-1", "2024-01-1", "2024-1-01"
    # A8: "0000-01-01", "-001-01-01", "9999-12-31"
    return [
        None, 123, True, b"2024-01-01",
        "2024-00-01", "2024-13-01", "2024-01-00", "2024-01-32",
        "2023-02-29", "2024-02-29",
        " 2024-01-01", "2024-01-01 ", "\t2024-01-01", "2024-01-01\n",
        "2024-01-01T00:00", "X2024-01-01", "2024-01-01+00:00",
        "1"*1000000,
        "2024-1-1", "2024-01-1", "2024-1-01",
        "0000-01-01", "-001-01-01", "9999-12-31"
    ]

def attack():
    authorized_scope = "local parse_date function only; no external systems, no network, no file I/O"
    findings = []
    tested = 0
    for case in adversarial_cases():
        tested += 1
        expected = oracle(case)
        try:
            result = parse_date(case)
            actual = ("ok", str(result))
        except (TypeError, ValueError) as e:
            actual = ("error", type(e).__name__)
        if actual != expected:
            # Minimize: for huge string, reduce length while failure persists
            if isinstance(case, str) and len(case) > 20:
                reduced = case[:20]
                try:
                    parse_date(reduced)
                    reduced_actual = ("ok", str(parse_date(reduced)))
                except (TypeError, ValueError) as e:
                    reduced_actual = ("error", type(e).__name__)
                if reduced_actual != oracle(reduced):
                    case = reduced
            findings.append({
                "input": (case[:30] + "...") if isinstance(case, str) and len(case) > 30 else case,
                "expected": expected,
                "actual": actual,
                "violated": "A1" if case is None or not isinstance(case, str) or isinstance(case, bool) else
                            "A2" if isinstance(case, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", case) and not oracle(case)[0] == "ok" else
                            "A3" if isinstance(case, str) and (case != case.strip() or "\t" in case or "\n" in case) else
                            "A4" if isinstance(case, str) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", case) and len(case) <= 20 else
                            "A6" if isinstance(case, str) and len(case) > 20 else
                            "A7" if isinstance(case, str) and re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", case) else
                            "A8" if isinstance(case, str) and (case.startswith("0000") or case.startswith("-")) else
                            "unknown"
            })
    verdict = "REPAIR" if findings else "PASS"
    return {
        "authorized_scope": authorized_scope,
        "tested": tested,
        "findings": findings,
        "verdict": verdict
    }

report = attack()
print("=== ADVERSARIAL REPORT ===")
print("Scope:", report["authorized_scope"])
print("Cases tested:", report["tested"])
print("Verdict:", report["verdict"])
print("Findings:")
for f in report["findings"]:
    print(f"  input={f['input']!r} expected={f['expected']} actual={f['actual']} violated={f['violated']}")
if not report["findings"]:
    print("  None - all cases passed oracle")