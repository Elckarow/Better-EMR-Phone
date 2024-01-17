Functions and Actions
=====================

Utility Functions
-----------------

*The following functions, variables and Actions are defined in the* **phone** *namespace.*

``def format_date(month, day, year)``
    Returns a formatted string using ``phone.config.date_format``.

``def format_time(hour, minute)``
    Returns a formatted string using ``phone.config.time_format``.

``def show_layer_at(at_list, layer="master", camera=True, reset=False)``
    A wrapper around ``renpy.show_layer_at``. If ``at_list`` is a string (or ``None``), it is looked up in ``phone.config.layer_at_transform``. The transform or list of transforms is then passed to ``renpy.show_layer_at`` along with the other parameters.

``def short_name(s, length)``
    Shortens the string ``s`` after translating it. The string is sliced to ``length - 3`` and ``"..."`` is appended to it.

``def path_join(*args)``
    Computes *os.path.join(\*args).replace("\\\\", "/")*

``def asset(path)``
    Computes *path_join(phone.config.basedir, path)*

``def execute_default(f, id)``
    Mimics the behavior of the ``default`` statement by calling ``f`` if a function with the unique value ``id`` has never been called before.
    The function is added to ``config.start_callbacks`` and ``config.after_load_callbacks``, and in the latter case, if the function is called, rollback will be blocked.
    A good *unique value*, for instance, is a tuple where the first component is a string describing what the function does, and where the remaining components are the actual unique value related to whatever the function does.
    For example, when calling ``phone.calendar.add_calendar`` during init phase, this function is called with the unique value ``("_phone_add_calendar", month, year, key)``, where ``month``, ``year`` and ``key`` are the values passed to ``phone.calendar.add_calendar``.

``data = {...}``
    The dictionnary that's storing all of the phone's in-game data. Each ``*character*`` has an entry (their key) in this dict and will return another dictionnary as described in ``phone.config.data``.

Screen Functions and Actions
----------------------------

``class PhoneMenu(Action)``
    The framework's equivalent of the ``ShowMenu`` action. 
    Arguments given are passed to the ``phone.call_screen`` function.

``def call_screen(_screen_name, *args, **kwargs)``
    The framework's equivalent of the ``renpy.call_screen`` function.
    Invokes ``renpy.call_screen`` in a new context, passing all arguments and keyword arguments to it. This ensures a sort of "depths" effect (going to screen A, then screen B, then screen C, returning brings you back to screen B, and so on).

``def PhoneReturn(value=None)``
    The framework's equvalent of the ``Return`` action. It should be used to return from a phone screen.

``menu = False``
    Indicates whether we're in a phone menu or not. This is useful when a button is used in a phone screen that's used both in-game and through the ``PhoneMenu`` action (for instance, the ``Back`` textbutton in the ``phone_discussion`` is disabled during a phone discussion). As it is set by ``phone.call_screen``, this variable should be read-only.

*The* **PhoneReturn** *and* **PhoneMenu** *actions are available in the global store. If their values are overridden during init phase, an error is raised.*