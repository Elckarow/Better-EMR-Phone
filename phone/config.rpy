python early in phone.config:
    from renpy.store import store, config as renpy_config, Dissolve, _warper, _, phone, Transform
    _constant = True

    # Where the assets are located.
    basedir = "phone/assets/"

    # A list of screen names. Those screens are shown above the phone screens (but still inside the phone).
    overlay_screens = [ ]

    # Do we use the game's quick menu or the phone's quick menu during phone calls?
    quick_menu = True

    # A transition used when showing the phone.
    enter_transition = Dissolve(0.6, time_warp=_warper.ease)

    # A transition used when hiding the phone.
    exit_transition = Dissolve(0.6, time_warp=_warper.ease)

    # A transition used when going from a phone screen to another.
    intra_transition = Dissolve(0.1)

    # A string used to format a time. Passed to `time.strftime`.
    time_format = _("%H:%M")

    # A string used to format a date. Passed to `datetime.datetime.strftime`.
    date_format = _("%m/%d/%Y")

    # The radius of the rounded corners of the textboxes.
    textbox_radius = 15

    # How many calls do we save?
    call_history_lenght = 20

    # A set of text tags that are allowed in text messages.
    # They should not change the size of the text.
    message_text_tags = {
        "emoji", "alpha", "color", "u", "i", "b", "a"
    } 

    # Use the status bar?
    status_bar = True

    # Hide the status bar when any of those screens are showing.
    hide_status_bar_screens = [ ]

    # A dictionary mapping screen names to transforms or lists of transforms.
    # When a phone screen is shown, the screen name is looked up in the map (None is used if not found),
    # and the layer "master" is shown at those transforms.
    layer_at_transforms = {
        None: Transform(matrixcolor=renpy.display.matrix.Matrix([1, 0, 0, -0.03, # BrightnessMatrix(-0.03)
                                                                0, 1, 0, -0.03,
                                                                0, 0, 1, -0.03,
                                                                0, 0, 0, 1]),
                        blur=2
                )
    }

    # How many "pages" of application we use in the `phone` screen.
    applications_pages = 4

    # A dictionnary mapping a name to a callable.
    # Each *character* has an entry (their key) containing these values in the `phone.data` dictionnary.
    # When the entry is created, the callables are called without arguments, and the values are set.
    # tl;dr collections.defaultdict
    data = {
        "call_history": list,
        "group_chats": list,
        "background_image": lambda: None,
        "calendars": list,
        "group_chat_unread_pov": dict
    }

    def _generate_applications_dict():
        rv = {
            i: phone.application._generate_applications_page()
            for i in range(applications_pages)
        }
        rv[None] = phone.application._generate_bottom_applications_page()
        rv["max"] = 0
        return rv
    
    data["applications"] = _generate_applications_dict

    # From 0.0 (complete darkness) to 1.0 (normal), how low can the brightness go?
    lowest_brightness = 0.3

    # A list of functions that are called whenever a phone discussion function executes.
    # They are called with three arguments:
    #     -the *group chat* the interaction is taking place in.
    #     -an event:
    #          `"start"` is delivered at the start of the interaction.
    #          `"end"` is delivered just before the data has been saved.
    #          `"save"` is delivered after the data has been saved (called after the `register_` function associated to what's happening). 
    #     -an object representing the data, which has the following fields:
    #          `source`, the *character* that's sending the data, or `None`.
    #          `type`, one of the following constants (in the `phone.discussion` namespace):
    #               `TYPING`, `TEXT`, `IMAGE`, `LABEL`, `DATE`, `MENU`, `AUDIO`, `VIDEO` (if it ever gets implemented).
    #          `data`:
    #               -For a typing, the time to wait for.             
    #               -For a text message, the text that's been formatted by `phone.discussion.remove_text_tags`.             
    #               -For an image, the displayable.
    #               -For a label, the text.
    #               -For a date, a tuple of (`month`, `day`, `year`, `hours`, `minutes`, `seconds`).
    #               -For a menu, a list of all the captions.
    #               -For an audio, the string of the audio.
    #               -For a video, `None`.
    discussion_callbacks = [ ]

    # The name of the layer usied in video calls. It is appended to `config.detached_layers`
    video_call_layer = "phone_video_call"

    # A dict of transform properties applied to the `Layer` displayable used during a video call. 
    video_call_layer_transform_properties = {
        "align": (0.5, 1.0),
        "ysize": 1.0,
        "fit": "contain"
    }
    
    # How many messages we display at the same time.
    messages_displayed = 100

    # If the next "load" of messages contains this many or less messages, add those messages to the current load.
    messages_fill_if_lower = 30

    # A number of seconds added to the pause before each message.
    message_delay = 0.6

    # An index. The default calendar used when the `phone_calendars` screen is shown.
    # If `True`, tries to retrieve the calendar that's in concordance to `phone.system.get_date()`.
    default_calendar_index = -1

    # If true, a group chat's "unreadness" is determined on the pov the group chat was read in.
    # I.e, if the group chat was read in the "mc" pov, then it won't be marked as read in the "s" pov.
    # If false, it is determined by whether the player has opened the group chat or not.
    unread_group_chat_pov = False

    # If true, will define all images found in "assets/emojis" as emojis.
    auto_emojis = True

    # The default value of the `delay` property for the `time` and `label` discussion statements.
    default_label_delay = 0.5

python early: # prevent "default"
    config.special_namespaces["store.phone.config"] = type(config.special_namespaces["store.config"])(phone.config, "phone.config")

init 1500 python in phone:
    @renpy_config.after_load_callbacks.append
    def __ensure_phone_data_entries():
        changed = False
        for d in data.values():
            for thing, f in config.data.items():
                if thing not in d:
                    d[thing] = f()
                    changed = True
        if changed:
            renpy.block_rollback()