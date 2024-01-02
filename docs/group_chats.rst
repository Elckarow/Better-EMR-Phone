Group Chats
===========

*The following functions and classes are defined in the* **phone.group_chat** *namespace.*

The ``GroupChat`` class
-----------------------

``class GroupChat(object)``
    The core of the discussion part of this framework.

``def __init__(self, name, icon, key, transient=False)``

* ``name``: a string, the name of the character.
* ``icon``: a displayable.
* ``key``: any hashable object that is not ``None``. this must be a unique object proper to this ``phone.group_chat.GroupChat`` object.
* ``transient``: a boolean. If true, the group chat is cleared once the discussion is over.

Once created, the following fields can be read and safely modified:

* ``name``
* ``icon``

while following fields should be read only:

* ``unread``
* ``date``
* ``transient``

``def add_character(self, char)``
    Adds the ``*character*`` ``char`` to this group chat, saves the group chat in the ``*character*``'s list of known group chats, and returns the group chat.

``def remove_character(self, char)``
    Removes the ``*character*`` ``char`` from this group chat, and removes the group chat from the ``*character*``'s known group chats.

``def number_of_messages_sent(self, char)``
    Returns the number of messages sent by the ``*character*`` ``char``. If ``None`` is passed, returns the total number of messages sent.

``def clear(self)``
    Clears the group chat's history.

These objects are *hashable* (their key will be hashed).

Functions
---------

``def group_chat(x)``
    If ``x`` is a ``phone.group_chat.GroupChat`` object, will return that object, otherwise, the group chat with the same key will be returned, or raise a ``KeyError`` if it wasn't found.

``def has_group_chat(key)``
    Returns if a group chat with the key ``key`` exists.

``def get_all()``
    Returns a list of every group chats defined.

Example
-------
::

    # default /!\
    default eileen_gc = phone.group_chat.GroupChat("Eileen", phone.asset("default_icon.png"), "eileen_gc").add_character("eileen")

or use the ``define`` clause of the ``init phone register`` statement. ::

    init phone register:
        define "Hello":
            icon "icon.png" add "eileen" key "hello"