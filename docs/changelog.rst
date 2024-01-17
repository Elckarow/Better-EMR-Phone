Changelog
=========

*See* ``Incompatible Changes`` *for additional information.*

A list of all the changes throughout the versions, starting from 3.0.0.

3.2.2
-----

* The ``phone call`` statement can now take a ``nosave`` clause.
* Added new default emojis.
* 4 new functions ``phone.asset``, ``phone.path_join``, ``phone.short_name`` and ``phone.execute_default``.
* ``GroupChat.short_name`` and ``Character.short_name`` are now deprecated. See the new ``phone.short_name`` function.
* Reworked a bit the ``phone_contacts`` screen.
* Reset the yadjustment when starting a phone discussion.
* 7 new phone config variables.
* Fixed an issue where changes applied to a calendar would persist when going back to the main menu.

3.2.1
-----

* Checks for the correct version before appending to ``config.detached_layers``.

3.2.0
-----

* Group chats can now be transient. A transient group chat will be cleared once a discussion is over.
* Added video phone calls.
* A battery level of 0% will now display an empty battery (as it should).
* Added the ``pause`` phone discussion statement.
* Can now start a phone discussion when another discussion is going on.

3.1.1
-----

* Clearer error messages when a group chat / phone character isn't defined.
* Document some GUI variables.
* Phone definitions will now work on an already existing save. Before, if you had a save where no group chat was defined (this is just an example), that you created a group chat, and then loaded that save, the group chat wouldn't be registered. This change replicates the behavior of the ``default`` statement, allowing creators to, for instance, add this framework to an already released game. After loading the save, rollback will be blocked in such cases.
* Fixed an issue where running ``PhoneMenu`` during an interaction would block the player from advancing after returning.

3.1.0
-----

* Improved lint.
* ``phone.discussion.date`` and ``phone.discussion.register_date`` now accept ``None`` and ``True`` values (before, only the ``date`` phone statement could use ``None`` values).
* ``phone.discussion.date`` and ``phone.discussion.register_date`` now accept two new arguments: ``second`` and ``auto``.
* The ``image`` phone statement and ``phone.discussion.image`` can now take any displayable.
* Fixed an issue with ``gui.phone_message_label_null_height``.
* Added ``phone.config.discussion_callbacks``.

3.0.3
-----

* Fixed the ``calendar`` app layout.

3.0.2
-----

* Fixed the ``pass`` phone discussion statement.

3.0.1
-----

* Phone messages now respect the ``delay`` property.
* Phone labels can now accept ``None`` values.
* The audio icon in the status bar now uses ``preferences.get_mixer`` on 7.6/8.1+ and ``preferences.get_volume`` on other Ren'Py versions.
* A new function has been introduced to the ``phone.character`` namespace: ``get_all()``.
* A new function has been introduced to the ``phone.group_chat`` namespace: ``get_all()``.

3.0.0
-----

* None