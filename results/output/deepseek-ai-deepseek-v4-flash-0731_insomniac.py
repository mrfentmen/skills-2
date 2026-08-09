class Job:
    def __init__(self, name, steps, fail_at=None):
        self.name, self.steps, self.progress = name, steps, 0
        self.fail_at = fail_at
        self.cancelled = False
        self.polls = 0

    def poll(self):
        if self.cancelled:
            return "cancelled"
        self.polls += 1
        if self.fail_at is not None and self.progress == self.fail_at:
            return "failed"
        if self.progress < self.steps:
            self.progress += 1
        return "ready" if self.progress == self.steps else "pending"

jobs = [Job("first", 3), Job("second", 5)]
budget = 20
statuses = {}
useful_work = 0
for round_number in range(budget):
    active = [job for job in jobs if job.name not in statuses and not job.cancelled and job.progress < job.steps]
    if not active:
        break
    for job in active:
        status = job.poll()
        useful_work += round_number + 1
        if status in {"ready", "failed"}:
            statuses[job.name] = status
for job in jobs:
    if job.cancelled:
        statuses[job.name] = "cancelled"
    elif job.name not in statuses:
        statuses[job.name] = "budget-exhausted"
assert statuses == {"first": "ready", "second": "ready"}
assert all(job.polls <= budget for job in jobs) and useful_work > 0
print({"statuses": statuses, "work": useful_work})