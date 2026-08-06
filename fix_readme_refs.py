#!/usr/bin/env python3
"""Correct every `name` (#NN) cross-reference in README.md to match the real
table numbering, so the prose references point at the right blocks."""
import re
from pathlib import Path

HERE = Path(__file__).parent
README = HERE / "README.md"

text = README.read_text(encoding="utf-8")

# name -> number map straight from the table rows
name2num = {}
for m in re.finditer(r"^\| (\d+) \| `([a-z0-9-]+)`", text, re.M):
    name2num[m.group(2)] = int(m.group(1))

# Every `name` (#NN) or `name` (#NN–#MM) reference. We fix the single-number
# form; ranges are left alone (they describe spans, not single skills).
pat = re.compile(r"`([a-z0-9-]+)`\s+\(#(\d+)\)")

fixes = 0
def fix(m):
    global fixes
    name, num = m.group(1), int(m.group(2))
    if name in name2num and name2num[name] != num:
        fixes += 1
        return f"`{name}` (#{name2num[name]})"
    return m.group(0)

new = pat.sub(fix, text)

# Guard: also handle the "(`name` (#NN))" style and any whitespace variants
pat2 = re.compile(r"\(`([a-z0-9-]+)`\s*\(#(\d+)\)\)")
def fix2(m):
    global fixes
    name, num = m.group(1), int(m.group(2))
    if name in name2num and name2num[name] != num:
        fixes += 1
        return f"(`{name}` (#{name2num[name]}))"
    return m.group(0)

new = pat2.sub(fix2, new)

README.write_text(new, encoding="utf-8")
print(f"Fixed {fixes} cross-references against the table map "
      f"({len(name2num)} skills mapped).")
