# base rate: 9 of 10 similar string-processing tasks took 1.5x the initial estimate due to edge cases
# the ticket says "small task" — that is an anchor, not a fact
# failure story: the string contains non-ASCII whitespace or mixed line endings that split incorrectly
# unmentioned: empty string, None input, very long strings, tabs vs spaces, Unicode spaces, surrogate pairs
# evidence that would change the conclusion: a failing test with one of the unmentioned edge cases

def count_words(text):
    if text is None:
        return 0
    return len(text.split())

# outside view: similar tasks historically took 1.5x the initial estimate
initial_estimate_minutes = 5
adjusted_estimate_minutes = initial_estimate_minutes * 1.5

# premortem: the string contains non-ASCII whitespace or mixed line endings that split incorrectly
test_string = "  Hello,\tworld!  \n  This is a test.  "
actual_result = count_words(test_string)

print(f"Estimated time: {adjusted_estimate_minutes} minutes")
print(f"Actual result: {actual_result}")