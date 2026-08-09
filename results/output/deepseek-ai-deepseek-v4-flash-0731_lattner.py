class TinyIR:
    # IR boundary: TinyIR is a linear list of instructions, each a tuple
    # (op, dest, *operands). Invariants:
    #   - dest is a unique SSA name (assigned exactly once)
      #   - operands are either SSA names or literal constants
    #   - no control flow; evaluation is a straight-line dataflow
    def __init__(self):
        self.instrs = []
        self.names = set()

    def emit(self, op, dest, *operands):
        assert dest not in self.names, f"SSA violation: {dest} assigned twice"
        for opnd in operands:
            if isinstance(opnd, str):
                assert opnd in self.names or opnd in consts, f"use before def: {opnd}"
        self.names.add(dest)
        self.instrs.append((op, dest, operands))

    def eval(self, env=None):
        env = env or {}
        for op, dest, operands in self.instrs:
            vals = [env[o] if isinstance(o, str) else o for o in operands]
            if op == "const":
                env[dest] = vals[0]
            elif op == "add":
                env[dest] = vals[0] + vals[1]
            elif op == "mul":
                env[dest] = vals[0] * vals[1]
            elif op == "sub":
                env[dest] = vals[0] - vals[1]
            else:
                raise ValueError(f"unknown op: {op}")
        return env

# Safety default: division is forbidden (no div op) — avoids division-by-zero
# and overflow traps; all values are Python ints, but the IR itself forbids
# undefined behavior by construction (SSA + use-before-def check).

# Frontend: parse a tiny expression into TinyIR
def parse_to_ir(expr):
    # Grammar: expr := number | expr ('+'|'-'|'*') expr
    # Simple recursive descent, no precedence (left-to-right for demo)
    tokens = expr.replace(" ", "")
    ir = TinyIR()
    pos = 0
    def parse_expr():
        nonlocal pos
        if pos >= len(tokens):
            raise SyntaxError("unexpected end")
        if tokens[pos].isdigit():
            num = tokens[pos]
            pos += 1
            name = f"t{len(ir.instrs)}"
            ir.emit("const", name, int(num))
            return name
        left = parse_expr()
        if pos >= len(tokens):
            return left
        op = tokens[pos]
        pos += 1
        right = parse_expr()
        dest = f"t{len(ir.instrs)}"
        if op == "+":
            ir.emit("add", dest, left, right)
        elif op == "-":
            ir.emit("sub", dest, left, right)
        elif op == "*":
            ir.emit("mul", dest, left, right)
        else:
            raise SyntaxError(f"bad op: {op}")
        return dest
    parse_expr()
    return ir

# Dogfood test: real input "2+3*4" (left-assoc: (2+3)*4 = 20)
ir = parse_to_ir("2+3*4")
print("TinyIR instructions:")
for op, dest, operands in ir.instrs:
    print(f"  {dest} = {op} {', '.join(str(o) for o in operands)}")
result = ir.eval()
print("Result:", result[ir.instrs[-1][1]])

# Ecosystem note: plugs into a larger stack — frontend (parser) emits TinyIR,
# optimizer could run const-prop on it, backend could lower to bytecode or
# machine code. Callers (e.g., a REPL) only see the eval() interface, so
# swapping the backend doesn't change the frontend contract.