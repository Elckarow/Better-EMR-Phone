init -100 python in phone.calls:
    from store import Text
    def _call_time(st, at):
        global _call_time_st; _call_time_st = st # breh. st might not be the same when loading
        return Text(time.strftime("%M:%S", time.gmtime(st)), style="phone_call_time"), 0.0

default phone.calls._call_time_st = 0.0

screen phone_call(video=False):
    use _phone(xpos=gui.phone_call_xpos, xanchor=0.0):
        add Solid("#302D29")

        if video and is_renpy_version_or_above(7, 6, 0): # _phone_video_call uses the `Layer` displayable
            use _phone_video_call()
        else:
            use _phone_call()
    
    if not phone.config.quick_menu and quick_menu:
        use quick_menu()

screen _phone_call():
    style_prefix "phone_call"

    vbox:
        text phone.short_name(phone.calls._current_caller.name, 12)
        add DynamicDisplayable(phone.calls._call_time)

    frame:            
        add phone.calls._current_caller.icon at _fits(None)

    if phone.config.quick_menu and quick_menu:
        frame style "empty" xalign 0.5 ypos 0.45:
            use phone_quick_menu()

    add phone.asset("hang_up.png"):
        subpixel True xysize (63, 63)
        xalign 0.5 ypos 0.8

style phone_call_vbox is empty:
    spacing 3
    ypos 0.05
    xfill True

style phone_call_text is empty:
    xalign 0.5
    text_align 0.5
    outlines [ ]
    line_spacing 0
    size 24
    font phone.asset("Aller_Rg.ttf")
    hyperlink_functions hyperlink_functions_style("phone_call_text_hyperlink")

style phone_call_text_hyperlink is phone_call_text:
    hover_underline True

style phone_call_time is phone_call_text:
    size 16

style phone_call_frame is empty:
    background CircleDisplayable(2)
    xysize (           120,                   120) # :)
    padding (int(22 * (120 / 404)), int(22 * (120 / 404)))
    ypos 0.18
    xalign 0.5

screen _phone_video_call():
    style_prefix "phone_video_call"

    add Layer(phone.config.video_call_layer):
        at Transform(**phone.config.video_call_layer_transform_properties)
    
    vbox:
        text _("Facetime - [phone.calls._current_caller.name!t]")
        add DynamicDisplayable(phone.calls._call_time)
    
    use phone_quick_menu_video()

style phone_video_call_vbox is phone_call_vbox:
    ypos 0.03

style phone_video_call_text is phone_call_text:
    size 27