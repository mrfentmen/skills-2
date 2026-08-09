# Lamport-style message ordering system with happens-before causality

class LamportMessage:
    def __init__(self, ts, pid, content):
        self.ts = ts
        self.pid = pid
        self.content = content

    def __repr__(self):
        return f"Msg(ts={self.ts}, pid={self.pid}, content={self.content})"

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.clock = 0
        self.queue = []

    def send(self, content, target):
        self.clock += 1
        msg = LamportMessage(self.clock, self.pid, content)
        target.queue.append(msg)
        return msg

    def receive(self):
        if not self.queue:
            return None
        # Process messages in happens-before order (FIFO queue)
        msg = self.queue.pop(0)
        self.clock = max(self.clock, msg.ts) + 1
        return msg

# === SPECIFICATION ===
# INVARIANTS (safety properties):
# 1. Happens-before ordering: For any two messages m1 and m2, if m1 happens before m2,
#    then m1.ts < m2.ts in the observed order.
# 2. Local order: Messages sent by a single process are observed in the order they were sent.
# 3. Quorum halt: If a process cannot communicate with a majority, it halts (queue processing stops).
# 4. No duplication: Each message is processed exactly once by each process.

# STATE MACHINE:
# Init: Two processes with empty queues and clock=0
# Next: A transition is either:
#   - A send event: process increments clock, creates message, appends to target queue
#   - A receive event: process dequeues message, updates clock to max(clock, msg.ts)+1

# FAILURE ASSUMPTIONS:
# - Message loss: Messages may be lost (queue may be empty when expected)
# - Message reorder: Messages may arrive out of order (queue is FIFO but network may reorder)
# - Crash: A process may crash (stop processing messages)

# PARTITION BEHAVIOR:
# - Minority partition halts: If a process cannot communicate with a majority (here, both processes),
#   it stops processing messages (halts).

# === IMPLEMENTATION ===
def run_ordering_system():
    # Init: two processes with empty queues and clock=0
    p1 = Process(1)
    p2 = Process(2)

    # Send messages
    m1 = p1.send("A", p2)  # p1: clock=1, p2: queue=[Msg(ts=1, pid=1, content="A")]
    m2 = p2.send("B", p1)  # p2: clock=1, p1: queue=[Msg(ts=1, pid=2, content="B")]
    m3 = p1.send("C", p2)  # p1: clock=2, p2: queue=[Msg(ts=1, pid=1, content="A"), Msg(ts=2, pid=1, content="C")]

    # Receive messages in happens-before order
    observed_order = []
    while True:
        msg1 = p1.receive()
        msg2 = p2.receive()
        if msg1 is None and msg2 is None:
            break
        if msg1 is not None:
            observed_order.append(("p1", msg1))
        if msg2 is not None:
            observed_order.append(("p2", msg2))

    # Print observed order
    for proc, msg in observed_order:
        print(f"{proc} received {msg}")

run_ordering_system()