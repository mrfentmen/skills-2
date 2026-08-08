import hashlib
import json
import time

class HashChainedLedger:
    def __init__(self):
        self.chain = []
        self.genesis()

    def genesis(self):
        # trust removal: no central party, genesis is the only anchor
        block = {
            "index": 0,
            "timestamp": time.time(),
            "data": "genesis",
            "prev_hash": "0" * 64,
            "nonce": 0
        }
        block["hash"] = self.hash_block(block)
        self.chain.append(block)

    def hash_block(self, block):
        # proof: any tampering changes the hash, and redoing the work is infeasible
        block_copy = {k: v for k, v in block.items() if k != "hash"}
        return hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()

    def add_block(self, data, difficulty=4):
        # proof of work: honest nodes pay a cost, attackers pay the same cost per block
        index = len(self.chain)
        prev_hash = self.chain[-1]["hash"]
        nonce = 0
        target = "0" * difficulty
        while True:
            block = {
                "index": index,
                "timestamp": time.time(),
                "data": data,
                "prev_hash": prev_hash,
                "nonce": nonce
            }
            block_hash = self.hash_block(block)
            if block_hash.startswith(target):
                block["hash"] = block_hash
                self.chain.append(block)
                return block
            nonce += 1

    def is_valid(self):
        # consensus rule: every block must chain to the previous hash and meet the difficulty
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            prev = self.chain[i-1]
            if block["prev_hash"] != prev["hash"]:
                return False
            if self.hash_block(block) != block["hash"]:
                return False
            if not block["hash"].startswith("0" * 4):
                return False
        return True

    def longest_chain_wins(self, other):
        # objective conflict resolution: the longest valid chain wins, no moderator
        if len(other.chain) > len(self.chain) and other.is_valid():
            return other
        return self

    def tamper(self, index, new_data):
        # edge case: tampering is detectable and the chain becomes invalid
        self.chain[index]["data"] = new_data

# incentive line: honest mining is rational — the cost of rewriting history grows
# exponentially with each block, so attack costs more than any reward it buys
ledger = HashChainedLedger()
ledger.add_block("alice->bob 1 coin")
ledger.add_block("bob->carol 2 coins")
ledger.add_block("carol->dave 3 coins")

print("valid before tamper:", ledger.is_valid())

# edge case: no bailout — a corrupted block invalidates the chain, value is lost
ledger.tamper(1, "alice->mallory 100 coins")
print("valid after tamper:", ledger.is_valid())

# consensus: a longer valid chain wins, even if it arrives later
rival = HashChainedLedger()
rival.add_block("alice->bob 1 coin")
rival.add_block("bob->carol 2 coins")
rival.add_block("carol->dave 3 coins")
rival.add_block("dave->eve 4 coins")
winner = ledger.longest_chain_wins(rival)
print("winning chain length:", len(winner.chain))
print("winner valid:", winner.is_valid())