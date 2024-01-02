Incompatible Changes
====================

A list of all changes that may require you to modify some of your code.

3.2.2
-----

* The ``phone.config`` and ``phone.emojis`` namespaces now behave the same way as renpy's ``config``. The ``default`` statement cannot be used to declare a variable in those namespaces.
* The ``phone.calendar.add_calendar`` and ``phone.calendar.add_calendar_to_all_characters`` functions have had their signature changed.

3.2.1
-----

* None

3.2.0
-----

* The ``Quit`` button in the ``phone`` screen has been removed in place of a dismiss-like button.
* The ``pass`` phone discussion statement now doesn't do anything, like a regular ``pass`` statement. To wait for a user input, see the ``pause`` phone discussion statement.

3.1.1
-----

* The ``phone register`` statement can't be ran during init phase anymore. Use the ``init phone register`` statement instead.
* ``auto`` can't be used anymore for the ``time`` statement in the ``init phone register`` statement.

3.1.0
-----

* None

3.0.3
-----

* None

3.0.2
-----

* None

3.0.1
-----

* None

3.0.0
-----

* Functions and classes related to phone characters have been moved in the ``phone.character`` namespace.
* Functions and classes related to group chats have been moved in the ``phone.group_chat`` namespace.