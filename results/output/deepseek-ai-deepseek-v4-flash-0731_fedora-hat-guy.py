def cozy_text_tidy(rough_text, max_line=40):
    """
    Input: a string of words (rough_text) and an optional int max_line > 0.
    Output: a dict with status "ok" and "lines" (list of wrapped strings),
    or status "rejected" with a kind message for bad input.
    """
    # First, let's make sure our friend gave us something we can work with.
    if not isinstance(rough_text, str) or not isinstance(max_line, int) or max_line <= 0:
        return {"status": "rejected", "message": "please pass a string and a positive line length — we'll fix it together!"}
    
    # Split on whitespace and keep the words in a cozy little basket.
    word_basket = rough_text.split()
    if not word_basket:
        return {"status": "ok", "lines": []}
    
    # Here's the tricky part: we build lines one word at a time,
    # and when adding the next word would overflow, we tuck the current line away.
    tidy_lines = []
    current_line = word_basket[0]
    for word in word_basket[1:]:
        if len(current_line) + 1 + len(word) <= max_line:
            current_line += " " + word
        else:
            tidy_lines.append(current_line)
            current_line = word
    tidy_lines.append(current_line)
    
    # This little guy holds the final result, all neat and ready to share.
    return {"status": "ok", "lines": tidy_lines}

# Let's show our friend how it works with a happy little example.
sample_text = "The quick brown fox jumps over the lazy dog and keeps on going"
result = cozy_text_tidy(sample_text, 20)
assert result["status"] == "ok"
assert result["lines"] == ["The quick brown fox", "jumps over the lazy", "dog and keeps on", "going"]

# And a gentle check for when the input isn't quite right.
bad_result = cozy_text_tidy(123, 5)
assert bad_result["status"] == "rejected"

print("Happy path:", result)
print("Kind rejection:", bad_result)