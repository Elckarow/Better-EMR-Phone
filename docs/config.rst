Configuration Variables
=======================

*The following variables are defined in the* **phone.config** *namespace.*

**This namespace is considered *constant* and should not be modified outside of init time.**

``basedir = "phone/assets/"``
    A path from the game folder to the directory where the assets are located.

``overlay_screens = [...]``
    A list of screen names shown above the phone screens (but still inside the phone). As the framework uses it internally, creators should ``append`` their screen name to the list rather than replacing it entirely.

``quick_menu = True``
    If true, the framework's quick menu is used during phone calls. If false, the game's quick menu is used.

``enter_transition = Dissolve(0.6, time_warp=_warper.ease)``
    A transition used when showing the phone.

``exit_transition = Dissolve(0.6, time_warp=_warper.ease)``
    A transition used when hiding the phone.

``intra_transition = Dissolve(0.1)``
    A transition used when going from a phone screen to another.

``time_format = _("%H:%M")``
    A string used to format a time. Passed to ``time.strftime``.

``date_format = _("%m/%d/%Y")``
    A string used to format a date. Passed to ``datetime.datetime.strftime``.

``textbox_radius = 15``
    The radius of the rounded corners of the text messages' textboxes.

``call_history_lenght = 20``
    How many phone calls we save.

``message_text_tags = set(...)``
    A set of text tags that are allowed in text messages. They should not affect the text's size.

``status_bar = True``
    If true, the phone uses the status bar. If false, it doesn't.

``hide_status_bar_screens = [...]``
    A list of screen names. When the status bar is used, it is hidden when any of these screens are showing.

``layer_at_transforms = {...}``
    A dictionary mapping a screen name to a transform or a list of transforms. When a phone screen is shown, the screen name is looked up in the map (None is used if not found), and the layer "master" is shown at those transforms using ``phone.show_layer_at``.

``applications_pages = 4``
    How many "pages" of application we use in the ``phone`` screen.

``lowest_brightness = 0.3``
    From 0.0 (complete darkness) to 1.0 (normal), how low can the brightness go?

``data = {...}``
    A dictionnary mapping a name to a callable. Each \*character\* has an entry (their key) containing these values in the ``phone.data`` dictionnary. When the entry is created, the callables are called without arguments, and the values are set.
    tl;dr ``collections.defaultdict``
    The following keys are documented:
    
    * ``"call_history"``
    * ``"group_chats"``
    * ``"background_image"``
    * ``"calendars"``
    * ``"applications"``

``discussion_callbacks = [...]``
    A list of functions that are called whenever a phone discussion function executes.
    They are called with three arguments:

    * the ``*group chat*`` the interaction is taking place in.
    * an event:
  
      * ``"start"`` is delivered at the start of the interaction.
      * ``"end"`` is delivered just before the data has been saved.
      * ``"save"`` is delivered after the data has been saved (called after the ``register_`` function associated to what's happening).

    * an object representing the data, which has thefollowing fields:
        
      * ``source``, the ``*character*`` that's sending the data, or ``None``.
      * ``type``, one of the following constants (in the ``phone.discussion`` namespace): ``TYPING``, ``TEXT``, ``IMAGE``, ``LABEL``, ``DATE``, ``MENU``, ``AUDIO``, ``VIDEO`` (if it ever gets implemented).
      * ``data``:
  
        * For a typing, the time to wait for.             
        * For a text message, the text that's been formatted by ``phone.discussion.remove_text_tags``.             
        * For an image, the displayable.
        * For a label, the text.
        * For a date, a tuple of (``month``, ``day``, ``year``, ``hours``, ``minutes``, ``seconds``).
        * For a menu, a list of all the captions.
        * For an audio, the string of the audio.
        * For a video, ``None``.

``video_call_layer = "phone_video_call"``
    The name of the layer usied in video calls. It is appended to ``config.detached_layers``

``video_call_layer_transform_properties = {...}``
    A dict of transform properties applied to the ``Layer`` displayable (not the layer itself) used during a video call. The default dict centers the displayable and makes it fit the phone vertically.

``messages_displayed = 100``
    How many messages we display at the same time.

``messages_fill_if_lower = 30``
    If the next "load" of messages contains this many or less messages, add those messages to the current load.
    
``message_delay = 0.6``
    A number of seconds added to the pause before each message.

``unread_group_chat_pov = False``
    If true, a group chat's "unreadness" is determined on the pov the group chat was read in.
    I.e, if the group chat was read in the "mc" pov, then it won't be marked as read in the "s" pov.
    If false, it is determined by whether the player has opened the group chat or not.

``auto_emojis = True``
    If true, will define all images found in "assets/emojis" as emojis.

``default_label_delay = 0.5``
    The default value of the `delay` property for the `time` and `label` discussion statements.