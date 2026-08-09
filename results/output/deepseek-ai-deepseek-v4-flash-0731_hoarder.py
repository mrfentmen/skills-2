history = []
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
for idx, num in enumerate(numbers):
    history.append(("read", idx, num))
    if idx == 0:
        current_max = num
        history.append(("init_max", current_max))
    else:
        if num > current_max:
            history.append(("candidate", num, "greater_than", current_max))
            current_max = num
            history.append(("update_max", current_max))
        else:
            history.append(("candidate", num, "not_greater_than", current_max))
    history.append(("state_after_step", idx, current_max))
history.append(("final_max", current_max))
print(history)