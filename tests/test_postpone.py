import unittest
from unittest.mock import MagicMock, patch
from datetime import date
from attendance_tracker import main

class TestPostpone(unittest.TestCase):
    def test_prompt_for_attendance_skip(self):
        # Mock click.prompt to return 's'
        with patch('click.prompt', return_value='s'), \
             patch('click.echo') as mock_echo:
            
            day = date(2026, 1, 5)
            subjects = ['Math']
            records = []
            holidays = []
            
            # Should return False
            result = main.prompt_for_attendance(day, subjects, records, holidays)
            
            self.assertFalse(result)
            # Ensure records were not modified
            self.assertEqual(len(records), 0)
            self.assertEqual(len(holidays), 0)

    def test_prompt_for_attendance_present(self):
        # Mock click.prompt to return 'p'
        with patch('click.prompt', return_value='p'), \
             patch('click.echo') as mock_echo:
            
            day = date(2026, 1, 5)
            subjects = ['Math']
            records = []
            holidays = []
            
            # Should return True
            result = main.prompt_for_attendance(day, subjects, records, holidays)
            
            self.assertTrue(result)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['status'], 'present')

if __name__ == '__main__':
    unittest.main()
