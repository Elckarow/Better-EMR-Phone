# System

*The following functions and variables are defined in the* **`phone.system`** *namespace.*

`def get_battery_level()`
Returns the battery level. If the variable `battery_level` is `None`, the value is taken from the player's device.

`def get_internet_connection_state()`
Returns the state of the internet connection, represented by the following constants:
- `CONNECTED` wifi is on and connected to the internet
- `NO_INTERNET` wifi is on but no internet connection
- `NOT_CONNECTED` wifi is off
- `AIRPLANE_MODE` airplane mode is on
- `CELLULAR_DATA` wifi is off and cellular data is on

`def get_date()`
Returns the date. If the variable `date` is `None`, the date used is the player's.

`date` *(defaults to `None`)*
If not `None`, a `datetime.datetime` object.

`battery_level` *(defaults to `None`)*
If not `None`, an integer.

`wifi` *(defaults to `None`)*
If not `None`, a boolean.

`locked` *(defaults to `False`)*
If true, some `Action`s (notably in the status bar screen) won't do anything, preventing the player from changing variables when they're not supposed to.

`at_list` *(defaults to `[]`)*
A transform or list of transforms applied to the phone screen (overlay screens excluded). Set back to `[]` when exiting the phone.

`cellular_data` *(defaults to `False`)*
Is cellular data on?

`airplane_mode` *(defaults to `False`)*
Is airplane mode on?

`bluetooth` *(defaults to `False`)*
Is bluetooth on?

`internet_connection` *(defaults to `True`)*
This can be turned on/off for more a realistic gameplay (say the main character is in a very rural place, they won't have access to the internet).

Other variables (`flashlight`, `rotation_locked`, `dark_mode`) currently don't have any use and should not be used by creators.