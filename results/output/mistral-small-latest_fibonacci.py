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

# Verify growth structure
stages = [1, 1]
while len(stages) < 7:
    stages.append(stages[-1] + stages[-2])
assert stages == [1, 1, 2, 3, 5, 8, 13]
for i in range(2, len(stages)):
    assert stages[i] == stages[i - 1] + stages[i - 2]

# Compute F(10)
result = fib_iter(10)
print(result)