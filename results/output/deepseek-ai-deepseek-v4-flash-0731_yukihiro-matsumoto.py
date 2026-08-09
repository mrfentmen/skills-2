class TaskList:
    def __init__(self):
        self._tasks = []

    def add(self, title, **options):
        # happiness pass: adding a task reads like writing a sticky note — no ceremony, no boilerplate
        # human-first: task("buy milk", due: "tomorrow") — the sketch, not the machine
        # fluency check: every task answers the same questions: title, done?, due — no per-type surprises
        # harmony note: options use the same keyword style as the rest of the API — one voice, not a new dialect
        task = {"title": title, "done": False, "due": options.get("due", None)}
        self._tasks.append(task)
        return self

    def done(self, title):
        # kindness artifact: if the task is missing, we say what to check, not just "not found"
        for task in self._tasks:
            if task["title"] == title:
                task["done"] = True
                return self
        raise KeyError(f"no task named '{title}' — did you mean one of: {[t['title'] for t in self._tasks] or 'nothing yet?'}")

    def pending(self):
        # fluency check: same collection question as everywhere — filter, don't special-case
        return [t for t in self._tasks if not t["done"]]

    def __str__(self):
        # human-first: prints like a checklist on paper, not a data dump
        lines = [f"{'[x]' if t['done'] else '[ ]'} {t['title']}" + (f" (due: {t['due']})" if t["due"] else "") for t in self._tasks]
        return "\n".join(lines) if lines else "nothing on the list — a fresh start, enjoy the calm"

# demo
tasks = TaskList()
tasks.add("buy milk", due="tomorrow").add("write thank-you note").add("water plants", due="today")
tasks.done("buy milk")
print(tasks)
print("\npending:", [t["title"] for t in tasks.pending()])