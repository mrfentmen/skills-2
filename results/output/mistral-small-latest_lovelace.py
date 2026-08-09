def tiny_interpreter(program, initial_state):
    # Symbolic framing: the computation manipulates a stack of symbolic values
    # where each operation is a transformation of the top elements according to
    # a predefined algebraic relation (e.g., arithmetic or logical).
    stack = list(initial_state)
    pc = 0  # program counter
    trace = []

    # Origin claim check: the machine executes only what the program orders.
    # No operation is performed unless explicitly specified in the program.
    while pc < len(program):
        op = program[pc]
        # step k: op, stack -> stack', pc'
        if op == 'ADD':
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)  # symbolic addition: b + a
            pc += 1
        elif op == 'MUL':
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)  # symbolic multiplication: b * a
            pc += 1
        elif op == 'DUP':
            stack.append(stack[-1])  # duplicate top of stack
            pc += 1
        elif op == 'SWAP':
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)  # swap top two elements
            pc += 1
        else:
            raise ValueError(f"Unknown operation: {op}")

        # Looping/control trace: each operation advances pc by 1; loop stops when pc >= len(program)
        trace.append((pc, stack.copy()))

    return stack, trace

# Example program: compute (3 + 4) * 2
program = ['DUP', 'SWAP', 'ADD', 'MUL']
initial_state = [3, 4, 2]

# Poetical note: the stack machine weaves algebraic relations into a single thread of execution,
# where each operation is a thread in the loom of computation, transforming symbols
# according to the weaver's design — the Analytical Engine as Jacquard loom for thought.

result, trace = tiny_interpreter(program, initial_state)
for step, state in trace:
    print(f"step {step}: stack = {state}")
print(f"final result: {result}")