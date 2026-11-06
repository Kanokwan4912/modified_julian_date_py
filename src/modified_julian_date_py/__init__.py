"""Modified Julian Date to Gregorian calendar conversion.

This package provides a single public function, :func:`mjd_to_gregorian`,
which converts a Modified Julian Date (MJD) into a Gregorian calendar date
and time.  The implementation is deliberately dependency-free and uses only
the Python standard library.
"""

from .core import mjd_to_gregorian

__all__ = ["mjd_to_gregorian"]
