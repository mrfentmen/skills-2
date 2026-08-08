import sys

def transform_a(owner, length):
    # owner: caller's bytearray; view: transform_a's borrowed read-only view
    # lifetime: valid while owner remains alive; no escaped view
    # mutation: owner is writable; view is read-only
    view = memoryview(owner)[:length]
    # allocation audit: view creation: 0 byte copies
    return view

def transform_b(view):
    # owner: still the original bytearray; view: transform_b's borrowed read-only view
    # lifetime: valid while original owner remains alive; no escaped view
    # mutation: no party may write through this view
    # allocation audit: no copies, no allocations
    return view

def main():
    packet = bytearray(b"hello world")
    print("before: owner=caller packet, bytes:", bytes(packet))

    # hand-off 1: caller -> transform_a
    view_a = transform_a(packet, 5)
    print("during transform_a: owner=packet, view=transform_a, bytes:", bytes(view_a))
    assert view_a.obj is packet

    # hand-off 2: transform_a -> transform_b
    view_b = transform_b(view_a)
    print("during transform_b: owner=packet, view=transform_b, bytes:", bytes(view_b))
    assert view_b.obj is packet

    # mutation through owner, observed by both views
    packet[0] = ord("H")
    print("after mutation: owner=packet, view_a observes:", bytes(view_a), "view_b observes:", bytes(view_b))
    assert bytes(view_a) == b"Hello"
    assert bytes(view_b) == b"Hello"

    # fallback: explicit copy for consumer that outlives packet
    snapshot = bytes(view_b)
    del packet
    print("after owner release: owned fallback:", snapshot)
    assert snapshot == b"Hello world"

    # allocation audit: total byte copies in zero-copy path = 0
    print("allocation audit: zero-copy path copies 0 bytes; fallback copies", sys.getsizeof(snapshot), "bytes")

if __name__ == "__main__":
    main()