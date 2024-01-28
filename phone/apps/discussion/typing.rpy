transform _phone_message_typing(delay):
    alpha 0.25
    pause delay

    block:
        ease 0.2 alpha 0.75
        pause 0.2
        ease 0.2 alpha 0.25
        pause 0.6
        repeat

screen _phone_message_typing(sender):
    style_prefix "phone_typing"

    hbox:
        frame:
            hbox:
                text "⚫" at _phone_message_typing(0.0)
                text "⚫" at _phone_message_typing(0.2)
                text "⚫" at _phone_message_typing(0.4)
        
        text __("{short_name} is typing...").format(short_name=phone.short_name(sender.name, 9)) style "phone_typing_istyping" yalign 0.5

style phone_typing_hbox is empty:
    spacing 3

style phone_typing_frame is phone_messages_frame:
    background phone.character.get_textbox("#f2f2f2")

style phone_typing_text is phone_messages_text:
    color "#000"
    font "DejaVuSans.ttf"

style phone_typing_istyping is empty:
    color "#626262"
    outlines [ ]
    size 16
    font phone.asset("Aller_Rg.ttf")

init python:
    if is_renpy_version_or_above(7, 7, 0):
        style.phone_typing_text.emoji_font = None