from threading import Condition, RLock
from typing import Any, Callable, Deque
from collections import deque

class QuiescentConfig:
    def __init__(self, initial: dict[str, Any]):
        self.active: dict[str, Any] = initial.copy()
        self.candidate: dict[str, Any] | None = None
        self.queue: Deque[Callable[[], None]] = deque()
        self.deferred: Deque[Callable[[], None]] = deque()
        self.accepting: bool = True
        self.running: int = 0
        self.lock = RLock()
        self.changed = Condition(self.lock)

    def emit(self, callback: Callable[[], None]) -> None:
        with self.changed:
            (self.queue if self.accepting else self.deferred).append(callback)
            self.changed.notify_all()

    def drain(self) -> None:
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

    def swap_config(self, new_config: dict[str, Any]) -> None:
        with self.changed:
            self.accepting = False
        self.drain()
        candidate = new_config.copy()
        with self.changed:
            assert not self.queue and self.running == 0
            self.candidate = candidate
            self.active, self.candidate = self.candidate, None
            self.accepting = True
            self.queue.extend(self.deferred)
            self.deferred.clear()
            self.changed.notify_all()

    def run_ready(self) -> None:
        self.drain()

cfg = QuiescentConfig({"timeout": 5, "retries": 3})
cfg.emit(lambda: cfg.emit(lambda: None))
cfg.swap_config({"timeout": 10, "retries": 5})
cfg.run_ready()
assert cfg.active == {"timeout": 10, "retries": 5}
assert not cfg.deferred and not cfg.queue
print(cfg.active)