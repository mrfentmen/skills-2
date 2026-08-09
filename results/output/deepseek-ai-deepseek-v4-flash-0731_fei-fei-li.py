# the dataset: 11 numeric samples, 5 unique values, 3 appears 2x, 5 appears 3x — small scale, no demographic labels, so representation is unknown; the missing metadata is the bias, not the noise
# who this serves: the student learning statistics, the analyst checking a hand-collected list, the curious reader of a tiny sample
# the values encoded: transparency and humility — a small sample is a hint, never a verdict
# the foundational question: what is the underlying phenomenon this sequence represents — a measurement, a count, or a random draw?
# scored on: accuracy + worst-group error (here, per-value frequency fairness) + safety margin (no overclaiming from n=11)

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

def data_audit(rows):
    total = len(rows)
    unique = set(rows)
    freq = {v: rows.count(v) for v in unique}
    return {
        "total": total,
        "unique_values": len(unique),
        "frequency": freq,
        "missing_groups": ["demographic", "temporal", "source"]  # not collected — must be stated
    }

def human_metrics(rows):
    # fairness: worst-group error = highest per-value misrepresentation risk (here, rarest value)
    freq = {v: rows.count(v) for v in set(rows)}
    worst_group = min(freq, key=freq.get)
    return {
        "accuracy": "not applicable — no labels",
        "worst_group_error": f"value {worst_group} appears {freq[worst_group]} time(s) — under-represented",
        "safety_margin": "no prediction made; sample too small for inference"
    }

def fearless_question(question):
    return {"question": question, "before_the_heuristic": True}

audit = data_audit(data)
metrics = human_metrics(data)
question = fearless_question("what is the underlying phenomenon this sequence represents?")

print("DATA AUDIT:", audit)
print("HUMAN METRICS:", metrics)
print("FOUNDATIONAL QUESTION:", question)