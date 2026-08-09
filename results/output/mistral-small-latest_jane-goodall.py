import json
from datetime import datetime, timedelta
from collections import defaultdict

# Observation plan:
# Watch the "event-logger" service for 30 days in production, not 10 minutes in staging.
# Conditions: real user traffic, no synthetic load, capture all events with timestamps.

# Named individual:
# "event-logger" has a history: high latency spikes at 10am since the March 15 deploy.
# It processes 1200 events/hour on average, with peaks at 1400 during business hours.

# Challenged assumption:
# Everyone assumes the database is the bottleneck; the logs say otherwise.
# The evidence trail shows CPU saturation during peak hours, not disk I/O.

# Evidence trail:
# 2026-08-01T10:00:00Z latency=1250ms, cpu=98%, events=1420
# 2026-08-01T10:15:00Z latency=1310ms, cpu=99%, events=1450
# 2026-08-02T10:00:00Z latency=1280ms, cpu=97%, events=1410
# 2026-08-03T10:00:00Z latency=1270ms, cpu=98%, events=1430

# Patient-action note:
# One page of monitoring per week; in a quarter the system is visible.
# Start with 5-minute granularity, then refine to 1-minute during peak hours.

def generate_field_notes(days=30):
    # Simulate sustained observation over 30 days
    start_date = datetime(2026, 8, 1)
    event_logger = {
        "name": "event-logger",
        "deploy_date": "2026-03-15",
        "avg_events_per_hour": 1200,
        "peak_events_per_hour": 1400,
        "latency_history": [],
        "cpu_history": [],
        "event_history": []
    }

    observations = []
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        for hour in range(24):
            # Simulate peak at 10am
            if hour == 10:
                latency = 1250 + (day % 3) * 30
                cpu = 97 + (day % 2)
                events = 1400 + (day % 5) * 10
            else:
                latency = 200 + (day % 7) * 10
                cpu = 30 + (day % 10)
                events = 800 + (day % 15) * 20

            timestamp = current_date.replace(hour=hour, minute=0, second=0, microsecond=0).isoformat() + "Z"
            observations.append({
                "timestamp": timestamp,
                "service": event_logger["name"],
                "latency_ms": latency,
                "cpu_percent": cpu,
                "events_processed": events,
                "deploy_age_days": (current_date - datetime.strptime(event_logger["deploy_date"], "%Y-%m-%d")).days
            })

    # Evidence analysis
    peak_observations = [o for o in observations if o["timestamp"].endswith("10:00:00Z")]
    cpu_values = [o["cpu_percent"] for o in peak_observations]
    latency_values = [o["latency_ms"] for o in peak_observations]

    challenged_assumption = (
        "Database is the bottleneck during peak hours. "
        "Evidence shows CPU saturation (avg 98%) with stable event processing rates."
    )

    patient_action = (
        "Collect 5-minute granularity metrics for 4 weeks. "
        "Then refine to 1-minute during 9-11am window to identify micro-spikes."
    )

    field_notes = {
        "observation_plan": (
            "Watch 'event-logger' service for 30 days in production. "
            "Capture all events with 5-minute granularity. "
            "Focus on 9-11am window where latency spikes occur."
        ),
        "named_individual": event_logger,
        "challenged_assumption": challenged_assumption,
        "evidence_trail": peak_observations[:3],  # Show first 3 days as evidence
        "patient_action": patient_action,
        "summary": {
            "days_observed": days,
            "avg_peak_cpu": sum(cpu_values) / len(cpu_values),
            "avg_peak_latency": sum(latency_values) / len(latency_values),
            "deploy_age_at_end": observations[-1]["deploy_age_days"]
        }
    }

    return field_notes

field_notes = generate_field_notes()
print(json.dumps(field_notes, indent=2))