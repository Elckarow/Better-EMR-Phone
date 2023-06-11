init -100 python in phone.discussion:
    from renpy import store
    from store import ui, pause
    from store.phone import config, show_layer_at, set_current_screen, format_date, format_time, emojis
    import datetime

    def sort_messages(key):
        global data
        data[character(key).key]["group_chats"].sort(key=lambda gc: group_chat(gc).date, reverse=True)
    
    def _check_for_tags(s):
        if renpy.filter_text_tags(s, allow=config.message_text_tags) != s:
            raise ValueError("only the following text tags are allowed:\n{}\n\ntext: '{}'".format("\n".join(config.message_text_tags), s))

    def discussion(gc):
        global _group_chat

        if gc is None:
            if _group_chat is not None:
                return
            else:
                raise Exception("group chat not given (no previous group chat was found)")

        if _group_chat is not None:
            raise Exception("preparing group chat while another convesation is going on")
        
        gc = group_chat(gc)

        if not gc._characters:
            raise Exception("group chat '{}' has no characters".format(gc.name))
        
        store._window_hide()
        
        _group_chat = gc
        _group_chat.unread = False

        set_current_screen("phone_discussion")
        show_layer_at("phone_discussion")
        renpy.show_screen("phone_discussion")
        renpy.with_statement(config.enter_transition)

        store._window_auto = True
    
    def end_discussion():
        store._window_hide()

        global _group_chat
        if _group_chat is None:
            raise Exception("ending discussion, but no discussion ever started")
            
        for key in _group_chat._characters:
            sort_messages(key)
        
        _group_chat = None

        show_layer_at([], reset=True)
        renpy.hide_screen("phone_discussion")
        renpy.with_statement(config.exit_transition)
        
        set_current_screen(None)
    
        store._window_auto = True

    class _Payload(object):
        def __init__(self, source, data, _type):
            self.source = source
            self.data = data
            if _type not in _PayloadTypes.ALL: raise Exception("'{}' is not a valid payload type".format(_type))
            self.type = _type
    
    def remove_text_tags(s):
        s = emojis.format_emoji_tag(s)
        return renpy.filter_text_tags(s, allow=())

    def message(sender, message, delay=None):
        store._window_hide()

        sender = character(sender)
        formatted_message = remove_text_tags(message)

        global _current_payload
        _current_payload = _Payload(sender.key, formatted_message, _PayloadTypes.TEXT)
        if _group_chat._page == 0:
            _yadjustment.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        pause(sender.get_typing_delay(formatted_message))
        store._dismiss_pause = _dismiss_pause

        register_message(_group_chat, sender, message)
        if _group_chat._page == 0:
            _yadjustment.value = float("inf")

        _current_payload = None

        store._window_auto = True
        pause(delay)

    def register_message(group, sender, text):
        _check_for_tags(text)

        group = group_chat(group)
        sender = character(sender)

        group._save_payload(_Payload(sender.key, text, _PayloadTypes.TEXT))

    def image(sender, image, time=2.0, delay=None):
        store._window_hide()

        sender = character(sender)

        global _current_payload
        _current_payload = _Payload(sender.key, image, _PayloadTypes.IMAGE)
        if _group_chat._page == 0:
            _yadjustment.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        pause(time)
        store._dismiss_pause = _dismiss_pause

        register_image(_group_chat, sender, image)
        if _group_chat._page == 0:
            _yadjustment.value = float("inf")
        
        _current_payload = None
        
        store._window_auto = True
        pause(delay)
    
    def register_image(group, sender, image):
        if not isinstance(image, basestring):
            raise TypeError("a phone image expects a string")

        group = group_chat(group)
        sender = character(sender)

        group._save_payload(_Payload(sender.key, image, _PayloadTypes.IMAGE))
    
    def label(label, delay=0.5):
        register_label(_group_chat, label)

        if _group_chat._page == 0:
            _yadjustment.value = float("inf")

        pause(delay)
    
    def register_label(group, label):
        _check_for_tags(label)

        group = group_chat(group)
        group._save_payload(_Payload(None, label, _PayloadTypes.LABEL), False)
    
    def date(month, day, year, hour, minute, delay=0.5):
        register_date(_group_chat, month, day, year, hour, minute)
        pause(delay)

    def register_date(group, month, day, year, hour, minute):
        group = group_chat(group)

        if (group.date.year, group.date.month, group.date.day) < (year, month, day):
            group._save_payload(_Payload(None, format_date(month, day, year), _PayloadTypes.DATE), False)
        
        group.date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        group._save_payload(_Payload(None, format_time(hour, minute), _PayloadTypes.DATE), False)

    def typing(sender, value, delay=None):
        sender = character(sender)

        if isinstance(value, basestring):
            value = sender.get_typing_delay(value)

        global _current_payload
        _current_payload = _Payload(sender.key, "", _PayloadTypes._DUMMY)
        if _group_chat._page == 0:
            _yadjustment.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        pause(value)
        store._dismiss_pause = _dismiss_pause

        if _group_chat._page == 0:
            _yadjustment.value = float("inf")
        
        _current_payload = None
        
        store._window_auto = True
        pause(delay)
    
    def choice(captions, delay=0.3):
        store._window_hide()

        global _current_payload
        _current_payload = _Payload(None, captions, _PayloadTypes._MENU)

        if _group_chat._page == 0:
            _yadjustment.value = float("inf")

        rv = ui.interact()

        _current_payload = None

        pause(delay)
        store._window_auto = True

        return captions.index(rv)

    def audio(sender, audio, time=2.0, delay=None):
        store._window_hide()

        sender = character(sender)

        global _current_payload
        _current_payload = _Payload(sender.key, audio, _PayloadTypes.AUDIO)
        if _group_chat._page == 0:
            _yadjustment.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        pause(time)
        store._dismiss_pause = _dismiss_pause

        register_audio(_group_chat, sender, audio)
        if _group_chat._page == 0:
            _yadjustment.value = float("inf")
        
        _current_payload = None
        
        store._window_auto = True
        pause(delay)
    
    def register_audio(group, sender, audio):
        if not isinstance(audio, basestring):
            raise TypeError("audio is expected to be a string")

        group = group_chat(group)
        sender = character(sender)

        group._save_payload(_Payload(sender.key, audio, _PayloadTypes.AUDIO))
    
    _yadjustment = ui.adjustment()

default -100 phone.discussion._current_payload = None
default -100 phone.discussion._group_chat = None

python early in phone.discussion._PayloadTypes: # fake enum because of the module not existing in python 2.7 (it's a 3.4 thing)
    _DUMMY = 0
    TEXT = 1
    IMAGE = 2
    LABEL = 3
    DATE = 4
    _MENU = 5
    AUDIO = 6
    VIDEO = 7

    ALL = (_DUMMY, TEXT, IMAGE, LABEL, DATE, _MENU, AUDIO, VIDEO)

    _constant = True

init python in phone.discussion:
    from store.phone.group_chat import group_chat
    from store.phone.character  import character

init python in phone:
    renpy_config.start_callbacks.append(lambda: setattr(discussion, "data", data))

init 1400 python in phone:
    @renpy_config.start_callbacks.append
    def __sort_register_messages():
        global data
        for key in data:
            discussion.sort_messages(key)