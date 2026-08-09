import json
import os
import sys
import tempfile
from pathlib import Path

# [INSPECT]
# - Files examined: this script only; no external repository or existing codebase was inspected.
# - Dependencies: Python 3.8+ standard library only (json, os, sys, tempfile, pathlib).
# - Symbols examined: sys.argv, Path, json.load/dump, tempfile.TemporaryDirectory.
# - Limits: no network, no third-party packages, no persistent storage beyond user-provided file.

# [LAWS]
# 1. The CLI must accept exactly one positional argument: a path to a JSON file.
#    Any other argument count exits with code 2 and a usage message on stderr.
# 2. The JSON file must contain an object with a "numbers" key that is a list of
#    integers. Any other shape exits with code 1 and an error message on stderr.
# 3. The output must be a single line: the sum of the integers, printed to stdout.
# 4. The input file must not be modified; the tool is read-only.

# [DESIGN]
# - Boundary: a pure CLI that reads a JSON file, validates its shape, computes a sum.
# - Data flow: argv -> file path -> json.load -> validate -> sum -> stdout.
# - Failure behavior: explicit error messages to stderr, non-zero exit codes.
# - Out of scope: writing files, network, interactive input, large-file streaming.

def _usage():
    print("usage: divine_sum <path-to-json-file>", file=sys.stderr)

def _load_and_validate(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON in {path}: {e}")

    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    if "numbers" not in data:
        raise ValueError("missing required key 'numbers'")
    numbers = data["numbers"]
    if not isinstance(numbers, list):
        raise ValueError("'numbers' must be a list")
    if not all(isinstance(n, int) and not isinstance(n, bool) for n in numbers):
        raise ValueError("'numbers' must contain only integers")
    return numbers

def main(argv):
    if len(argv) != 2:
        _usage()
        return 2
    path = argv[1]
    try:
        numbers = _load_and_validate(path)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(sum(numbers))
    return 0

# [IMPLEMENT]
# - The implementation is the main() function above plus _load_and_validate().
# - Validation of laws:
#   * Law 1: len(argv) != 2 -> usage + exit 2.
#   * Law 2: _load_and_validate enforces object, 'numbers' key, list, int-only.
#   * Law 3: print(sum(numbers)) emits exactly one line to stdout.
#   * Law 4: the file is opened read-only ("r"); no write operation exists.

# [VERIFY]
# - The acceptance conditions are checked below with real temporary files.
# - Each check prints PASS/FAIL and the observed output/exit code.

def _run_check(name, argv, expected_exit, expected_stdout=None, expected_stderr_substr=None):
    import io
    import contextlib
    out = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    ok = code == expected_exit
    if expected_stdout is not None:
        ok = ok and out.getvalue() == expected_stdout
    if expected_stderr_substr is not None:
        ok = ok and expected_stderr_substr in err.getvalue()
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}: exit={code}, stdout={out.getvalue()!r}, stderr={err.getvalue()!r}")
    return ok

if __name__ == "__main__":
    all_ok = True
    with tempfile.TemporaryDirectory() as tmpdir:
        good_path = os.path.join(tmpdir, "good.json")
        with open(good_path, "w") as f:
            json.dump({"numbers": [1, 2, 3, 4]}, f)

        bad_missing = os.path.join(tmpdir, "missing.json")
        with open(bad_missing, "w") as f:
            json.dump({"values": [1]}, f)

        bad_type = os.path.join(tmpdir, "bad_type.json")
        with open(bad_type, "w") as f:
            json.dump({"numbers": [1, "two"]}, f)

        bad_syntax = os.path.join(tmpdir, "bad_syntax.json")
        with open(bad_syntax, "w") as f:
            f.write("{not json")

        all_ok &= _run_check("valid input", [sys.argv[0], good_path], 0, "10\n")
        all_ok &= _run_check("no args", [sys.argv[0]], 2, expected_stderr_substr="usage:")
        all_ok &= _run_check("too many args", [sys.argv[0], good_path, "extra"], 2, expected_stderr_substr="usage:")
        all_ok &= _run_check("missing key", [sys.argv[0], bad_missing], 1, expected_stderr_substr="missing required key")
        all_ok &= _run_check("non-int element", [sys.argv[0], bad_type], 1, expected_stderr_substr="only integers")
        all_ok &= _run_check("invalid JSON", [sys.argv[0], bad_syntax], 1, expected_stderr_substr="invalid JSON")
        all_ok &= _run_check("nonexistent file", [sys.argv[0], os.path.join(tmpdir, "nope.json")], 1, expected_stderr_substr="file not found")

        # Law 4: verify the good file is unchanged after the run.
        with open(good_path) as f:
            after = f.read()
        original = '{"numbers": [1, 2, 3, 4]}'
        unchanged = after == original
        print(f"[{'PASS' if unchanged else 'FAIL'}] input file unchanged: {unchanged}")
        all_ok &= unchanged

    print("ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")
    sys.exit(0 if all_ok else 1)