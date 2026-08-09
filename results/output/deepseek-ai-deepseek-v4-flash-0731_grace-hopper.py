def count_bytes(text):
    # shipped: this byte counter runs now, no install, no ceremony — the demo below is the proof
    # questioned assumption: "we've always counted bytes with len(text)" — that's wrong for
    #   non-ASCII; len() counts code points, not bytes. UTF-8 is the wire format, so encode first.
    return len(text.encode("utf-8"))

def human_byte_report(text):
    # human-first: the user types a sentence, not a byte offset — we translate intent to reality
    n = count_bytes(text)
    # concrete rendering: one byte = one character on a punch card; this message is N cards tall
    return f"'{text}' is {n} byte(s) — that's {n} punch-card columns, or {n/1000:.2f} KB on disk"

def debug_helper(rows):
    # human-first: no manual index math — the helper shows shape and first row, not raw dumps
    return {"rows": len(rows), "columns": len(rows[0]) if rows else 0, "sample": rows[0] if rows else None}

# people note: let the junior dev run this on their own strings first — back them up when
#   they hit emoji or accented chars, not before. They learn by doing, we catch the edge cases.
print(human_byte_report("hello"))
print(human_byte_report("héllo"))
print(human_byte_report("🚀"))
print(debug_helper([["a", 1], ["b", 2]]))