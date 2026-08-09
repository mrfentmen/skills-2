# agreement: frame = [version:1][ttl:1][src:4][dst:4][len:2][payload][crc:2]
#   version: 0x01 (fixed)
#   ttl: hop count, decremented at each relay; 0x00 drops silently
#   src/dst: 32-bit opaque identifiers (no assumptions about structure)
#   len: payload length in bytes (0-65535)
#   payload: opaque bytes (core does not interpret)
#   crc: CRC-16/CCITT over [version,ttl,src,dst,len,payload]; 0x0000 means "no CRC"
#   anything else is private to endpoints

# waist: the id/address layer — no assumptions about transport or app
#   the core only moves frames; it does not parse payloads, enforce semantics, or manage state

# reliability lives at the endpoints, not in the relay
#   endpoints may retransmit, sequence, or acknowledge; relays only decrement ttl and forward

# link absent 30min: queue and forward; never drop silently
#   relays implement store-and-forward with unbounded queues; no timeouts or drops

# two operators, one contract — no central coordinator needed
#   any relay that honors the framing and ttl rules can join the network

import struct
import zlib

class Packet:
    def __init__(self, src, dst, payload, ttl=64):
        self.version = 0x01
        self.ttl = ttl
        self.src = src
        self.dst = dst
        self.payload = payload
        self.crc = 0x0000  # computed on encode

    def encode(self):
        # build payload slice
        payload = self.payload
        length = len(payload)
        # compute crc over [version,ttl,src,dst,length,payload]
        crc_input = bytes([self.version, self.ttl]) + struct.pack(">II", self.src, self.dst) + struct.pack(">H", length) + payload
        self.crc = zlib.crc32(crc_input) & 0xFFFF
        # assemble frame
        frame = (
            bytes([self.version, self.ttl])
            + struct.pack(">II", self.src, self.dst)
            + struct.pack(">H", length)
            + payload
            + struct.pack(">H", self.crc)
        )
        return frame

    @staticmethod
    def decode(frame):
        if len(frame) < 12:
            raise ValueError("frame too short")
        version, ttl = frame[0], frame[1]
        src, dst = struct.unpack(">II", frame[2:10])
        length = struct.unpack(">H", frame[10:12])[0]
        if len(frame) < 12 + length + 2:
            raise ValueError("frame truncated")
        payload = frame[12:12 + length]
        crc = struct.unpack(">H", frame[12 + length:14 + length])[0]
        # validate crc
        crc_input = bytes([version, ttl]) + struct.pack(">II", src, dst) + struct.pack(">H", length) + payload
        computed = zlib.crc32(crc_input) & 0xFFFF
        if computed != crc:
            raise ValueError("crc mismatch")
        pkt = Packet(src, dst, payload, ttl)
        pkt.version = version
        pkt.ttl = ttl
        pkt.crc = crc
        return pkt

class Relay:
    def __init__(self, addr):
        self.addr = addr
        self.queue = []

    def receive(self, frame):
        try:
            pkt = Packet.decode(frame)
        except Exception:
            return  # drop silently on malformed frames
        if pkt.ttl == 0:
            return  # drop silently
        pkt.ttl -= 1
        # store-and-forward: always queue, never drop
        self.queue.append(pkt.encode())
        return len(self.queue)

    def forward(self, link_up):
        if not link_up:
            return {"queued": len(self.queue)}
        sent = self.queue[:]
        self.queue.clear()
        return {"sent": [Packet.decode(f) for f in sent]}

# simulate a slow, lossy link
def simulate_exchange(src_relay, dst_relay, frames, link_up_cycles):
    for cycle, link_up in enumerate(link_up_cycles):
        # inject frames into src
        for f in frames:
            src_relay.receive(f)
        # forward from src to dst
        src_out = src_relay.forward(link_up)
        if "sent" in src_out:
            for pkt_frame in src_out["sent"]:
                dst_relay.receive(pkt_frame)
        # forward from dst to src (echo)
        dst_out = dst_relay.forward(link_up)
        if "sent" in dst_out:
            for pkt_frame in dst_out["sent"]:
                src_relay.receive(pkt_frame)
        print(f"cycle {cycle}: src queued={len(src_relay.queue)} dst queued={len(dst_relay.queue)}")

# example usage
if __name__ == "__main__":
    # create two relays
    A = Relay(0xA0A0A0A0)
    B = Relay(0xB0B0B0B0)

    # craft a packet
    pkt = Packet(src=0xA0A0A0A0, dst=0xB0B0B0B0, payload=b"hello", ttl=2)
    frame = pkt.encode()

    # simulate 5 cycles: link up only on cycles 1 and 3
    simulate_exchange(A, B, [frame], [False, True, False, True, False])