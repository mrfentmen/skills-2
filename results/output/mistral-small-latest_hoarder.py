history = []
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
for attempt in numbers:
    history.append(attempt)
answer = history[-1]
print(history, answer)