import hashlib

def hash_chain_append_only(ledger, new_entry):
    # who must we trust here? no one — the hash chain makes tampering detectable
    # cheating requires redoing the entire chain — infeasible, not just forbidden
    if not ledger:
        return hashlib.sha256(new_entry.encode()).hexdigest()
    last_hash = ledger[-1]
    new_hash = hashlib.sha256(f"{last_hash}|{new_entry}".encode()).hexdigest()
    return ledger + [new_hash]

def verify_chain(ledger):
    # proof over promises: the hash chain binds every entry to the past
    for i in range(1, len(ledger)):
        expected = hashlib.sha256(f"{ledger[i-1]}|{ledger[i]}".encode()).hexdigest()
        if ledger[i] != expected:
            return False
    return True

def longest_chain_wins(candidates):
    # objective consensus: the protocol rule decides, no moderator
    return max(candidates, key=len)

# trust audit: no admin, no central party — the chain enforces integrity
ledger = []
ledger = hash_chain_append_only(ledger, "genesis block")
ledger = hash_chain_append_only(ledger, "alice sends 1 coin to bob")
ledger = hash_chain_append_only(ledger, "bob sends 0.5 coin to charlie")

# incentive line: honest behavior is the rational choice — tampering breaks the chain
# edge case: lost key? the value is lost to the network — no bailout, no restore desk
print("Verification result:", verify_chain(ledger))