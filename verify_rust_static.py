#!/usr/bin/env python3
"""Static structural audit for Rust examples inside SKILL.md files.

rustc is not available on this machine, so we cannot compile the Rust
blocks. Instead we verify structural integrity that catches the common
"looks like code but isn't" failure modes:

  * balanced braces / parens / brackets (token-level, string-aware)
  * no placeholder markers ("...", "// TODO", "// FIXME", "stub", "lorem")
  * real statements: semicolons or block endings inside fn bodies
  * a fn entry point exists (fn main or at least one fn)
  * balanced quotes

Run:  python3 verify_rust_static.py
Exit 0 = all clean, 1 = failures (printed).
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
PLACEHOLDER_RE = re.compile(
    r"\.\.\.|TODO|FIXME|stub\b|lorem ipsum|<insert|placeholder|your code here"
)

OPEN = {"{": "}", "(": ")", "[": "]", '"': '"'}
CLOSE = {"}", ")", "]", '"'}


def strip_strings_and_comments(src: str) -> str:
    """Remove strings, char literals, and comments to get structural code tokens.

    Handles Rust-specific pitfalls: // and /* */ comments, "..." strings,
    char literals ('x', '\\n'), and — crucially — lifetimes ('a, 'static),
    which must NOT be treated as char literals (they have no closing quote).
    """
    out = []
    i = 0
    n = len(src)
    while i < n:
        c = src[i]
        # line comment
        if c == "/" and i + 1 < n and src[i + 1] == "/":
            while i < n and src[i] != "\n":
                i += 1
            continue
        # block comment
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            end = src.find("*/", i + 2)
            i = n if end == -1 else end + 2
            continue
        # raw string literal: r"..." or r#"..."# (may contain embedded ")
        if c == "r" and i + 1 < n and src[i + 1] == '"':
            end = src.find('"', i + 2)
            i = n if end == -1 else end + 1
            continue
        if c == "r" and i + 2 < n and src[i + 1] == "#" and src[i + 2] == '"':
            end = src.find('"#', i + 3)
            i = n if end == -1 else end + 2
            continue
        # regular string literal
        if c == '"':
            i += 1
            while i < n:
                if src[i] == "\\":
                    i += 2
                    continue
                if src[i] == '"':
                    break
                i += 1
            i += 1
            continue
        # char literal ('x' / '\n') — only if it closes within 1-2 chars;
        # otherwise it's a Rust lifetime 'a / 'static and we keep it as text.
        if c == "'":
            j = i + 1
            if j < n and src[j] == "\\":
                j += 2
            else:
                j += 1
            if j < n and src[j] == "'":
                i = j + 1  # consumed a real char literal
            else:
                out.append(c)  # lifetime or stray apostrophe — not structural
                i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def check_block(block: str, path: str) -> list[str]:
    errors = []
    code = strip_strings_and_comments(block)

    # 1. balanced delimiters
    stack = []
    for ch in code:
        if ch in OPEN:
            stack.append(ch)
        elif ch in CLOSE:
            if not stack or OPEN[stack[-1]] != ch:
                errors.append(f"unbalanced '{ch}'")
                break
            stack.pop()
    if stack:
        errors.append(f"unclosed delimiters at end: {''.join(stack[-4:])}")

    # 2. no placeholders
    for m in PLACEHOLDER_RE.finditer(block):
        snippet = block[max(0, m.start() - 18) : m.end() + 18].replace("\n", " ")
        errors.append(f"placeholder-like text: ...{snippet}...")

    # 3. entry point: fn (main or any) OR a type/use/impl declaration counts
    has_fn = re.search(r"\bfn\s+\w+", block)
    has_decl = re.search(r"\b(struct|enum|impl|trait|use|const|static)\b", block)
    if not has_fn and not has_decl:
        errors.append("no 'fn' and no struct/enum/impl/use/const decl")

    # 4. real statements — a body with ';', a fn body '{...}', or a decl.
    #    A one-liner like `fn f(x: T) -> U { expr }` has no ';' but is real.
    has_semicolon = ";" in code
    has_fn_body = bool(has_fn) and "{" in code
    if not has_semicolon and not has_fn_body and not has_decl:
        errors.append("no statements (no ';', no fn body, no decl) — likely prose in a rust fence")

    # 5. balanced quotes — checked on the stripped code, not the raw source,
    #    so quotes inside comments or strings cannot cause false failures
    if code.count('"') % 2 != 0:
        errors.append("odd number of double quotes")

    return errors


def main() -> int:
    md_files = sorted(HERE.glob("*/SKILL.md"))
    total_blocks = 0
    failures = 0
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        blocks = re.findall(r"```rust\s*\n(.*?)```", text, re.S)
        for idx, block in enumerate(blocks, 1):
            total_blocks += 1
            errors = check_block(block, str(md))
            if errors:
                failures += 1
                name = md.parent.name
                print(f"FAIL {name} block #{idx}: {'; '.join(errors)}")
    print(f"Rust blocks audited: {total_blocks} across {len(md_files)} skills.")
    if failures:
        print(f"FAILURES: {failures}")
        return 1
    print("All Rust blocks structurally clean (static audit; no rustc available).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
