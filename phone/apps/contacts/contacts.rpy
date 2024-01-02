screen phone_contacts():
    default group_chats = phone.data[pov_key]["group_chats"]

    use _phone():
        style_prefix "phone_contacts"

        side "t c":
            use app_base():
                style_prefix "app_base"
                text _("Messages") xalign 0.5 text_align 0.5

            if not group_chats:
                text _("No group chats") style "phone_contacts_no_friends" align (0.5, 0.05)
            
            else:
                viewport:
                    draggable True
                    mousewheel True
                    yfill True

                    frame:
                        vbox:
                            for i, gc in enumerate(group_chats):
                                $ group_chat = phone.group_chat.group_chat(gc)

                                if i != 0:
                                    add Solid("#000"):
                                        xysize (1.0, 1) nearest True 

                                button:
                                    action (
                                        SetField(phone.discussion, "_group_chat", group_chat),
                                        SetField(group_chat, "unread", False),
                                        PhoneMenu("phone_discussion")
                                    )

                                    hbox:
                                        add group_chat.icon at _fits(46) yalign 0.5

                                        fixed:
                                            text phone.short_name(group_chat.name, 26) yalign 0.2:
                                                if group_chat.unread:
                                                    color "#000"

                                            text (
                                                _("The [group_chat._date_text] at [group_chat._hour_text]")
                                                if group_chat.number_of_messages != 0
                                                else _("Empty group chat")
                                            ):
                                                style "phone_contacts_date_text" yalign 1.0

style phone_contacts_side is empty:
    xfill True
    yfill True

style phone_contacts_frame is empty:
    padding (10, 0, 10, 0)

style phone_contacts_vbox is empty:
    xfill True
    spacing 0

style phone_contacts_button is empty:
    xfill True
    hover_background Solid("#e4e4e4")
    ysize 60
    padding (10, 7)

style phone_contacts_hbox is empty:
    spacing 6

style phone_contacts_text is empty:
    outlines [ ]
    color "#525252"
    size 18
    font phone.asset("Aller_Rg.ttf")

style phone_contacts_no_friends is phone_contacts_text:
    color "#000"
    size 20

style phone_contacts_date_text is phone_contacts_text:
    color "#9d9d9d"
    size 14