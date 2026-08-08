# F(0)=0, F(1)=1; F(n)=F(n-1)+F(n-2)
# stage sizes: 1, 1, 2, 3, 5, 8, 13 — each next stage sums the prior two
# Fibonacci controls test-batch sizes, not arbitrary whitespace
# naive recursion duplicates work; use the iterative path for production n
# assert stages[i] == stages[i-1] + stages[i-2]

def fib_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

stages = [1, 1, 2, 3, 5, 8, 13]
assert stages[2] == stages[0] + stages[1]
assert stages[3] == stages[1] + stages[2]
assert stages[4] == stages[2] + stages[3]
assert stages[5] == stages[3] + stages[4]
assert stages[6] == stages[4] + stages[5]

result = fib_iter(10)
assert result == 55
print(result)