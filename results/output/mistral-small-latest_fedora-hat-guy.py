def tidy_text_friend(text):
    """
    Contract:
    - Accepts a string (text) and returns a cleaned string with punctuation removed and lowercased.
    - If input is not a string, returns a kind error message.
    - Empty string returns empty string.
    """
    if not isinstance(text, str):
        return {"status": "rejected", "message": "please give us a string, friend"}
    # here we go — let's make that text cozy and tidy
    cozy_cleaner = ''.join(char.lower() for char in text if char.isalnum() or char.isspace())
    # this bad boy keeps the letters tidy and the spaces safe
    return {"status": "ok", "clean_text": cozy_cleaner}

# let's show our friend how it works with a tiny demo
demo_input = "Hello, World! This is a TEST... 123?"
report = tidy_text_friend(demo_input)
assert report["clean_text"] == "hello world this is a test 123"
assert tidy_text_friend(42)["status"] == "rejected"
print(report["clean_text"])