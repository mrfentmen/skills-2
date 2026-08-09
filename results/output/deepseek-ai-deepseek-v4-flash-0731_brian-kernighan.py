def count_words(text):
    # clarity pass: the original split-and-len one-liner hid the empty case
    if not text:
        return 0
    words = text.split()
    return len(words)

def days_in_month(month, year):
    # clarity pass: the clever leap-year expression was hard to read
    if month == 2:
        if year % 400 == 0:
            return 29
        if year % 100 == 0:
            return 28
        if year % 4 == 0:
            return 29
        return 28
    if month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    return 31

def is_valid_date(day, month, year):
    # modularity: one check per function, named for what it does
    if month < 1 or month > 12:
        return False
    if day < 1:
        return False
    max_day = days_in_month(month, year)
    return day <= max_day

def debug_hint(text):
    # debugging note: model says split handles all whitespace; check with a print
    print(f"input: '{text}'")
    return count_words(text)

# correctness-first: these are right before any speed talk
print(count_words("hello world"))
print(days_in_month(2, 2024))
print(is_valid_date(29, 2, 2023))
print(debug_hint("  one   two  three  "))