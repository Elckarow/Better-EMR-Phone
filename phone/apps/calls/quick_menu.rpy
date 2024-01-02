screen phone_quick_menu():
    grid 3 2 style_prefix "phone_quick_menu":
        vbox:
            imagebutton:
                idle phone.asset("quick_menu_history_idle.png")
                hover phone.asset("quick_menu_history_selected.png")
                selected_idle phone.asset("quick_menu_history_selected.png")
                action ShowMenu("history")
            text _("History")

        vbox:
            imagebutton:
                idle phone.asset("quick_menu_afm_idle.png")
                hover phone.asset("quick_menu_afm_selected.png")
                selected_idle phone.asset("quick_menu_afm_selected.png")
                action Preference("auto-forward", "toggle")
            text _("Auto")

        vbox:
            imagebutton:
                idle phone.asset("quick_menu_skip_idle.png")
                hover phone.asset("quick_menu_skip_selected.png")
                selected_idle phone.asset("quick_menu_skip_selected.png")
                action Skip()
            text _("Skip")

        vbox:
            imagebutton:
                idle phone.asset("quick_menu_settings_idle.png")
                hover phone.asset("quick_menu_settings_selected.png")
                selected_idle phone.asset("quick_menu_settings_selected.png")
                action ShowMenu("preferences")
            text _("Settings")

        vbox:
            imagebutton:
                idle phone.asset("quick_menu_save_idle.png")
                hover phone.asset("quick_menu_save_selected.png")
                selected_idle phone.asset("quick_menu_save_selected.png")
                action ShowMenu("save")
            text _("Save")

        vbox:
            imagebutton:
                idle phone.asset("quick_menu_load_idle.png")
                hover phone.asset("quick_menu_load_selected.png")
                selected_idle phone.asset("quick_menu_load_selected.png")
                action ShowMenu("load")
            text _("Load")

style phone_quick_menu_grid is empty:
    xspacing 31 yspacing 22

style phone_quick_menu_vbox is empty
style phone_quick_menu_text is phone_call_time:
    size 14

screen phone_quick_menu_video():
    default qm = False
    default anim_time = 0.35

    showif qm:
        add "#000":
            at transform:
                alpha 0.0
                on show:
                    ease anim_time alpha 0.35
                on hide:
                    ease anim_time alpha 0.0

    vbox style "empty" yalign 1.0 xsize 1.0 xfill True:
        button style "empty" padding (5, 7, 5, 4) xalign 0.5:
            at transform:
                ease anim_time matrixtransform RotateMatrix(0, 0, 180 * qm) matrixcolor OpacityMatrix(0.8 if qm else 0.6)
            
            action ToggleLocalVariable("qm")

            add phone.asset("arrow_icon.png"):
                at transform:
                    subpixel True xysize (70, 18)
                        
        showif qm:
            frame style "empty" top_padding 30 bottom_padding 15 xsize 1.0 modal True:
                at transform:
                    subpixel True crop (0, 0, 1.0, 0.0)
                    on show:
                        ease anim_time crop (0, 0, 1.0, 1.0) alpha 1.0
                    on hide:
                        ease anim_time crop (0, 0, 1.0, 0.0) alpha 0.0

                background "#00000060"

                vbox style "empty" xalign 0.5:
                    use phone_quick_menu()

                    null height 15

                    add phone.asset("hang_up.png"):
                        subpixel True xysize (63, 63) xalign 0.5