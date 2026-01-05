import unittest
from unittest.mock import patch
from attendance_tracker import date
from datetime import date as datetime_date, timedelta
from attendance_tracker import logic

class TestLogic(unittest.TestCase):

    def test_calculate_attendance_percentage(self):
        records = [
            {"subject": "Math", "status": "present"},
            {"subject": "Math", "status": "present"},
            {"subject": "Math", "status": "absent"},
            {"subject": "Physics", "status": "present"},
        ]
        self.assertAlmostEqual(logic.calculate_attendance_percentage(records, "Math"), 66.666, places=2)
        self.assertEqual(logic.calculate_attendance_percentage(records, "Physics"), 100.0)
        self.assertEqual(logic.calculate_attendance_percentage(records, "Chemistry"), 100.0)

    @patch('attendance_tracker.logic.date')
    def test_get_missed_days_no_missed_days(self, mock_date):
        today = date(2026, 1, 6) # A Tuesday
        mock_date.today.return_value = today
        mock_date.fromisoformat.side_effect = datetime_date.fromisoformat
        yesterday = today - timedelta(days=1)
        missed_days = logic.get_missed_days(yesterday.isoformat(), [], yesterday.isoformat())
        self.assertEqual(len(missed_days), 0)

    @patch('attendance_tracker.logic.date')
    def test_get_missed_days_one_missed_day(self, mock_date):
        today = date(2026, 1, 7) # A Wednesday
        mock_date.today.return_value = today
        mock_date.fromisoformat.side_effect = datetime_date.fromisoformat
        two_days_ago = today - timedelta(days=2) # Monday
        missed_days = logic.get_missed_days(two_days_ago.isoformat(), [], two_days_ago.isoformat())
        self.assertEqual(len(missed_days), 1)
        self.assertEqual(missed_days[0], date(2026, 1, 6))

    @patch('attendance_tracker.logic.date')
    def test_get_missed_days_no_missed_days_since_start(self, mock_date):
        today = date(2026, 1, 5) # A Monday
        mock_date.today.return_value = today
        mock_date.fromisoformat.side_effect = datetime_date.fromisoformat
        start_date = date(2026, 1, 5) # A Monday
        missed_days = logic.get_missed_days(start_date.isoformat(), [], start_date.isoformat())
        self.assertEqual(len(missed_days), 0)

    def test_calculate_classes_needed(self):
        records = [
            {"subject": "Math", "status": "present"},
            {"subject": "Math", "status": "present"},
            {"subject": "Math", "status": "absent"},
            {"subject": "Math", "status": "absent"},
        ]
        self.assertEqual(logic.calculate_classes_needed(records, "Math"), 4)

        records_good_attendance = [
            {"subject": "Physics", "status": "present"},
            {"subject": "Physics", "status": "present"},
            {"subject": "Physics", "status": "present"},
            {"subject": "Physics", "status": "absent"},
        ]
        self.assertEqual(logic.calculate_classes_needed(records_good_attendance, "Physics"), 0)

if __name__ == '__main__':
    unittest.main()
