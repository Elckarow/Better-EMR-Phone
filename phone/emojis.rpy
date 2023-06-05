init -150 python in phone.emojis:
    from renpy import store
    from store import Transform
    from store.phone import config

    import string
    _NOT_ALLOWED_CHARACTERS = set(string.punctuation.strip("_") + " ")

    _emojis = { }

    def add(name, emoji):
        global _NOT_ALLOWED_CHARACTERS
        if set(name) & _NOT_ALLOWED_CHARACTERS:
            raise Exception("not a valid emoji name: {}".format(name))
        
        global _emojis
        _emojis[name] = renpy.displayable(emoji)
    
    add("clueless", config.basedir + "emojis/clueless.png")
    add("randomguy", config.basedir + "emojis/randomguy.png")
    
    def get(name):
        return _emojis[name]
    
    def _emoji_tag(tag, name):
        return [
            (renpy.TEXT_DISPLAYABLE, Transform(get(name), subpixel=True, ysize=1.0, fit="contain", yoffset=2))
        ]
    
    store.config.self_closing_custom_text_tags["emoji"] = _emoji_tag

    import re
    _tag_pattern = re.compile(r"\{emoji\=([a-zA-Z0-9_]*)\}")

    def format_emoji_tag(s):
        for emoji in _tag_pattern.findall(s): s = _tag_pattern.sub(":" + emoji + ":", s, 1)
        return s