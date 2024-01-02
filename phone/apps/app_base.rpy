screen app_base(action=NullAction()):
    style_prefix "app_base"

    frame:
        ysize 50 + (gui.phone_status_bar_height * bool(phone.config.status_bar))
        top_padding 10 + (gui.phone_status_bar_height * bool(phone.config.status_bar))
        textbutton _("< Back"):
            action (action, PhoneReturn())
            sensitive phone.menu
        
        transclude

style app_base_frame is empty:
    background "#F2F2F2"
    xfill True
    xpadding 10
    bottom_padding 10

style app_base_hbox is empty:
    spacing 5
    align (0.5, 0.5)

style app_base_text is empty:
    outlines [ ]
    yalign 0.5
    color "#000" size 19
    font phone.asset("Aller_Rg.ttf")

style app_base_button is empty:
    yalign 0.5
    xalign 0.0

style app_base_button_text is app_base_text:
    color "#0094FF" 
    size 18 