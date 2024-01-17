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
        
        gc = group_chat(gc)

        if not gc._characters:
            raise Exception("group chat '{}' has no characters".format(gc.name))
        
        store._window_hide()
        
        _group_chat = gc
        _group_chat.unread = False

        _yadjustment.value = float("inf")

        set_current_screen("phone_discussion")
        show_layer_at("phone_discussion")
        renpy.show_screen("phone_discussion")
        renpy.with_statement(config.enter_transition)

        store._window_auto = True
    
    def end_discussion():
        global _group_chat
        if _group_chat is None: return

        store._window_hide()
            
        for key in _group_chat._characters:
            sort_messages(key)

        if _group_chat.transient:
            _group_chat.clear()
            
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

    def _run_callbacks(gc, event, payload):
        callback_object = object()

        callback_object.source = payload.source
        callback_object.type = payload.type

        if payload.type == VIDEO:
            callback_object.data = None
        else:
            callback_object.data = payload.data

        for i in config.discussion_callbacks:
            i(gc, event, callback_object)

    def _discussion_coroutine():
        store._window_hide()

        global _current_payload
        _current_payload = payload = yield

        if _group_chat._page == 0:
            _yadjustment.value = float("inf")
        
        _run_callbacks(_group_chat, "start", payload)

        _dismiss_pause = store._dismiss_pause
        store._dismiss_pause = True
        p = yield
        pause(p)
        store._dismiss_pause = _dismiss_pause

        _run_callbacks(_group_chat, "end", payload)

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

        dc.send(_Payload(sender.key, formatted_message, TEXT))
        dc.send(sender.get_typing_delay(formatted_message))

        register_message(_group_chat, sender, message)
        
        dc.send(delay)

    def register_message(group, sender, text):
        _check_for_tags(text)

        group = group_chat(group)
        sender = character(sender)

        p = _Payload(sender.key, text, TEXT)
        group._save_payload(p)
        _run_callbacks(group, "save", p)

    def image(sender, image, time=2.0, delay=None):
        dc = _discussion_coroutine()
        dc.send(None)

        sender = character(sender)

        dc.send(_Payload(sender.key, image, IMAGE))
        dc.send(time)

        register_image(_group_chat, sender, image)
        
        dc.send(delay)
    
    def register_image(group, sender, image):
        group = group_chat(group)
        sender = character(sender)

        p = _Payload(sender.key, image, IMAGE)
        group._save_payload(p)
        _run_callbacks(group, "save", p)
    
    def label(label, delay=0.5):
        dc = _discussion_coroutine()
        dc.send(None)
        dc.send(_Payload(None, label, LABEL))
        dc.send(-1)

        register_label(_group_chat, label)

        dc.send(delay)
    
    def register_label(group, label):
        _check_for_tags(label)

        group = group_chat(group)

        p = _Payload(None, label, LABEL)
        group._save_payload(p, False)
        _run_callbacks(group, "save", p)
    
    def _register_date(group, month, day, year, hour, minute, second):
        group = group_chat(group)

        if (group.date.year, group.date.month, group.date.day) < (year, month, day):
            group._save_payload(_Payload(None, format_date(month, day, year), DATE), False)
        
        group.date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        group._save_payload(_Payload(None, format_time(hour, minute), DATE), False)

        _run_callbacks(group, "save", _Payload(None, (month, day, year, hour, minute, second), LABEL))
    
    def _get_date(group, month, day, year, hour, minute, second, auto):
        group = group_chat(group)

        current_gc_date = group.date
        current_date = phone.system.get_date()

        if auto:
            month = year = day = hour = minute = second = True

        if month is None:   month = current_gc_date.month
        elif month is True: month = current_date.month

        if day is None:   day = current_gc_date.day
        elif day is True: day = current_date.day

        if year is None:   year = current_gc_date.year
        elif year is True: year = current_date.year

        if hour is None:   hour = current_gc_date.hour
        elif hour is True: hour = current_date.hour

        if minute is None:   minute = current_gc_date.minute
        elif minute is True: minute = current_date.minute

        if second is None:   second = current_gc_date.second
        elif second is True: second = current_date.second

        return (month, day, year, hour, minute, second)
        
    def date(month, day, year, hour, minute, second, delay=0.5, auto=False):
        dc = _discussion_coroutine()
        dc.send(None)

        date_tuple = _get_date(_group_chat, month, day, year, hour, minute, second, auto)

        dc.send(_Payload(None, date_tuple, DATE))
        dc.send(-1)

        _register_date(_group_chat, *date_tuple)
        
        dc.send(delay)

    def register_date(group, month, day, year, hour, minute, second, auto=False):
        _register_date(group, *_get_date(group, month, day, year, hour, minute, second, auto))

    def typing(sender, value, delay=None):
        dc = _discussion_coroutine()
        dc.send(None)

        if isinstance(value, basestring):
            value = sender.get_typing_delay(value)

        dc.send(_Payload(sender.key, value, TYPING))
        dc.send(value)
        dc.send(delay)
    
    def choice(captions, delay=0.3):
        dc = _discussion_coroutine()
        dc.send(None)
        dc.send(_Payload(None, captions, MENU))

        rv = ui.interact()

        dc.send(delay)
        dc.send(-1)

        return captions.index(rv)

    def audio(sender, audio, time=2.0, delay=None):
        dc = _discussion_coroutine()
        dc.send(None)

        sender = character(sender)

        dc.send(_Payload(sender.key, audio, AUDIO))
        dc.send(time)

        register_audio(_group_chat, sender, audio)
        
        dc.send(delay)
    
    def register_audio(group, sender, audio):
        if not isinstance(audio, basestring):
            raise TypeError("audio is expected to be a string")

        group = group_chat(group)
        sender = character(sender)

        p = _Payload(sender.key, audio, AUDIO)
        group._save_payload(p)
        _run_callbacks(group, "save", p)
    
    _yadjustment = ui.adjustment()

default -100 phone.discussion._current_payload = None
default -100 phone.discussion._group_chat = None

python early in phone.discussion._PayloadTypes: # fake enum because of the module not existing in python 2.7 (it's a 3.4 thing)
    TYPING = 0
    TEXT = 1
    IMAGE = 2
    LABEL = 3
    DATE = 4
    MENU = 5
    AUDIO = 6
    VIDEO = 7

    ALL = (TYPING, TEXT, IMAGE, LABEL, DATE, MENU, AUDIO, VIDEO)

    renpy.store.phone.discussion.TYPING = TYPING
    renpy.store.phone.discussion.TEXT = TEXT
    renpy.store.phone.discussion.IMAGE = IMAGE
    renpy.store.phone.discussion.LABEL = LABEL
    renpy.store.phone.discussion.DATE = DATE
    renpy.store.phone.discussion.MENU = MENU
    renpy.store.phone.discussion.AUDIO = AUDIO
    renpy.store.phone.discussion.VIDEO = VIDEO

    _constant = True

init python in phone.discussion:
    from store.phone.group_chat import group_chat
    from store.phone.character  import character

init 1400 python in phone:
    @renpy.partial(execute_default, id="__sort_register_messages")
    def __sort_register_messages():
        global data
        for key in data:
            discussion.sort_messages(key)