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
    Indicates whether we're in a phone menu or not. This is useful when a button is used in a phone screen that's used both in-game and through the ``PhoneMenu`` action (for instance, the ``Back`` button is disabled during a phone discussion). As it is set by ``phone.call_screen``, this variable should be read-only.

*The* **PhoneReturn** *and* **PhoneMenu** *actions are available in the global store. If their values are overridden during init phase, an error is raised.*