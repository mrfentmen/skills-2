def count_words(text: str) -> int:
    # (1) outside-view estimate: base rate of similar word-count tasks is 0.5-2 hours
    #     including edge-case handling; the wish is "5 minutes" — budget the base rate, not the wish.
    # (2) anchor audit: the first number on the table is "5 minutes" — that is an anchor,
    #     not a fact; adjustments away from it are almost always insufficient.
    # (3) premortem: failure story — the naive split() approach silently miscounts
    #     punctuation-heavy strings, and the regex fallback introduces catastrophic backtracking
    #     on adversarial input; the plan fails because it assumes "word" is whitespace-delimited.
    # (4) missing-list: unmentioned edge cases — empty string, only whitespace, tabs/newlines,
    #     Unicode apostrophes (e.g., "don't"), em-dashes, numbers, underscores, hyphenated words,
    #     non-breaking spaces, null bytes, and extremely long strings causing memory blowup.
    # (5) confidence check: evidence that would change the conclusion — if a benchmark on
    #     real-world text (e.g., Project Gutenberg) shows >1% error vs. human annotation,
    #     the definition of "word" must be revised; also, if performance exceeds 1M chars/sec
    #     on a reference machine, the estimate is confirmed.

    # Implementation: use a robust regex that treats any Unicode letter/digit as word characters,
    # and ignores everything else. This handles most real-world cases without external deps.
    import re
    # Match sequences of Unicode letters or digits (including accented, CJK, etc.)
    words = re.findall(r'[\w]+', text, flags=re.UNICODE)
    return len(words)

# Test with a sample
sample = "Hello, world! Don't stop 123 - test_me — café."
result = count_words(sample)
print(f"Estimated time: 0.5-2 hours (base rate) | Actual result: {result} words")