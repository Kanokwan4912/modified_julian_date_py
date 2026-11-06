# modified_julian_date_py

Convert satellite-tracking Modified Julian Dates (MJD) to timezone-aware Gregorian datetimes.

```python
from modified_julian_date_py import mjd_to_gregorian

# MJD 51544 is 2000-01-01T00:00:00Z.
dt = mjd_to_gregorian(51544)
print(dt)  # 2000-01-01 00:00:00+00:00

# Fractional days are supported.
dt = mjd_to_gregorian(51544.5)
print(dt)  # 2000-01-01 12:00:00+00:00
```

## Why this exists

Satellite tracking systems, TLEs, and orbital element sets frequently express
timestamps as Modified Julian Dates: a real number of days since
1858-11-17T00:00:00Z.  Python's standard library has no built-in MJD type,
and the usual workaround is to subtract the Julian Date offset (2400000.5)
and hope the floating-point arithmetic lands on the right day.

This library makes the single, explicit choice that MJD is measured from the
standard epoch 1858-11-17T00:00:00Z and returns a timezone-aware UTC
`datetime`.  It does not accept leap seconds, it does not guess a local
timezone, and it does not try to be a full Julian Date library.  The trade-off
is that sub-microsecond precision is lost because `datetime.timedelta` rounds
to microseconds; for satellite tracking this is far below the noise floor.

## The awkward edge

The fractional part of an MJD is a binary float, so values such as `0.1` are
not exact.  The conversion uses `timedelta`, which rounds to the nearest
microsecond, so the returned datetime is deterministic but may differ from an
exact rational calculation by up to half a microsecond.  If you need exact
rational arithmetic, do the conversion with `fractions.Fraction` before
calling this function.
