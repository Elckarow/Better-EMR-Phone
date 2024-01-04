screen phone_discussion():
    use _phone():
        side "t b c":
            use app_base(action=(SetField(phone.discussion, "_group_chat", None), Function(phone.discussion.audio_messages.reset))):
                style_prefix "app_base"

                hbox:
                    add phone.discussion._group_chat.icon at _fits(36) yalign 0.5
                    text phone.short_name(phone.discussion._group_chat.name, 9)

            use _chat_textbox()
            use _chat_messages()


init -100 python in phone.discussion:
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
            if phone.discussion._current_payload is not None and phone.discussion._current_payload.source is not None:
                $ sender = phone.character.character(phone.discussion._current_payload.source)
                if (
                    sender.is_pov and
                    phone.discussion._current_payload.type == phone.discussion._PayloadTypes.TEXT
                ):
                    fixed style "empty":
                        yfill True
                        xsize 0.9

                        viewport at phone.discussion._AutoScrollVP style "empty":
                            draggable False
                            mousewheel False
                            yalign 0.5

                            frame style "phone_textbox_typing_text_frame":
                                add renpy.display.layout.AdjustTimes(
                                        Text(
                                            phone.discussion._current_payload.data,
                                            style="phone_textbox_text",
                                            slow_cps=sender.cps,
                                        ),
                                        None,
                                        None
                                    )
                else:
                    text _("Type a message.") color "#666"
                # ugly ahh
            else:
                text _("Type a message.") color "#666"

            text _("Send") color "#0094FF" xalign 1.0
            

style phone_textbox_frame is empty:
    ysize 50 xfill True
    background "#F2F2F2"
    padding (10, 10)

style phone_textbox_side is empty:
    xfill True
    yfill True

style phone_textbox_text is empty:
    outlines [ ]
    size 16
    color "#000"
    line_leading 0
    line_spacing 0
    font phone.asset("Aller_Rg.ttf")
    yalign 0.5
    layout "nobreak"

style phone_textbox_typing_text_frame is empty:
    yfill True


screen _chat_message(p):
    style_prefix "phone_messages"

    $ sender = phone.character.character(p.source)

    hbox:
        # sus but hey
        if sender.is_pov:
            xalign 1.0

            frame:
                background sender.get_textbox()
                transclude

            add sender.icon at _fits(33) yalign 0.0

        else:
            add sender.icon at _fits(33) yalign 0.0

            frame:
                background sender.get_textbox()
                transclude

screen _chat_messages():
    style_prefix "phone_messages"

    $ _label = False

    viewport style "empty" at Flatten:
        yadjustment phone.discussion._yadjustment
        draggable True
        mousewheel True
        yinitial 1.0
        yalign 1.0
        yfill True

        frame style "empty":
            yalign 1.0
            padding (10, 10)

            vbox:
                if phone.discussion._group_chat._can_load_more():
                    textbutton _("Load More"):
                        action (
                            Function(phone.discussion._group_chat._page_up),
                            SetField(phone.discussion._yadjustment, "value", float("inf")),
                            Function(phone.discussion.audio_messages.reset)
                        )
                        bottom_margin 5

                for i, p in enumerate(phone.discussion._group_chat._get_messages()):
                    if p.type in (phone.discussion._PayloadTypes.LABEL, phone.discussion._PayloadTypes.DATE):
                        if not _label:
                            $ _label = True
                            if i != 0:
                                null height gui.phone_message_label_null_height

                        text p.data style "phone_messages_text_label"
                    
                    else:
                        if _label:
                            $ _label = False
                            null height gui.phone_message_label_null_height

                        if p.type == phone.discussion._PayloadTypes.TEXT:                        
                            use _chat_message(p):
                                text p.data

                        elif p.type == phone.discussion._PayloadTypes.IMAGE:
                            use _chat_message(p):
                                imagebutton:
                                    at transform:
                                        xsize 1.0 subpixel True
                                        fit "scale-down"

                                    idle p.data
                                    action Show("_phone_image", Dissolve(0.5), img=p.data)

                        elif p.type == phone.discussion._PayloadTypes.AUDIO:
                            use _chat_message(p):
                                hbox style_prefix "phone_messages_audio":
                                    button at _fits(0.8), Transform(yalign=0.5):
                                        add DynamicDisplayable(phone.discussion.audio_messages.button_image, p=p)
                                        action Function(phone.discussion.audio_messages.play_audio, p, p.data),
                                    
                                    add phone.asset("audio_message_wave_icon.png"):
                                        at _fits(None), phone.discussion.audio_messages.AudioWave(p)

                        else:
                            null

                if phone.discussion._group_chat._page == 0:
                    if phone.discussion._current_payload is not None:
                        if phone.discussion._current_payload.type == phone.discussion._PayloadTypes.MENU:
                            if _label:
                                $ _label = False
                                null height gui.phone_message_label_null_height
                            
                            for i, caption in enumerate(phone.discussion._current_payload.data):
                                frame style "empty":
                                    at transform: # support for versions that can't have `at` and `at transform` at the same time
                                        subpixel True alpha 0.0 xoffset -20 xalign 1.0
                                        i / 9
                                        ease_quad 0.35 alpha 1.0 xoffset 0

                                    textbutton caption at CurriedRoundedCorners(radius=phone.config.textbox_radius):
                                        style_prefix "phone_messages_choice"
                                        action Return(caption)
                                                
                        else:
                            $ sender = phone.character.character(phone.discussion._current_payload.source)
                            if sender.is_pov:
                                if _label and phone.discussion._current_payload.type != phone.discussion._PayloadTypes.TEXT:
                                    $ _label = False
                                    null height gui.phone_message_label_null_height

                                if phone.discussion._current_payload.type == phone.discussion._PayloadTypes.IMAGE:
                                    use _chat_message(phone.discussion._current_payload):
                                        text _("{u}{i}Loading Image...{i}{/u}")
                                
                                elif phone.discussion._current_payload.type == phone.discussion._PayloadTypes.AUDIO:
                                    use _chat_message(phone.discussion._current_payload):
                                        text _("{u}{i}Loading Audio...{i}{/u}")

                                elif phone.discussion._current_payload.type == phone.discussion._PayloadTypes.VIDEO:
                                    use _chat_message(phone.discussion._current_payload):
                                        text _("{u}{i}Loading Video...{i}{/u}")

                            else:    
                                if _label:
                                    $ _label = False
                                    null height gui.phone_message_label_null_height

                                use _phone_message_typing(sender)
                
                if phone.discussion._group_chat._page > 0:
                    textbutton _("Go Back"):
                        action (
                            Function(phone.discussion._group_chat._page_down),
                            SetField(phone.discussion._yadjustment, "value", 0.0),
                            Function(phone.discussion.audio_messages.reset)
                        )
                        top_margin 5

screen _phone_image(img):
    modal True
    add Solid("#000")

    add img:
        align (0.5, 0.5)
    
    key ["mouseup_1", "mouseup_3"] action Hide("_phone_image", Dissolve(0.5))

style phone_messages_button is empty:
    xalign 0.5

style phone_messages_button_text is phone_say_dialogue:
    xalign 0.5
    text_align 0.5
    ypos 0.0
    size 16
    color "#000"

style phone_messages_vbox is empty:
    spacing 5
    yalign 1.0
    xfill True 

style phone_messages_hbox is empty:
    spacing 5

style phone_messages_text is empty:
    outlines [ ]
    size 19
    line_leading 0
    line_spacing 0
    layout "greedy"
    font phone.asset("Aller_Rg.ttf")
    hyperlink_functions hyperlink_functions_style("phone_messages_text_hyperlink")

style phone_messages_text_hyperlink is phone_messages_text:
    hover_underline True

style phone_messages_frame is empty:
    xmaximum 240
    padding gui.phone_message_frame_padding

style phone_messages_text_label is phone_messages_text:
    color "#000"
    xalign 0.5 text_align 0.5
    size 15
    xsize 0.8

style phone_messages_choice_button is phone_messages_frame:
    background "#eeeeee"
    hover_background "#b4b4b4"
    padding (12, 8)

style phone_messages_choice_button_text is phone_messages_text:
    color "#000"
    outlines [ ]
    yalign 0.5
    size 18
    layout "tex"

style phone_messages_audio_hbox is empty:
    spacing 8
    ysize 40

style phone_messages_audio_button is empty