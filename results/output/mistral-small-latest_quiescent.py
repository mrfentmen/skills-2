from collections import deque
from threading import Condition, RLock

class QuiescentConfig:
    def __init__(self):
        self.active = {"version": 0, "settings": {}}
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

    def transition(self, settings):
        with self.changed:
            self.accepting = False
        self.drain()
        candidate = {"version": self.active["version"] + 1, "settings": dict(settings)}
        with self.changed:
            assert not self.queue and self.running == 0
            assert candidate["version"] == self.active["version"] + 1
            self.active = candidate
            self.accepting = True
            self.queue.extend(self.deferred)
            self.deferred.clear()
            self.changed.notify_all()

    def run_ready(self):
        self.drain()

store = QuiescentConfig()
store.emit(lambda: store.emit(lambda: None))
store.transition({"timeout": 30, "retries": 3})
store.run_ready()
assert store.active == {"version": 1, "settings": {"timeout": 30, "retries": 3}}
assert not store.deferred and not store.queue
print(store.active)