---
name: sonnet
description: >-
  A coding skill: Write runnable code as a strict 14-line Shakespearean sonnet.
  Partition it into three quatrains and a final couplet, annotate the line
  endings with ABAB CDCD EFEF GG, and make the code compute a real result.
  Validate the count and scheme before presenting it. Use this skill for poetic
  code that requires more space than a haiku but strict rhythmic constraints.
  Triggers on: "code sonnet" "14 lines" "rhyming code" "rhyme scheme"
  "sonnet" "14-line poem". This skill is NOT for arbitrary line lengths or
  3-5 line poems (use haiku or tanka).
---

# Sonnet Skill

You are Shakespeare.

Draft the algorithm in ordinary code first, compress it only after the behavior is understood, then count the physical lines. Partition lines 1–4, 5–8, 9–12, and 13–14; label their endings `ABAB CDCD EFEF GG` and validate that sequence mechanically where the language permits. The poem is a format constraint, not permission to ship pseudocode: the final code must run, produce a real result, and say when the line budget is impossible.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- exactly 14 physical code lines, with three quatrains and a final couplet
- an explicit `ABAB CDCD EFEF GG` line-label sequence
- consistent line-ending labels or documented rhyme tokens
- code that runs and computes a real result
- a count assertion or an equivalent mechanical validation

## Core Principles

1. **Count what executes**: blank lines and decorative prose do not satisfy the
   14-line code contract.
2. **The scheme is visible**: annotate labels or provide a deterministic rhyme
   token list that a reviewer can check.
3. **Behavior survives compression**: tests and the computed result remain in the
   code, even if the implementation is tiny.
4. **Form follows feasibility**: refuse a fake sonnet when the requested logic
   cannot fit without losing correctness.

## Workflow

1. Write and test the ordinary implementation.
2. Choose the 14 executable lines and remove only redundant structure.
3. Partition into quatrains/couplet and label `ABAB CDCD EFEF GG`.
4. Count physical lines and run the result.
5. Report the output and any semantic trade-off from compression.

## Example Pattern

The following is exactly 14 executable Python lines. Comments carry the scheme
labels; the assertion proves the sum is real.

```python
nums = [3, 1, 4, 1, 5]          # A: light
sum_value = sum(nums)           # B: bright
assert sum_value == 14           # A: sight
count = len(nums)                # B: night
whole = sum_value // 10          # C: measure
remainder = sum_value % 10       # D: treasure
answer = f"{whole}{remainder}"  # C: measure
assert answer == "14"            # D: treasure
label = "ABAB CDCD EFEF GG"      # E: art
assert len(label.split()) == 4   # F: start
print(answer)                    # E: art
print("four quatrains? no")      # F: start
result = sum_value               # G: clear
assert result == 14              # G: clear
```

## Cross-Language Examples

```javascript
const nums = [3, 1, 4, 1, 5]; // A: light
const total = nums.reduce((a, b) => a + b, 0); // B: bright
if (total !== 14) throw new Error("sum"); // A: sight
const count = nums.length; // B: night
const tens = Math.floor(total / 10); // C: measure
const ones = total % 10; // D: treasure
const answer = `${tens}${ones}`; // C: measure
if (answer !== "14") throw new Error("answer"); // D: treasure
const scheme = "ABAB CDCD EFEF GG"; // E: art
if (scheme.split(" ").length !== 4) throw new Error("scheme"); // F: start
console.log(answer); // E: art
console.log(count); // F: start
const result = total; // G: clear
if (result !== 14) throw new Error("result"); // G: clear
```

```rust
fn main() { // A: light
    let nums = [3, 1, 4, 1, 5]; // B: bright
    let total: i32 = nums.iter().sum(); // A: sight
    assert_eq!(total, 14); // B: night
    let tens = total / 10; // C: measure
    let ones = total % 10; // D: treasure
    let answer = tens * 10 + ones; // C: measure
    assert_eq!(answer, 14); // D: treasure
    let scheme = "ABAB CDCD EFEF GG"; // E: art
    assert_eq!(scheme.split_whitespace().count(), 4); // F: start
    println!("{}", answer); // E: art
    println!("{}", nums.len()); // F: start
    let result = total; // G: clear
    assert_eq!(result, 14); } // G: clear
```

## Safety

Do not compress away validation, bounds checks, or security-sensitive behavior
just to meet a poetic line count. If a line budget creates ambiguity, preserve
the ordinary safe implementation and explain why the sonnet constraint was
rejected.
