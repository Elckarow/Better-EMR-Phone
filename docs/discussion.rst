Discussion
==========

*probably the longest part of the doc have fun*

Functions
---------

*The following functions and variables are defined in the* **phone.discussion** *namespace.*

``def remove_text_tags(s)``
    Formats the ``emoji`` text tag in ``s`` according to ``phone.emojis.format_emoji_tag`` and removes all other text tags.

``def discussion(gc)``
    Starts a discussion with the ``*group chat*`` ``gc``. If ``None`` is passed, the current group chat is used.
    The python equivalent of the ``phone discussion`` statement.

``def end_discussion()``
    Ends the current discussion.
    The python equivalent of the ``phone end discussion`` statement.

``def message(sender, message, delay=None)``
    Sends a message by the ``*character*`` ``sender`` to the current group chat. Text tags should not be used.
    Pauses for ``delay`` seconds after the message's been saved.
    The python equivalent of the default discussion statement.

``def image(sender, image, time=2.0, delay=None)``
    Sends an image by the ``*character*`` ``sender`` to the current group chat. ``time`` is the time the image is being sent for.
    The python equivalent of the ``image`` discussion statement.

``def label(label, delay=0.5)``
    Adds a label to the current group chat.
    The python equivalent of the ``label`` discussion statement.

``def date(month, day, year, hour, minute, second, delay=0.5, auto=False)``
    Adds a date as label to the current group chat. The date is saved to the group chat using ``datetime.datetime``. If any of these values are ``None``, they are taken from the currently saved date. If any of these values are ``True``, they are taken from the date returned by ``phone.system.get_date()``. If ``auto`` is true, sets every values to ``True``.
    The python equivalent of the ``time`` discussion statement.

``def typing(sender, value, delay=None)``
    Simulates the ``*character*`` ``sender`` typing for ``value`` seconds. If ``value`` is a string, ``sender.get_typing_delay`` is called.
    The python equivalent of the ``type`` discussion statement.

``def choice(captions, delay=0.3)``
    Causes a choice to occur inside the phone, and returns the caption that has been chosen. ``captions`` is a list of strings.
    The python equivalent of the ``menu`` discussion statement.

``def audio(sender, audio, time=2.0, delay=None)``
    Sends an audio by the ``*character*`` ``sender`` to the current group chat. ``time`` is the time the audio is being sent for.

``def register_message(group, sender, text)``
    Saves a message sent by the ``*character*`` ``sender`` in the ``*group chat*`` ``group``.
    This is called automatically by the ``phone.discussion.message`` function.
    The python equivalent of the default register statement.

``def register_image(group, sender, image)``
    Saves an image sent by the ``*character*`` ``sender`` in the ``*group chat*`` ``group``.
    This is called automatically by the ``phone.discussion.image`` function.
    The python equivalent of the ``image`` register statement.

``def register_label(group, label)``
    Saves a label in the ``*group chat*`` ``group``.
    This is called automatically by the ``phone.discussion.label`` function.
    The python equivalent of the ``label`` register statement.

``def register_date(group, month, day, year, hour, minute, second, auto=False)``
    Saves a date in the ``*group chat*`` ``group``.
    This is called automatically by the ``phone.discussion.date`` function.
    The python equivalent of the ``time`` register statement.

``def register_audio(group, sender, audio)``
    Saves an audio sent by the ``*character*`` ``sender`` in the ``*group chat*`` ``group``.
    This is called automatically by the ``phone.discussion.audio`` function.
    The python equivalent of the ``audio`` register statement.

``def sort_messages(key)``
    Sorts the group chats of the ``*character*`` ``key`` in descending order according to their last registered date.

The statements
--------------

The framework comes with its load of custom statements aiming at making it easier to use.

The discussion statements
^^^^^^^^^^^^^^^^^^^^^^^^^

``phone discussion``
    Used to start a phone discussion.
    If a simple expression is given, it must be a ``*group chat*``.
    If no simple expression is given (or that ``None`` is given), it's assumed that a discussion is already going on, and will therefore use the current group chat.

    If a block is given, the following statements can be used:

    * `` ``
        The default statement, equivalent of the ``phone.discussion.message`` function.
        It expects a ``*character*`` and a string (flagged as translatable).
        It accepts the ``delay`` property (defaults to ``None``) which is the time to wait before the next statement executes. A ``None`` delay will wait for user input. A negative value delay won't wait.

    * ``image`` 
        The equivalent of the ``phone.discussion.image`` function.
        It expects a ``*character*`` and a simple expression (the image).
        It accepts the ``time`` property (defaults to ``2.0``), which is the time the image is being sent for.

    * ``label``
        The equivalent of the ``phone.discussion.label`` function.
        It expects a string (the string is flagged as being translatable).
        It also accepts the ``delay`` property (defaults to ``0.5``).
    
    * ``time``
        The equivalent of the ``phone.discussion.date`` function.
        It expects at least one of the following property; ``year``, ``month``, ``day``, ``hour``, ``minute``, ``second``; which can be a number, ``None`` or ``True``, as well as the ``auto`` property.
        If one of these is missing, it is retrieved from the current date registered.
        It also accepts the ``delay`` property (defaults to 0.5).
    
    * ``type``
        The equivalent of the ``phone.discussion.typing`` function.
        It expects a ``*character*`` and a ``value`` property, which can be a number or a string.
        The string is NOT flagged as translatable.
        It also accepts the ``delay`` property (defaults to ``None``).
    
    * ``if/elif/else``
        Does exactly what you'd expect from this statement.

    * ``menu``
        The equivalent of the ``phone.discussion.choice`` function.
        It expects a block which can contain the following:
        The ``delay`` property, which has to be given before the menu items (defaults to ``0.3``).
        A series of menuitems. A menuitem is a string (flagged as translatable) which may be followed by an ``if`` clause and a simple expression. If the expression is false, the choice won't appear. The line ends with a colon ``:`` and must be followed by a block that contains any of the phone discussion statements.
    
    * ``$``
        The one-line python statement.
        Executes code in the global store.
    
    * ``python``
        Works the same way as the normal ``python`` statement except for one thing:
        If the ``in`` clause is given, the substore is created at init 0, unlike the regular ``python`` statement which does it at early time.
    
    * ``pass``
        Does nothing.
    
    * ``pause``
        Same as the regular ``pause`` statement.

    If no block is given, it behaves as if a single ``pass`` statement was given.

``phone end discussion``
    Used to end a phone discussion.
    It doesn't expect anything.

The register statements
^^^^^^^^^^^^^^^^^^^^^^^

``phone register``
    Used to register messages in a group chat.
    It expects a ``*group chat*`` and a block (see the part above).
    It doesn't accept the ``type``, ``menu``, ``$`` nor ``python`` statements, nor the properties related to time (``delay``, ``time``, ``cps`` ...).

``init phone register``
    Used to register messages in a group chat at init time and / or create a new group chat.
    The statement is run at init priority 700.

    If a ``*group chat*`` is given, it behaves the same way as the ``phone register`` statement.
    If no ``*group chat*`` is given, the block expects a ``define`` clause.

    The ``define`` clause expects a string, the name of the group chat, and a block which can contain the following statements:

    * ``add``
        Expects a ``*character*``. Will add this ``*character*`` to the group chat when created.
    
    * ``key``
        Expects a simple expression. The key of the group chat.
    
    * ``icon``
        Expects a displayable. The icon of the group chat.
    
    * ``as``
        Expects a dotted name. The group chat will be saved in the global store under this name (as if the group chat was manually created using the ``default`` statement).

    * ``transient``
        Optional. If present, the group chat becomes transient. Transient group chats are cleared once the discussion is over.

Example
-------

::

    # create two phone Character objects
    default phone_sayori = phone.character.Character("Sayori", phone.asset("sayori_icon.png"), "s", 21,   "#22Abf8")
    default phone_mc = phone.character.Character("MC", phone.asset("mc_icon.png"), "mc", 35, "#484848")

    # create a group chat manually
    default mc_sayo_gc = phone.group_chat.GroupChat("Sayori", phone.asset("sayori_icon.png"), "mc_sayo"). add_character("mc").add_character("s")

    # create another group chat using `init phone register`
    # and add a few messages
    init phone register:
        define "goofy ahh chat":
            icon phone.asset("sayori_icon.png") key "goofy"
            add "mc" add "s" as goofy
            transient
    
        time month 1 day 26 year 2013 hour 14 minute 31
        "mc" "Ah!"
        "s" "Boo!"
        "mc" "Ah!"

    label phone_discussion_test:
        scene expression "#fdfdfd"
        phone register mc_sayo_gc:  # using the group chat object directly
            time month 5 day 12 year 2015 hour 20 minute 40
            image "s" Solid("#000", xysize=(50, 50))
            "s" "oops"

        "..."
        "Hmm?"
        "A message from Sayori?"

        phone discussion "mc_sayo": # using the gc's key
            pause

        "..."
        "... Really now?"

        phone discussion: # no gc. uses the one used before
            menu:
                "a square?":
                    "mc" "a square?"
                "a black square?":
                    "mc" "a black square?"

        "..."

        phone discussion:
            time minute 50 # year, month, day, hour are all taken from the date before
            "s" "missinput"
        phone end discussion

        "What an airhead..."

        return
