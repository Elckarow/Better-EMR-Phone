# /!\ default
# pc as in phone character :monikk:
default pc_sayori  = phone.character.Character("Sayori", phone.config.basedir + "sayori_icon.png", "s", 21, "#22Abf8")
default pc_mc      = phone.character.Character("MC", phone.config.basedir + "mc_icon.png", "mc", 35, "#484848")
default pc_yuri    = phone.character.Character("Yuri", phone.config.basedir + "yuri_icon.png", "y", 20, "#a327d6")
default pc_monika  = phone.character.Character("Monika", phone.config.basedir + "monika_icon.png", "m", 40, "#0a0")
default pc_natsuki = phone.character.Character("Natsuki", phone.config.basedir + "natsuki_icon.png", "n", 45, "#fbb")

default pov_key = "mc"

define phone_s  = Character("Sayori", screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
define phone_mc = Character("MC", screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")

init 100 python in phone.application:
    add_app_to_all_characters(message_app)
    add_app_to_all_characters(call_history_app)
    add_app_to_all_characters(calendar_app)

init 100 python in phone.calendar:
    june_2023_calendar = Calendar(6, 2023, MONDAY)
    add_calendar_to_all_characters(june_2023_calendar)
    june_2023_calendar[30].description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed finibus libero vel ligula dictum eleifend. Fusce pellentesque, lacus a venenatis bibendum, neque lacus pretium arcu, eu porttitor nunc neque ut justo. Cras ornare semper ligula, non sodales nibh tincidunt sit amet. Cras ornare, ligula id pulvinar bibendum, sem lacus malesuada augue, lobortis lobortis lorem nisl eget ante. Morbi turpis purus, semper sed semper sed, pretium vel lectus. Mauris quis ipsum id eros scelerisque pellentesque eu a quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aliquam justo odio, vehicula ut tellus vitae, consequat commodo tellus. Curabitur blandit lorem sed nulla tempor, viverra malesuada felis finibus. Sed imperdiet ultricies mi et aliquet. Donec facilisis eget augue eu finibus."

init phone register:
    define "Welcome":
        add "s" add "mc" add "y" add "m" add "n"
        icon phone.config.basedir + "default_icon.png"
        as thanks_for_using_my_framework key "ddu"

label phone_discussion_test:
    phone discussion "ddu":
        time year 2023 month 6 day 5 hour 16 minute 30 # exact date and time at which i wrote this. yes i am feeling quite silly and goofy
        label "'Sayori' has been added to the group"
        label "'MC' has been added to the group"
        label "'Yuri' has been added to the group"
        label "'Monika' has been added to the group"
        label "'Natsuki' has been added to the group"
        "m" "Hey there!"
        "n" "Thank you for using my framework."
        "n" "I mean {i}of course{/i} you're using {b}this{/b} framework."
        "n" "...not like there are any better ones out there~"
        "s" "natsuki!!!!!"
        "s" "no being a meanie!!!!!!!"
        "y" "If you are interested in DDLC mods, be sure to check out our mod {a=https://undercurrentsmod.weebly.com}Doki Doki Undercurrents{/a}!"
        "mc" "In case you encounter an issue (or wanna make a suggestion),"
        "mc" "please DM me at Elckarow#8399 or open an issue on {a=https://github.com/Elckarow/Better-EMR-Phone}GitHub{/a}."
    phone end discussion

    return

label phone_call_test:
    phone call "s"
    phone_s "Ohayouuu!!!!!!!!!!!!!!!!"
    phone_mc "Hey!"
    "Why is she always this energetic?"
    phone end call
    "..."

    return