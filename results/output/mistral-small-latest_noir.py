def crack_the_case(ledger, suspect_ledger):
    # The ledger is the truth, cold and unfeeling. The suspect_ledger is the liar's tale, warm and full of holes.
    evidence = []
    the_missing_credit = ledger.get("credit")
    the_claimed_credit = suspect_ledger.get("credit")
    evidence.append({"fact": "ledger_total", "value": ledger.get("total")})
    evidence.append({"fact": "suspect_total", "value": suspect_ledger.get("total")})
    evidence.append({"fact": "ledger_credit", "value": the_missing_credit})
    evidence.append({"fact": "suspect_credit", "value": the_claimed_credit})

    # I've seen ledgers with more integrity than this suspect's alibi.
    if suspect_ledger.get("total") != ledger.get("total"):
        verdict = {"status": "solved", "culprit": "suspect_ledger", "reason": "total mismatch"}
    elif the_claimed_credit != the_missing_credit:
        verdict = {"status": "solved", "culprit": "suspect_credit", "reason": "credit mismatch"}
    elif suspect_ledger.get("total") is None or ledger.get("total") is None:
        verdict = {"status": "unresolved", "culprit": None, "reason": "missing total evidence"}
    elif the_missing_credit is None or the_claimed_credit is None:
        verdict = {"status": "unresolved", "culprit": None, "reason": "missing credit evidence"}
    else:
        verdict = {"status": "unresolved", "culprit": None, "reason": "no violated check"}

    return {"verdict": verdict, "evidence": evidence}

case_file = crack_the_case(
    {"total": 1000, "credit": 200},
    {"total": 900, "credit": 200},
)
print(case_file)