Characters
==========

*The following functions and classes are defined in the* **phone.character** *namespace.*

The phone ``Character`` class
-----------------------------

``class Character(object)``
    Not to confuse with Ren'Py's ``Character`` objects (we're in the ``phone.character`` namespace remember), these objects form the core of the framework.

    When talking about a phone ``Character`` object, I will (most of the time) use this notation:

    ``*character*``

    which means the phone ``Character`` object itself or its ``key`` (you'll see what it is just below).

``def __init__(self, name, icon, key, cps, color)``

* ``name``: a string, the name of the character.
* ``icon``: a displayable.
* ``key``: any hashable object that is not ``None``. this must be a unique object proper to this phone ``Character`` object.
* ``cps``: an integer.
* ``color``: any valid color value.

Once the object has been created, the ``name``, ``icon`` and ``cps`` fields can be safely changed. The ``key`` and ``color`` fields are read-only.

``def get_textbox(self)``
    Returns a solid with rounded corners of the character's color and the radius given by ``phone.config.textbox_radius``.

``def is_pov(self)`` *(property)*
    Returns whether the character's key is equal to the store variable ``store.pov_key``.

``def get_typing_delay(self, message, substitute=True)``
    Returns a number of second this character would be typing out ``message`` (a string). If ``substitute`` is true, text substitution occurs before computing the time.

These objects are *hashable* (their key will be hashed).

**When creating a phone** ``Character`` **object, you must use** ``default`` **and not** ``define`` **.**

Functions
---------

``def character(x)``
    Returns the ``*character*`` ``x``. If ``x`` is a phone ``Character``, returns it, otherwise it is taken to be the key to a phone ``Character`` object and will return that object, or raise ``KeyError`` if no phone ``Character`` object has a key like this (if ``None`` is passed, ``store.pov_key`` is used).

``def has_character(key)``
    Returns true if there is a phone ``Character`` with the key ``key``, or fals if there is not.

``def get_textbox(color)``
    Returns a solid with rounded corners of color ``color`` and the radius given by ``phone.config.textbox_radius``.

``def get_all()``
    Returns a list of all phone ``Character`` objects defined.

Example
------- 
::

    # default /!\
    default p_eileen = phone.character.Character("Eileen", phone.asset("default_icon.png"), "eileen", 20, "#fff")
