import threading
from collections.abc import Callable
from typing import Dict


class AsyncService:
    def __init__(self):
        self.jobs: Dict[str, tuple[threading.Thread, threading.Event]] = {}
        self._lock = threading.Lock()

    def schedule_every(self, name: str, millis: int, do_job: Callable[[], None]):
        interval = millis / 1000.0
        stop_event = threading.Event()

        def loop():
            while not stop_event.is_set():
                try:
                    do_job()
                except Exception as e:
                    print(f"[{name}] job error:", e)
                if stop_event.wait(interval):
                    break

        thread = threading.Thread(target=loop, daemon=True)

        with self._lock:
            if name in self.jobs:
                self.kill(name)

            self.jobs[name] = (thread, stop_event)

        thread.start()
        return thread

    def kill(self, name: str):
        with self._lock:
            if name not in self.jobs:
                return
            thread, stop_event = self.jobs.pop(name)
            stop_event.set()

    def kill_all(self):
        with self._lock:
            for name, (thread, stop_event) in self.jobs.items():
                stop_event.set()
            self.jobs.clear()