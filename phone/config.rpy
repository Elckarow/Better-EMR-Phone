python early in phone.config:
    from renpy import store
    from store import Dissolve, _warper, _, phone, Transform
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
    layer_at_transforms = { }
    # `None` is set later

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

init -1400 python in phone.config:
    from store import BrightnessMatrix
    layer_at_transforms[None] = Transform(matrixcolor=BrightnessMatrix(-0.03), blur=5)