import re
from collections import Counter
from datetime import datetime

def musk_log_analyzer(log_str):
    # REQUIREMENTS QUESTIONED / JUSTIFIED
    # 1. "We need to parse timestamps" -> why? because logs have them. Physics: time is a dimension; we must extract it.
    # 2. "We need to count error codes" -> why? because errors are important. Physics: errors are discrete events; counting is fundamental.
    # 3. "We need to aggregate by hour" -> why? because logs are temporal. Physics: time is continuous; binning is a human convention we can simplify.
    # 4. "We need to support multiple log formats" -> why? because logs vary. Physics: logs are text; regex is a tool, not a requirement. We delete format flexibility to reduce complexity.
    # 5. "We need to output JSON" -> why? because it's conventional. Physics: text is the fundamental medium; JSON is a serialization overhead we can avoid.

    # NAIVE SOLUTION DELETED / SIMPLIFIED
    # Deleted: multi-format parser (e.g., JSON, CSV, custom). Reason: logs are fundamentally text; regex is sufficient. Cost: flexibility. Benefit: 0 deps, 10x less code.

    # PHYSICS-LEVEL FUNDAMENTALS
    # - Logs are sequences of characters with temporal ordering.
    # - Errors are discrete symbols (e.g., "ERROR", "CRITICAL").
    # - Time is a continuous variable we discretize for analysis.

    # TRADE-OFF NOTES
    # Sacrificed: multi-format support, real-time streaming, distributed processing.
    # Acceptable because: logs are small, static, and local. Physics: latency and weight (code size) are forces; we engineer against them.

    # SIMPLIFY THEN ACCELERATE
    # - Use stdlib only (re, Counter, datetime).
    # - No loops that never end: bounded regex passes over the log string.
    # - No external dependencies: physics doesn't require them.

    # Extract timestamps and errors using a single regex pass
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) .* (ERROR|CRITICAL)"
    matches = re.findall(pattern, log_str)

    # Physics: time is a dimension; we bin it into hours for analysis
    hour_counts = Counter()
    error_types = Counter()

    for ts, level in matches:
        # Parse timestamp once (physics: time is a fundamental constraint)
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        hour = dt.replace(minute=0, second=0, microsecond=0)
        hour_counts[hour] += 1
        error_types[level] += 1

    # Output: print raw counts (physics: the fundamental truth is the count)
    print("Hourly error counts:")
    for hour, count in sorted(hour_counts.items()):
        print(f"{hour}: {count}")

    print("\nError type counts:")
    for level, count in error_types.items():
        print(f"{level}: {count}")

# HARDCODED SAMPLE DATA (physics: the input is a given; we don't ask why)
log_data = """
2023-10-01 12:01:23 INFO System started
2023-10-01 12:05:45 ERROR Disk full
2023-10-01 12:30:12 CRITICAL Temperature high
2023-10-01 13:01:00 INFO System started
2023-10-01 13:05:45 ERROR Network timeout
2023-10-01 13:10:12 ERROR Permission denied
2023-10-01 14:01:00 INFO System started
"""

musk_log_analyzer(log_data)