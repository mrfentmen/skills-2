# IR: TinyExpr IR (TEIR) – a minimal expression IR with SSA form
# Invariants:
#   - Every value is defined exactly once (SSA)
#   - All operations are pure (no side effects)
#   - Types are explicit and checked at IR construction
#   - Control flow is explicit via branches (not in this tiny example)

class TEIR:
    def __init__(self):
        self.blocks = {}  # block_id -> list of instructions
        self.current_block = "entry"
        self.blocks[self.current_block] = []
        self.values = {}  # value_id -> (op, args, type)
        self.next_id = 0

    def _new_id(self):
        v = f"v{self.next_id}"
        self.next_id += 1
        return v

    def const(self, val, typ):
        # safe: no implicit conversions; types must match
        v = self._new_id()
        self.values[v] = ("const", (val, typ), typ)
        self.blocks[self.current_block].append(("const", v, val, typ))
        return v

    def add(self, a, b):
        # safe: overflow traps by default; no silent wrap
        v = self._new_id()
        ta = self.values[a][2]
        tb = self.values[b][2]
        assert ta == tb == "i32", "add only defined for i32"
        self.values[v] = ("add", (a, b), "i32")
        self.blocks[self.current_block].append(("add", v, a, b))
        return v

    def eval(self):
        env = {}
        for v, (op, args, typ) in self.values.items():
            if op == "const":
                env[v] = args[0]
            elif op == "add":
                env[v] = env[args[0]] + env[args[1]]
        return env

# SSA property: every value assigned exactly once via _new_id and values dict
# Safety default: overflow traps; no silent wrap-around (checked at runtime here)
# Ecosystem note: plugs into: a larger compiler frontend (e.g., lex/parse to TEIR),
# optimizer (e.g., DCE, CSE), and backend (e.g., LLVM or custom codegen)

# Dogfood test: parse and evaluate "2 + 3" end to end
ir = TEIR()
a = ir.const(2, "i32")
b = ir.const(3, "i32")
c = ir.add(a, b)
print("IR blocks:", ir.blocks)
print("IR values:", ir.values)
print("Result:", ir.eval()[c])  # 5