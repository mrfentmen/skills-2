#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# freedom audit:
#   freedom 0 (run): kept — runs locally with python3, no network, no license server
#   freedom 1 (study & change): kept — source is the .py file, readable and editable
#   freedom 2 (share): kept — copies can be given to anyone, no restriction
#   freedom 3 (share modified): kept — modified versions can be distributed, copyleft ensures they stay free
#   no freedom is violated by this design

# source note:
#   preferred form: this plain-text .py file, not a minified or compiled blob
#   every line is human-readable, no obfuscation, no generated code

# control line:
#   who controls this program? the user's machine, entirely
#   guaranteed by: no remote calls, no telemetry, no hidden state — all data lives in local variables

# copyleft move:
#   GPL-3.0-or-later: any downstream fork must keep the same freedoms
#   if someone modifies and distributes, they must release source under GPL

# anti-lockdown note:
#   rejected: DRM, phone-home, remote kill-switch, forced cloud dependency
#   the program does not restrict modification — no checksums, no license validation, no obfuscation

def word_frequency(text):
    """Count word frequencies in a given text. Pure function, no side effects."""
    # normalize: lowercase, split on whitespace, strip punctuation
    words = []
    for raw_word in text.split():
        word = ''.join(ch for ch in raw_word if ch.isalnum()).lower()
        if word:
            words.append(word)
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq

def format_frequencies(freq):
    """Return a sorted, human-readable string of word frequencies."""
    lines = []
    for word in sorted(freq.keys()):
        lines.append(f"{word}: {freq[word]}")
    return "\n".join(lines)

# demo data — no argv, no argparse, runs with `python3 -c` or directly
sample_text = """
The free software movement aims at giving users freedom, not just convenience.
If the users don't control the program, the program controls the users.
Free software is a matter of liberty, not price.
"""

frequencies = word_frequency(sample_text)
print("=== Word Frequency Tool (free software) ===")
print("Input text:")
print(sample_text.strip())
print("\nOutput:")
print(format_frequencies(frequencies))

# freedom audit output — checkable at a glance
print("\n=== Freedom Audit ===")
print("freedom 0 (run): kept — runs locally, no network")
print("freedom 1 (study & change): kept — source is the .py file")
print("freedom 2 (share): kept — copies unrestricted")
print("freedom 3 (share modified): kept — GPL-3.0-or-later downstream")
print("free_software: True")
print("free_as_in: liberty")

# anti-lockdown pass — explicit rejection
print("\n=== Anti-Lockdown Pass ===")
print("rejected: drm, phone_home, remote_kill, forced_cloud")
print("kept: local computation, user-controlled data, modifiable source")