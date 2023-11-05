init -100 python in phone.character:
    from renpy.store import store, Color, __, RoundedFrame, phone
    from store.phone import config

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

            # deprecated
            self.short_name = short_name

        def get_textbox(self):
            return get_textbox(self.color)
            
        @property
        def is_pov(self):
            return self.key == store.pov_key
        
        def get_typing_delay(self, message, substitute=True, translate=True):
            if substitute: message = renpy.substitute(message, translate=translate)
            return (len(message) / self.cps) + config.message_delay
        
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

    def get_all():
        global _characters
        return list(_characters.values())

default phone.character._characters = { }