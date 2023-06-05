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
        It accepts the `delay` property (default to None) which is the time to wait before the next statement executes.
        A `None` delay will wait for user input. A negative value delay won't wait.

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
    
    `if/elif/else`
        Does exactly what you'd expect from this statement.

    `menu`
        The equivalent of the `phone.choice` function. It expects a block which can contain the following:
            The `delay` property, which has to be given before the menu items (defaults to 0.3).
            A string (flagged as translatable) which may be followed by an `if` clause and a simple expression. If the expression is false,
            the choice won't appear. The line ends with a colon `:` and must be followed by a block that contains any of the phone discussion statements.
    
    `$`
        The one-line python statement. Executes code in the global store.
    
    `python`
        Works the same way as the normal `python` statement except for 2 things:
            Does not accept the `early` close.
            If the `in` clause is given, the substore is created at init 0, unlike the regular `python` statement
            which does it at early time.
    
    `pass`
        Does nothing and waits for user input. Can be used to display the phone screen without actually sending any message.

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
It doesn't accept the `type`, `menu`, `$` and `python` statements, nor the properties related to time (`delay`, `time`, `cps` ...).
If the `pass` statement is used, does nothing.

example of use:
```
phone register "mc_sayo":
    time day 18 hour 7 minute 10
    "mc" "wake up sleepy head!"
```

######################

`init phone register`

Used to register messages in a group chat at init time and / or create a new group chat.
The statement is run at init priority 700.

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

python early in cds_utils:
    from renpy import store

    Lexer = renpy.lexer.Lexer if renpy.version_tuple >= ((7, 6) if renpy.compat.PY2 else (8, 1)) else renpy.parser.Lexer

    def null_parser(l):
        """
        Expects an eol, no block, and returns `None`.
        """
        l.expect_eol()
        l.expect_noblock("")
        l.advance()
        return None

    class Statement(python_object):
        __slots__ = ()

        def execute(self, *args, **kwargs):
            raise NotImplementedError("'{}.execute' not implemented".format(type(self).__name__))
        
        def lint(self):
            pass

        def get_translatable_strings(self):
            return [ ]
    
    def execute(rv):
        """
        Calls the `execute` method of the object passed.
        """
        rv.execute()
    
    def lint(rv):
        """
        Calls the `lint` method of the object passed.
        """
        rv.lint()
    
    def get_translatable_strings(rv):
        """
        Calls the `get_translatable_strings` method of the object passed.
        """
        return rv.get_translatable_strings()

python early in phone:
    from renpy.store import cds_utils    

    class _RawPhoneMessage(cds_utils.Statement):
        __slots__ = ("sender", "message", "delay")

        def __init__(self, sender, message, delay):
            self.sender = sender
            self.message = message
            self.delay = delay
        
        def execute(self):
            globals = store.__dict__
            discussion.message(
                eval(self.sender, globals),
                self.message,
                eval(self.delay, globals)
            )
        
        def lint(self):
            try:
                character.character(eval(self.sender, store.__dict__))
            except Exception:
                renpy.error("{} is not a *character*.".format(self.sender))
        
        def get_translatable_strings(self):
            return [self.message]
    
    class _RawPhoneImage(cds_utils.Statement):
        __slots__ = ("sender", "image", "time", "delay")

        def __init__(self, sender, image, time, delay):
            self.sender = sender
            self.image = image
            self.time = time
            self.delay = delay
        
        def execute(self):
            globals = store.__dict__
            discussion.image(
                eval(self.sender, globals),
                self.image,
                eval(self.time, globals),
                eval(self.delay, globals)
            )
        
        def lint(self):
            try:
                character.character(eval(self.sender, store.__dict__))
            except Exception:
                renpy.error("'{}' is not a *character*.".format(self.sender))

            if renpy.get_registered_image(self.image) is None and not renpy.loader.loadable(self.image):
                renpy.error("'{}' is not a defined image nor a valid file path.".format(self.image))

    class _RawPhoneLabel(cds_utils.Statement):
        __slots__ = ("label", "delay")

        def __init__(self, label, delay):
            self.label = label
            self.delay = delay
        
        def execute(self):
            discussion.label(self.label, eval(self.delay, store.__dict__))
        
        def get_translatable_strings(self):
            return [self.label]
    
    class _RawPhoneDate(cds_utils.Statement):
        __slots__ = ("kwargs", "delay")

        def __init__(self, kwargs, delay):
            self.kwargs = kwargs
            self.delay = delay
        
        def execute(self):
            kwargs = dict(self.kwargs)

            current_date = discussion._group_chat.date

            for k, v in kwargs.items():
                if v is None:
                    kwargs[k] = getattr(current_date, k)

            discussion.date(delay=eval(self.delay, store.__dict__), **kwargs)
        
        def lint(self):
            month = self.kwargs["month"]
            if month is not None and not 1 <= month <= 12:
                renpy.error("{} isn't a valid month.".format(month))
            
            day = self.kwargs["day"]
            if day is not None and not 1 <= day <= 31:
                renpy.error("{} isn't a valid day.".format(day))
            
            minute = self.kwargs["minute"]
            if minute is not None and not 0 <= minute <= 59:
                renpy.error("{} isn't a valid minute.".format(minute))
            
            hour = self.kwargs["hour"]
            if hour is not None and not 0 <= hour <= 23:
                renpy.error("{} isn't a valid hour.".format(hour))
    
    class _RawPhoneTyping(cds_utils.Statement):
        __slots__ = ("sender", "value", "delay")

        def __init__(self, sender, value, delay):
            self.sender = sender
            self.value = value
            self.delay = delay
        
        def execute(self):
            globals = store.__dict__
            discussion.typing(
                eval(self.sender, globals),
                eval(self.value, globals),
                eval(self.delay, globals)
            )
        
        def lint(self):
            try:
                character.character(eval(self.sender, store.__dict__))
            except Exception:
                renpy.error("'{}' is not a *character*.".format(self.sender))
    
    class _RawPhoneIf(cds_utils.Statement):
        __slots__ = ("entries",)

        def __init__(self, entries):
            self.entries = entries
        
        def execute(self):
            globals = store.__dict__
            for condition, block in self.entries:
                if eval(condition, globals):
                    for statement in block:
                        statement.execute()
                    return
        
        def get_translatable_strings(self):
            rv = [ ]
            for _condition, block in self.entries:
                for statement in block:
                    rv.extend(statement.get_translatable_strings())
            return rv
    
    class _RawPhoneMenu(cds_utils.Statement):
        __slots__ = ("entries", "delay")

        def __init__(self, entries, delay):
            self.entries = entries
            self.delay = delay
        
        def execute(self):
            globals = store.__dict__

            blocks = [ ]
            captions = [ ]

            for caption, condition, block in self.entries:
                if not eval(condition, globals): continue
                blocks.append(block); captions.append(caption)
            
            i = discussion.choice(captions, eval(self.delay, globals))

            for statement in blocks[i]:
                statement.execute()
        
        def get_translatable_strings(self):
            rv = [ ]
            for caption, _condition, block in self.entries:
                rv.append(caption)
                for statement in block:
                    rv.extend(statement.get_translatable_strings())
            return rv
    
    class _RawPhonePython(cds_utils.Statement):
        __slots__ = ("code", "hide", "store")

        def __init__(self, code, hide, store):
            self.code = code
            self.hide = hide
            self.store = store

        def execute(self):
            try:
                renpy.python.py_exec(self.code, self.hide, store=renpy.python.store_dicts[self.store])
            finally:
                if not renpy.is_init_phase():
                    for i in renpy.config.python_callbacks:
                        i()
    
    class _RawPhoneAudio(cds_utils.Statement):
        __slots__ = ("sender", "audio", "time", "delay")

        def __init__(self, sender, audio, time, delay):
            self.sender = sender
            self.audio = audio
            self.time = time
            self.delay = delay
        
        def execute(self):
            globals = store.__dict__
            discussion.audio(
                eval(self.sender, globals),
                self.audio,
                eval(self.time, globals),
                eval(self.delay, globals)
            )
        
        def lint(self):
            try:
                character.character(eval(self.sender, store.__dict__))
            except Exception:
                renpy.error("'{}' is not a *character*.".format(self.sender))

            if not renpy.loader.loadable(self.audio):
                renpy.error("audio '{}' isn't loadable.".format(self.audio))
    
    class _RawPhonePass(cds_utils.Statement):
        def execute(self):
            pause()

    class _RawPhoneDiscussion(python_object):
        __slots__ = ("gc", "statements")

        def __init__(self, gc, statements):
            self.gc = gc
            self.statements = statements
        
        def execute(self):
            gc = self.gc
            if gc is not None: gc = group_chat.group_chat(eval(gc, store.__dict__))
            discussion.discussion(gc)

            for statement in self.statements:
                statement.execute()
    
        def lint(self):
            if self.gc is not None:
                try:
                    group_chat.group_chat(eval(self.gc, store.__dict__))
                except Exception:
                    renpy.error("'{}' is not a *group chat*.".format(self.gc))

            for statement in self.statements:
                statement.lint()
        
        def get_translatable_strings(self):
            rv = [ ]
            for statement in self.statements:
                rv.extend(statement.get_translatable_strings())
            return rv
    
    ############################

    class _RawPhoneRegisterMessage(cds_utils.Statement):
        __slots__ = ("sender", "message")

        def __init__(self, sender, message):
            self.sender = sender
            self.message = message

        def execute(self, gc):
            discussion.register_message(
                gc,
                eval(self.sender, store.__dict__),
                self.message
            )
        
        def lint(self):
            try:
                character.character(eval(self.sender, store.__dict__))
            except Exception:
                renpy.error("{} is not a *character*.".format(self.sender))
        
        def get_translatable_strings(self):
            return [self.message]
    
    class _RawPhoneRegisterImage(cds_utils.Statement):
        __slots__ = ("sender", "image")

        def __init__(self, sender, image):
            self.sender = sender
            self.image = image

        def execute(self, gc):
            discussion.register_image(
                gc,
                eval(self.sender, store.__dict__),
                self.image
            )
        
        def lint(self):
            try:
                character.character(eval(self.sender, store.__dict__))
            except Exception:
                renpy.error("'{}' is not a *character*.".format(self.sender))

            if renpy.get_registered_image(self.image) is None and not renpy.loader.loadable(self.image):
                renpy.error("'{}' is not a defined image nor a valid file path.".format(self.image))
    
    class _RawPhoneRegisterLabel(cds_utils.Statement):
        __slots__ = ("label",)

        def __init__(self, label):
            self.label = label
        
        def execute(self, gc):
            discussion.register_label(gc, self.label)

        def get_translatable_strings(self):
            return [self.label]
    
    class _RawPhoneRegisterDate(cds_utils.Statement):
        __slots__ = ("kwargs",)

        def __init__(self, kwargs):
            self.kwargs = kwargs
        
        def execute(self, gc):
            kwargs = dict(self.kwargs)

            current_date = gc.date

            for k, v in kwargs.items():
                if v is None:
                    kwargs[k] = getattr(current_date, k)

            discussion.register_date(gc, **kwargs)
        
        def lint(self):
            month = self.kwargs["month"]
            if month is not None and not 1 <= month <= 12:
                renpy.error("{} isn't a valid month.".format(month))
            
            day = self.kwargs["day"]
            if day is not None and not 1 <= day <= 31:
                renpy.error("{} isn't a valid day.".format(day))
            
            minute = self.kwargs["minute"]
            if minute is not None and not 0 <= minute <= 59:
                renpy.error("{} isn't a valid minute.".format(minute))
            
            hour = self.kwargs["hour"]
            if hour is not None and not 0 <= hour <= 23:
                renpy.error("{} isn't a valid hour.".format(hour))

    class _RawPhoneRegisterIf(cds_utils.Statement):
        __slots__ = ("entries",)

        def __init__(self, entries):
            self.entries = entries
        
        def execute(self, gc):
            globals = store.__dict__
            for condition, statements in self.entries:
                if eval(condition, globals):
                    for statement in statements:
                        statement.execute(gc)
                    return

        def get_translatable_strings(self):
            rv = [ ]
            for _condition, statements in self.entries:
                for statement in statements:
                    rv.extend(statement.get_translatable_strings())
            return rv
    
    class _RawPhoneRegisterAudio(cds_utils.Statement):
        __slots__ = ("sender", "audio")

        def __init__(self, sender, audio):
            self.sender = sender
            self.audio = audio

        def execute(self, gc):
            discussion.register_audio(
                gc,
                eval(self.sender, store.__dict__),
                self.audio
            )
        
        def lint(self):
            try:
                character.character(eval(self.sender, store.__dict__))
            except Exception:
                renpy.error("'{}' is not a *character*.".format(self.sender))

            if not renpy.loader.loadable(self.audio):
                renpy.error("audio '{}' isn't loadable.".format(self.audio))
    
    class _RawPhoneRegisterPass(cds_utils.Statement):
        def execute(self, gc):
            pass
    
    class _RawPhoneRegister(cds_utils.Statement):
        __slots__ = ("gc", "statements")

        def __init__(self, gc, statements):
            self.gc = gc
            self.statements = statements
        
        def execute(self):
            gc = group_chat.group_chat(eval(self.gc, store.__dict__))

            for statement in self.statements:
                if isinstance(statement, _RawPhonePython): # breh
                    statement.execute() 
                else:
                    statement.execute(gc)
    
        def lint(self):
            try:
                group_chat.group_chat(eval(self.gc, store.__dict__))
            except Exception:
                renpy.error("'{}' is not a *group chat*.".format(self.gc))

            for statement in self.statements:
                statement.lint()
        
        def get_translatable_strings(self):
            rv = [ ]
            for statement in self.statements:
                rv.extend(statement.get_translatable_strings())
            return rv

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
    
    def _parse_phone_if(ll, register): # literally renpy.parser.if_statement
        entries = [ ]

        condition = ll.require(ll.python_expression)

        ll.require(":")
        ll.expect_eol()
        ll.expect_block("phone if statement")

        entries.append((condition, _get_phone_statements(ll.subblock_lexer(), not register)))

        ll.advance()

        while ll.keyword("elif"):
            condition = ll.require(ll.python_expression)

            ll.require(":")
            ll.expect_eol()
            ll.expect_block("phone elif clause")

            entries.append((condition, _get_phone_statements(ll.subblock_lexer(), not register)))

            ll.advance()

        if ll.keyword("else"):
            ll.require(":")
            ll.expect_eol()
            ll.expect_block("phone else clause")

            entries.append(("True", _get_phone_statements(ll.subblock_lexer(), not register)))

            ll.advance()
        
        return entries

    def _parse_phone_menu(ll):
        ll.require(":")
        ll.expect_eol()
        ll.expect_block("phone menu")

        menu_l = ll.subblock_lexer()
        menu_l.advance()

        delay = "0.3"
        if menu_l.keyword("delay"):
            delay = menu_l.require(menu_l.simple_expression)
            menu_l.expect_eol()
            menu_l.advance()
            
        entries = [ ]

        while not menu_l.eob:
            caption = menu_l.require(menu_l.string)

            condition = "True"
            if menu_l.keyword("if"):
                condition = menu_l.require(menu_l.python_expression)
            
            menu_l.require(":")
            menu_l.expect_eol()
            menu_l.expect_block("phone menuitem")

            entries.append((caption, condition, _get_phone_statements(menu_l.subblock_lexer(), True)))
            menu_l.advance()
        
        return entries, delay
    
    def _parse_phone_one_line_python(ll):
        code = ll.rest_statement()
        if not code: ll.error("expected python code")
        ll.expect_noblock("one-line python statement")

        return code, False, "store"
    
    def _prase_phone_python(ll):
        hide = False
        store = "store"

        if ll.keyword("hide"):
            hide = True

        if ll.keyword("in"):
            store = "store." + ll.require(ll.dotted_name)

        ll.require(":")
        ll.expect_eol()

        ll.expect_block("python block")

        return ll.python_block(), hide, store
    
    def _parse_phone_audio(ll, register):
        sender = ll.require(ll.simple_expression)
        audio = ll.require(ll.string)

        if register: return sender, audio

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
        return sender, audio, time, delay

    def _get_phone_statements(ll, discussion):
        statements = [ ]

        if discussion:
            while ll.advance():
                if ll.keyword("image"):
                    statement = _RawPhoneImage(*_parse_phone_image(ll, False))

                elif ll.keyword("label"):
                    statement = _RawPhoneLabel(*_parse_phone_label(ll, False))

                elif ll.keyword("time"):
                    statement = _RawPhoneDate(*_parse_phone_date(ll, False))

                elif ll.keyword("type"):
                    statement = _RawPhoneTyping(*_parse_phone_typing(ll))
                
                elif ll.keyword("if"):
                    statement = _RawPhoneIf(_parse_phone_if(ll, False))
                
                elif ll.keyword("menu"):
                    statement = _RawPhoneMenu(*_parse_phone_menu(ll))
                
                elif ll.match("\$"):
                    statement = _RawPhonePython(*_parse_phone_one_line_python(ll))
                
                elif ll.keyword("python"):
                    statement = _RawPhonePython(*_prase_phone_python(ll))
                
                elif ll.keyword("audio"):
                    statement = _RawPhoneAudio(*_parse_phone_audio(ll, False))
                
                elif ll.keyword("pass"):
                    statement = _RawPhonePass()

                else:
                    statement = _RawPhoneMessage(*_parse_phone_message(ll, False))

                statements.append(statement)

                ll.expect_eol()
        
        else:
            while ll.advance():
                if ll.keyword("image"):
                    statement = _RawPhoneRegisterImage(*_parse_phone_image(ll, True))

                elif ll.keyword("label"):
                    statement = _RawPhoneRegisterLabel(_parse_phone_label(ll, True))

                elif ll.keyword("time"):
                    statement = _RawPhoneRegisterDate(_parse_phone_date(ll, True))
                
                elif ll.keyword("if"):
                    statement = _RawPhoneRegisterIf(*_parse_phone_if(ll, True))
                
                elif ll.match("\$"):
                    statement = _RawPhonePython(*_parse_phone_one_line_python(ll))
                
                elif ll.keyword("python"):
                    statement = _RawPhonePython(*_prase_phone_python(ll))
                
                elif ll.keyword("audio"):
                    statement = _RawPhoneRegisterAudio(*_parse_phone_audio(ll, True))
                
                elif ll.keyword("pass"):
                    statement = _RawPhoneRegisterPass()

                else:
                    statement = _RawPhoneRegisterMessage(*_parse_phone_message(ll, True))

                statements.append(statement)

                ll.expect_eol()
        
        return statements

    def _parse_phone_discussion(l):
        gc = None

        if not l.match(":"):
            gc = l.require(l.simple_expression)
            l.require(":")
        
        l.expect_eol()
        l.expect_block("phone discussion")

        ll = l.subblock_lexer()
        return _RawPhoneDiscussion(gc, _get_phone_statements(ll, True))
    
    def _predict_phone_discussion(rd):
        renpy.predict_screen("phone_message")
        return [ ]
    
    def _phone_execute_init(rv):
        for statement in rv.statements:
            if isinstance(statement, _RawPhonePython):
                renpy.python.create_store(statement.store)

    renpy.register_statement(
        "phone discussion",
        block=True,
        parse=_parse_phone_discussion,
        execute=cds_utils.execute,
        execute_init=_phone_execute_init,
        translation_strings=cds_utils.get_translatable_strings,
        lint=cds_utils.lint,
        predict=_predict_phone_discussion
    )       

    ########################################################

    def _execute_phone_end_discussion(rv):
        discussion.end_discussion()

    renpy.register_statement(
        "phone end discussion",
        parse=cds_utils.null_parser,
        execute=_execute_phone_end_discussion
    )

    ########################################################

    def _parse_phone_call(l):
        rv = l.require(l.simple_expression)
        l.expect_eol()
        l.expect_noblock("phone call")
        return rv

    def _execute_phone_call(c):
        c = character.character(eval(c, store.__dict__))
        calls.call(c)
    
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
        calls.end_call()

    renpy.register_statement(
        "phone end call",
        parse=cds_utils.null_parser,
        execute=_execute_phone_end_call
    )

    ########################################################
    
    def _parse_phone_register(l):
        gc = l.require(l.simple_expression)

        l.require(":")
        l.expect_eol()
        l.expect_block("phone register")
        ll = l.subblock_lexer()
        
        statements = _get_phone_statements(ll, False)
        
        if not statements:
            ll.error("expected at least one statement")
        
        return _RawPhoneRegister(gc, statements)

    def _translation_strings_phone_register(rpr):
        rv = [ ]

        def get_strings(l):
            for statement in l:
                if isinstance(statement, _RawPhoneRegisterMessage):
                    rv.append(statement.message)
                elif isinstance(statement, _RawPhoneRegisterLabel):
                    rv.append(statement.label)
                elif isinstance(statement, _RawPhoneRegisterIf):
                    get_strings(block[1] for block in statement.blocks)
        
        get_strings(rpr.statements)

        return rv

    renpy.register_statement(
        "phone register",
        block=True,
        parse=_parse_phone_register,
        execute=cds_utils.execute,
        execute_init=_phone_execute_init,
        translation_strings=_translation_strings_phone_register
    ) 

    ########################################################

    class _RawInitPhoneRegister(_RawPhoneRegister):
        __slots__ = ("define",)

        def __init__(self, gc, statements, define):
            super(_RawInitPhoneRegister, self).__init__(gc, statements)
            self.define = define
        
        def execute(self):
            if self.define is not None:
                self.define.execute()
            renpy.config.start_callbacks.append(super(_RawInitPhoneRegister, self).execute)
        
        def get_translatable_strings(self):
            rv = super(_RawInitPhoneRegister, self).get_translatable_strings()
            if self.define is not None:
                rv.insert(0, self.define.name)
            return rv
    
    class _RawDefineGroupChat(python_object):
        __slots__ = ("name", "icon", "key", "chars", "default_statement")

        def __init__(self, name, icon, key, chars, default_statement):
            self.name = name
            self.icon = icon
            self.key = key
            self.chars = chars
            self.default_statement = default_statement
        
        def execute(self):
            if self.default_statement is not None:
                self.default_statement.execute()
            renpy.config.start_callbacks.append(self.register)
        
        def register(self):
            globals = store.__dict__
            if self.default_statement is not None:
                gc = getattr(store, self.default_statement.varname)
            else:
                gc = group_chat.GroupChat(self.name, eval(self.icon, globals), eval(self.key, globals))
            
            for char in self.chars:
                gc.add_character(character.character(eval(char, globals)))
    
    ############################

    _INIT_PHONE_REGISTER_PRIORITY = 700

    def _parse_init_phone_register(l):
        gc = l.simple_expression()

        no_gc = gc is None

        l.require(":")
        l.expect_eol()
        l.expect_block("init phone register")
        ll = l.subblock_lexer()
        
        define = None

        if no_gc:
            ll.advance()
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
                        icon = dl.require(dl.simple_expression)

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
            
            if len(chars) == 0:
                dl.error("expected at least 1 'add' statements")
            
            if icon is None:
                icon = 'phone.config.basedir + "default_icon.png"'
            
            if _as is not None:
                filename, linenumber = l.get_location()

                global _INIT_PHONE_REGISTER_PRIORITY
                string = "{init} {_as} = phone.group_chat.GroupChat('{name}', {icon}, {key})" \
                        .format(
                            init=_INIT_PHONE_REGISTER_PRIORITY,
                            _as=_as,
                            name=name,
                            icon=icon,
                            key=key,
                        )

                lexer = cds_utils.Lexer(
                    [(filename, linenumber, string, None)], True
                )
                lexer.advance()

                default_statement = renpy.parser.default_statement(lexer, (filename, linenumber))
            
            else:
                default_statement = None

            define = _RawDefineGroupChat(name, icon, key, chars, default_statement)

        statements = _get_phone_statements(ll, False)
        
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
        execute=cds_utils.execute,
        execute_init=_phone_execute_init,
        translation_strings=cds_utils.get_translatable_strings,
        lint=cds_utils.lint,
    ) 

# screen displayables
python early:
    renpy.register_sl_statement("gradient", 0, "_gradient_displayable") \
        .add_positional("start_color") \
        .add_positional("end_color") \
        .add_property("theta") \
        .add_property("start_pos") \
        .add_property("end_pos") \
        .add_property_group("position") \
        .add_property_group("ui")

screen _gradient_displayable(start_color, end_color, theta=0, start_pos=0.0, end_pos=1.0, **properties):
    add Gradient(start_color, end_color, theta, start_pos, end_pos):
        properties properties

python early:
    renpy.register_sl_statement("circle", 0, "_circle_displayable") \
        .add_property("border") \
        .add_property("radius") \
        .add_property("color") \
        .add_property_group("position") \
        .add_property_group("ui")

screen _circle_displayable(border, radius=None, color="#fff", **properties):
    add CircleDisplayable(border, radius, color):
        properties properties