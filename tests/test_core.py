import unittest
from datetime import datetime, timezone

from modified_julian_date_py import mjd_to_gregorian


class TestMjdToGregorian(unittest.TestCase):
    def test_epoch(self):
        # MJD 0 is the defined epoch.
        self.assertEqual(
            mjd_to_gregorian(0),
            datetime(1858, 11, 17, tzinfo=timezone.utc),
        )

    def test_positive_integer_day(self):
        # 1 day after epoch.
        self.assertEqual(
            mjd_to_gregorian(1),
            datetime(1858, 11, 18, tzinfo=timezone.utc),
        )

    def test_negative_integer_day(self):
        # 1 day before epoch.
        self.assertEqual(
            mjd_to_gregorian(-1),
            datetime(1858, 11, 16, tzinfo=timezone.utc),
        )

    def test_fractional_half_day(self):
        # 0.5 days after epoch is noon on the epoch date.
        self.assertEqual(
            mjd_to_gregorian(0.5),
            datetime(1858, 11, 17, 12, 0, 0, tzinfo=timezone.utc),
        )

    def test_fractional_quarter_day(self):
        # 0.25 days after epoch is 06:00.
        self.assertEqual(
            mjd_to_gregorian(0.25),
            datetime(1858, 11, 17, 6, 0, 0, tzinfo=timezone.utc),
        )

    def test_fractional_negative(self):
        # -0.25 days before epoch is 18:00 on the previous day.
        self.assertEqual(
            mjd_to_gregorian(-0.25),
            datetime(1858, 11, 16, 18, 0, 0, tzinfo=timezone.utc),
        )

    def test_microsecond_precision(self):
        # 1 microsecond is 1e-6 seconds = 1/86400e6 days.
        # This checks that sub-second precision is preserved.
        one_microsecond_in_days = 1.0 / (24 * 60 * 60 * 1_000_000)
        result = mjd_to_gregorian(one_microsecond_in_days)
        self.assertEqual(result.microsecond, 1)

    def test_known_mjd_2000_01_01(self):
        # MJD 51544 is 2000-01-01T00:00:00Z, a widely used reference point.
        self.assertEqual(
            mjd_to_gregorian(51544),
            datetime(2000, 1, 1, tzinfo=timezone.utc),
        )

    def test_known_mjd_2024_01_01(self):
        # MJD 60310 is 2024-01-01T00:00:00Z.
        self.assertEqual(
            mjd_to_gregorian(60310),
            datetime(2024, 1, 1, tzinfo=timezone.utc),
        )

    def test_type_error_on_string(self):
        with self.assertRaises(TypeError):
            mjd_to_gregorian("51544")

    def test_type_error_on_none(self):
        with self.assertRaises(TypeError):
            mjd_to_gregorian(None)

    def test_overflow(self):
        # A value far beyond the datetime range should raise OverflowError.
        with self.assertRaises(OverflowError):
            mjd_to_gregorian(1e12)

    def test_result_is_timezone_aware_utc(self):
        result = mjd_to_gregorian(51544)
        self.assertIsNotNone(result.tzinfo)
        self.assertEqual(result.utcoffset(), timezone.utc.utcoffset(None))


if __name__ == "__main__":
    unittest.main()
