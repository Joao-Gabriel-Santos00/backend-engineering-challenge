from collections import deque
from datetime import datetime, timedelta

class SlidingWindow:
    """
    This class maintains a queue of events and a running sum of their durations.
    """
    
    def __init__(self, window_size_minutes: int):
        self.window_size = timedelta(minutes=window_size_minutes)
        self.events = deque()
        self.current_sum = 0.0
        self.count = 0

    def add_event(self, timestamp: datetime, duration: float):
        """
        Adds a new event to the window and updates the running stats.
        """
        self.events.append((timestamp, duration))
        self.current_sum += duration
        self.count += 1

    def prune(self, current_time: datetime):
        """
        Removes events that have fallen out of the window relative to current_time.
        
        Args:
            current_time: The specific minute we are currently calculating for.
            Any event older than (current_time - window_size) is removed.
        
        """
        # Calculate the cutoff time. 
        limit = current_time - self.window_size
        
        # While the oldest event is older than the limit, remove it.
        while self.events and self.events[0][0] <= limit:
            _, duration = self.events.popleft()
            self.current_sum -= duration
            self.count -= 1

    def get_average(self) -> float:
        """
        Returns the moving average of the current window.
        """
        if self.count == 0:
            return 0.0
        return self.current_sum / self.count