init -100 python in phone.character:
    from renpy import store
    from store import Color, __, RoundedFrame
    from store.phone import config

    # The max lenght of a *character*'s name shortened.
    character_short_name_length = 16

    # A number of seconds added to the pause before each message.
    message_delay = 0.6

    class Character(object):
        def __init__(self, name, icon, key, cps, color):
            global _characters
            _characters[key] = self

            self.name = name
            self.icon = icon

            self.cps = int(cps)
            self.color = Color(color)

            if key is None: raise ValueError("key may not be 'None'")
            self.key = key

        def get_textbox(self):
            return get_textbox(self.color)
        
        @property
        def short_name(self):
            global character_short_name_length
            name = __(self.name)
            if len(name) > character_short_name_length:
                name = name[:character_short_name_length - 3] + "..."
            
            return name
        
        @property
        def is_pov(self):
            return self.key == store.pov_key
        
        def get_typing_delay(self, message, substitute=True):
            global message_delay
            if substitute: message = renpy.substitute(message)
            return (len(message) / self.cps) + message_delay
        
        def __hash__(self):
            return hash(self.key)
        
    def character(x):
        if isinstance(x, Character): return x
        global _characters
        if x is None: x = store.pov_key
        return _characters[x]
    
    def has_character(key):
        global _characters
        return key in _characters
    
    def get_textbox(color):
        return RoundedFrame(color, radius=config.textbox_radius)

default phone.character._characters = { }