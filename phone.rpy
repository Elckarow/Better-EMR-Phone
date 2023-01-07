init offset = 5

init python:
    phone.__doc__ = """\
Phone framework, inspired from EMR's phone / the quickphone / whatever you call it.
This framework comes with a lot of improved stuff, as well as more features.

The 1st part of the doc is... well... documentation. It describes the functions, classes and variables available.
The 2nd part will show various examples of how things can be done.


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
-`key` is a unique value used to represent the object. It can be any value that can be hashed.
For simplicity, you can set it to the character's name but in lowercase. 
-`cps` is an integer giving how fast the character can type text messages.
-`color` is a color value. Used to color the message's textbox.


```
def get_textbox(self):
```
Returns a `RoundedFrame`, used as background for the phone message textbox.


```
# 'property' means that you can access it as attribute, rather than calling the function
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
def get_typing_delay(self, message):
```
Returns a number of seconds the character should be typing the message `message`.


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
Else, the character with the same key will be returned, or `None` if it wasn't found.


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


```
def end_call():
```
Ends the current phone call, and registers it for both *characters* (the caller and the current pov).
Sets the `narrator` back.


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
Same behavior as described in the `Character` class, but with the `phone.group_chat_short_name_length` variable.


```
def add_character(self, char):
```
Adds a character to this group chat, and registers the group chat in the character's group chats.


```
def remove_character(self, char):
```
Removes a character to this group chat, and removes the group chat from the character's group chats.


-These objects are hashable (their key will be hashed).
-These objects are iterable (the list of messages saved starting from the most recent will be iterated over).
-The `len` function can be used on these objects (it'll be used on the list of messages).


Additionally, the following field can be read and safely modified:
`name`
`icon`
`date` (should not be modified)


Various functions related to these objects.


```
def group_chat(x):
```
If `x` is a `GroupChat` object, will return that object.
Else, the group chat with the same key will be returned, or `None` if it wasn't found.


```
def has_group_chat(key):
```
Returns if a group chat with the key `key` exists.


```
def register_group_chat(group, *keys):
```
Registers the group chat `group` (a `GroupChat` object), adds the *characters* passed as positional arguments (there must be at least 2), and returns that `group`.
Be sure to use this function. Doing `default my_group = phone.GroupChat(...)` isn't enough to use that group. You'll have to call this function at some point.


Now that we have group chats, we can have messages.


```
def discussion(gc):
```
Starts a discussion with the *group chat* `gc`.


```
def end_discussion():
```
Ends the current discussion.


```
PhoneMessage
```
A `collections.namedtuple` with the fields `sender` (a character key) and `message` (a str).
Used (mostly intenally) to represent... a phone message. W O W


```
def message(sender, message, delay=None):
```
Sends a message by the *character* sender to the current group chat. Text tags should not be used.
Pauses for `delay` seconds after the message's been saved.


```
def image(sender, image, time=2.0, delay=None):
```
Sends an image by the *character* sender to the current group chat. `image` should be a string to a defined image / path.
`time` is the time the image is being sent for.


```
def label(label, delay=0.5):
```
Adds a label to the current group chat. The equivalent of the `DateSep` from the previous phone, but this can be any text.


```
def date(month, day, year, hour, minute, delay=0.5):
```
Adds a date as label to the current group chat. The date is saved to the group chat using `datetime.datetime`.


```
def register_message(group, sender, text):
```
Saves a message sent by the *character* `sender` in the *group chat* `group`.
This is called automatically by the `phone.message` function.


```
def register_image(group, sender, image):
```
Saves a message sent by the *character* `sender` in the *group chat* `group`.
This is called automatically by the `phone.image` function.


```
def register_label(group, label)
```
Saves a label in the *group chat* `group`.
This is called automatically by the `phone.label` function.


```
def register_date(group, month, day, year, hour, minute):
```
Saves a date in the *group chat* `group`.
This is called automatically by the `phone.date` function.


```
def sort_messages(key):
```
Sorts the group chats of the *character* `key` according to their last registered date.


###########


And lastly, some variables.


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
Used when registering a date. The string should contain both "{hour}" and "{minute}" formating tags.


```
message_date_pattern
```
Used when registering a date. The string should contain all "{month}", "{day}" and "{year}" formating tags.


########################################################################################
########################################################################################
########################################################################################


Now that you've read the doc (I really hope you did), it's time to show you how to use this bad boy.


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
Simple as that. All they need to have is those three keyword arguments (screen, who_style and what_style).


If you already have characters defined and don't want to lose their characteristics, you can use the `kind` keyword argument.
```
define s = DynamicCharacter('s_name', image='sayori', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define phone_s = Character(kind=s, screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
```


Then, all you have to do is start a phone call with the `phone.call` function and here ya go!


```
label start:
    $ phone.call("s") # key of the `phone.sayori` object
    phone_s "Ohayouuu!!!!!!!!!"
    "This is the new narrator...."
    $ phone.end_call()
    "This is the narrator we all know."
```
ez clap


2) The phone messages.


We'll be needing a group chat for this.
As stated previously, "Doing `default my_group = phone.GroupChat(...)` isn't enough.".
BUT, doing:

```
default mc_sayo = phone.register_group_chat(
    phone.GroupChat("Sayori", "mod_assets/phone/sayori_icon.png", "mc_sayo"),
    "mc", "s"
)
```
won't work because of renpy's behavior. You can still default your group chat no problemo, but `phone.register_group_chat` is to be called at runtime.
A good example of doing both at the same time (defining a group chat and registering it) can be found after this part.


To enter a text conversation, same thing as with phone calls.
Start a discussion with `phone.discussion` and have fun with `phone.message`, `phone.image`, `phone.label` and `phone.date`:

```
label start:          
    $ phone.discussion(mc_sayo)

    $ phone.date(2, 12, 2022, 10, 11)

    # Make sure the text messages are translatable _()
    $ phone.message("mc", _("Sup Sayo! Got a new phone"))

    # using the object    v
    $ phone.message(phone.sayori, _("NO WAY"))
 
    # using the key   v
    $ phone.message("mc", _("YES WAY"))

    $ phone.message("s", _("That's why you've left me on read for a week..."))
```


To register messages before the game starts, simply decorate your function with `register`:
```
init python in phone:
    @register
    def __register_mc_sayo_messages():
        # using the object    v    we defaulted above
        register_group_chat(store.mc_sayo, "mc", "s")
        register_date("mc_sayo", 5, 2, 2022, 10, 11)
        register_message("mc_sayo", "s", _("Yo MC, can I come over to your house today???"))
    
    @register
    def __register_mc_sayo_messages_2():
        register_group_chat(GroupChat( # defining the gc directly
            "goofy ahh group chat", "mod_assets/phone/default_icon.png", "goofy"
        ), "mc", "s")
        register_date("goofy", 5, 20, 2022, 12, 32)
        register_label("goofy", "'Sayori' was added to the group chat")
        register_image("goofy", "mc", "mod_assets/phone/sayori_icon.png")
        register_message("goofy", "s", _("What the f-"))
```
And NOW you are good to go.
(for those who a version prior to 1.1.0, the label `_phone_register` is not needed anymore. It was a dumb mistake on my part.)


For those who want to define their own screens:


```
screen my_screen():
    tag phone # important
    use phone():
        #your screen code goes here
```
The `phone` screen has 4 parameters:
-`xpos`    (defaults to 0.0)
-`xanchor` (defaults to 0.0)
-`ypos`    (defaults to 0.5)
-`yanchor` (defaults to 0.5)

They will control the position of the phone.
"""

define phone.enter_transition = Dissolve(0.6, time_warp=_warper.ease)
define phone.exit_transition = Dissolve(0.6, time_warp=_warper.ease)

define phone.character_short_name_length = 16

define phone.group_chat_short_name_length = 9
define phone.group_chat_messages_displayed = 175
define phone.group_chat_messages_fill_if_lower = 15

define phone.message_delay = 0.6
define phone.message_time_pattern = _("{hour}:{minute}")
define phone.message_date_pattern = _("{month}/{day}/{year}")

# /!\ default
default phone.sayori  = phone.Character("Sayori", "mod_assets/phone/sayori_icon.png", "s", 21, "#22Abf8")
default phone.mc      = phone.Character("MC", "mod_assets/phone/mc_icon.png", "mc", 35, "#484848")
default phone.natsuki = phone.Character("Natsuki", "mod_assets/phone/natsuki_icon.png", "n", 45, "#fbb")
default phone.monika  = phone.Character("Monika", "mod_assets/phone/monika_icon.png", "m", 40, "#0a0")
default phone.yuri    = phone.Character("Yuri", "mod_assets/phone/yuri_icon.png", "y", 20, "#a327d6")

default pov_key = "mc"

define phone_s  = Character(kind=s, screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
define phone_mc = Character(kind=mc, screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
define phone_m  = Character(kind=m, screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
define phone_n  = Character(kind=n, screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
define phone_y  = Character(kind=y, screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")

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

screen phone(xpos=0.0, xanchor=0.0, ypos=0.5, yanchor=0.5):
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

init python in phone:
    from renpy import store
    from store import RoundedFrame, Color, Solid, __, pause, collections, Text, Transform, BrightnessMatrix, datetime
    from store import basestring

    class Character(object):
        def __init__(self, name, icon, key, cps, color):
            _characters[key] = self

            self.name = name
            self.icon = icon

            self.cps = int(cps)
            self.color = Color(color)

            self.key = key

            # used when sending a message
            self._current_message = None
        
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
        
        def get_typing_delay(self, message):
            global message_delay
            return (len(__(message)) / self.cps) + message_delay
        
        def __hash__(self):
            return hash(self.key)
        
    def character(x):
        if isinstance(x, Character): return x
        return _characters.get(x, None)
    
    def has_character(key):
        return key in _characters
    
    def get_textbox(color):
        return RoundedFrame(Solid(color), radius=15)

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

        register_call(_characters[store.pov_key], _current_caller)
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

init 1 python in phone:
    def _call_time(st, at):
        return Text(time.strftime("%M:%S", time.gmtime(st)), style="phone_call_time"), 0.0)

screen phone_call():
    tag phone
    use phone(xpos=gui.phone_call_xpos):
        style_prefix "phone_call"

        add Solid("#302D29")

        vbox:
            text "[phone._current_caller.name!t]"
            add DynamicDisplayable(phone._call_time)

        frame:            
            add phone._current_caller.icon:
                at transform:
                    subpixel True fit "contain"

        use phone_quick_menu()

        add "mod_assets/phone/hang_up.png":
            subpixel True zoom 0.35
            xalign 0.5 ypos 0.8

style phone_call_vbox:
    spacing 3
    ypos 0.05
    xfill True

style phone_call_text is _base_phone_text:
    xalign 0.5
    text_align 0.5
    ypos 0.0
    outlines []
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
    style_prefix "phone_quick_menu"

    showif quick_menu:
        grid 3 2:
            vbox:
                imagebutton:
                    idle "mod_assets/phone/quick_menu_history_idle.png"
                    selected_idle "mod_assets/phone/quick_menu_history_selected.png"
                    selected_hover "mod_assets/phone/quick_menu_history_selected.png"
                    action ShowMenu("history")
                text _("History")
            
            vbox:
                imagebutton:
                    idle "mod_assets/phone/quick_menu_afm_idle.png"
                    selected_idle "mod_assets/phone/quick_menu_afm_selected.png"
                    selected_hover "mod_assets/phone/quick_menu_afm_selected.png"
                    action Preference("auto-forward", "toggle")
                text _("Auto")
            
            vbox:
                imagebutton:
                    idle "mod_assets/phone/quick_menu_skip_idle.png"
                    selected_idle "mod_assets/phone/quick_menu_skip_selected.png"
                    selected_hover "mod_assets/phone/quick_menu_skip_selected.png"
                    action Skip()
                text _("Skip")
            
            vbox:
                imagebutton:
                    idle "mod_assets/phone/quick_menu_settings_idle.png"
                    selected_idle "mod_assets/phone/quick_menu_settings_selected.png"
                    selected_hover "mod_assets/phone/quick_menu_settings_selected.png"
                    action ShowMenu("preferences")
                text _("Settings")
        
            vbox:
                imagebutton:
                    idle "mod_assets/phone/quick_menu_save_idle.png"
                    selected_idle "mod_assets/phone/quick_menu_save_selected.png"
                    selected_hover "mod_assets/phone/quick_menu_save_selected.png"
                    action ShowMenu("save")
                text _("Save")
            
            vbox:
                imagebutton:
                    idle "mod_assets/phone/quick_menu_load_idle.png"
                    selected_idle "mod_assets/phone/quick_menu_load_selected.png"
                    selected_hover "mod_assets/phone/quick_menu_load_selected.png"
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
            self.name = name
            self.icon = icon
            self.date = datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0)

            self._characters = set()            
            self._messages = []
            self._page = 0
            
            self.key = key
        
        @property
        def short_name(self):
            global group_chat_short_name_length

            name = __(self.name)
            if len(name) > group_chat_short_name_length:
                name = name[:group_chat_short_name_length - 3] + "..."
            
            return name
        
        def add_character(self, char):
            char = character(char)
            self._characters.add(char.key)

            global _data
            if self.key not in _data[char.key]["message"]:
                _data[char.key]["message"].append(self.key)
        
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

            for message in reversed(self._messages[::-1][min_x:max_x]):
                yield message
        
        def _register_message(self, message):
            if message.sender not in self._characters: raise Exception("sender '{}' isn't in group chat".format(character(message.sender).name))
            self._messages.append(message)
        
        def _register_image(self, image):
            if image.sender not in self._characters: raise Exception("sender '{}' isn't in group chat".format(character(image.sender).name))
            self._messages.append(image)
        
        def _register_label(self, label):
            self._messages.append(label)
        
        def __iter__(self):
            return reversed(self._messages)
        
        def __len__(self):
            return len(self._messages)

        def __hash__(self):
            return hash(self.key)
        
    def register_group_chat(group, *keys):
        if len(keys) < 2: raise Exception("expected at least 2 keys")

        global _group_chats
        _group_chats[group.key] = group

        for key in keys:
            group.add_character(character(key))
        
        return group
    
    def group_chat(x):
        if isinstance(x, GroupChat): return x
        return _group_chats.get(x, None)
    
    def has_group_chat(key):
        return key in _group_chats

    def discussion(gc):
        store._window_hide()

        global _group_chat
        if _group_chat is not None:
            raise Exception("preparing group chat while another convesation is going on")
        
        _group_chat = group_chat(gc)

        renpy.show_layer_at([Transform(matrixcolor=BrightnessMatrix(-0.03), blur=5)], layer="master", camera=True)
        renpy.show_screen("phone_message")
        renpy.with_statement(enter_transition)

        store._window_auto = True
    
    def end_discussion():
        store._window_hide()

        global _group_chat
        if _group_chat is None:
            raise Exception("ending discussion, but no discussion ever started")
            
        for key in group_chat._characters:
            sort_messages(key)
        
        _group_chat = None

        renpy.show_layer_at([], layer="master", camera=True)
        renpy.hide_screen("phone_message")
        renpy.with_statement(exit_transition)
    
        store._window_auto = True
    
    PhoneMessage = collections.namedtuple("PhoneMessage", ("sender", "message"))

    def message(sender, message, delay=None):
        store._window_hide()

        sender = character(sender)
        sender._current_message = message

        global _currently_typing
        _currently_typing = sender
        if _group_chat._page == 0:
            _message_yadj.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        pause(sender.get_typing_delay(message))
        store._dismiss_pause = _dismiss_pause

        global _group_chat
        register_message(_group_chat, sender.key, message)
        if _group_chat._page == 0:
            _message_yadj.value = float("inf")

        _currently_typing = None
        sender._current_message = None

        store._window_auto = True
        pause(None)

    def register_message(group, sender, text):
        group = group_chat(group)
        sender = character(sender)

        group._register_message(PhoneMessage(sender.key, text))

    class PhoneImage(PhoneMessage): pass

    def image(sender, image, time=2.0, delay=None):
        store._window_hide()

        sender = character(sender)

        global _currently_typing
        _currently_typing = sender
        if _group_chat._page == 0:
            _message_yadj.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        pause(time)
        store._dismiss_pause = _dismiss_pause

        global _group_chat
        register_image(_group_chat, sender, image)
        if _group_chat._page == 0:
            _message_yadj.value = float("inf")
        
        _currently_typing = None
        
        store._window_auto = True
        pause(delay)
    
    def register_image(group, sender, image):
        if not isinstance(image, basestring):
            raise TypeError("a phone image expects a string")

        group = group_chat(group)
        sender = character(sender)

        group._register_image(PhoneImage(sender.key, image))

    class Label(object):
        def __init__(self, text):
            self.text = text
        
        def to_text(self):
            return Text(self.text, style="phone_message_text_label")
    
    def label(label, delay=0.5):
        global _group_chat
        register_label(_group_chat, label)

        if _group_chat._page == 0:
            _message_yadj.value = float("inf")

        pause(delay)
    
    def register_label(group, label):
        group = group_chat(group)
        group._register_label(Label(label))
    
    def date(month, day, year, hour, minute, delay=0.5):
        global _group_chat
        register_date(_group_chat, month, day, year, hour, minute)

        pause(delay)

    def register_date(group, month, day, year, hour, minute):
        group = group_chat(group)

        if (group.date.month, group.date.day, group.date.year) < (month, day, year):
            global message_date_pattern
            register_label(group, __(message_date_pattern).format(month=str(month).zfill(2), day=str(day).zfill(2), year=str(year).zfill(2)))
        
        group.date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

        global message_hour_pattern
        register_label(group, __(message_time_pattern).format(hour=str(hour).zfill(2), minute=str(minute).zfill(2)))


default phone._currently_typing = None
default phone._group_chat = None

default phone._group_chats = { }


init python in phone:
    _message_yadj = renpy.display.behavior.Adjustment()

screen phone_message():
    tag phone

    use phone(xpos=0.5, xanchor=0.5, ypos=0.1, yanchor=0.1):
        side "t b c":
            use _chat_header()
            use _chat_textbox()
            use _chat_messages()


screen _chat_header():
    style_prefix "phone_header"

    frame:
        text _("< Back"):
            color "#0094FF" size 18 xalign 0.0
        
        hbox:
            add phone._group_chat.icon:
                at transform:
                    subpixel True yalign 0.5
                    xysize (36, 36) fit "contain"

            text "[phone._group_chat.short_name!t]":
                color "#000" size 19

        text _("Active"):
            color "#0a0" size 16 xalign 1.0

style phone_header_frame is empty:
    ysize 50
    background "#F2F2F2"
    xfill True
    padding (10, 10)

style phone_header_hbox:
    spacing 5
    align (0.5, 0.5)

style phone_header_text is _base_phone_text:
    outlines [ ]
    yalign 0.5


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
            if phone._currently_typing is not None and phone._currently_typing.is_pov and phone._currently_typing._current_message is not None:
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
                                        phone._currently_typing._current_message,
                                        style="phone_textbox_text",
                                        slow_cps=phone._currently_typing.cps,
                                    ),
                                    None,
                                    None
                                )
                        
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

screen _chat_messages():
    style_prefix "phone_messages"

    default label = False

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
                        action (Function(phone._group_chat._page_up), SetField(phone._message_yadj, "value", float("inf")), SetScreenVariable("label", False))
                        bottom_margin 5

                for thing in phone._group_chat._get_messages():
                    if isinstance(thing, phone.PhoneMessage):
                        if label:
                            $ label = False
                            null height gui.phone_message_label_null_height

                        $ key, message = thing
                        $ sender = phone._characters[key]

                        hbox:
                            # sus but hey
                            if sender.is_pov:
                                xalign 1.0

                                frame:
                                    background sender.get_textbox()

                                    if isinstance(thing, phone.PhoneImage):
                                        imagebutton style "empty":
                                            at transform:
                                                xsize 1.0 subpixel True
                                                fit "contain"
                                                
                                            idle message
                                            action Show("_phone_image", dissolve, img=message)

                                    else:
                                        text "[message!t]"

                                add sender.icon:
                                    subpixel True yalign 0.0
                                    xysize (33, 33) fit "contain"

                            else:
                                add sender.icon:
                                    subpixel True yalign 0.0
                                    xysize (33, 33) fit "contain"

                                frame:
                                    background sender.get_textbox()

                                    if isinstance(thing, phone.PhoneImage):
                                        imagebutton style "empty":
                                            at transform:
                                                subpixel True
                                                xsize 1.0 fit "contain"

                                            idle message
                                            action Show("_phone_image", dissolve, img=message)

                                    else:
                                        text "[message!t]"
                    
                    elif isinstance(thing, phone.Label):
                        if not label:
                            $ label = True
                            null height gui.phone_message_label_null_height

                        add thing.to_text()
                    
                    else:
                        null

                if phone._currently_typing is not None and not phone._currently_typing.is_pov:
                    use _typing_indicator()
                
                showif phone._group_chat._page > 0:
                    textbutton _("Go Back"):
                        action (Function(phone._group_chat._page_down), SetField(phone._message_yadj, "value", 0.0), SetScreenVariable("label", False))
                        top_margin 5

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

transform typing_blink(delay):
    alpha 0.25
    pause delay

    block:
        ease 0.2 alpha 0.75
        pause 0.2
        ease 0.2 alpha 0.25
        pause 0.6
        repeat

screen _typing_indicator():
    style_prefix "phone_typing"

    hbox:
        frame style "phone_messages_frame":
            background phone.get_textbox("#f2f2f2")

            hbox:
                text "⚫" at typing_blink(0.0)
                text "⚫" at typing_blink(0.2)
                text "⚫" at typing_blink(0.4)
        
        text _("[phone._currently_typing.short_name!t] is typing...") style "phone_typing_istyping"
    
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

define -10 config.early_start_store = False

label _phone_register: # not used anymore but kept for backwards comptability
    return

default mc_sayo = phone.GroupChat("Sayori", "mod_assets/phone/sayori_icon.png", "mc_sayo")

init -1 python in phone:
    from store import config
    
    def register(f):
        config.start_callbacks.append(f)

    @register
    def __register_mc_sayo_messages():
        # using the object    v    we defaulted above
        register_group_chat(store.mc_sayo, "mc", "s")
        register_date("mc_sayo", 5, 2, 2022, 10, 11)
        register_message("mc_sayo", "s", _("Yo MC, can I come over to your house today???"))
    
    @register
    def __register_mc_sayo_messages_2():
        register_group_chat(GroupChat( # defining the gc directly
            "goofy ahh group chat", "mod_assets/phone/default_icon.png", "goofy"
        ), "mc", "s")
        register_date("goofy", 5, 20, 2022, 12, 32)
        register_label("goofy", "'Sayori' was added to the group chat")
        register_image("goofy", "mc", "mod_assets/phone/sayori_icon.png")
        register_message("goofy", "s", _("What the f-"))

init 10 python in phone:
    @config.start_callbacks.append
    def __sort_register_messages():
        global _data
        for key in _data:
            sort_messages(key)
