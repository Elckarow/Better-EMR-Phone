init -100 python in phone.status_bar:
    from renpy import store
    from store import Text, Transform, Null, TintMatrix, phone, __
    config = phone.config
    system = phone.system

    def time_displayable(st, at):
        return Text(system.get_date().strftime(__(config.time_format)), style="_phone_status_bar_text"), 0.1

    def battery_text_displayable(st, at):
        return Text("{}%".format(system.get_battery_level()), style="_phone_status_bar_text"), 0.1
    
    EMPTY = 0
    ONE_FOURTH = 1
    HALF = 2
    THREE_FOURTH = 3
    NINE_TENTH = 4 
    FULL = 5

    _battery_displayables = {
        EMPTY:        renpy.displayable(config.basedir + "status_bar_battery_empty.png"),
        ONE_FOURTH:   renpy.displayable(config.basedir + "status_bar_battery_one_fourth.png"),
        HALF:         renpy.displayable(config.basedir + "status_bar_battery_half.png"),
        THREE_FOURTH: renpy.displayable(config.basedir + "status_bar_battery_three_fourth.png"),
        NINE_TENTH:   renpy.displayable(config.basedir + "status_bar_battery_nine_tenth.png"),
        FULL:         renpy.displayable(config.basedir + "status_bar_battery_full.png"),
    }

    def battery_displayable(st, at):
        battery_level = system.get_battery_level()

        REDRAW = 0.5

        if battery_level == 0:
            return _battery_displayables[EMPTY], REDRAW

        if battery_level <= 33: # bamboozled
            return _battery_displayables[ONE_FOURTH], REDRAW
        
        if battery_level <= 66:
            return _battery_displayables[HALF], REDRAW
        
        if battery_level <= 80:
            return _battery_displayables[THREE_FOURTH], REDRAW
        
        if battery_level <= 90:
            return _battery_displayables[NINE_TENTH], REDRAW

        return _battery_displayables[FULL], REDRAW
    
    internet_connection_displayables = {
        system.CONNECTED:     Transform(config.basedir + "wifi_icon.png", crop=(0.0, 35, 1.0, 110), crop_relative=True, subpixel=True),
        system.NO_INTERNET:   Null(),
        system.NOT_CONNECTED: Null(),
        system.AIRPLANE_MODE: renpy.displayable(config.basedir + "airplane_icon.png"),
        system.CELLULAR_DATA: Text(_("LTE"), style="_phone_status_bar_text"),
    }

    def internet_connection_displayable(st, at):
        return internet_connection_displayables[system.get_internet_connection_state()], 0.1
        
    def bluetooth_displayable(st, at):
        if system.airplane_mode or not system.bluetooth: return Null(), 0.5
        return config.basedir + "bluetooth_icon.png", 0.5

screen _phone_status_bar():
    default control_center = False

    if phone.config.status_bar and phone.get_current_screen() not in phone.config.hide_status_bar_screens:
        showif not control_center:
            button style_prefix "_phone_status_bar":
                at transform:
                    subpixel True
                    parallel:
                        on idle:
                            matrixcolor BrightnessMatrix(0.0)
                        on hover:
                            matrixcolor BrightnessMatrix(0.3)
                    parallel:
                        on appear:
                            yanchor 0.0 alpha 1.0
                        on show:
                            ease_quad 0.4 yanchor 0.0 alpha 1.0
                        on hide:
                            ease 0.2 yanchor 1.0 alpha 0.0

                hbox xalign 0.0:
                    add DynamicDisplayable(phone.status_bar.internet_connection_displayable) at _fits(0.6) yalign 0.5

                add DynamicDisplayable(phone.status_bar.time_displayable) xalign 0.5

                hbox xalign 1.0:
                    add DynamicDisplayable(phone.status_bar.bluetooth_displayable) at _fits(0.7) yalign 0.5
                    null width 2
                    add DynamicDisplayable(phone.status_bar.battery_text_displayable)
                    add DynamicDisplayable(phone.status_bar.battery_displayable) at _fits(0.74) yalign 0.5

                action (SetLocalVariable("control_center", True), SetField(phone.system, "at_list", _phone_control_center))
        
        else:
            add "#c4c4c438":
                at transform:
                    on show:
                        alpha 0.0
                        ease_quad 0.3 alpha 1.0
                    on hide:
                        easeout 0.2 alpha 0.0

            fixed style_prefix "_phone_control_center":
                at transform:
                    subpixel True
                    xalign 1.0 yanchor 0.0
                    on show:
                        alpha 0.0 zoom 0.98 offset (5, -2)
                        ease_quad 0.3 alpha 1.0 offset (0, 0) zoom 1.0
                    on hide:
                        easeout 0.2 alpha 0.0 zoom 0.98 offset (5, -2)

                frame style "empty" modal True:
                    button:
                        style "empty" xfill True yfill True
                        action (SetLocalVariable("control_center", False), SetField(phone.system, "at_list", _phone_status_bar))

                hbox at Flatten:
                    xalign 0.5 yanchor 1.0 ypos 0.98

                    vbox:
                        use _phone_control_center_block(cols=2, rows=2, layout="grid"):
                            button at _fits_block align (0.5, 0.5):
                                add phone.asset("airplane_icon.png")
                                action If(
                                    phone.system.locked,
                                    NullAction(),
                                    ToggleVariable("phone.system.airplane_mode")
                                )

                            button at _fits_block align (0.5, 0.5):
                                add phone.asset("cellular_data_icon.png")
                                action If(
                                    phone.system.locked,
                                    NullAction(),
                                    If(
                                        not phone.system.airplane_mode,
                                        ToggleVariable("phone.system.cellular_data")
                                    )
                                )
                                selected_background Transform(phone.asset("circle.png"), matrixcolor=TintMatrix("#35C759"), subpixel=True, fit="contain")
                                padding (90, 90)

                            button at _fits_block align (0.5, 0.5):
                                add phone.asset("wifi_icon.png")
                                action (
                                    If(
                                        phone.system.locked,
                                        NullAction(),
                                        If(
                                            not phone.system.airplane_mode,
                                            If(
                                                phone.system.wifi is not None,
                                                ToggleVariable("phone.system.wifi"),
                                                NullAction()
                                            )
                                        )
                                    ),
                                    SelectedIf(phone.system.get_internet_connection_state() == phone.system.CONNECTED),
                                    SensitiveIf(phone.system.locked or not phone.system.airplane_mode)
                                )
                            
                            button at _fits_block align (0.5, 0.5):
                                add phone.asset("bluetooth_icon.png")
                                action If(
                                    phone.system.locked,
                                    NullAction(),
                                    If(
                                        not phone.system.airplane_mode,
                                        ToggleVariable("phone.system.bluetooth"),
                                    )
                                )

                        hbox:
                            use _phone_control_center_block():
                                button at _fits_block align (0.5, 0.5):
                                    if phone.system.rotation_locked:
                                        add phone.asset("rotation_locked_icon.png")
                                    else:
                                        add phone.asset("rotation_unlocked_icon.png")
                                    action ToggleVariable("phone.system.rotation_locked")

                            use _phone_control_center_block():
                                button at _fits_block align (0.5, 0.5):
                                    add phone.asset("moon_icon.png")
                                    action ToggleVariable("phone.system.dark_mode")
                        
                        use _phone_control_center_block(cols=2):
                            button at _yfits_block:
                                style "empty" align (0.5, 0.5)
                                hbox style "empty" yfill True:
                                    add phone.asset("screen_mirroring_icon.png") at _yfits(0.67) yalign 0.5
                                    null width 10
                                    text _("Screen\nMirroring") size 14 yalign 0.5
                                
                                action NullAction()
                        
                        hbox:
                            use _phone_control_center_block():
                                button at _fits_block align (0.5, 0.5):
                                    add phone.asset("flashlight_icon.png")
                                    action ToggleVariable("phone.system.flashlight")
                                    padding (30, 30)

                            use _phone_control_center_block():
                                button at _fits_block align (0.5, 0.5):
                                    add phone.asset("timer_icon.png")
                                    action NullAction()
                                    padding (30, 30) hover_background None

                    vbox:
                        use _phone_control_center_block(cols=2, rows=2):
                            text _("Music"):
                                xalign 0.5 text_align 0.5 
                                ycenter 0.27 size 18
                            
                            hbox style "empty":
                                xalign 0.5 ycenter 0.73
                                spacing 10

                                button style "empty" yalign 0.5:
                                    text "▸▸":
                                        at transform:
                                            subpixel True alpha 0.5
                                            xzoom -1
                                        size 25
                                    action NullAction()
                                
                                imagebutton:
                                    xysize (50, 50)
                                    selected_idle  Transform(phone.asset("play_icon.png"), fit="contain", subpixel=True, align=(0.5, 0.5))
                                    selected_hover Transform(phone.asset("play_icon.png"), fit="contain", subpixel=True, align=(0.5, 0.5))

                                    if renpy.music.get_playing("phone_music") is None:
                                        idle Transform(phone.asset("play_icon.png"), fit="contain", subpixel=True, align=(0.5, 0.5))
                                        action (NullAction(), SelectedIf(False))
                                    else:
                                        idle Transform(phone.asset("pause_icon.png"), fit="contain", subpixel=True, align=(0.5, 0.5))
                                        action PauseAudio("phone_music", "toggle")

                                button style "empty" yalign 0.5:
                                    text "▸▸":
                                        at transform:
                                            subpixel True alpha 0.5
                                        size 25
                                    action NullAction()
                            
                        hbox:
                            use _phone_control_center_block(rows=2):
                                vbar value FieldValue(phone.system, "brightness", 1.0 - phone.config.lowest_brightness, offset=phone.config.lowest_brightness)
                                add phone.asset("sun_icon.png"):
                                    at transform:
                                        subpixel True xysize (0.5, 0.5) fit "contain"
                                        xalign 0.5 yalign 0.75
                                        matrixcolor TintMatrix("#9b9b9b")

                            use _phone_control_center_block(rows=2):
                                                                # epic breh
                                vbar value MixerValue("phone") style "_phone_control_center_vbar"
                                add DynamicDisplayable(
                                    lambda st, at: (
                                        (
                                            phone.asset("volume_icon_0.png")
                                            if get_mixer("phone") == 0.0
                                            else phone.asset("volume_icon_1.png")
                                            if get_mixer("phone") < 0.5
                                            else phone.asset("volume_icon_2.png")
                                        ),
                                        0.1
                                    )
                                ):
                                    at transform:
                                        subpixel True xysize (0.4, 0.4) fit "contain"
                                        xalign 0.5 yalign 0.75
                                        matrixcolor TintMatrix("#9b9b9b")
                        
                        hbox:
                            use _phone_control_center_block():
                                button at _fits_block align (0.5, 0.5):
                                    add phone.asset("calculator_icon.png")
                                    action NullAction()
                                    padding (30, 30) hover_background None

                            use _phone_control_center_block():
                                button at _fits_block align (0.5, 0.5):
                                    add phone.asset("camera_icon.png")
                                    action NullAction()
                                    padding (30, 30) hover_background None

screen _phone_control_center_block(cols=1, rows=1, layout="empty"):
    frame at (CurriedRoundedCorners(radius=gui.phone_control_center_block_rounded_corners_radius), Flatten):
        # https://github.com/renpy/renpy/issues/4666
        if is_renpy_version_or_above(7, 6, 1):
            xysize (
                absolute((gui.phone_control_center_block_size * cols) + (gui.phone_control_center_spacing * (cols - 1))),
                absolute((gui.phone_control_center_block_size * rows) + (gui.phone_control_center_spacing * (rows - 1)))
            )
        else:
            xysize (
                int((gui.phone_control_center_block_size * cols) + (gui.phone_control_center_spacing * (cols - 1))),
                int((gui.phone_control_center_block_size * rows) + (gui.phone_control_center_spacing * (rows - 1)))
            )
        style_prefix "_phone_control_center_block"
        
        if layout == "empty":
            transclude
        elif layout == "vbox":
            vbox:
                transclude
        elif layout == "hbox":
            hbox:
                transclude
        elif layout == "grid":
            grid cols rows:
                allow_underfull True
                transclude

transform _phone_control_center:
    easeout 0.3 blur 22.0

transform _phone_status_bar:
    ease 0.3 blur 0.0

init 1400 python in phone.config:
    overlay_screens.append("_phone_status_bar") 

style _phone_status_bar_button is empty:
    ysize gui.phone_status_bar_height
    xsize 1.0 xpadding 12
    background "#0000008f"
    hover_background "#00000079"

style _phone_status_bar_hbox is empty:
    yfill True 
    spacing 2

style _phone_status_bar_text is empty:
    color "#fff" outlines [ ]
    size 12 line_spacing 0 
    yalign 0.5
    font phone.asset("Aller_Rg.ttf")

transform _fits_block(factor=gui.phone_control_center_block_scaling_factor):
    _fits(absolute(gui.phone_control_center_block_size * factor))

transform _xfits_block(factor=gui.phone_control_center_block_scaling_factor):
    _xfits(absolute(gui.phone_control_center_block_size * factor))

transform _yfits_block(factor=gui.phone_control_center_block_scaling_factor):
    _yfits(absolute(gui.phone_control_center_block_size * factor))

style _phone_control_center_text is empty:
    color "#fff" outlines []
    font "DejaVuSans.ttf"
    size 20 line_spacing 0

style _phone_control_center_fixed is empty

style _phone_control_center_hbox is empty:
    spacing gui.phone_control_center_spacing

style _phone_control_center_vbox is empty:
    spacing gui.phone_control_center_spacing

image _phone_control_center_bar = "#fafafa"

style _phone_control_center_bar is empty:
    left_bar "_phone_control_center_bar"

style _phone_control_center_vbar is empty:
    bar_vertical True
    bottom_bar "_phone_control_center_bar"

style _phone_control_center_button is empty:
    padding (70, 70)
    background             None
    hover_background       Transform(phone.asset("circle.png"), matrixcolor=TintMatrix("#5a5a5a"), subpixel=True, fit="contain")
    selected_background    Transform(phone.asset("circle.png"), matrixcolor=TintMatrix("#007BFA"), subpixel=True, fit="contain")
    insensitive_background Transform(phone.asset("circle.png"), matrixcolor=TintMatrix("#b1b1b1"), subpixel=True, fit="contain")

style _phone_control_center_block_frame is empty:
    modal True
    background "#000000d0"

style _phone_control_center_block_base_box is empty:
    spacing int(gui.phone_control_center_spacing + (gui.phone_control_center_block_size * (1.0 - gui.phone_control_center_block_scaling_factor) * 0.5))
    align (0.5, 0.5)

style _phone_control_center_block_hbox is _phone_control_center_block_base_box:
    yfill True
style _phone_control_center_block_vbox is _phone_control_center_block_base_box:
    xfill True
style _phone_control_center_block_grid is _phone_control_center_block_base_box