init -100 python in phone.discussion:
    from renpy import store
    from store import ui, pause, phone
    from store.phone import config, show_layer_at, set_current_screen, format_date, format_time, emojis
    import datetime

    def sort_messages(key):
        phone.data[character(key).key]["group_chats"].sort(key=lambda gc: group_chat(gc).date, reverse=True)
    
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

    def _discussion_coroutine():
        store._window_hide()

        global _current_payload
        _current_payload = yield
        if _group_chat._page == 0:
            _yadjustment.value = float("inf")

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        p = yield
        pause(p)
        store._dismiss_pause = _dismiss_pause

        if _group_chat._page == 0:
            _yadjustment.value = float("inf")

        _current_payload = None

        store._window_auto = True
        delay = yield
        pause(delay)

        yield None

    def message(sender, message, delay=None):
        dc = _discussion_coroutine()
        dc.send(None)

        sender = character(sender)
        formatted_message = remove_text_tags(message)

        dc.send(_Payload(sender.key, formatted_message, _PayloadTypes.TEXT))
        dc.send(sender.get_typing_delay(formatted_message))

        register_message(_group_chat, sender, message)
        
        dc.send(delay)

    def register_message(group, sender, text):
        _check_for_tags(text)

        group = group_chat(group)
        sender = character(sender)

        group._save_payload(_Payload(sender.key, text, _PayloadTypes.TEXT))

    def image(sender, image, time=2.0, delay=None):
        dc = _discussion_coroutine()
        dc.send(None)

        sender = character(sender)

        dc.send(_Payload(sender.key, image, _PayloadTypes.IMAGE))
        dc.send(time)

        register_image(_group_chat, sender, image)
        
        dc.send(delay)
    
    def register_image(group, sender, image):
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
        current_gc_date = _group_chat.date
        current_date = phone.system.get_date()

        if month is None:   month = current_gc_date.month
        elif month is True: month = current_date.month

        if day is None:   day = current_gc_date.day
        elif day is True: day = current_date.day

        if year is None:   year = current_gc_date.year
        elif year is True: year = current_date.year

        if hour is None:   hour = current_gc_date.hour
        elif hour is True: hour = current_date.hour

        if minute is None: minute = current_gc_date.minute
        elif minute is True: minute = current_date.minute

        register_date(_group_chat, month, day, year, hour, minute)
        pause(delay)

    def register_date(group, month, day, year, hour, minute):
        group = group_chat(group)

        if (group.date.year, group.date.month, group.date.day) < (year, month, day):
            group._save_payload(_Payload(None, format_date(month, day, year), _PayloadTypes.DATE), False)
        
        group.date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        group._save_payload(_Payload(None, format_time(hour, minute), _PayloadTypes.DATE), False)

    def typing(sender, value, delay=None):
        dc = _discussion_coroutine()
        dc.send(None)

        if isinstance(value, basestring):
            value = sender.get_typing_delay(value)

        dc.send(_Payload(sender.key, "", _PayloadTypes._DUMMY))
        dc.send(value)
        dc.send(delay)
    
    def choice(captions, delay=0.3):
        dc = _discussion_coroutine()
        dc.send(None)
        dc.send(_Payload(None, captions, _PayloadTypes._MENU))

        rv = ui.interact()

        dc.send(delay)
        dc.send(-1)

        return captions.index(rv)

    def audio(sender, audio, time=2.0, delay=None):
        dc = _discussion_coroutine()
        dc.send(None)

        sender = character(sender)

        dc.send(_Payload(sender.key, audio, _PayloadTypes.AUDIO))
        dc.send(time)

        register_audio(_group_chat, sender, audio)
        
        dc.send(delay)
    
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

init 1400 python in phone:
    @renpy_config.start_callbacks.append
    def __sort_register_messages():
        global data
        for key in data:
            discussion.sort_messages(key)