import math
import unittest

# Inspected the computation: it's a simple geometric mean of a list of positive numbers.
# No existing implementation found. Need to implement from scratch.

def geometric_mean(numbers):
    """
    Compute the geometric mean of a list of positive numbers.
    Formula: (x1 * x2 * ... * xn) ** (1/n)
    """
    if not numbers:
        raise ValueError("Input list cannot be empty")
    if any(n <= 0 for n in numbers):
        raise ValueError("All numbers must be positive")
    product = math.prod(numbers)
    return product ** (1.0 / len(numbers))

# Verification: I wrote a test suite and ran it.
class TestGeometricMean(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertAlmostEqual(geometric_mean([1, 2, 3, 4]), 2.213363839400643)
        self.assertAlmostEqual(geometric_mean([2, 8]), 4.0)
        self.assertAlmostEqual(geometric_mean([10]), 10.0)

    def test_empty_list(self):
        with self.assertRaises(ValueError):
            geometric_mean([])

    def test_non_positive_numbers(self):
        with self.assertRaises(ValueError):
            geometric_mean([1, 2, 0])
        with self.assertRaises(ValueError):
            geometric_mean([1, -1, 3])

# Ran the tests. All passed.
unittest.main(argv=[''], exit=False)

# What changed:
# - Implemented geometric_mean function
# - Added input validation for empty list and non-positive numbers

# What was verified:
# - Function logic tested with 3 positive cases
# - Edge cases (empty list, non-positive numbers) tested
# - All tests passed

# What remains unverified:
# - Performance under large input sizes (e.g., 1M elements)
# - Behavior with very large or very small numbers (overflow/underflow)
# - Thread safety if used in concurrent contexts
# - Integration with any existing codebase patterns

# Print the result for the sample input [1, 2, 3, 4]
result = geometric_mean([1, 2, 3, 4])
print(result)