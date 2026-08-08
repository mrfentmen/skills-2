def count_words(text):
    # Another Jira ticket, another "AI-powered NLP pipeline" for counting words.
    # The PM's PowerPoint had more layers than a lasagna made by a committee.
    if not isinstance(text, str):
        return {"status": "rejected", "reason": "text required"}
    if not text.strip():
        return {"status": "ok", "words": 0, "operations": 0, "complexity": "O(n) time, O(1) memory"}

    in_word = False
    word_count = 0
    operations = 0
    for char in text:
        operations += 1
        if char.isalnum():
            if not in_word:
                in_word = True
        else:
            if in_word:
                word_count += 1
                in_word = False
    # Final word if string ends with alphanumeric
    if in_word:
        word_count += 1

    return {"status": "ok", "words": word_count, "operations": operations, "complexity": "O(n) time, O(1) memory"}

# Reference: "hello world" -> 2 words, 11 operations
report = count_words("hello world")
assert report["words"] == 2 and report["operations"] == 11
assert count_words("")["words"] == 0
assert count_words(None)["status"] == "rejected"
print(report)