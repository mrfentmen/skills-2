from collections import deque
from threading import Condition, RLock

class QuiescentJobQueue:
    def __init__(self):
        self.state = {"version": 0, "config": None}
        self.queue = deque()
        self.deferred = deque()
        self.accepting = True
        self.running = 0
        self.lock = RLock()
        self.changed = Condition(self.lock)

    def emit(self, callback):
        with self.changed:
            (self.queue if self.accepting else self.deferred).append(callback)
            self.changed.notify_all()

    def drain(self):
        while True:
            with self.changed:
                while not self.queue and self.running:
                    self.changed.wait()
                if not self.queue and self.running == 0:
                    return
                callback = self.queue.popleft()
                self.running += 1
            try:
                callback()
            finally:
                with self.changed:
                    self.running -= 1
                    self.changed.notify_all()

    def swap_config(self, new_config):
        with self.changed:
            self.accepting = False
        self.drain()
        candidate = {"version": self.state["version"] + 1, "config": new_config}
        if candidate["config"] is None:
            raise ValueError("config cannot be None: old state remains published")
        with self.changed:
            assert not self.queue and self.running == 0
            assert candidate["version"] == self.state["version"] + 1
            self.state = candidate
            self.accepting = True
            self.queue.extend(self.deferred)
            self.deferred.clear()
            self.changed.notify_all()

    def run_ready(self):
        self.drain()

store = QuiescentJobQueue()
store.emit(lambda: store.emit(lambda: None))
store.swap_config({"workers": 4})
store.run_ready()
assert store.state == {"version": 1, "config": {"workers": 4}}
assert not store.deferred and not store.queue
print(store.state)