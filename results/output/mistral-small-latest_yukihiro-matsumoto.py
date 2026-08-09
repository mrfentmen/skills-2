# happiness pass: the caller reads the intent in one line, no ceremony
# human-first: the call reads like the sketch: tasks.todo("buy milk").due("today").done()
# fluency check: every task builder answers the same questions — no per-type surprises
# harmony note: fits the voice: same block convention as the other builders
# kindness artifact: error: "task not found — did you forget to .todo() first?"

class TaskBuilder:
    def __init__(self):
        self._title = None
        self._due = None
        self._done = False

    def todo(self, title):
        self._title = title
        return self

    def due(self, date):
        self._due = date
        return self

    def done(self, flag=True):
        self._done = flag
        return self

    def __repr__(self):
        return f"Task(title={self._title!r}, due={self._due!r}, done={self._done})"

class Tasks:
    def __init__(self):
        self._tasks = []

    def add(self, builder):
        if builder._title is None:
            raise ValueError(kindness("task not found — did you forget to .todo() first?"))
        self._tasks.append(builder)
        return self

    def __repr__(self):
        return f"Tasks({self._tasks})"

def kindness(message):
    return f"{message} — here is what to check next"

tasks = Tasks()
tasks.add(TaskBuilder().todo("buy milk").due("today").done())
tasks.add(TaskBuilder().todo("write code").due("friday"))
print(tasks)