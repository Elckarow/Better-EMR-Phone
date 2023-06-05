# Group Chats

*The following functions and classes are defined in the* **`phone.group_chat`** *namespace.*

## The `GroupChat` class

`class GroupChat(object)`
The core of the discussion part of this framework.

`def __init__(self, name, icon, key)`
- `name`: a string, the name of the character.
- `icon`: a displayable.
- `key`: any hashable object that is not `None`. this must be a unique object proper to this `phone.group_chat.GroupChat` object.

Once created, the following fields can be read and safely modified:
`name`
`icon`
while following fields should be read only:
`unread`
`date`

`def add_character(self, char)`
Adds the `*character*` `char` to this group chat, saves the group chat in the `character`'s list of known group chats, and returns the group chat.

`def remove_character(self, char)`
Removes the `*character*` `char` from this group chat, and removes the group chat from the `*character*`'s known group chats.

`def number_of_messages_sent(self, char)`
Returns the number of messages sent by the `*character*` `char`. If `None` is passed, returns the total number of messages sent.

These objects are *hashable* (their key will be hashed).


---
## Functions

`def group_chat(x)`
If `x` is a `phone.group_chat.GroupChat` object, will return that object, otherwise, the group chat with the same key will be returned, or raise a `KeyError` if it wasn't found.

`def has_group_chat(key)`
Returns if a group chat with the key `key` exists.

---
## Example

```
# default /!\
default eileen_gc = phone.group_chat.GroupChat("Eileen", phone.config.basedir + "default_icon.png", "eileen_gc").add_character("eileen")
```
or
use the `define` clause of the `init phone register` statement.