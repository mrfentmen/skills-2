# === Mise en Place ===
# Environment: Python 3.8+, no external dependencies
# Inputs: time in seconds (int), optional label (str)
# Tests: happy path, zero, negative, boundary, malformed
# Rollback: simple exit on invalid input
# Observability: print-based feedback loop

# === Fundamentals ===
# The base technique is time conversion and safe arithmetic
# Master the conversion before adding features

# === Fearlessness Note ===
# Fear of invalid input scares us — good. That is the what-the-hell moment.
# We'll handle it with a clear error and a smile.

# === Joy Check ===
# Are we still interested? If not, the timer will still work — but the craft
# deserves our abandon. Let's keep it fun.

def timer(seconds, label="Timer"):
    if not isinstance(seconds, int) or seconds < 0:
        print(f"Bonjour! {label} cannot run with invalid time: {seconds}")
        return
    print(f"🍳 {label} started for {seconds} seconds...")
    for remaining in range(seconds, -1, -1):
        print(f"  {remaining}...")
    print(f"🎉 {label} complete!")

# === Test Loop ===
# Ran the recipe 5 times:
# 1. Happy path: 3 seconds — sang
# 2. Zero seconds — worked
# 3. Negative seconds — handled with error
# 4. Boundary: 1 second — sang
# 5. Malformed: "five" — handled with error
# Variables are now pinned: seconds must be non-negative int

# === Production ===
timer(3, "Soufflé Rise")
timer(0, "Quick Check")
timer(-1, "Oops")
timer(1, "Flash")
timer("five", "Oops Again")