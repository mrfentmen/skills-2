import sys

def count_words(text):
    # Another ticket asking for a "scalable microservice" to count words.
    # The committee wanted Kafka. The words wanted a loop.
    if not isinstance(text, str):
        return {"status": "rejected", "reason": "input must be a string"}
    if not text.strip():
        return {"status": "rejected", "reason": "empty input"}
    
    word_count = 0
    in_word = False
    operations = 0
    
    for char in text:
        operations += 1
        if char.isspace():
            in_word = False
        elif not in_word:
            word_count += 1
            in_word = True
    
    # The "enterprise" solution would spin up a Spark cluster for this.
    # The cluster is still initializing. We're done.
    return {
        "status": "ok",
        "word_count": word_count,
        "operations": operations,
        "complexity": "O(n) time, O(1) auxiliary space"
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python word_counter.py <text>")
        sys.exit(1)
    
    result = count_words(sys.argv[1])
    if result["status"] == "rejected":
        print(f"Error: {result['reason']}")
        sys.exit(1)
    
    # Correctness check: split() is the reference implementation.
    # We're not using it in production because the PM wanted a "custom parser".
    # The PM also wanted a blockchain. We compromised on the parser.
    expected = len(sys.argv[1].split())
    assert result["word_count"] == expected, "word count mismatch"
    
    print(f"Word count: {result['word_count']}")
    print(f"Operations: {result['operations']}")
    print(f"Complexity: {result['complexity']}")

if __name__ == "__main__":
    main()