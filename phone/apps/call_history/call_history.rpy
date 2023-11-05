screen phone_call_history():
    default call_history = phone.data[pov_key]["call_history"]

    use _phone():
        style_prefix "phone_call_history"

        side "t c":
            use app_base():
                style_prefix "app_base"
                text _("Calls") xalign 0.5 text_align 0.5

            if not call_history:
                text _("No recent calls") style "phone_call_history_empty" align (0.5, 0.05)
            
            else:
                viewport:
                    draggable True
                    mousewheel True
                    yfill True

                    frame:
                        vbox:
                            for i, entry in enumerate(call_history):
                                $ char = phone.character.character(entry.caller)

                                if i != 0:
                                    add Solid("#000"):
                                        xysize (1.0, 1) nearest True 

                                button:
                                    action NullAction()

                                    hbox:
                                        add char.icon at _fits(46) yalign 0.5   

                                        fixed:
                                            hbox style "empty" yalign 0.2 spacing 10:
                                                text phone.short_name(char.name, 26) 
                                                if entry.duration is not None:
                                                    text "-"
                                                    text entry._duration_to_str()

                                            text __("The {date} at {time}").format(
                                                date=phone.format_date(entry.date.month, entry.date.day, entry.date.year),
                                                time=phone.format_time(entry.date.hour, entry.date.minute)
                                            ):
                                                style "phone_call_history_date_text" yalign 1.0

style phone_call_history_side is phone_contacts_side
style phone_call_history_frame is phone_contacts_frame
style phone_call_history_vbox is phone_contacts_vbox
style phone_call_history_button is phone_contacts_button
style phone_call_history_fixed is empty
style phone_call_history_hbox is phone_contacts_hbox
style phone_call_history_text is phone_contacts_text:
    color "#000"

style phone_call_history_empty is phone_contacts_no_friends
style phone_call_history_date_text is phone_contacts_date_text