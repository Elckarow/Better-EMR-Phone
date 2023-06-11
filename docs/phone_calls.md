# Phone calls

*The following functions are defined in the* **`phone.calls`** *namespace (not **`phone.call`**, Ren'Py doesn't like me using that).*

Phone calls require a certain type of sayer. The need **those 3** properties:
- `screen` set to `"phone_say" `
- `who_style` set to `"phone_say_label"`
- `what_style` set to `"phone_say_dialogue"`

The rest is as usual.
```
define phone_eileen = Character("Eileen", screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
```

## Functions

`def call(caller)`
Starts a phone call with the `*character*` `caller`. 
Replaces the `narrator` with a special narrator.
The python equivalent of the `phone call` statement.

`def end_call()`
Ends the current phone call, and registers it for both `*character*`s (the caller and the current pov).
Sets the `narrator` back.
The python equivalent of the `phone end call` statement.

`def register_call(char1, char2, duration=None)`
Saves a call between the `*character*`s `char1` and `char2`. If `duration` is not `None`, it's a float, a number of seconds the call lasted. This is called automatically by the `phone.calls.end_call` function.

## Statements

`phone call`
Used to start a phone call. It expects a `*character*`.

`phone end call`
Used to end a phone call. It doesn't expect anything.

---
## Example

```
# define two phone sayers
define phone_s  = Character("Sayori", screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")
define phone_mc = Character("MC", screen="phone_say", who_style="phone_say_label", what_style="phone_say_dialogue")

# create the two phone characters
default pc_sayori = phone.character.Character("Sayori", phone.config.basedir + "sayori_icon.png", "s", 21, "#22Abf8")
default pc_mc     = phone.character.Character("MC", phone.config.basedir + "mc_icon.png", "mc", 35, "#484848")

label phone_call_test:
    phone call "s"
    phone_s "Ohayouuu!!!!!!!!!!!!!!!!"
    phone_mc "Hey!"
    "Why is she always this energetic?"
    phone end call
    "..."

    return
```