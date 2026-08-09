def solve_the_case(evidence_log, witness_statements):
    # The dame called it a locked room. The lock was a lie, and so was she.
    # Suspects: "Mona the Maven" (the data source) and "Vic the Vault" (the cache).
    # Evidence trail: observed facts first, hypotheses second, verdict last.
    observed_facts = []
    hypotheses = []

    # Observed facts: what the ledger actually says.
    observed_facts.append({"fact": "source_ledger_version", "value": evidence_log.get("source_version")})
    observed_facts.append({"fact": "vault_ledger_version", "value": evidence_log.get("vault_version")})
    observed_facts.append({"fact": "source_ledger_entry", "value": evidence_log.get("source_entry")})
    observed_facts.append({"fact": "vault_ledger_entry", "value": evidence_log.get("vault_entry")})

    # Hypotheses: who could have done it, before we check the alibi.
    hypotheses.append({"suspect": "Mona the Maven", "motive": "version drift"})
    hypotheses.append({"suspect": "Vic the Vault", "motive": "stale payload"})

    # The first divergence: if versions disagree, the vault is dirty before we even look at the entry.
    if observed_facts[0]["value"] != observed_facts[1]["value"]:
        verdict = {"status": "solved", "culprit": "Vic the Vault", "reason": "version mismatch"}
    elif observed_facts[2]["value"] != observed_facts[3]["value"]:
        verdict = {"status": "solved", "culprit": "Vic the Vault", "reason": "payload mismatch"}
    else:
        # No violated invariant. The case goes cold, and I don't fabricate a confession.
        verdict = {"status": "unresolved", "culprit": None, "reason": "no violated check"}

    # Missing evidence: if either ledger is silent, we can't pin the crime.
    if observed_facts[0]["value"] is None or observed_facts[1]["value"] is None:
        verdict = {"status": "unresolved", "culprit": None, "reason": "missing version evidence"}

    return {"verdict": verdict, "evidence": observed_facts, "hypotheses": hypotheses}

# The case file: a clean source, a dirty vault, and a witness who swears she saw nothing.
case_file = solve_the_case(
    {"source_version": 3, "vault_version": 2, "source_entry": "new", "vault_entry": "old"},
    {"witness": "The Night Clerk", "statement": "I only saw the shadows."}
)

# I've seen cleaner alibis. This one had a version stamp that didn't match.
print(case_file)