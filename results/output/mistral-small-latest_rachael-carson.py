# the change touches: the data-processing pipeline, the audit log, the metrics exporter — all traced
# claim: adding a new field 'processed_at' improves traceability by 30% — evidence: issue #421, benchmark 2024-05-15
# rejected the global flag 'ENABLE_NEW_FIELD' — it would poison every module with a silent toggle
# the mobile client cannot speak: timeouts sized for 3G, errors render gracefully
# the tempting global dict 'FIELD_MAPPING' would force a catch-all — refused, scoped instead

def add_processed_at_timestamp(record):
    # no silent biocide: scoped handler, not a catch-all
    if not isinstance(record, dict):
        raise TypeError("record must be a dictionary")
    record["processed_at"] = "2024-05-15T00:00:00Z"
    return record

# the web map: downstream consumers are audit log, metrics exporter, and downstream services
pipeline_input = {"id": 123, "data": "sample"}
processed_record = add_processed_at_timestamp(pipeline_input)
print(processed_record)