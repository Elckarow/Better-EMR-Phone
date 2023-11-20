Calendars
=========

*This one requires a bit more explaination.*

Loops over the list of calendars saved at ``phone.data[store.pov_key]["calendars"]`` and displays them.
A day passed is rendered with a gray background. 
A day that has a description has a ``?`` added in the top right.

Uses the ``phone_calendars`` screen.

The ``Calendar`` class
----------------------

*The following functions, variables and classes are defined in the* **phone.calendar** *namespace.*

``class Calendar(calendar.Calendar)``

``def __init__(self, month, year=2017, first_day=_default_first_day)``

* ``month`` A valid month from 1-12.
* ``year`` An integer.
* ``first_day`` An integer, one of the day constants described below.

``def is_day_passed(self, day)``
    Returns whether the day ``day`` of this calendar is passed, compared to ``phone.system.get_date``. ``day`` has to be a valid day (from 1 to whatever the last day is).

``def lenght(self, offsets=False)``
    If ``offsets`` is false, returns the number of days. If true, also returns the number of "out of range" days (take the 2023 June calendar for instance, the first 4 days and the last day are considered "out of range").

``def get_week_days(self)``
    Returns an generator iterating over the days of the week (that are strings, so ``"Monday"``, ``"Tuesday"``, ``etc...``).

These objects are *iterable*. Each iteration will either return ``None`` if it's an "out of range" day or will return an object that has the following fields:

* ``day`` The number of the day. Read-only.
* ``description`` If not ``None``, a string.

The dunder method ``__getitem__`` is also defined. It takes an integer, a valid day, and will return an object as described above, or raise an ``IndexError`` if it's not a valid day (``my_calendar[1]`` will return the first day object, ``my_calendar[0]`` will raise an ``IndexError``).

Functions and Variables
-----------------------

``days = (...)``
    A tuple containing strings corresponding to the week days name. The strings are flagged as translatable.

``months = (...)``
    A tuple containing strings corresponding to the months name (similar to ``calendar.month_name``, it follows normal convention of January being month number 1, so it has a length of 13 and ``months[0]`` is the empty string). The strings are flagged as translatable.

The constants ``MONDAY``, ``TUESDAY``, ``WEDNESDAY``, ``THURSDAY``, ``FRIDAY``, ``SATURDAY``, ``SUNDAY`` all represent a week day.

``def get_week_days(first_day=_default_first_day)``
    Returns an generator iterating over the days of the week (that are strings, so ``"Monday"``, ``"Tuesday"``, ``etc...``).

``def day_name(year, month, day)``
    Returns the day name of the corresponding date.

``def add_calendar(year, month, key=None, first_day=SUNDDAY)``
    Creates and adds a calendar to the list of calendars for the ``*character*`` ``key``.

``def add_calendar_to_all_characters(year, month, first_day=SUNDAY)``
    Same as above but for every ``*character*`` known at execution time.

``def get_calendar(year, month, key=None)``
    Returns the calendar for the ``*character*`` ``key`` that has the corresponding year and month number. ``None`` is returned if no such calendar was found.