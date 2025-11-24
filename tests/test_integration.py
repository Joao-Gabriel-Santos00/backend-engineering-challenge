import unittest
import os
import json
import tempfile
from io import StringIO
from unittest.mock import patch
from src.processor import process_stream

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        """ Create a temporary file for each test to avoid messing with real files """
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')

    def tearDown(self):
        """ Delete the temp file after test finishes """
        self.temp_file.close()
        os.remove(self.temp_file.name)

    def create_input_file(self, json_lines):
        """Helper to write lines to the temp file."""
        for line in json_lines:
            self.temp_file.write(line + '\n')
        self.temp_file.close()

    @patch('sys.stdout', new_callable=StringIO)
    def test_standard_flow(self, mock_stdout):
        """
        Tests the example scenario from the challenge README.
        Verifies that output is the same.
        """
        data = [
            '{"timestamp": "2018-12-26 18:11:08.509654", "duration": 20}',
            '{"timestamp": "2018-12-26 18:15:19.903159", "duration": 31}',
            '{"timestamp": "2018-12-26 18:23:19.903159", "duration": 54}'
        ]
        self.create_input_file(data)

        # Run the application
        process_stream(self.temp_file.name, window_size=10)

        # Capture output
        output_lines = mock_stdout.getvalue().strip().split('\n')
        results = [json.loads(line) for line in output_lines]

        # CHECK 1: Start Time
        self.assertEqual(results[0]['date'], "2018-12-26 18:11:00")
        self.assertEqual(results[0]['average_delivery_time'], 0.0)

        # CHECK 2: End Time
        last_entry = results[-1]
        self.assertEqual(last_entry['date'], "2018-12-26 18:24:00")
        self.assertEqual(last_entry['average_delivery_time'], 42.5)

        # CHECK 3: Total Line Count
        self.assertEqual(len(results), 14)

    @patch('sys.stdout', new_callable=StringIO)
    def test_single_event(self, mock_stdout):
        """
        Test with a file that has only one event.
        """
        data = ['{"timestamp": "2021-01-01 12:00:30.000000", "duration": 10}']
        self.create_input_file(data)

        process_stream(self.temp_file.name, window_size=10)

        output_lines = mock_stdout.getvalue().strip().split('\n')
        results = [json.loads(line) for line in output_lines]

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['date'], "2021-01-01 12:00:00")
        self.assertEqual(results[1]['date'], "2021-01-01 12:01:00")
        self.assertEqual(results[1]['average_delivery_time'], 10.0)

    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_file(self, mock_stdout):
        """
        File exists but is empty.
        """
        self.create_input_file([])

        try:
            process_stream(self.temp_file.name, window_size=10)
        except Exception as e:
            self.fail(f"Processing empty file raised an exception: {e}")

        # Output should be empty
        self.assertEqual(mock_stdout.getvalue().strip(), "")

if __name__ == '__main__':
    unittest.main()