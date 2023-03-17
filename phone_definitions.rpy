init offset = 5

define phone.quick_menu = True
define phone.textbox_radius = 15

define phone.enter_transition = Dissolve(0.6, time_warp=_warper.ease)
define phone.exit_transition = Dissolve(0.6, time_warp=_warper.ease)

define phone.character_short_name_length = 16

define phone.group_chat_short_name_length = 9
define phone.group_chat_messages_displayed = 175
define phone.group_chat_messages_fill_if_lower = 15

define phone.message_delay = 0.6
define phone.message_time_pattern = _("{hour}:{minute}")
define phone.message_date_pattern = _("{month}/{day}/{year}")

# /!\ default
default phone.sayori  = phone.Character("Sayori", "mod_assets/phone/sayori_icon.png", "s", 21, "#22Abf8")
default phone.mc      = phone.Character("MC", "mod_assets/phone/mc_icon.png", "mc", 35, "#484848")
default phone.natsuki = phone.Character("Natsuki", "mod_assets/phone/natsuki_icon.png", "n", 45, "#fbb")
default phone.monika  = phone.Character("Monika", "mod_assets/phone/monika_icon.png", "m", 40, "#0a0")
default phone.yuri    = phone.Character("Yuri", "mod_assets/phone/yuri_icon.png", "y", 20, "#a327d6")

default pov_key = "mc"

define phone_s = Character("Sayori", screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")

init offset = 0


