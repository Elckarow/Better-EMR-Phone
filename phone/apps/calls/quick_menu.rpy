screen phone_quick_menu():
    grid 3 2:
        style_prefix "phone_quick_menu"
        xalign 0.5 ypos 0.45

        vbox:
            imagebutton:
                idle phone.config.basedir + "quick_menu_history_idle.png"
                hover phone.config.basedir + "quick_menu_history_selected.png"
                selected_idle phone.config.basedir + "quick_menu_history_selected.png"
                action ShowMenu("history")
            text _("History")

        vbox:
            imagebutton:
                idle phone.config.basedir + "quick_menu_afm_idle.png"
                hover phone.config.basedir + "quick_menu_afm_selected.png"
                selected_idle phone.config.basedir + "quick_menu_afm_selected.png"
                action Preference("auto-forward", "toggle")
            text _("Auto")

        vbox:
            imagebutton:
                idle phone.config.basedir + "quick_menu_skip_idle.png"
                hover phone.config.basedir + "quick_menu_skip_selected.png"
                selected_idle phone.config.basedir + "quick_menu_skip_selected.png"
                action Skip()
            text _("Skip")

        vbox:
            imagebutton:
                idle phone.config.basedir + "quick_menu_settings_idle.png"
                hover phone.config.basedir + "quick_menu_settings_selected.png"
                selected_idle phone.config.basedir + "quick_menu_settings_selected.png"
                action ShowMenu("preferences")
            text _("Settings")

        vbox:
            imagebutton:
                idle phone.config.basedir + "quick_menu_save_idle.png"
                hover phone.config.basedir + "quick_menu_save_selected.png"
                selected_idle phone.config.basedir + "quick_menu_save_selected.png"
                action ShowMenu("save")
            text _("Save")

        vbox:
            imagebutton:
                idle phone.config.basedir + "quick_menu_load_idle.png"
                hover phone.config.basedir + "quick_menu_load_selected.png"
                selected_idle phone.config.basedir + "quick_menu_load_selected.png"
                action ShowMenu("load")
            text _("Load")

style phone_quick_menu_grid is empty:
    xspacing 31 yspacing 22

style phone_quick_menu_vbox is empty
style phone_quick_menu_text is phone_call_time:
    size 14