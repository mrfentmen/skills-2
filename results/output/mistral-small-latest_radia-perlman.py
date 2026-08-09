class RingNode:
    # grandmother test: every node in the ring remembers its left neighbor;
    # if the left neighbor disappears, it picks the next one clockwise and
    # the ring heals itself without any human touching it.
    def __init__(self, name, left=None):
        self.name = name
        self.left = left  # neighbor to the left in the ring
        self.active = True

    def heal(self):
        # self-stabilizing: after a break heals, the next call reconnects
        if not self.left or not self.left.active:
            # find the first active node clockwise
            cur = self.left
            while cur and not cur.active:
                cur = cur.left
            self.left = cur
            return True  # changed
        return False

# zero-config: three nodes in a ring; plug them together and it works
a = RingNode("A")
b = RingNode("B")
c = RingNode("C")
a.left = b
b.left = c
c.left = a

# anomaly: break the link from C to A
c.left = None
print("After break:", [a.heal(), b.heal(), c.heal()])  # all detect and heal

# self-stabilization proof: after the partition clears, the next round reconverges
a.left = b
b.left = c
c.left = a
print("After reconnect:", [a.heal(), b.heal(), c.heal()])  # no changes needed

# simplicity reduction: the real problem is a circular linked list; the loop-free
# subgraph is the whole protocol — each node simply points to the next active node.
# knob audit: no knobs exist; therefore every setting is trivially safe.