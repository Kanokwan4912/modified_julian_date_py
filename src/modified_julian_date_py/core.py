"""Core conversion logic for Modified Julian Dates."""

from datetime import datetime, timedelta, timezone

# The Modified Julian Date epoch is 1858-11-17T00:00:00Z.
# This is the standard definition used in satellite tracking: MJD = JD - 2400000.5.
_MJD_EPOCH = datetime(1858, 11, 17, tzinfo=timezone.utc)


def mjd_to_gregorian(mjd: float) -> datetime:
    """Convert a Modified Julian Date to a timezone-aware Gregorian datetime.

    Parameters
    ----------
    mjd : float
        The Modified Julian Date.  The value is interpreted as a real number
        of days since 1858-11-17T00:00:00Z.  Fractional days are supported.

    Returns
    -------
    datetime.datetime
        A timezone-aware datetime in UTC representing the same instant.

    Raises
    ------
    TypeError
        If *mjd* is not an int or float.
    OverflowError
        If the resulting date falls outside the range supported by
        :class:`datetime.datetime`.

    Notes
    -----
    The conversion is exact for values that are representable as a
    ``timedelta``.  Because ``timedelta`` has microsecond resolution, any
    fractional part of the day is rounded to the nearest microsecond.
    """
    if not isinstance(mjd, (int, float)):
        raise TypeError("mjd must be an int or float")
    if not isinstance(mjd, float):
        mjd = float(mjd)

    # timedelta accepts floats but internally rounds to microseconds.
    # We rely on that behaviour so that the result is deterministic and
    # matches the precision of datetime.
    return _MJD_EPOCH + timedelta(days=mjd)
