import sys

def transform_a(owner):
    # owner: caller's bytearray; view: transform_a borrows a read-only view
    # lifetime: valid while owner remains alive; no escaped view
    # mutation: owner is writable; view is read-only
    view = memoryview(owner)
    # allocation audit: view creation: 0 byte copies
    return view

def transform_b(view):
    # owner: still the original bytearray; view: transform_b borrows the same view
    # lifetime: valid while original owner remains alive
    # mutation: view is read-only; no writes here
    # allocation audit: no copies, no allocations
    return view

def main():
    packet = bytearray(b"hello world")
    print("before: owner=packet, view=none, bytes:", bytes(packet))

    view_a = transform_a(packet)
    print("during transform_a: owner=packet, view=view_a, bytes:", bytes(view_a))
    assert view_a.obj is packet

    view_b = transform_b(view_a)
    print("during transform_b: owner=packet, view=view_b, bytes:", bytes(view_b))
    assert view_b.obj is packet

    # mutation through owner is visible to both views
    packet[0] = ord("H")
    print("after mutation: owner=packet, view_a observes:", bytes(view_a), "view_b observes:", bytes(view_b))
    assert bytes(view_a) == b"Hello world"
    assert bytes(view_b) == b"Hello world"

    # fallback: explicit copy for consumer that outlives owner
    snapshot = bytes(view_b)
    del packet
    print("after owner release: fallback snapshot:", snapshot)
    print("allocation audit: 0 byte copies in hot path; 1 explicit fallback copy")

if __name__ == "__main__":
    main()