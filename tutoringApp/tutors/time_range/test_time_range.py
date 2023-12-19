import unittest
from datetime import datetime, timedelta

from .time_range import TimeRange


class TimeRangeTest(unittest.TestCase):
    """Tests for the TimeRange class and its methods."""

    def test_initialization_from_start_and_duration(self):
        start = datetime(2023, 12, 1, 8, 0)
        duration = timedelta(minutes=60)
        time_range = TimeRange.from_start_and_duration(start=start, duration=duration)

        self.assertEqual(time_range.start, datetime(2023, 12, 1, 8, 0))
        self.assertEqual(time_range.end, datetime(2023, 12, 1, 9, 0))

    def test_second_time_range_completly_contained_in_first_overlap_detected(self):
        first_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 8, 0), duration=timedelta(hours=2)
        )
        second_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 8, 30), duration=timedelta(hours=1)
        )

        self.assertTrue(second_time_range in first_time_range)

    def test_second_ranges_start_included_in_first_end_not_included_overlap_detected(
        self,
    ):
        first_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 8, 0), duration=timedelta(hours=1)
        )
        second_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 8, 30), duration=timedelta(hours=2)
        )

        self.assertTrue(second_time_range in first_time_range)

    def test_second_ranges_end_included_in_first_start_not_included_overlap_detected(
        self,
    ):
        first_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 8, 0), duration=timedelta(hours=1)
        )
        second_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 7, 30), duration=timedelta(hours=1)
        )

        self.assertTrue(second_time_range in first_time_range)

    def test_second_range_not_included_and_after_first_overlap_not_detected(self):
        first_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 8, 0), duration=timedelta(hours=1)
        )
        second_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 10, 0), duration=timedelta(hours=1)
        )

        self.assertFalse(second_time_range in first_time_range)

    def test_second_range_not_included_and_before_first_overlap_not_detected(self):
        first_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 10, 0), duration=timedelta(hours=1)
        )
        second_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 8, 0), duration=timedelta(hours=1)
        )

        self.assertFalse(second_time_range in first_time_range)

    def test_second_range_includes_first_one_overlap_not_detected(self):
        first_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 8, 30), duration=timedelta(hours=1)
        )
        second_time_range = TimeRange.from_start_and_duration(
            start=datetime(2023, 12, 1, 8, 0), duration=timedelta(hours=2)
        )

        self.assertFalse(second_time_range in first_time_range)
        self.assertTrue(first_time_range in second_time_range)


if __name__ == "__main__":
    unittest.main()
