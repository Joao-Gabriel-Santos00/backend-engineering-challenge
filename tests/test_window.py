import unittest
from datetime import datetime
from src.window import SlidingWindow

class TestSlidingWindow(unittest.TestCase):
    def setUp(self):
        self.window = SlidingWindow(window_size_minutes=10)

    def test_initial_state(self):
        """Test that a new window is empty."""
        self.assertEqual(self.window.get_average(), 0.0)
        self.assertEqual(self.window.count, 0)

    def test_math_calculation(self):
        """Test simple average calculation."""
        now = datetime(2021, 1, 1, 10, 0, 0)
        self.window.add_event(now, 10)
        self.window.add_event(now, 20)
        
        self.assertEqual(self.window.get_average(), 15.0)

    def test_pruning(self):
        """Test that old events are removed correctly."""
        t1 = datetime(2021, 1, 1, 10, 0, 0)
        self.window.add_event(t1, 100)
        
        current_time = datetime(2021, 1, 1, 10, 11, 0)
        self.window.prune(current_time)
        
        self.assertEqual(self.window.count, 0)
        self.assertEqual(self.window.get_average(), 0.0)

if __name__ == '__main__':
    unittest.main()