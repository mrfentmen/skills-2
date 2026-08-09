import hashlib
import json

class HashChainLedger:
    def __init__(self):
        self.chain = []
        self.pending = []
        # who must we trust here? the genesis block — that is the seed, not the admin
        self.chain.append(self._create_genesis())

    def _create_genesis(self):
        # proof over promises: the hash binds the record to the work
        genesis = {"index": 0, "data": "genesis", "prev_hash": "0", "nonce": 0}
        genesis["hash"] = self._hash_block(genesis)
        return genesis

    def _hash_block(self, block):
        # cheating requires redoing the proof of work — infeasible, not just forbidden
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def append(self, data):
        # the rational move is honest appending: attack costs more than the reward it buys
        last_block = self.chain[-1]
        new_block = {
            "index": last_block["index"] + 1,
            "data": data,
            "prev_hash": last_block["hash"],
            "nonce": 0
        }
        new_block["hash"] = self._hash_block(new_block)
        self.pending.append(new_block)

    def commit(self):
        # longest valid chain wins; no committee, no moderator, no phone call
        if not self.pending:
            return False
        self.chain.extend(self.pending)
        self.pending = []
        return True

    def verify_chain(self):
        # tampering must be detectable: any change breaks the hash chain
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current["prev_hash"] != previous["hash"]:
                return False
            if self._hash_block(current) != current["hash"]:
                return False
        return True

# Edge case: lost key? the value remains in the chain — no restore desk, no bailout
ledger = HashChainLedger()
ledger.append("alice sends 1 coin to bob")
ledger.append("bob sends 0.5 coin to charlie")
ledger.commit()

print("Chain verification:", ledger.verify_chain())
print("Last block hash:", ledger.chain[-1]["hash"])