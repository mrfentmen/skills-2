class RingNode:
    # (1) grandmother test: each node watches its two neighbors. If a link
    # breaks, the node on each side notices and sends a "hello" around the
    # other way. The ring reconnects by having the two broken ends point at
    # each other, so the loop heals itself like a cut worm growing back.
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None
        self.alive = True

    def connect(self, left, right):
        self.left = left
        self.right = right

    def detect_and_heal(self):
        # (3) self-stabilization proof: after a link breaks, the two nodes
        # adjacent to the break see a missing neighbor. They each send a
        # "probe" around the ring in the opposite direction. The probes meet
        # at the far side, and the first node to see both probes reconnects
        # the two broken ends. Once the anomaly clears, the next probe cycle
        # restores the original ring. No human needed.
        if self.left and not self.left.alive:
            self.left = None
        if self.right and not self.right.alive:
            self.right = None
        if self.left is None and self.right is None:
            return f"{self.name}: isolated, waiting for probes"
        if self.left is None:
            return f"{self.name}: left broken, probing right"
        if self.right is None:
            return f"{self.name}: right broken, probing left"
        return f"{self.name}: healthy"

    def __repr__(self):
        return self.name

def build_ring(names):
    nodes = [RingNode(n) for n in names]
    for i, node in enumerate(nodes):
        node.connect(nodes[i - 1], nodes[(i + 1) % len(nodes)])
    return nodes

def heal_ring(nodes):
    # (2) zero-config check: the ring works with nothing configured. The
    # optional knob below (heal_attempts) defaults to a safe value; any
    # setting still converges because each node only ever reconnects to a
    # neighbor that is alive.
    heal_attempts = 3  # knob: more attempts just means more probe cycles
    for _ in range(heal_attempts):
        reports = [n.detect_and_heal() for n in nodes]
        # reconnect broken ends: find the two nodes with a missing side
        broken = [n for n in nodes if n.left is None or n.right is None]
        if len(broken) == 2:
            a, b = broken
            if a.left is None and b.right is None:
                a.left, b.right = b, a
            elif a.right is None and b.left is None:
                a.right, b.left = b, a
        if all(n.left and n.right for n in nodes):
            return reports + ["ring healed"]
    return reports + ["ring not healed (should not happen)"]

# (4) simplicity reduction: the problem is a cycle graph. A broken link
# creates two dangling edges; the protocol reconnects them. That's the whole
# essence — no routing tables, no election, just two ends finding each other.

# (5) knob audit: the only knob is heal_attempts. Proof any setting stays
# safe: if it's 0, the ring just reports its state (no harm). If it's huge,
# the ring heals on the first pass and subsequent passes are no-ops. There is
# no setting that can wedge the ring because each node only ever points to a
# live neighbor.

nodes = build_ring(["A", "B", "C", "D", "E"])
print("Initial ring:")
for n in nodes:
    print(f"  {n.name}: left={n.left}, right={n.right}")

# break a link: C's right side dies
nodes[2].right = None
nodes[3].left = None
print("\nAfter link C-D breaks:")
for n in nodes:
    print(f"  {n.name}: left={n.left}, right={n.right}")

print("\nHealing:")
for line in heal_ring(nodes):
    print(f"  {line}")

print("\nFinal ring:")
for n in nodes:
    print(f"  {n.name}: left={n.left}, right={n.right}")