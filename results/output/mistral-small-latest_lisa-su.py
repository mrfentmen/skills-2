# Focus statement: # building: a minimal CLI tool for local file diffing. NOT building: GUI, cloud sync, multi-language support
# Roadmap commitment: # ships v0.2 on the 15th; risk: file locking on Windows, mitigated by exclusive read handles
# Next 5%: # next 5%: p95 diff time down 12ms via memory-mapped file reads
# Hardest problem first: # the bottleneck is the byte-level diff engine, not the CLI polish
# Postmortem: # postmortem: assumed POSIX file semantics; Windows lock contention added 40ms; measure OS-specific I/O first

def lisa_plan():
    plan = {
        "focus": ["minimal CLI tool", "local file diffing", "simplify everything"],
        "not_building": ["GUI", "cloud sync", "multi-language support"],
        "roadmap": {
            "deliverable": "v0.2 CLI diff tool",
            "date": "15th",
            "risk": "file locking on Windows",
            "mitigation": "exclusive read handles",
            "done": "passing unit tests, 100% diff accuracy on 1KB-1MB files"
        },
        "next_5_percent": {
            "metric": "p95 diff time",
            "improvement": "12ms reduction",
            "method": "memory-mapped file reads"
        },
        "hardest_problem": "byte-level diff engine",
        "postmortem": "assumed POSIX file semantics; Windows lock contention added 40ms; measure OS-specific I/O first"
    }
    return plan

print(lisa_plan())