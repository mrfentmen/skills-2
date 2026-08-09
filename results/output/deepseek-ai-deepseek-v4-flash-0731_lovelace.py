def tiny_interpreter(program, initial_state):
    # (2) Symbolic framing: we manipulate a machine state as a single integer
    #     register, and instructions as ordered transformations upon it.
    #     The abstraction is a tiny stored-program machine: a list of
    #     operations, each a pure function of the current state.
    
    # (1) Step table: for each instruction, we record (pc, op, state_before, state_after).
    #     Example program: [("inc",), ("dec",), ("inc",), ("halt",)]
    #     step 0: pc=0, op=inc, state=0 -> state=1
    #     step 1: pc=1, op=dec, state=1 -> state=0
    #     step 2: pc=2, op=inc, state=0 -> state=1
    #     step 3: pc=3, op=halt, state=1 -> state=1 (no change)
    
    state = initial_state
    pc = 0
    trace = []
    
    # (4) Looping/control trace: the loop advances pc by 1 each iteration,
    #     and stops when pc reaches len(program) or when it executes "halt".
    #     Termination is guaranteed because pc strictly increases and the
    #     program is finite.
    while pc < len(program):
        op = program[pc]
        before = state
        if op == "inc":
            state += 1
        elif op == "dec":
            state -= 1
        elif op == "halt":
            trace.append((pc, op, before, state))
            break
        else:
            raise ValueError(f"Unknown op: {op}")
        trace.append((pc, op, before, state))
        pc += 1
    
    # (3) Origin claim check: the machine did not originate this sequence;
    #     it merely executed the ordered operations we supplied. Every
    #     transition is a direct consequence of the instruction list.
    
    return state, trace

# (5) Poetical note: the deeper relation is that a finite list of simple
#     transformations can embody any deterministic process — the Jacquard
#     loom of arithmetic, where the pattern (program) and the thread (state)
#     weave together, and the machine is but a faithful shuttle.

program = ["inc", "dec", "inc", "halt"]
final_state, trace = tiny_interpreter(program, 0)

for step in trace:
    pc, op, before, after = step
    print(f"pc={pc}, op={op}, state {before} -> {after}")
print(f"final state: {final_state}")