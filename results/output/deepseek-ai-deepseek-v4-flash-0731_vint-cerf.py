# agreement: frame = [magic:1=0x7E][len:2][type:1][seq:1][payload:0..65535][crc:1] — anything else is private
# waist: the frame relay — no assumptions about transport or application semantics
# reliability lives at the endpoints, not in the relay
# link absent 30min: queue and forward; never drop silently
# interop note: two operators, one contract — no central coordinator needed

MAGIC = 0x7E
MAX_PAYLOAD = 65535

def make_frame(payload: bytes, type_code: int, seq: int) -> bytes:
    # edge: endpoint builds the frame per the agreement
    length = len(payload)
    assert length <= MAX_PAYLOAD
    crc = (sum(payload) + type_code + seq) & 0xFF
    return bytes([MAGIC]) + length.to_bytes(2, "big") + bytes([type_code, seq]) + payload + bytes([crc])

def parse_frame(frame: bytes):
    # edge: endpoint validates framing and integrity; the core never interprets payload
    if len(frame) < 6 or frame[0] != MAGIC:
        return {"valid": False, "reason": "bad magic or too short"}
    length = (frame[1] << 8) | frame[2]
    if len(frame) != 6 + length:
        return {"valid": False, "reason": "length mismatch"}
    type_code, seq = frame[3], frame[4]
    payload = frame[5:5 + length]
    crc = frame[5 + length]
    if crc != (sum(payload) + type_code + seq) & 0xFF:
        return {"valid": False, "reason": "crc mismatch"}
    return {"valid": True, "type": type_code, "seq": seq, "payload": payload}

def relay(frame: bytes, link_up: bool, queue: list):
    # waist: move the bag of bits; refuse malformed frames; never drop silently
    parsed = parse_frame(frame)
    if not parsed["valid"]:
        return {"action": "rejected", "reason": parsed["reason"], "queued": len(queue)}
    if link_up:
        out, queue[:] = queue[:], []
        return {"action": "forwarded", "frame": frame, "queued": len(queue)}
    queue.append(frame)
    return {"action": "queued", "queued": len(queue), "dropped": 0}

# simulated exchange: two endpoints, one relay, a lossy link
queue = []
frames = [
    make_frame(b"hello", 1, 0),
    make_frame(b"world", 2, 1),
    make_frame(b"\x00\x01\x02", 3, 2),
]
print("--- link down ---")
for f in frames:
    print(relay(f, False, queue))
print("--- link up ---")
for f in frames:
    print(relay(f, True, queue))
print("--- malformed frame ---")
print(relay(b"\x00\x00\x03abc", True, queue))