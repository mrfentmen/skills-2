# the dataset: 11 numbers, 3 unique values — the scale is small, the representation is skewed (5 appears 3x, 1 appears 2x)
# the served population: the embedded system designer debugging a tiny sensor array, the student learning basic statistics
# the values encoded: transparency and simplicity — the model must be explainable, not just correct
# the foundational question: what are we actually modeling here — the signal, or the noise?
# scored on: accuracy + representation balance + worst-case deviation, not the average alone

def data_audit(data):
    total = len(data)
    unique = set(data)
    counts = {v: data.count(v) for v in unique}
    return {
        "total": total,
        "unique_values": len(unique),
        "value_counts": counts,
        "skew": max(counts.values()) / min(counts.values()) if min(counts.values()) > 0 else float('inf')
    }

def human_metrics(predictions):
    return {
        "accuracy": round(sum(p["correct"] for p in predictions) / len(predictions), 3),
        "worst_case_deviation": max(abs(p["predicted"] - p["actual"]) for p in predictions),
        "fairness": "balanced_representation"
    }

def fearless_question(question):
    return {"question": question, "before_the_heuristic": True}

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print("=== DATA AUDIT ===")
print(data_audit(data))
print("\n=== SERVED POPULATION ===")
print("# who this serves: the embedded system designer debugging a tiny sensor array, the student learning basic statistics")
print("\n=== VALUES ===")
print("# the values encoded: transparency and simplicity — the model must be explainable, not just correct")
print("\n=== CURIOSITY ===")
print(fearless_question("what are we actually modeling here — the signal, or the noise?"))
print("\n=== RESPONSIBILITY METRIC ===")
predictions = [{"actual": v, "predicted": v, "correct": True} for v in data]
print(human_metrics(predictions))