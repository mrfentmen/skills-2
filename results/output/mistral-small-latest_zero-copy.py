# owner: packet; view: transform1; transform2 borrows transform1's view
# valid while packet remains alive; no escaped view
# transform1 is read-only; transform2 is read-only; packet is writable
# view creation: 0 byte copies; bytes([view]) would copy — not in the hot path
# fallback: copy required when the consumer outlives packet or crosses an ownership boundary

def transform1(owner):
    # owner retains the allocation; the returned memoryview borrows it.
    view = memoryview(owner)[1::2]  # every other byte
    return view

def transform2(view):
    # view borrows from transform1; owner remains packet
    view = memoryview(view)[::-1]  # reverse the bytes
    return view

packet = bytearray(b"0123456789")
print("original packet:", bytes(packet))

# First transform: packet -> transform1
t1_view = transform1(packet)
print("after transform1:", bytes(t1_view))
assert t1_view.obj is packet  # ownership remains with packet

# Second transform: transform1 -> transform2
t2_view = transform2(t1_view)
print("after transform2:", bytes(t2_view))
assert t2_view.obj is packet  # ownership remains with packet

# Mutation through owner is visible in all views
packet[0] = ord('X')
print("after mutation:", "packet:", bytes(packet), "t1_view:", bytes(t1_view), "t2_view:", bytes(t2_view))

# Fallback: bytes(t2_view) is an explicit copy for a consumer that must outlive packet.
snapshot = bytes(t2_view)
del packet
print("owned fallback:", snapshot)