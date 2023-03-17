init python:
    """\
This part of the doc describes the different custom statements.
It's recommended to read the doc about the functions before getting here.

######################

`phone call`

Used to start a phone call. It expects a *character*.

example of use:
```
phone call "s"
```

######################

`phone end call`

Used to end a phone call. It doesn't expect anything.

example of use:
```
phone end call
```

######################

`phone discussion`

Used to start a phone discussion.
If a simple expression is given, it must be a *group chat*.
If no simple expression is given (or that None is given), it's assumed that a discussion is already going on,
and will therefore use the current group chat.

It expects a block which can contain the following statements:
    `image`
        The equivalent of the `phone.image` function. It expects a *character* and a string (the name of the image).
        It accepts the `time` property (defaults to 2.0), which is the time the image is being sent for.
        It accepts the `delay` property (default to None) which is the time to wait before the next statement executes

    `label`
        The equivalent of the `phone.label` function. It expects a string (the string is flagged as being translatable).
        It also accepts the delay property (defaults to 0.5).
    
    `time`
        The equivalent of the `phone.date` function. It expects at least one of the following property: year, month, day, hour, minute.
        If one of these is missing, it is retrieved from the current date registered.
        It also accepts the delay property (defaults to 0.5).
    
    `type`
        The equivalent of the `phone.typing` function. It expects a *character* and a `value` property, which can be a number or a string.
        The string is NOT flagged as translatable.
        It also accepts the delay property (defaults to None).
    
    ``
        The default statement, equivalent of the `phone.message` function. It expects a *character* and a string (flagged as translatable).
        It also accepts the delay property (defaults to None).

example of use:
```
phone discussion "mc_sayo":
    time year 2017 month 9 day 17 hour 14 minute 32
    image "mc" "bg room" time 1.0 delay 1.0
    "mc" "my new room"
    label "'Sayori' took a screenshot"
    "s" "nice! it's all cleaned, unlike mine"
    "mc" "send a pic"
    type "s" value 10.0

"2 hours later..."

phone discussion: # no *group chat* given.
    time hour 16 minute 40 # year, month and day are taken from the date given above
    "s" "shoot i feel asleep!" delay 1.0
    image "s" "bg s_room"
    "mc" "smh"
```

######################

`phone end discussion`

Used to end a phone discussion. It doesn't expect anything.

example of use:
```
phone end discussion
```

######################

`phone register`

Used to register messages in a group chat. It expects a *group chat* and a block (see the part about `phone discussion`).
It doesn't accept the `type` statement nor the `delay` property.

example of use:
```
phone register "mc_sayo":
    time day 18 hour 7 minute 10
    "mc" "wake up sleepy head!"
```

######################

`init phone register`

Used to register messages in a group chat at init time and / or create a new group chat.
The statement is run at init priority 15.

It if a *group chat* is given, it behaves the same way as the `phone register` statement.
If no *group chat* is given, the block expects a `define` clause.

The `define` clause expects a string, the name of the group chat, and a block, which can contain the following statements:
    `add`
        Expects a *character*. Will add this *character* to the group chat when created.
    
    `key`
        Expects a simple expression. The key of the group chat.
    
    `icon`
        Expects a string. The icon of the gorup chat.
    
    `as`
        Expects a dotted name. The group chat will be saved in the global store under this name.

example of use:
```
init phone register:
    define "Sayori":
        key "mc_sayo" add "mc" add "s"
        as mc_sayo_gc icon "mod_assets/Phone/sayori_icon.png"

init phone register "mc_sayo":
    time year 2016 month 12 day 26 hour 0 minute 24
    "mc" "merry christmas sayori. got a new phone"

init phone register:
    define "Monika":
        key "mc_monikk"
        add "mc"
        add "m"
        icon "mod_assets/Phone/monika_icon.png"
    time year 2016 month 12 day 26 hour 0 minute 30
    "mc" "merry christmas monika. got a new phone"
```

######################

That's it. Have fun using it!
If you encounter a bug or have any suggestion:
    -Open an issue on GitHub https://github.com/Elckarow/Phone
    -DM me at Elckarow#8399
"""

python early in parser_utils:
    Lexer = renpy.lexer.Lexer if renpy.version_tuple >= ((7, 6) if renpy.compat.PY2 else (8, 1)) else renpy.parser.Lexer

    def null_parser(l):
        """
        Expects an eol, no block, and returns `None`.
        """
        l.expect_eol()
        l.expect_noblock("")
        l.advance()
        return None
    
    def execute(rv):
        """
        Calls the `execute` method of the object passed.
        """
        rv.execute()

python early in phone:
    from renpy.store import parser_utils

    class _RawPhoneMessage(object):
        def __init__(self, sender, message, delay):
            self.sender = sender
            self.message = message
            self.delay = delay
        
        def execute(self):
            globals = store.__dict__
            message(
                eval(self.sender, globals),
                self.message,
                eval(self.delay, globals)
            )
    
    class _RawPhoneImage(object):
        def __init__(self, sender, image, time, delay):
            self.sender = sender
            self.image = image
            self.time = time
            self.delay = delay
        
        def execute(self):
            globals = store.__dict__
            image(
                eval(self.sender, globals),
                self.image,
                eval(self.time, globals),
                eval(self.delay, globals)
            )
    
    class _RawPhoneLabel(object):
        def __init__(self, label, delay):
            self.label = label
            self.delay = delay
        
        def execute(self):
            label(self.label, eval(self.delay, store.__dict__))
    
    class _RawPhoneDate(object):
        def __init__(self, kwargs, delay):
            self.kwargs = kwargs
            self.delay = delay
        
        def execute(self):
            kwargs = dict(self.kwargs)

            global _group_chat
            current_date = _group_chat.date

            for k, v in kwargs.items():
                if v is None:
                    kwargs[k] = getattr(current_date, k)

            date(delay=eval(self.delay, store.__dict__), **kwargs)

    class _RawPhoneDiscussion(object):
        def __init__(self, gc, statements):
            self.gc = gc
            self.statements = statements
        
        def execute(self):
            gc = self.gc
            if gc is not None: gc = group_chat(eval(gc, store.__dict__))
            discussion(gc)

            for statement in self.statements:
                statement.execute()
    
    class _RawPhoneTyping(object):
        def __init__(self, sender, value, delay):
            self.sender = sender
            self.value = value
            self.delay = delay
        
        def execute(self):
            globals = store.__dict__
            typing(
                eval(self.sender, globals),
                eval(self.value, globals),
                eval(self.delay, globals)
            )
    
    ############################

    def _parse_phone_message(ll, register):
        sender = ll.require(ll.simple_expression)
        message = ll.require(ll.string)

        if register: return sender, message

        delay = "None" if not ll.keyword("delay") else ll.require(ll.simple_expression)
        return sender, message, delay    

    def _parse_phone_image(ll, register):
        sender = ll.require(ll.simple_expression)
        image = ll.require(ll.string)

        if register: return sender, image

        time = None
        delay = None

        while not ll.eol():
            state = ll.checkpoint()
            kwarg = ll.require(ll.word)

            if kwarg == "time":
                if time is not None:
                    ll.revert(state)
                    ll.error("'time' property already given")
                time = ll.require(ll.simple_expression)
            
            elif kwarg == "delay":
                if delay is not None:
                    ll.revert(state)
                    ll.error("'delay' property already given")
                delay = ll.require(ll.simple_expression)
            
            else:
                ll.revert(state)
                ll.error("unknown property '{}'".format(kwarg))

        if time is None: time = "2.0"
        if delay is None: delay = "None"
        return sender, image, time, delay
    
    def _parse_phone_label(ll, register):
        label = ll.require(ll.string)

        if register: return label

        delay = "0.5" if not ll.keyword("delay") else float(ll.require(ll.float))
        return label, delay
    
    def _parse_phone_date(ll, register):
        kwargs = {time_thing: None for time_thing in ("month", "day", "year", "hour", "minute")}

        while True:
            state = ll.checkpoint()
            t = ll.require(ll.word)

            if t not in kwargs:
                ll.revert(state)
                ll.error("'{}' isn't a valid property for the 'time' statement".format(t))

            if kwargs[t] is not None:
                ll.revert(state)
                ll.error("'{}' already given".format(t))

            kwargs[t] = int(ll.require(ll.integer))

            if ll.eol():
                break

        if register:
            return kwargs

        delay = "0.5" if not ll.keyword("delay") else ll.require(ll.simple_expression)
        return kwargs, delay
    
    def _parse_phone_typing(ll):
        sender = ll.require(ll.simple_expression)

        value = None
        delay = None

        while True:
            state = ll.checkpoint()
            kwarg = ll.require(ll.word)

            if kwarg == "value":
                if value is not None:
                    ll.revert(state)
                    ll.error("'value' property already given")
                value = ll.require(ll.simple_expression)
            
            elif kwarg == "delay":
                if delay is not None:
                    ll.revert(state)
                    ll.error("'delay' property already given")
                delay = ll.require(ll.simple_expression)
            
            else:
                ll.revert(state)
                ll.error("unknown property '{}'".format(kwarg))

            if ll.eol():
                break
        
        if value is None: ll.error("expected 'value' property not found")
        if delay is None: delay = "None"
        return sender, value, delay


    def _parse_phone_discussion(l):
        gc = None

        if not l.match(":"):
            gc = l.require(l.simple_expression)
            l.require(":")
        
        l.expect_eol()
        l.expect_block("phone discussion")
        ll = l.subblock_lexer()

        statements = [ ]

        while ll.advance():
            if ll.keyword("image"):
                statement = _RawPhoneImage(*_parse_phone_image(ll, False))

            elif ll.keyword("label"):
                statement = _RawPhoneLabel(*_parse_phone_label(ll, False))

            elif ll.keyword("time"):
                statement = _RawPhoneDate(*_parse_phone_date(ll, False))
            
            elif ll.keyword("type"):
                statement = _RawPhoneTyping(*_parse_phone_typing(ll))
            
            else:
                statement = _RawPhoneMessage(*_parse_phone_message(ll, False))

            statements.append(statement)

            ll.expect_eol()
        
        return _RawPhoneDiscussion(gc, statements)
    
    def _translation_strings_phone_discussion(rd):
        rv = [ ]
        for statement in rd.statements:
            if isinstance(statement, _RawPhoneMessage):
                rv.append(statement.message)
            elif isinstance(statement, _RawPhoneLabel):
                rv.append(statement.label)
        return rv
    
    def _predict_phone_discussion(rd):
        renpy.predict_screen("phone_message")
        return [ ]

    renpy.register_statement(
        "phone discussion",
        block=True,
        parse=_parse_phone_discussion,
        execute=parser_utils.execute,
        translation_strings=_translation_strings_phone_discussion,
        predict=_predict_phone_discussion,
    )       

    ########################################################

    def _execute_phone_end_discussion(rv):
        end_discussion()

    renpy.register_statement(
        "phone end discussion",
        parse=parser_utils.null_parser,
        execute=_execute_phone_end_discussion
    )

    ########################################################

    def _parse_phone_call(l):
        rv = l.require(l.simple_expression)
        l.expect_eol()
        l.expect_noblock("phone call")
        return rv

    def _execute_phone_call(c):
        c = character(eval(c, store.__dict__))
        call(c)
    
    def _predict_phone_call(c):
        renpy.predict_screen("phone_call")
        return [ ]

    renpy.register_statement(
        "phone call",
        parse=_parse_phone_call,
        execute=_execute_phone_call,
        predict=_predict_phone_call
    )

    ########################################################

    def _execute_phone_end_call(rv):
        end_call()

    renpy.register_statement(
        "phone end call",
        parse=parser_utils.null_parser,
        execute=_execute_phone_end_call
    )

    ########################################################

    class _RawPhoneRegisterMessage(object):
        def __init__(self, sender, message):
            self.sender = sender
            self.message = message

        def execute(self, gc):
            register_message(
                gc,
                eval(self.sender, store.__dict__),
                self.message
            )
    
    class _RawPhoneRegisterImage(object):
        def __init__(self, sender, image):
            self.sender = sender
            self.image = image

        def execute(self, gc):
            register_image(
                gc,
                eval(self.sender, store.__dict__),
                self.image
            )
    
    class _RawPhoneRegisterLabel(object):
        def __init__(self, label):
            self.label = label
        
        def execute(self, gc):
            register_label(gc, self.label)
    
    class _RawPhoneRegisterDate(object):
        def __init__(self, kwargs):
            self.kwargs = kwargs
        
        def execute(self, gc):
            kwargs = dict(self.kwargs)

            current_date = gc.date

            for k, v in kwargs.items():
                if v is None:
                    kwargs[k] = getattr(current_date, k)

            register_date(gc, **kwargs)
    
    class _RawPhoneRegister(object):
        def __init__(self, gc, statements):
            self.gc = gc
            self.statements = statements
        
        def execute(self):
            gc = group_chat(eval(self.gc, store.__dict__))

            for statement in self.statements:
                statement.execute(gc)
    
    ############################
    
    def _parse_phone_register(l):
        gc = l.require(l.simple_expression)

        l.require(":")
        l.expect_eol()
        l.expect_block("phone register")
        ll = l.subblock_lexer()
        
        statements = [ ]

        while ll.advance():
            if ll.keyword("image"):
                statement = _RawPhoneRegisterImage(*_parse_phone_image(ll, True))

            elif ll.keyword("label"):
                statement = _RawPhoneRegisterLabel(_parse_phone_label(ll, True))

            elif ll.keyword("time"):
                statement = _RawPhoneRegisterDate(_parse_phone_date(ll, True))
            
            else:
                statement = _RawPhoneRegisterMessage(*_parse_phone_message(ll, True))

            statements.append(statement)

            ll.expect_eol()
        
        if not statements:
            ll.error("expected at least one statement")
        
        return _RawPhoneRegister(gc, statements)

    def _translation_strings_phone_register(rpr):
        rv = [ ]
        for statement in rpr.statements:
            if isinstance(statement, _RawPhoneRegisterMessage):
                rv.append(statement.message)
            elif isinstance(statement, _RawPhoneRegisterLabel):
                rv.append(statement.label)
        return rv

    renpy.register_statement(
        "phone register",
        block=True,
        parse=_parse_phone_register,
        execute=parser_utils.execute,
        translation_strings=_translation_strings_phone_register
    ) 

    ########################################################

    class _RawInitPhoneRegister(_RawPhoneRegister):
        def __init__(self, gc, statements, define):
            super(_RawInitPhoneRegister, self).__init__(gc, statements)
            self.define = define
        
        def execute(self):
            if self.define is not None:
                self.define.execute()
            config.start_callbacks.append(super(_RawInitPhoneRegister, self).execute)
    
    class _RawDefineGroupChat(object):
        def __init__(self, name, icon, key, chars, _as, default_statement):
            self.name = name
            self.icon = icon
            self.key = key
            self.chars = chars
            self._as = _as
            self.default_statement = default_statement
        
        def execute(self):
            if self.default_statement is not None:
                self.default_statement.execute()
            config.start_callbacks.append(self.register)
        
        def register(self):
            globals = store.__dict__
            if self.default_statement is not None:
                gc = getattr(store, self._as)
            else:
                gc = GroupChat(self.name, self.icon, eval(self.key, globals))
            
            for char in self.chars:
                gc.add_character(character(eval(char, globals)))
    
    ############################

    _INIT_PHONE_REGISTER_PRIORITY = 15

    def _parse_init_phone_register(l):
        gc = l.simple_expression()

        no_gc = gc is None

        l.require(":")
        l.expect_eol()
        l.expect_block("init phone register")
        ll = l.subblock_lexer()
        ll.advance()

        define = None

        if no_gc:
            ll.require("define")

            name = ll.require(ll.string)

            ll.require(":")
            ll.expect_eol()
            ll.expect_block("define group chat")

            dl = ll.subblock_lexer()

            key = None
            icon = None
            chars = [ ]
            _as = None

            while dl.advance():
                while not dl.eol():
                    state = dl.checkpoint()
                    p = dl.require(dl.word)

                    if p == "key":
                        if key is not None:
                            dl.error("'key' property already given")
                        gc = key = dl.require(dl.simple_expression)

                    elif p == "icon":
                        if icon is not None:
                            dl.error("'icon' property already given")
                        icon = dl.require(dl.string)

                    elif p == "add":
                        char = dl.require(dl.simple_expression)
                        if char in chars:
                            dl.error("character '{}' already given".format(char))
                        chars.append(char)

                    elif p == "as":
                        if _as is not None:
                            dl.error("'as' property already given")
                        _as = dl.require(dl.dotted_name)

                    else:
                        dl.revert(state)
                        dl.error("unknown property '{}'".format(p))

            if key is None:
                dl.error("expected 'key' property")
            
            if len(chars) < 2:
                dl.error("expected at least 2 'add' statements")
            
            if icon is None:
                icon = "mod_assets/phone/default_icon.png"
            
            if _as is not None:
                filename, linenumber = l.get_location()

                global _INIT_PHONE_REGISTER_PRIORITY
                string = "{init} {_as} = phone.GroupChat('{name}', '{icon}', {key})".format(init=_INIT_PHONE_REGISTER_PRIORITY, _as=_as, name=name, icon=icon, key=key)

                lexer = parser_utils.Lexer(
                    [(filename, linenumber, string, None)], True
                )
                lexer.advance()

                default_statement = renpy.parser.default_statement(lexer, (filename, linenumber))
            
            else:
                default_statement = None

            define = _RawDefineGroupChat(name, icon, key, chars, _as, default_statement)

            ll.advance()

        statements = [ ]

        while not ll.eob:
            if ll.keyword("image"):
                statement = _RawPhoneRegisterImage(*_parse_phone_image(ll, True))

            elif ll.keyword("label"):
                statement = _RawPhoneRegisterLabel(_parse_phone_label(ll, True))

            elif ll.keyword("time"):
                statement = _RawPhoneRegisterDate(_parse_phone_date(ll, True))
            
            else:
                statement = _RawPhoneRegisterMessage(*_parse_phone_message(ll, True))

            statements.append(statement)

            ll.expect_eol()
            ll.advance()
        
        if not statements and not no_gc:
            ll.error("expected at least one statement")
        
        return _RawInitPhoneRegister(gc, statements, define)
    
    def _translation_strings_init_phone_register(ripr):
        rv = _translation_strings_phone_register(ripr)
        if ripr.define is not None:
            rv.insert(0, ripr.define.name)
        return rv

    renpy.register_statement(
        "init phone register",
        block=True,
        init=True,
        init_priority=_INIT_PHONE_REGISTER_PRIORITY,
        parse=_parse_init_phone_register,
        execute=parser_utils.execute,
        translation_strings=_translation_strings_init_phone_register
    ) 