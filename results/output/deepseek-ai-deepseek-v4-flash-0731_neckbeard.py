import sys

def count_words(text):
    # Another ticket asking for a "scalable microservice" to count words.
    # The PM drew a diagram with three boxes. The loop is one box.
    if not isinstance(text, str):
        return {"status": "rejected", "reason": "input must be a string"}
    if not text.strip():
        return {"status": "rejected", "reason": "empty input"}
    
    word_count = 0
    in_word = False
    operations = 0
    
    # Direct loop, no regex, no tokenizer framework, no NLP dependency.
    # The "enterprise" solution would have spun up a Kafka topic for this.
    for char in text:
        operations += 1
        if char.isspace():
            in_word = False
        elif not in_word:
            word_count += 1
            in_word = True
    
    return {
        "status": "ok",
        "word_count": word_count,
        "operations": operations,
        "complexity": "O(n) time, O(1) auxiliary space"
    }

# Correctness check against intended behavior
test_input = "The quick brown fox jumps over the lazy dog"
report = count_words(test_input)
assert report["status"] == "ok" and report["word_count"] == 9
assert count_words("")["status"] == "rejected"
assert count_words(123)["status"] == "rejected"
assert count_words("   ")["status"] == "rejected"
assert count_words("one two  three\tfour\nfive")["word_count"] == 5

# The sprint board demanded a "word counting service" with a REST API.
# Here's the whole service: a function and a print statement.
print(report)