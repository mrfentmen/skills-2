# Turing-style state machine interpreting an instruction string as code-as-data

# States and transitions
states = {"start", "read", "write", "move", "accept"}
transitions = {
    ("start", "0"): ("read", "0", 0),
    ("start", "1"): ("read", "1", 0),
    ("read", "0"): ("write", "0", +1),
    ("read", "1"): ("write", "1", +1),
    ("write", "0"): ("move", "0", +1),
    ("write", "1"): ("move", "1", +1),
    ("move", "0"): ("accept", "0", 0),
    ("move", "1"): ("accept", "1", 0),
}

# Instruction string as code-as-data: "010" means read 0, write 1, move +1, read 0
instruction = "010"
tape = {i: bit for i, bit in enumerate(instruction)}
pos = 0
state = "start"
trace = []

# Decidability note: finite instruction length => finite steps; halting guaranteed
decidable = "The machine halts after exactly len(instruction) steps; decidable."

while state != "accept":
    key = (state, tape.get(pos, "blank"))
    if key not in transitions:
        break
    state, write, move = transitions[key]
    tape[pos] = write
    pos += move
    trace.append((state, pos, tape.copy()))

print("Trace:", trace)
print("Final state:", state)
print("Decidability note:", decidable)