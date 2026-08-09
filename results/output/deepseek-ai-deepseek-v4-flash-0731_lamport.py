class LamportClock:
    # Invariant 1: For any two events e1, e2 in the same process, if e1 occurs before e2, then clock(e1) < clock(e2).
    # Invariant 2: For any message m, if send(m) happens-before recv(m), then clock(send(m)) < clock(recv(m)).
    # Invariant 3: The happens-before relation is a strict partial order (irreflexive, antisymmetric, transitive).
    # Invariant 4: No two events in the same process have the same clock value.
    # Invariant 5: The clock value of any event is always a positive integer (>= 1).
    def __init__(self, pid):
        self.time = 0
        self.pid = pid

    def tick(self):
        # Local event: advance clock by 1
        self.time += 1
        return self.time

    def send(self):
        # Send event: advance clock by 1, stamp message
        self.time += 1
        return (self.time, self.pid)

    def receive(self, ts, pid):
        # Receive event: clock = max(local, received) + 1
        # This enforces happens-before: recv is causally after send
        self.time = max(self.time, ts) + 1
        return self.time

# State machine: Init predicate and Next relation
# Init: (clock_a = 0, clock_b = 0, queue = empty, log = empty)
# Next: 
#   - Process A performs a local tick
#   - Process B performs a local tick
#   - Process A sends a message (stamped with A's clock) to the queue
#   - Process B sends a message (stamped with B's clock) to the queue
#   - Process A receives a message from the queue (if non-empty)
#   - Process B receives a message from the queue (if non-empty)
# Failure assumption: 
#   - Message loss: not modeled (queue is reliable)
#   - Message reorder: not modeled (FIFO queue)
#   - Crash: not modeled (both processes run to completion)
# Partition behavior: 
#   - If the queue is partitioned (unreachable), the processes halt — they do not diverge.
#   - A minority partition (one process isolated) stops sending/receiving, never invents events.

# Two processes with logical clocks
a = LamportClock(1)
b = LamportClock(2)

# Shared FIFO queue (reliable, no loss, no reorder)
queue = []

# Event log to record observed order
log = []

# Process A sends first message
m1 = a.send()
queue.append(m1)
log.append(("A_send", m1))

# Process B receives it
if queue:
    msg = queue.pop(0)
    b.receive(*msg)
    log.append(("B_recv", msg))

# Process B sends a reply
m2 = b.send()
queue.append(m2)
log.append(("B_send", m2))

# Process A receives the reply
if queue:
    msg = queue.pop(0)
    a.receive(*msg)
    log.append(("A_recv", msg))

# Process A does a local tick
a_tick = a.tick()
log.append(("A_tick", a_tick))

# Process B does a local tick
b_tick = b.tick()
log.append(("B_tick", b_tick))

# Print the observed order (causal, not wall-clock)
print("Observed happens-before order:")
for event in log:
    print(event)