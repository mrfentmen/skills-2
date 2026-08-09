def interpret(program, initial_state, initial_tape):
    # code-as-data: program is a string of instructions, tape is a dict
    states = {"q0", "q1", "q2", "halt"}
    transitions = {
        ("q0", "0"): ("q0", "0", +1),
        ("q0", "1"): ("q1", "1", +1),
        ("q0", "blank"): ("halt", "blank", 0),
        ("q1", "0"): ("q1", "0", +1),
        ("q1", "1"): ("q2", "1", +1),
        ("q1", "blank"): ("halt", "blank", 0),
        ("q2", "0"): ("q2", "0", +1),
        ("q2", "1"): ("q2", "1", +1),
        ("q2", "blank"): ("halt", "blank", 0),
    }
    # instruction string: '0'=stay, '1'=move right, '2'=halt
    # but here we use the tape symbols as data; program is the tape content
    tape = {i: ch for i, ch in enumerate(initial_tape)}
    pos = 0
    state = initial_state
    trace = []
    seen = set()
    step = 0
    max_steps = 100  # bounded termination control
    while state != "halt" and step < max_steps:
        symbol = tape.get(pos, "blank")
        key = (state, symbol)
        if key not in transitions or key in seen:
            break  # controlled cycle or undefined transition
        seen.add(key)
        trace.append((step, state, pos, symbol))
        state, write, move = transitions[key]
        tape[pos] = write
        pos += move
        step += 1
    trace.append((step, state, pos, tape.get(pos, "blank")))
    return trace, tape, state, step

# short-distance step: run a concrete example
program = "0110"  # tape data as code
trace, final_tape, final_state, steps = interpret(program, "q0", program)
print("Trace:")
for t in trace:
    print(t)
print("Final state:", final_state, "Steps:", steps)
print("Final tape:", dict(sorted(final_tape.items())))
print("Decidability note: This machine is decidable — finite states, finite tape length, bounded step limit (100). The halting problem for this restricted sub-language is decidable because every transition is total on reachable symbols and the step bound guarantees termination. General halting for arbitrary Turing machines remains undecidable, but here we stay within a decidable fragment.")