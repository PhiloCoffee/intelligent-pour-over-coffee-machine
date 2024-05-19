# File: utilities/timer.py
import time

class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        """Start a new timer."""
        self.start_time = time.time()

    def elapsed(self):
        """Return the number of seconds since the timer was last started."""
        if self.start_time is None:
            raise RuntimeError("Timer not started")
        return time.time() - self.start_time

    def wait(self, seconds):
        """Wait for a specific number of seconds."""
        time.sleep(seconds)
