import json

DATA = [
    {"service": "api", "status": "up"},
    {"service": "db", "status": "down"},
    {"service": "cache", "status": "up"}
]

# 1. Inspect the data set: confirm it is a list of dicts with 'service' and 'status' keys.
assert isinstance(DATA, list) and all(isinstance(item, dict) and "service" in item and "status" in item for item in DATA)

# 2. Plan:
#    a. Validate each record has a non-empty service name and a status of 'up' or 'down'.
#    b. Count services that are 'up' and 'down'.
#    c. Build a human-readable health report string.
#    d. Print the report.

# 3. Implement validation and counting.
up_services = []
down_services = []
for item in DATA:
    service = item["service"]
    status = item["status"]
    assert isinstance(service, str) and service.strip(), f"Invalid service name: {service!r}"
    assert status in ("up", "down"), f"Invalid status for {service}: {status!r}"
    if status == "up":
        up_services.append(service)
    else:
        down_services.append(service)

# 4. Build the report.
report_lines = []
report_lines.append(f"Total services: {len(DATA)}")
report_lines.append(f"Up: {len(up_services)} -> {', '.join(up_services) if up_services else 'none'}")
report_lines.append(f"Down: {len(down_services)} -> {', '.join(down_services) if down_services else 'none'}")
if down_services:
    report_lines.append("Health: DEGRADED")
else:
    report_lines.append("Health: OK")
report = "\n".join(report_lines)

# 5. Verify the computed counts against the actual data.
assert len(up_services) + len(down_services) == len(DATA)
assert up_services == ["api", "cache"]
assert down_services == ["db"]

# 6. Print the report.
print(report)

# Verification summary:
# - Tested: input structure validation, status validation, counting logic, and report string construction.
# - Verified: up_services == ['api', 'cache'], down_services == ['db'], total count matches.
# - Remains unverified: behavior with empty data, duplicate services, or non-string statuses (not present in the given data set).