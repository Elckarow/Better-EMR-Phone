init offset = -120

init python in phone.system:
    from renpy import store
    
    from pygame_sdl2.power import get_power_info    
    def get_battery_level():
        if battery_level is not None: return int(battery_level)
        return max(get_power_info().percent, 0)

    from socket import gethostbyname, gethostname
    CONNECTED = 1
    NO_INTERNET = 2
    NOT_CONNECTED = 3
    AIRPLANE_MODE = 4
    CELLULAR_DATA = 5

    renpy.const("phone.system.CONNECTED")
    renpy.const("phone.system.NO_INTERNET")
    renpy.const("phone.system.NOT_CONNECTED")
    renpy.const("phone.system.AIRPLANE_MODE")
    renpy.const("phone.system.CELLULAR_DATA")

    def get_internet_connection_state():
        if airplane_mode: return AIRPLANE_MODE

        _wifi = wifi
        if _wifi is None:
            _wifi = gethostbyname(gethostname()) != "127.0.0.1"

        if not _wifi:
            if cellular_data: return CELLULAR_DATA
            return NOT_CONNECTED

        if not internet_connection: return NO_INTERNET
        return CONNECTED
    
    from datetime import datetime
    def get_date():
        if date is not None: return date
        return datetime.now()

# If any of these "If not `None`" values are `None`, they're taken from the player's device.
default phone.system.date = None # If not `None`, a `datetime.datetime` object.
default phone.system.battery_level = None # If not `None`, an integer.
default phone.system.wifi = None # If not `None`, a boolean.

# If true, some actions (notably in the status bar screen) won't do anything, preventing the player
# from changing variables when they're not supposed to.
default phone.system.locked = False

default phone.system.airplane_mode = False
default phone.system.bluetooth = False
default phone.system.rotation_locked = False
default phone.system.cellular_data = False
default phone.system.internet_connection = True # Phone wifi can be on, yet no internet connection.
default phone.system.at_list = [] # A transform or list of transforms applied to the phone screen (overlay screens excluded).
default phone.system.dark_mode = False # `False` by default ew
default phone.system.flashlight = False # should've named it "flashbang" smh

# read only
default phone.system.brightness = 1.0 # [phone.config.lowest_brightness, 1.0]