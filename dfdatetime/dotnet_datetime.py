# -*- coding: utf-8 -*-
""".NET DateTime implementation."""

import decimal

from dfdatetime import definitions
from dfdatetime import factory
from dfdatetime import interface


class DotNetDateTimeEpoch(interface.DateTimeEpoch):
  """.NET DateTime epoch."""

  def __init__(self):
    """Initializes a .NET DateTime epoch."""
    super(DotNetDateTimeEpoch, self).__init__(1, 1, 1)


class DotNetDateTime(interface.DateTimeValues):
  """.NET DateTimetimestamp

  The .NET DateTime timestamp is a 64-bit signed integer that
  stores the date and time as the number of 100 nanosecond intervls since
  12:00 AM January 1, year 1 A.D. in the proleptic Gregorian Calendar.


  """
  _EPOCH = DotNetDateTimeEpoch()


  # The difference between January 1, 0001 and January 1, 1970 in seconds.
  _DOTNET_TO_POSIX_BASE =  (
      ((1969 * 365) + (1969 // 4) - (1969 // 100) + (1969 // 400)) *
      definitions.SECONDS_PER_DAY)


  def __init__(self, timestamp=None):
    super(DotNetDateTime, self).__init__(time_zone_offset=0)
    self._precision = definitions.PRECISION_100_NANOSECONDS
    self._timestamp = timestamp or 0

  @property
  def timestamp(self):
    """integer: .NET DateTime timestamp or None if not set."""
    return self._timestamp

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """
    if self._normalized_timestamp is None:
      if self._timestamp is not None:
        self._normalized_timestamp = (
            decimal.Decimal(self._timestamp) / self._100NS_PER_SECOND)
        self._normalized_timestamp -= self._DOTNET_TO_POSIX_BASE

        if self._time_zone_offset:
            self._normalized_timestamp -= self._time_zone_offset * 60

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a .NET DateTime timestamp from a string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get('year', 0)
    month = date_time_values.get('month', 0)
    day_of_month = date_time_values.get('day_of_month', 0)
    hours = date_time_values.get('hours', 0)
    minutes = date_time_values.get('minutes', 0)
    seconds = date_time_values.get('seconds', 0)
    microseconds = date_time_values.get('microseconds', None)
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    if year > 9999:
      raise ValueError('Unsupported year value: {0:d}.'.format(year))

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    timestamp += self._DOTNET_TO_POSIX_BASE
    timestamp += definitions.MICROSECONDS_PER_SECOND
    timestamp += microseconds
    timestamp += self._100NS_PER_MICROSECOND

    self._normalized_timestamp = None
    self._timestamp = timestamp
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the .NET DateTime timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp is missing.
    """
    if (self._timestamp is None or self._timestamp < 0 or
        self._timestamp > self._UINT64_MAX):
      return None

    timestamp, remainder = divmod(self._timestamp, self._100NS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:07d}'.format(
        year, month, day_of_month, hours, minutes, seconds, remainder)


factory.Factory.RegisterDateTimeValues(DotNetDateTime)
