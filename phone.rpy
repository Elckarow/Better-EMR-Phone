init offset = 5

init python:
    phone.__doc__ = """\
Phone framework, inspired from EMR's phone / the quickphone / whatever you call it.
This framework comes with a lot of improved stuff, as well as more features.

The part of the doc is... well... documentation. It describes the functions, classes and variables available.
The doc in `01phone.rpy` explains the different statements.
Each function has a statement equivalent (it's recommended to use those statements as they're more readable and easy to understand).


*character*  = either a `phone.Character` object or a key to a `phone.Character` object.
*group chat* = either a `phone.GroupChat` object or a key to a `phone.GroupChat` object.


Remember that everything below is in the `phone` substore.

######################

```
class Character(object):
```
The phone system relies on these objects (careful not to confuse them with renpy's Character objects, those are completely different).

```
def __init__(self, name, icon, key, cps, color):
```
-`name` is a string. The name of your character.
-`icon` is a displayable.
-`key` is a unique value used to represent the object. It can be any value that can be hashed. It may not be `None`.
For simplicity, you can set it to the character's name but in lowercase. 
-`cps` is an integer giving how fast the character can type text messages.
-`color` is a color value. Used to color the message's textbox.

```
def get_textbox(self):
```
Returns a `RoundedFrame`, used as background for the phone message textbox.

```
# 'property' means that you can access it as an attribute, rather than calling the function
# value = my_phone_character.is_pov
# and not
# value = my_phone_character.is_pov()
@property 
def is_pov(self):
```
Returns if the perspective is from this character. The character's key is compared to the store variable `pov_key`.

```
@property
def short_name(self)
```
Returns a shortened name of this character. If the character's name is longer than `phone.character_short_name_length`,
the last 3 letters are stripped, and "..." is appended.

```
def get_typing_delay(self, message, substitute=True):
```
Returns a number of seconds the character should be typing the message `message`.
If `substitute` is true, the string is passed to `renpy.substitute`.

-These objects are hashable (their key will be hashed).

Additionally, the following field can be read and safely modified:
`name`
`icon`
`cps`
`color`

Various functions related to these objects.

```
def character(x):
```
If `x` is a `Character` object, will return that object.
Else, the character with the same key will be returned, or raise a `KeyError` if it wasn't found.

```
def has_character(key):
```
Returns if a character with the key `key` exists.

###########

This part is related to the phone calls.

```
def call(caller):
```
Starts a phone call with the *character* `caller`.
Replaces the `narrator` with the `_phone_narrator`.
The python equivalent of the `phone call` statement.

```
def end_call():
```
Ends the current phone call, and registers it for both *characters* (the caller and the current pov).
Sets the `narrator` back.
The python equivalent of the `phone end call` statement.

```
def register_call(char1, char2, total_time):
```
Saves a call between `char1` and `char2` (both are *characters*). This is called automatically by the `end_call` function.

###########

This part focuses on text messages and group chats.

```
class GroupChat(object):
```
The big improvement compared to the previous phone system.
Several characters can chat together. Characters can be added / removed from the group chat.
The messages are saved.

```
def __init__(self, name, icon, key):
```
Same behavior for those 3 as described in the `Character` class.

```
@property
def short_name(self):
```
Same behavior as described in the `Character` class but with the `phone.group_chat_short_name_length` variable.

```
def add_character(self, char):
```
Adds a character to this group chat, registers the group chat in the character's group chats, and returns the group chat.
This can be a list of characters, which will add all of the characters.

```
def remove_character(self, char):
```
Removes a character from this group chat, and removes the group chat from the character's group chats.

-These objects are hashable (their key will be hashed).
-These objects are iterable (the list of messages saved starting from the most recent will be iterated over).
-The `len` function can be used on these objects (it'll be used on the list of messages).

-The following field can be read and safely modified:
`name`
`icon`

-The following fields should only be read:
`unread`
`date`

Various functions related to these objects.

```
def group_chat(x):
```
If `x` is a `GroupChat` object, will return that object.
Else, the group chat with the same key will be returned, or raise a `KeyError` if it wasn't found.

```
def has_group_chat(key):
```
Returns if a group chat with the key `key` exists.

```
def register_group_chat(group, *keys):
```
Deprecated.

Now that we have group chats, we can have messages.

```
def discussion(gc):
```
Starts a discussion with the *group chat* `gc`. If `None` is passed, the current group chat is used.
The python equivalent of the `phone discussion` statement.

```
def end_discussion():
```
Ends the current discussion.
The python equivalent of the `phone end discussion` statement.

```
def message(sender, message, delay=None):
```
Sends a message by the *character* sender to the current group chat. Text tags should not be used.
Pauses for `delay` seconds after the message's been saved.
The python equivalent of the default discussion statement.

```
def image(sender, image, time=2.0, delay=None):
```
Sends an image by the *character* sender to the current group chat. `image` should be a string to a defined image / path.
`time` is the time the image is being sent for.
The python equivalent of the `image` discussion statement.

```
def label(label, delay=0.5):
```
Adds a label to the current group chat. The equivalent of the `DateSep` from the previous phone, but this can be any text.
The python equivalent of the `label` discussion statement.

```
def date(month, day, year, hour, minute, delay=0.5):
```
Adds a date as label to the current group chat. The date is saved to the group chat using `datetime.datetime`.
The python equivalent of the `time` discussion statement.

```
def typing(sender, value, delay=None):
```
Simulates the *character* sender typing for `value` seconds. If `value` is a string, `sender.get_typing_delay` is called.
The python equivalent of the `type` discussion statement.

```
def register_message(group, sender, text):
```
Saves a message sent by the *character* `sender` in the *group chat* `group`.
This is called automatically by the `phone.message` function.
The python equivalent of the default register statement.

```
def register_image(group, sender, image):
```
Saves a message sent by the *character* `sender` in the *group chat* `group`.
This is called automatically by the `phone.image` function.
The python equivalent of the `image` register statement.

```
def register_label(group, label)
```
Saves a label in the *group chat* `group`.
This is called automatically by the `phone.label` function.
The python equivalent of the `label` register statement.

```
def register_date(group, month, day, year, hour, minute):
```
Saves a date in the *group chat* `group`.
This is called automatically by the `phone.date` function.
The python equivalent of the `time` register statement.

```
def sort_messages(key):
```
Sorts the group chats of the *character* `key` according to their last registered date.

###########

And lastly, some variables.

``` (global store)
pov_key
```
The object used to know the pov.

```
quick_menu
```
If true, the quick menu used during phone calls will be the phone one. If false, the nomal one is used.

```
textbox_radius
```
The radius used on the rounded textbox.

```
enter_transition
```
The transition used when showing the phone.

```
exit_transition
```
The transition used when hiding the phone.

```
character_short_name_length
```
Described above.

```
group_chat_short_name_length
```
Described above.

```
group_chat_messages_displayed
```
The number of messages that are displayed at once.
Setting it too high can cause performance issues. Setting it to low can be a pain.
Note that due to the `group_chat_messages_fill_if_lower` variable (just below), the number of messages displayed may not be this exact number.

```
group_chat_messages_fill_if_lower
```
If the number of messages in the next `load` is lower or equal than this variable, then those messages are fetched into the current `load`.

```
message_delay
```
A number of seconds added to th typing delay. This should be greater than 0.

```
message_time_pattern
```
A str used when registering a date. The string should contain both "{hour}" and "{minute}" formating tags.

```
message_date_pattern
```
A str sed when registering a date. The string should contain all "{month}", "{day}" and "{year}" formating tags.


########################################################################################
########################################################################################
########################################################################################

Now that you've read the doc (I really hope you did, don't you come crying "hlep phone not work"),
it's time to show you how to use this bad boy.

We'll first be defining 2 `phone.Characters` objects.

```
# MAKE SURE TO USE DEFAULT AND NOT DEFINE
default phone.sayori  = phone.Character("Sayori", "mod_assets/phone/sayori_icon.png", "s", 21, "#22Abf8")
default phone.mc      = phone.Character("MC", "mod_assets/phone/mc_icon.png", "mc", 35, "#714045")
```

1) The phone calls.
You're going to need characters (real `Character` objects, not `phone.Character` objects) that are a bit different.

```
define phone_eileen = Character("Eileen", image="eileen", screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
```
Simple as that. All they need to have is those three keyword arguments: `screen`, `who_style` and `what_style`.

If you already have characters defined and don't want to lose their characteristics, you can use the `kind` keyword argument.
```
define s = DynamicCharacter('s_name', image='sayori', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define phone_s = Character(kind=s, screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
```

Then, use the `phone.call` function or the `phone call` statement with a *character* to start the call.
```
$ phone.call("s") # `phone call "s"`
```

And finally, use the sayer you defined earlier.
```
phone_s "YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOooo"
```

When you're done, call the `phone.end_call` function (or use the `phone end call` statement).
```
phone end call # `$ phone.end_call()`
```

tl;dr
```
# in your definitions file
default phone.sayori  = phone.Character("Sayori", "mod_assets/phone/sayori_icon.png", "s", 21, "#22Abf8") 
define s = DynamicCharacter('s_name', image='sayori', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define phone_s = Character(kind=s, screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")

# in your story
phone call "s"
phone_s "YOOOOOOOOOOOOOOOOOOOOO"
phone end call
```

2) The phone chats.
You'll have to define a group chat and add at least one *character* to it.
This is done either via the `define` clause of the `init phone register` statement, or the usual `default` statement.
```
default mc_sayo_gc = phone.GroupChat("Sayori", icon="mod_assets/Phone/sayori_icon.png", key="mc_sayo").add_character(["mc", "s"])

# or

init phone register:
    define "Sayori":
        key "mc_sayo" add "mc" add "s"
        as mc_sayo_gc icon "mod_assets/Phone/sayori_icon.png"
```
no need to go through with `phone.register_group_chat` anymore. pongers!

To start a conversation, use the `phone.discussion` function (or the `phone discussion` statement) with the *group chat*.
```
$ phone.discussion("mc_s") # or `phone discussion "mc_s":`
```

If you used the function, you'll have to use the `phone.message`, `phone.image`, `phone.date` and `phone.label` functions.
If you used the statement, see the part about that statement in `01phone.rpy`.

When you're done, use the `phone.end_discussion` function (or the `phone end discussion` statement).
```
phone end discussion # or `$ phone.end_discussion()`
```

tl;dr
```
phone discussion "mc_s":
    time day 20 hour 17 minute 32
    "mc" "YOOOOOOOO"
    "s" "YOOOO"
    image "mc" "bg room" time 1.0 delay 2.0
    "mc" "my room"
    label "'Sayori' took a screenshot"
    "s" "pongers"
"did she really said 'pongers'?"
phone discussion:
    "mc" "smh"
phone end discussion

# or 

$ phone.discussion("mc_s")
$ phone.date(9, 20, 2017, 17, 32)
$ phone.message("mc", _("YOOOOOOOO"))
$ phone.message("s", _("YOOOO"))
$ phone.image("mc", "bg room", time=1.0, delay=2.0)
$ phone.message("mc", _("my room"))
$ phone.label(_("'Sayori' took a screenshot"))
$ phone.message("s", _("pongers"))
"did she really said 'pongers'?"
$ phone.message("mc", _("smh"))
$ phone.end_discussion()
```

######################

Want more information about those custom statemtents? Go to `01phone.rpy`.

######################

For those who want to define their own phone screens:

```
screen my_screen():
    tag phone # important
    use _phone():
        #your screen code goes here
```
The `_phone` screen has 4 parameters:
-`xpos`    (defaults to 0.0)
-`xanchor` (defaults to 0.0)
-`ypos`    (defaults to 0.5)
-`yanchor` (defaults to 0.5)

They will control the position of the phone.

######################

If you encounter a bug or have any suggestion:
    -Open an issue on GitHub https://github.com/Elckarow/Phone
    -DM me at Elckarow#8399
"""

define _phone_narrator = Character(kind=narrator, screen="phone_say", what_style="phone_say_dialogue")
define _backup_narrator = narrator

#############################################################################################################
#############################################################################################################
#############################################################################################################

init offset = 0

style _base_phone_text is empty:
    ypos 0.0
    outlines [(2, "#000000aa", 0, 0)]
    line_overlap_split 1
    line_spacing 1
    color "#fff"
    font "mod_assets/phone/Aller_Rg.ttf"
    size 24

screen _phone(xpos=0.0, xanchor=0.0, ypos=0.5, yanchor=0.5):
    frame style "phone_phone":
        at (Flatten, Transform(zoom=gui.phone_zoom, subpixel=True))
        xpos xpos xanchor xanchor
        ypos ypos yanchor yanchor
        add Solid("#fff")

        transclude

style phone_phone:
    background Transform("mod_assets/phone/background.png", align=(0.5, 0.5))
    yalign 0.5
    padding (15, 81, 15, 94)
    xysize (gui.phone_xsize, gui.phone_ysize)

#############################################################################################################
#############################################################################################################
#############################################################################################################

python early in phone:
    from renpy import store
    from store import config
    import datetime, time, collections

    __version__ = (2, 0, 0)
    __author__ = "Elckarow#8399" # smh my head my head

python early in phone._MessageType: # fake enum because of the module not existing in python 2.7 (it's a 3.4 thing)
    DUMMY = 0
    TEXT = 1
    IMAGE = 2
    LABEL = 3
    DATE = 4
    # VIDEO = 5 mayhaps???????????

    ALL = (DUMMY, TEXT, IMAGE, LABEL, DATE)

    _constant = True

init python in phone:
    from store import RoundedFrame, Color, Solid, __, pause, Text, Transform, BrightnessMatrix
    from store import basestring

    class Character(object):
        def __init__(self, name, icon, key, cps, color):
            global _characters
            _characters[key] = self

            self.name = name
            self.icon = icon

            self.cps = int(cps)
            self.color = Color(color)

            if key is None: raise ValueError("key can't be 'None'")
            self.key = key

        def get_textbox(self):
            return get_textbox(self.color)
        
        @property
        def short_name(self):
            global character_short_name_length

            name = __(self.name)
            if len(name) > character_short_name_length:
                name = name[:character_short_name_length - 3] + "..."
            
            return name
        
        @property
        def is_pov(self):
            return self.key == store.pov_key
        
        def get_typing_delay(self, message, substitute=True):
            global message_delay
            if substitute: message = renpy.substitute(message)
            return (len(message) / self.cps) + message_delay
        
        def __hash__(self):
            return hash(self.key)
        
    def character(x):
        if isinstance(x, Character): return x
        global _characters
        return _characters[x]
    
    def has_character(key):
        global _characters
        return key in _characters
    
    def get_textbox(color):
        global textbox_radius
        return RoundedFrame(Solid(color), radius=textbox_radius)

default phone._characters = { }

#############################################################################################################
#############################################################################################################
#############################################################################################################

init python in phone:
    class _DefaultData(object):
        def __call__(self):
            return {
                "call": [ ],
                "message": [ ]
            }

default phone._data = collections.defaultdict(
    phone._DefaultData() # can't pickle lambdas, sadge
)

init python in phone:
    def sort_messages(key):
        global _data
        _data[character(key).key]["message"].sort(key=lambda gc: group_chat(gc).date, reverse=True)
        
#############################################################################################################
#############################################################################################################
#############################################################################################################

init python in phone:
    def call(caller):
        store._window_hide()

        global _current_caller
        if _current_caller is not None:
            raise Exception("can't have 2 phone calls at the same time")
        _current_caller = character(caller)
        store.narrator = store._phone_narrator

        renpy.show_layer_at([Transform(matrixcolor=BrightnessMatrix(-0.21), blur=20)], layer="master", camera=True)
        renpy.show_screen("phone_call")
        renpy.with_statement(enter_transition)
    
    def end_call():
        global _current_caller
        if _current_caller is None:
            raise Exception("ending phone call, but no call was ever made")

        register_call(character(store.pov_key), _current_caller)
        _current_caller = None
        store.narrator = store._backup_narrator

        renpy.show_layer_at([], layer="master", camera=True)
        renpy.hide_screen("phone_call")
        renpy.with_statement(exit_transition)

        store._window_auto = True
    
    def register_call(char1, char2):
        global _data
        key1 = character(char1).key; key2 = character(char2).key

        _data[key1]["call"].append(key2)
        _data[key2]["call"].append(key1)

default phone._current_caller = None

init python in phone:
    def _call_time(st, at):
        return Text(time.strftime("%M:%S", time.gmtime(st)), style="phone_call_time"), 0.0

screen phone_call():
    tag phone
    use _phone(xpos=gui.phone_call_xpos):
        style_prefix "phone_call"

        add Solid("#302D29")

        vbox:
            text phone._current_caller.name
            add DynamicDisplayable(phone._call_time)

        frame:            
            add phone._current_caller.icon:
                at transform:
                    subpixel True fit "contain"

        showif phone.quick_menu and quick_menu:
            use phone_quick_menu()

        add "mod_assets/phone/hang_up.png":
            subpixel True zoom 0.35
            xalign 0.5 ypos 0.8
    
    showif not phone.quick_menu and quick_menu:
        use quick_menu()

style phone_call_vbox:
    spacing 3
    ypos 0.05
    xfill True

style phone_call_text is _base_phone_text:
    xalign 0.5
    text_align 0.5
    ypos 0.0
    outlines [ ]
    line_spacing 0
    size 24

style phone_call_time is phone_call_text:
    size 16

style phone_call_frame is empty:
    background Frame("mod_assets/phone/call_icon_background.png")
    xysize (           120,                   120) # :)
    padding (int(22 * (120 / 404)), int(22 * (120 / 404)))
    ypos 0.18
    xalign 0.5

screen phone_say(who, what):
    style_prefix "phone_say"

    hbox:
        null width ((config.screen_width * gui.phone_call_xpos) + (gui.phone_xsize * gui.phone_zoom))

        frame:
            if who is not None:
                window style "phone_say_namebox":
                    text who id "who"

            window:
                text what id "what"

style phone_say_frame is empty:
    xfill True yfill True
    padding (12, 15)

style phone_say_namebox is empty:
    yanchor 1.0 ypos 0.451
    xsize 200 xalign 0.5

style phone_say_window is empty:
    ypos 0.471 xalign 0.5
    xsize 600

style phone_say_dialogue is _base_phone_text:
    xalign 0.5
    text_align 0.5
    ypos 0.0
    outlines [ ]
    font "mod_assets/phone/JetBrainsMono-Regular.ttf"

style phone_say_label is phone_say_dialogue:
    font "mod_assets/phone/JetBrainsMono-ExtraBold.ttf"
    size 27
    
screen phone_quick_menu():
    grid 3 2:
        style_prefix "phone_quick_menu"

        vbox:
            imagebutton:
                idle "mod_assets/phone/quick_menu_history_idle.png"
                hover "mod_assets/phone/quick_menu_history_selected.png"
                selected_idle "mod_assets/phone/quick_menu_history_selected.png"
                action ShowMenu("history")
            text _("History")

        vbox:
            imagebutton:
                idle "mod_assets/phone/quick_menu_afm_idle.png"
                hover "mod_assets/phone/quick_menu_afm_selected.png"
                selected_idle "mod_assets/phone/quick_menu_afm_selected.png"
                action Preference("auto-forward", "toggle")
            text _("Auto")

        vbox:
            imagebutton:
                idle "mod_assets/phone/quick_menu_skip_idle.png"
                hover "mod_assets/phone/quick_menu_skip_selected.png"
                selected_idle "mod_assets/phone/quick_menu_skip_selected.png"
                action Skip()
            text _("Skip")

        vbox:
            imagebutton:
                idle "mod_assets/phone/quick_menu_settings_idle.png"
                hover "mod_assets/phone/quick_menu_settings_selected.png"
                selected_idle "mod_assets/phone/quick_menu_settings_selected.png"
                action ShowMenu("preferences")
            text _("Settings")

        vbox:
            imagebutton:
                idle "mod_assets/phone/quick_menu_save_idle.png"
                hover "mod_assets/phone/quick_menu_save_selected.png"
                selected_idle "mod_assets/phone/quick_menu_save_selected.png"
                action ShowMenu("save")
            text _("Save")

        vbox:
            imagebutton:
                idle "mod_assets/phone/quick_menu_load_idle.png"
                hover "mod_assets/phone/quick_menu_load_selected.png"
                selected_idle "mod_assets/phone/quick_menu_load_selected.png"
                action ShowMenu("load")
            text _("Load")

style phone_quick_menu_grid:
    xalign 0.5 ypos 0.45
    xspacing 31 yspacing 22

style phone_quick_menu_vbox is empty
style phone_quick_menu_text is phone_call_time:
    size 14

#############################################################################################################
#############################################################################################################
#############################################################################################################

init python in phone:
    class GroupChat(object):    
        def __init__(self, name, icon, key):
            global _group_chats
            _group_chats[key] = self

            self.name = name
            self.icon = icon
            self.date = datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0)

            self.unread = True

            self._characters = set()            
            self._messages = [ ]
            self._page = 0
            
            if key is None: raise ValueError("key can't be 'None'")
            self.key = key
        
        @property
        def short_name(self):
            global group_chat_short_name_length

            name = __(self.name)
            if len(name) > group_chat_short_name_length:
                name = name[:group_chat_short_name_length - 3] + "..."
            
            return name
        
        def add_character(self, char):
            if isinstance(char, list):
                map(self.add_character, char)
            
            else:
                char = character(char)
                self._characters.add(char.key)

                global _data
                if self.key not in _data[char.key]["message"]:
                    _data[char.key]["message"].append(self.key)
            
            return self
        
        def remove_character(self, char):
            char = character(char)
            if char not in self._characters: return
            self._characters.remove(char.key)

            global _data
            _data[char.key]["message"].remove(self.key)
        
        def _page_up(self):
            self._page += 1
        
        def _page_down(self):
            self._page -= 1
        
        def _can_load_more(self):
            if not self._messages: return False         
            return next(self._get_messages()) is not self._messages[0]
        
        def _get_messages(self):
            global group_chat_messages_displayed

            min_x = self._page * group_chat_messages_displayed
            max_x = min_x + group_chat_messages_displayed

            global group_chat_messages_fill_if_lower
            remaining = len(self._messages) - max_x
            if remaining <= group_chat_messages_fill_if_lower:
                max_x += remaining

            return reversed(self._messages[::-1][min_x:max_x])
        
        def _register_message(self, message, check_sender=True):
            if check_sender and message.sender not in self._characters:
                raise Exception("sender '{}' isn't in group chat".format(message.sender))
            self._messages.append(message)

            global _group_chat
            self.unread = _group_chat is not self 
        
        def __iter__(self):
            return reversed(self._messages)
        
        def __len__(self):
            return len(self._messages)

        def __hash__(self):
            return hash(self.key)
    
    def group_chat(x):
        if isinstance(x, GroupChat): return x
        global _group_chats
        return _group_chats[x]
    
    def has_group_chat(key):
        global _group_chats
        return key in _group_chats
    
    def _check_for_tags(s):
        no_tags = renpy.filter_text_tags(s, allow=())
        if no_tags != s:
            raise ValueError("no text tags are allowed: '{}'".format(s))

    def discussion(gc):
        global _group_chat

        if gc is None:
            if _group_chat is not None:
                return
            else:
                raise Exception("group chat not given (no previous group chat was found)")

        if _group_chat is not None:
            raise Exception("preparing group chat while another convesation is going on")
        
        gc = group_chat(gc)

        if not gc._characters:
            raise Exception("group chat '{}' has no characters".format(gc.name))
        
        store._window_hide()
        
        _group_chat = gc
        _group_chat.unread = False

        renpy.show_layer_at([Transform(matrixcolor=BrightnessMatrix(-0.03), blur=5)], layer="master", camera=True)
        renpy.show_screen("phone_message")
        renpy.with_statement(enter_transition)

        store._window_auto = True
    
    def end_discussion():
        store._window_hide()

        global _group_chat
        if _group_chat is None:
            raise Exception("ending discussion, but no discussion ever started")
            
        for key in _group_chat._characters:
            sort_messages(key)
        
        _group_chat = None

        renpy.show_layer_at([], layer="master", camera=True)
        renpy.hide_screen("phone_message")
        renpy.with_statement(exit_transition)
    
        store._window_auto = True

    class _RawMessage(object):
        def __init__(self, sender, message, _type):
            self.sender = sender
            self.message = message
            if _type not in _MessageType.ALL: raise Exception("'{}' is not a valid mesage type".format(_type))
            self.type = _type
    
    def message(sender, message, delay=None):
        store._window_hide()

        sender = character(sender)

        global _current_message
        _current_message = _RawMessage(sender.key, message, _MessageType.TEXT)
        if _group_chat._page == 0:
            _message_yadj.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        pause(sender.get_typing_delay(message))
        store._dismiss_pause = _dismiss_pause

        register_message(_group_chat, sender, message)
        if _group_chat._page == 0:
            _message_yadj.value = float("inf")

        _current_message = None

        store._window_auto = True
        pause(None)

    def register_message(group, sender, text):
        _check_for_tags(text)

        group = group_chat(group)
        sender = character(sender)

        group._register_message(_RawMessage(sender.key, text, _MessageType.TEXT))

    def image(sender, image, time=2.0, delay=None):
        store._window_hide()

        sender = character(sender)

        global _current_message
        _current_message = _RawMessage(sender.key, image, _MessageType.IMAGE)
        if _group_chat._page == 0:
            _message_yadj.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        pause(time)
        store._dismiss_pause = _dismiss_pause

        register_image(_group_chat, sender, image)
        if _group_chat._page == 0:
            _message_yadj.value = float("inf")
        
        _current_message = None
        
        store._window_auto = True
        pause(delay)
    
    def register_image(group, sender, image):
        if not isinstance(image, basestring):
            raise TypeError("a phone image expects a string")

        group = group_chat(group)
        sender = character(sender)

        group._register_message(_RawMessage(sender.key, image, _MessageType.IMAGE))
    
    def label(label, delay=0.5):
        register_label(_group_chat, label)

        if _group_chat._page == 0:
            _message_yadj.value = float("inf")

        pause(delay)
    
    def register_label(group, label):
        _check_for_tags(label)

        group = group_chat(group)
        group._register_message(_RawMessage(None, label, _MessageType.LABEL), False)
    
    def date(month, day, year, hour, minute, delay=0.5):
        register_date(_group_chat, month, day, year, hour, minute)
        pause(delay)

    def register_date(group, month, day, year, hour, minute):
        group = group_chat(group)

        if (group.date.year, group.date.month, group.date.day) < (year, month, day):
            global message_date_pattern
            group._register_message(_RawMessage(None, __(message_date_pattern).format(month=str(month).zfill(2), day=str(day).zfill(2), year=str(year).zfill(2)), _MessageType.DATE), False)
        
        group.date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

        global message_hour_pattern
        group._register_message(_RawMessage(None, __(message_time_pattern).format(hour=str(hour).zfill(2), minute=str(minute).zfill(2)), _MessageType.DATE), False)

    def typing(sender, value, delay=None):
        sender = character(sender)

        if isinstance(value, basestring):
            value = sender.get_typing_delay(value)

        global _current_message
        _current_message = _RawMessage(sender.key, "", _MessageType.DUMMY)
        if _group_chat._page == 0:
            _message_yadj.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        pause(value)
        store._dismiss_pause = _dismiss_pause

        if _group_chat._page == 0:
            _message_yadj.value = float("inf")
        
        _current_message = None
        
        store._window_auto = True
        pause(delay)

default phone._current_message = None
default phone._group_chat = None

default phone._group_chats = { }
default phone.menu = False

init python in phone:
    _message_yadj = renpy.display.behavior.Adjustment()

screen phone_message():
    use _phone(xpos=0.5, xanchor=0.5, ypos=0.1, yanchor=0.1):
        side "t b c":
            use _app_header_1(action=(SetField(phone, "_group_chat", None), Return())):
                style_prefix "app_header_1"

                hbox:
                    add phone._group_chat.icon:
                        at transform:
                            subpixel True yalign 0.5
                            xysize (36, 36) fit "contain"

                    text phone._group_chat.short_name:
                        color "#000" size 19

            use _chat_textbox()
            use _chat_messages()


screen _app_header_1(action=Return()):
    style_prefix "app_header_1"

    frame:
        textbutton _("< Back"):
            action action
            sensitive phone.menu
        
        transclude

style app_header_1_frame:
    ysize 50
    background "#F2F2F2"
    xfill True
    padding (10, 10)

style app_header_1_hbox:
    spacing 5
    align (0.5, 0.5)

style app_header_1_text is _base_phone_text:
    outlines [ ]
    yalign 0.5

style app_header_1_button:
    yalign 0.5
    xalign 0.0

style app_header_1_button_text is app_header_1_text:
    color "#0094FF" 
    size 18 

init python in phone:
    class _AutoScrollVP(renpy.display.layout.Container):
        """
        Actual dark magic...
        """
        def __init__(self, vp):
            super(_AutoScrollVP, self).__init__(vp)

            self.vp = vp
            self.adj_text = vp.child.child

            self.text_time = self.adj_text.child.get_time
            self.text_xsize = self.adj_text.child.size()[0]

        def render(self, w, h, st, at):
            text_time = self.text_time()

            if text_time:
                adjusted_st, _ = self.adj_text.adjusted_times()

                delta = min(1.0, adjusted_st / text_time)
                
                # not really its size, but the width of what has been rendered
                # |                                                                |
                # | This is a super dup                                            |
                # |                                                                |
                # The "size" of this for instance, if the text is "This is a super duper long message."
                current_text_size = self.text_xsize * delta

                if current_text_size > self.vp.width:
                    self.vp.xadjustment.value = current_text_size - self.vp.width
                    self.update()

            return super(_AutoScrollVP, self).render(w, h, st, at)

screen _chat_textbox():
    style_prefix "phone_textbox"

    frame:
        side "l r":
            if phone._current_message is not None:
                $ sender = phone.character(phone._current_message.sender)
                if (
                    sender.is_pov and
                    phone._current_message.type == phone._MessageType.TEXT
                ):
                    fixed:
                        yfill True
                        xsize 0.9

                        viewport at phone._AutoScrollVP:
                            draggable False
                            mousewheel False
                            yalign 0.5

                            frame style "phone_textbox_typing_text_frame":
                                add renpy.display.layout.AdjustTimes(
                                        Text(
                                            phone._current_message.message,
                                            style="phone_textbox_text",
                                            slow_cps=sender.cps,
                                        ),
                                        None,
                                        None
                                    )
                else: # ugly ahh
                    text _("Type a message.") color "#666"

            else:
                text _("Type a message.") color "#666"

            text _("Send") color "#0094FF" xalign 1.0
            

style phone_textbox_frame is empty:
    ysize 50 xfill True
    background "#F2F2F2"
    padding (10, 10)

style phone_textbox_side:
    xfill True
    yfill True

style phone_textbox_text is _base_phone_text:
    outlines [ ]
    size 16
    color "#000"
    line_leading 0
    line_spacing 0
    yalign 0.5
    layout "nobreak"

style phone_textbox_typing_text_frame is empty:
    yfill True

screen _chat_message(rm):
    style_prefix "phone_messages"

    $ sender = phone.character(rm.sender)

    hbox:
        # sus but hey
        if sender.is_pov:
            xalign 1.0

            frame:
                background sender.get_textbox()
                transclude

            add sender.icon at _phone_message_icon

        else:
            add sender.icon at _phone_message_icon

            frame:
                background sender.get_textbox()
                transclude


screen _chat_messages():
    style_prefix "phone_messages"

    default _label = False

    viewport:
        yadjustment phone._message_yadj
        draggable True
        mousewheel True
        yinitial 1.0
        yalign 1.0
        yfill True

        frame style "empty":
            yalign 1.0
            padding (10, 10)

            vbox:
                showif phone._group_chat._can_load_more():
                    textbutton _("Load More"):
                        action (Function(phone._group_chat._page_up), SetField(phone._message_yadj, "value", float("inf")), SetScreenVariable("_label", False))
                        bottom_margin 5

                for rm in phone._group_chat._get_messages():
                    if rm.type in (phone._MessageType.IMAGE, phone._MessageType.TEXT):
                        if _label:
                            $ _label = False
                            null height gui.phone_message_label_null_height
                        
                        use _chat_message(rm):
                            if rm.type == phone._MessageType.IMAGE:
                                imagebutton style "empty":
                                    at _phone_image
                                    idle rm.message
                                    action Show("_phone_image", dissolve, img=rm.message)

                            else:
                                text rm.message                                    
                    
                    elif rm.type in (phone._MessageType.LABEL, phone._MessageType.DATE):
                        if not _label:
                            $ _label = True
                            null height gui.phone_message_label_null_height

                        text rm.message style "phone_message_text_label"
                    
                    else:
                        null

                if phone._current_message is not None:
                    $ sender = phone.character(phone._current_message.sender)
                    if sender.is_pov:
                        if phone._current_message.type == phone._MessageType.IMAGE:
                            if _label:
                                $ _label = False
                                null height gui.phone_message_label_null_height

                            use _chat_message(phone._current_message):
                                add phone._current_message.message:
                                    at (Transform(matrixcolor=BrightnessMatrix(-0.1), blur=10), _phone_image)

                    else:    
                        use _typing_indicator(sender)
                
                showif phone._group_chat._page > 0:
                    textbutton _("Go Back"):
                        action (Function(phone._group_chat._page_down), SetField(phone._message_yadj, "value", 0.0), SetScreenVariable("_label", False))
                        top_margin 5

transform _phone_image:
    xsize 1.0 subpixel True
    fit "scale-down"

transform _phone_message_icon:
    subpixel True yalign 0.0
    xysize (33, 33) fit "contain"

screen _phone_image(img):
    modal True
    add Solid("#000")

    add img:
        align (0.5, 0.5)
    
    key ["mouseup_1", "mouseup_3"] action Hide("_phone_image", dissolve)

style phone_messages_button:
    xalign 0.5

style phone_messages_button_text is phone_say_dialogue:
    xalign 0.5
    text_align 0.5
    ypos 0.0
    size 16
    color "#000"

style phone_messages_vbox:
    spacing 5
    yalign 1.0
    xfill True 

style phone_messages_hbox:
    spacing 5

style phone_messages_text is _base_phone_text:
    outlines [ ]
    size 19
    line_leading 0
    line_spacing 0
    yoffset -1

style phone_messages_frame is empty:
    xmaximum 240
    padding gui.phone_message_frame_padding

style phone_message_text_label is phone_messages_text:
    color "#000"
    xalign 0.5 text_align 0.5
    size 15
    xsize 0.8

transform _typing_blink(delay):
    alpha 0.25
    pause delay

    block:
        ease 0.2 alpha 0.75
        pause 0.2
        ease 0.2 alpha 0.25
        pause 0.6
        repeat

screen _typing_indicator(sender):
    style_prefix "phone_typing"

    hbox:
        frame style "phone_messages_frame":
            background phone.get_textbox("#f2f2f2")

            hbox:
                text "⚫" at _typing_blink(0.0)
                text "⚫" at _typing_blink(0.2)
                text "⚫" at _typing_blink(0.4)
        
        text _("[sender.short_name!t] is typing...") style "phone_typing_istyping"
    
style phone_typing_hbox:
    spacing 3

style phone_typing_text is phone_messages_text:
    color "#000"
    font "DejaVuSans.ttf"

style phone_typing_istyping is _base_phone_text:
    color "#626262"
    yalign 0.5
    outlines [ ]
    size 16

#############################################################################################################
#############################################################################################################
#############################################################################################################

define -100 config.early_start_store = False

init 999 python in phone:
    @config.start_callbacks.append
    def __sort_register_messages():
        global _data
        for key in _data:
            sort_messages(key)

#############################################################################################################
#############################################################################################################
#############################################################################################################

# Deprecated stuff
label _phone_register:
    $ raise Exception("The label '_phone_register' isn't needed anymore")

init python in phone:
    def register_group_chat(group, *keys):
        raise Exception("The 'phone.register_group_chat' function isn't needed anymore")
    
    def register(f):
        raise Exception("The `phone.register` decorator isn't used anymore. (function being decorated: {})".format(f.__name__))