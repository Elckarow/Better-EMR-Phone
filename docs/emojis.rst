Emojis
======

This framework comes with a built-in emoji system (used in text messages but I guess creators can find usage elsewhere).

*The following functions are defined in the* **phone.emojis** *namespace.*

**This namespace is considered *constant* and should not be modified outside of init time.**

``def add(name, emoji)``
    This function adds an emoji to the list of known emojis. It take a string ``name`` (which amy only contain letters, numbers and underscores) and a displayable ``emoji``.

``def get(name)``
    Returns the emoji with the name ``name``. Raises a ``KeyError`` in case the emoji wasn't found.

**A custom text tag is also defined: the** ``emoji`` **text tag.**
    ``"This framework is {emoji=poggers}!"`` will use the ``poggers`` emoji. The displayable will be scaled up or down so that it fits in a line of text.

``def format_emoji_tag(s)``
    This function formats the string ``s`` by replacing each ``emoji`` text tag with a more readable version (basically it replaces the tag with how you'd write it in discord). ::

        phone.emoji.format_emoji_tag("This framework is {emoji=poggers}!")
        >>> "This framework is :poggers:!"

Default emojis include:
    * The most used twemojis
    * Some emojis from the Doki Doki Undercurrents discord server.