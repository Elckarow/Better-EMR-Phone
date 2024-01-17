python early in cds_utils:
    from renpy import store

                            # if store.is_renpy_version_or_above(7, 6, 0)
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

python early in phone._lint:
    from renpy.store import store, phone

    _eval = eval

    def error(msg):
        renpy.error("Better EMR Phone - {}".format(msg))   
    
    cant_evaluate = renpy.object.Sentinel("_phone_cant_evaluate")

    def eval(thing, log=True):
        try:
            return _eval(thing, store.__dict__)
        except Exception:
            if log:
                error("can't evaluate '{}'".format(thing))
            return cant_evaluate

    def character(c, log=True):
        c = eval(c, log)
        if c is not cant_evaluate:
            try:
                phone.character.character(c)
            except Exception:
                error("'{}' is not a *character*.".format(c))
    
    def group_chat(gc, log=True):
        gc = eval(gc, log)
        if gc is not cant_evaluate:
            try:
                phone.group_chat.group_chat(gc)
            except Exception:
                error("'{}' is not a *group chat*.".format(gc))
    
    def image(d, log=True):
        d = eval(d, log)
        if d is not cant_evaluate:
            try:
                renpy.displayable(d)
            except Exception:
                error("'{}' is not a displayable.".format(d))
    
    def audio(a, log=True):
        a = eval(a, log)
        if a is not cant_evaluate:
            if not renpy.loader.loadable(a):
                error("audio '{}' isn't loadable.".format(a))      

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
            _lint.character(self.sender)
            _lint.eval(self.delay)
        
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
                eval(self.image, globals),
                eval(self.time, globals),
                eval(self.delay, globals)
            )
        
        def lint(self):
            _lint.character(self.sender)
            _lint.image(self.image)    
            _lint.eval(self.time)
            _lint.eval(self.delay)    

    class _RawPhoneLabel(cds_utils.Statement):
        __slots__ = ("label", "delay")

        def __init__(self, label, delay):
            self.label = label
            self.delay = delay
        
        def execute(self):
            delay = config.default_label_delay if self.delay is None else eval(self.delay, store.__dict__)
            discussion.label(self.label, delay)
        
        def lint(self):
            if self.delay is not None:
                _lint.eval(self.delay)
        
        def get_translatable_strings(self):
            return [self.label]
    
    class _RawPhoneDate(cds_utils.Statement):
        __slots__ = ("kwargs", "delay", "auto")

        def __init__(self, kwargs, delay, auto):
            self.kwargs = kwargs
            self.delay = delay
            self.auto = auto
        
        def execute(self):
            globals = store.__dict__
            delay = config.default_label_delay if self.delay is None else eval(self.delay, globals)
            discussion.date(delay=delay, auto=eval(self.auto, globals), **{k: eval(v, globals) for k, v in self.kwargs.items()})
        
        def lint(self):
            month = _lint.eval(self.kwargs["month"])
            if month is not _lint.cant_evaluate:
                if month not in (None, True) and (not isinstance(month, (int, float)) or not 1 <= month <= 12):
                    _lint.error("'{}' isn't a valid month.".format(month))
            
            day = _lint.eval(self.kwargs["day"])
            if day is not _lint.cant_evaluate:
                if day not in (None, True) and (not isinstance(day, (int, float)) or not 1 <= day <= 31):
                    _lint.error("'{}' isn't a valid day.".format(day))

            minute = _lint.eval(self.kwargs["minute"])
            if minute is not _lint.cant_evaluate:
                if minute not in (None, True) and (not isinstance(minute, (int, float)) or not 0 <= minute <= 59):
                    _lint.error("'{}' isn't a valid minute.".format(minute))

            hour = _lint.eval(self.kwargs["hour"])
            if hour is not _lint.cant_evaluate:
                if hour not in (None, True) and (not isinstance(hour, (int, float)) or not 0 <= hour <= 23):
                    _lint.error("'{}' isn't a valid hour.".format(hour))
            
            second = _lint.eval(self.kwargs["second"])
            if second is not _lint.cant_evaluate:
                if second not in (None, True) and (not isinstance(second, (int, float)) or not 0 <= second <= 59):
                    _lint.error("'{}' isn't a valid second.".format(second))
            
            _lint.eval(self.kwargs["year"])
            if self.delay is not None:
                _lint.eval(self.delay)
            _lint.eval(self.auto)
    
    class _RawPhoneTyping(cds_utils.Statement):
        __slots__ = ("sender", "value", "delay")

        def __init__(self, sender, value, delay):
            self.sender = sender
            self.value = value
            self.delay = delay
        
        def execute(self):
            globals = store.__dict__
            discussion.typing(
                character.character(eval(self.sender, globals)),
                eval(self.value, globals),
                eval(self.delay, globals)
            )
        
        def lint(self):
            _lint.character(self.sender)
            _lint.eval(self.value)
            _lint.eval(self.delay)
    
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
    
        def lint(self):
            for _caption, _condition, block in self.entries:
                for statement in block:
                    statement.lint()
            
            _lint.eval(self.delay) 
    
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
                eval(self.audio, globals),
                eval(self.time, globals),
                eval(self.delay, globals)
            )
        
        def lint(self):
            _lint.character(self.sender)
            _lint.audio(self.audio)
            _lint.eval(self.time)
            _lint.eval(self.delay)
    
    class _RawPhonePass(cds_utils.Statement):
        def execute(self):
            pass
    
    class _RawPhonePause(cds_utils.Statement):
        __slots__ = ("duration",)

        def __init__(self, duration):
            self.duration = duration

        def execute(self):
            store.pause(eval(self.duration, store.__dict__))
        
        def lint(self):
            _lint.eval(self.duration)
    
    # class _RawPhoneRenpy(cds_utils.Statement):
    #     __slots__ = ("nodes",)

    #     def __init__(self, nodes):
    #         self.nodes = nodes
        
    #     def execute(self):
    #         for node in self.nodes:
    #             node.execute()
        
    #     def translation_strings(self):
    #         Say = renpy.ast.Say
    #         UserStatement = renpy.ast.UserStatement
    #         Menu = renpy.ast.Menu
    #         If = renpy.ast.If
    #         While = renpy.ast.While

    #         # assumes `node` is translation relevant
    #         def get_translatable_strings(node):
    #             if isinstance(node, Say):
    #                 yield node.what

    #             elif isinstance(node, UserStatement):
    #                 for s in node.call("translation_strings"):
    #                     yield s

    #             elif isinstance(node, Menu):
    #                 # renpy.translation.ScriptTranslator.take_translates
    #                 for i in node.items:
    #                     s = i[0]

    #                     if renpy.config.old_substitutions:
    #                         s = s.replace("%%", "%")

    #                     if s is None: continue
    #                     yield s

    #             else:
    #                 print("Better EMR Phone - type '{}' is translation relevant, but isn't used".format(type(node).__name__))

    #         def get_strings(nodes):
    #             for node in nodes:
    #                 if isinstance(node, If):
    #                     for s in get_strings(entry[1] for entry in node.entries):
    #                         yield s
                    
    #                 elif isinstance(node, While):
    #                     for s in get_strings(node.block):
    #                         yield s

    #                 if not node.translation_relevant: continue

    #                 for s in get_translatable_strings(node):
    #                     yield s 

    #         for string in get_strings(self.nodes):
    #             yield string

    class _RawPhoneDiscussion(cds_utils.Statement):
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
                _lint.group_chat(self.gc)

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
            _lint.character(self.sender)
        
        def get_translatable_strings(self):
            return [self.message]
    
    class _RawPhoneRegisterImage(cds_utils.Statement):
        __slots__ = ("sender", "image")

        def __init__(self, sender, image):
            self.sender = sender
            self.image = image

        def execute(self, gc):
            globals = store.__dict__
            discussion.register_image(
                gc,
                eval(self.sender, globals),
                eval(self.image, globals)
            )
        
        def lint(self):
            _lint.character(self.sender)
            _lint.image(self.image)
    
    class _RawPhoneRegisterLabel(cds_utils.Statement):
        __slots__ = ("label",)

        def __init__(self, label):
            self.label = label
        
        def execute(self, gc):
            discussion.register_label(gc, self.label)

        def get_translatable_strings(self):
            return [self.label]
    
    class _RawPhoneRegisterDate(cds_utils.Statement):
        __slots__ = ("kwargs", "auto")

        def __init__(self, kwargs, auto):
            self.kwargs = kwargs
            self.auto = auto
        
        def execute(self, gc):
            globals = store.__dict__
            discussion.register_date(gc, auto=eval(self.auto, globals), **{k: eval(v, globals) for k, v in self.kwargs.items()})
        
        def lint(self):
            month = _lint.eval(self.kwargs["month"])
            if month is not _lint.cant_evaluate:
                if month not in (None, True) and (not isinstance(month, (int, float)) or not 1 <= month <= 12):
                    _lint.error("'{}' isn't a valid month.".format(month))
            
            day = _lint.eval(self.kwargs["day"])
            if day is not _lint.cant_evaluate:
                if day not in (None, True) and (not isinstance(day, (int, float)) or not 1 <= day <= 31):
                    _lint.error("'{}' isn't a valid day.".format(day))

            minute = _lint.eval(self.kwargs["minute"])
            if minute is not _lint.cant_evaluate:
                if minute not in (None, True) and (not isinstance(minute, (int, float)) or not 0 <= minute <= 59):
                    _lint.error("'{}' isn't a valid minute.".format(minute))

            hour = _lint.eval(self.kwargs["hour"])
            if hour is not _lint.cant_evaluate:
                if hour not in (None, True) and (not isinstance(hour, (int, float)) or not 0 <= hour <= 23):
                    _lint.error("'{}' isn't a valid hour.".format(hour))
            
            second = _lint.eval(self.kwargs["second"])
            if second is not _lint.cant_evaluate:
                if second not in (None, True) and (not isinstance(second, (int, float)) or not 0 <= second <= 59):
                    _lint.error("'{}' isn't a valid second.".format(second))
            
            _lint.eval(self.kwargs["year"])
            _lint.eval(self.auto)

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
            globals = store.__dict__
            discussion.register_audio(
                gc,
                eval(self.sender, globals),
                eval(self.audio, globals)
            )
        
        def lint(self):
            _lint.character(self.sender)
            _lint.audio(self.audio)
    
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
            _lint.group_chat(self.gc)

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

        if register: return _RawPhoneRegisterMessage(sender, message)

        delay = "None" if not ll.keyword("delay") else ll.require(ll.simple_expression)
        return _RawPhoneMessage(sender, message, delay)

    def _parse_phone_image(ll, register):
        sender = ll.require(ll.simple_expression)
        image = ll.require(ll.simple_expression)

        if register: return _RawPhoneRegisterImage(sender, image)

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
        return _RawPhoneImage(sender, image, time, delay)
    
    def _parse_phone_label(ll, register):
        label = ll.require(ll.string)

        if register: return _RawPhoneRegisterLabel(label)

        delay = None if not ll.keyword("delay") else ll.require(ll.simple_expression)
        return _RawPhoneLabel(label, delay)
    
    def _parse_phone_date(ll, register):
        kwargs = {time_thing: "None" for time_thing in ("month", "day", "year", "hour", "minute", "second")}
        kwargs["auto"] = "False"
        kwargs["delay"] = None
        seen = set()

        while True:
            state = ll.checkpoint()
            t = ll.require(ll.word)

            if t not in kwargs:
                ll.revert(state)
                ll.error("'{}' isn't a valid property for the 'time' statement".format(t))

            if t in seen:
                ll.revert(state)
                ll.error("'{}' already given".format(t))
            
            if t == "auto" and ll.init:
                ll.revert(state)
                ll.error("'auto' can't be used in the `init phone register` statement")

            kwargs[t] = ll.require(ll.simple_expression)
            seen.add(t)

            if ll.eol():
                break
        
        auto = kwargs.pop("auto")
        delay = kwargs.pop("delay")

        if register:
            if delay is not None:
                renpy.error("'delay' can't be used here")
            return _RawPhoneRegisterDate(kwargs, auto)

        return _RawPhoneDate(kwargs, delay, auto)
    
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
        return _RawPhoneTyping(sender, value, delay)
    
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
        
        if register:
            return _RawPhoneRegisterIf(entries)
        else:
            return _RawPhoneIf(entries)

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
        
        return _RawPhoneMenu(entries, delay)
    
    def _parse_phone_one_line_python(ll):
        code = ll.rest_statement()
        if not code: ll.error("expected python code")
        ll.expect_noblock("one-line python statement")

        return _RawPhonePython(code, False, "store")
    
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

        return _RawPhonePython(ll.python_block(), hide, store)
    
    def _parse_phone_audio(ll, register):
        sender = ll.require(ll.simple_expression)
        audio = ll.require(ll.simple_expression)

        if register:
            return _RawPhoneRegisterAudio(sender, audio)

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
        return _RawPhoneAudio(sender, audio, time, delay)

    def _parse_phone_pause(ll):
        duration = ll.simple_expression()
        return _RawPhonePause(duration or "None")

    # def _parse_phone_renpy(ll):
    #     ll.require(":")
    #     ll.expect_eol()
    #     ll.expect_block("phone renpy")

    #     rl = ll.subblock_lexer()
    #     return renpy.parser.parse_block(rl)

    def _get_phone_statements(ll, discussion):
        statements = [ ]

        if discussion:
            while ll.advance():
                if ll.keyword("image"):
                    statement = _parse_phone_image(ll, False)

                elif ll.keyword("label"):
                    statement = _parse_phone_label(ll, False)

                elif ll.keyword("time"):
                    statement = _parse_phone_date(ll, False)

                elif ll.keyword("type"):
                    statement = _parse_phone_typing(ll)
                
                elif ll.keyword("if"):
                    statement = _parse_phone_if(ll, False)
                
                elif ll.keyword("menu"):
                    statement = _parse_phone_menu(ll)
                
                elif ll.match("\$"):
                    statement = _parse_phone_one_line_python(ll)
                
                elif ll.keyword("python"):
                    statement = _prase_phone_python(ll)
                
                elif ll.keyword("audio"):
                    statement = _parse_phone_audio(ll, False)
                
                elif ll.keyword("pass"):
                    statement = _RawPhonePass()
                
                elif ll.keyword("pause"):
                    statement = _parse_phone_pause(ll)
                
                # elif ll.keyword("renpy"):
                #     statement = _parse_phone_renpy(ll)

                else:
                    statement = _parse_phone_message(ll, False)

                statements.append(statement)

                ll.expect_eol()
        
        else:
            while ll.advance():
                if ll.keyword("image"):
                    statement = _parse_phone_image(ll, True)

                elif ll.keyword("label"):
                    statement = _parse_phone_label(ll, True)

                elif ll.keyword("time"):
                    statement = _parse_phone_date(ll, True)
                
                elif ll.keyword("if"):
                    statement = _parse_phone_if(ll, True)
                
                elif ll.match("\$"):
                    statement = _parse_phone_one_line_python(ll)
                
                elif ll.keyword("python"):
                    statement = _prase_phone_python(ll)
                
                elif ll.keyword("audio"):
                    statement = _parse_phone_audio(ll, True)
                
                elif ll.keyword("pass"):
                    statement = _RawPhoneRegisterPass()

                else:
                    statement = _parse_phone_message(ll, True)

                statements.append(statement)

                ll.expect_eol()
        
        return statements

    def _parse_phone_discussion(l):
        gc = l.simple_expression()

        if l.eol():
            l.expect_noblock("phone discussion")
            statements = [_RawPhonePass()]
        
        else:
            l.require(":")
            l.expect_eol()
            l.expect_block("phone discussion")

            ll = l.subblock_lexer()
            statements = _get_phone_statements(ll, True)

        return _RawPhoneDiscussion(gc, statements)
    
    def _predict_phone_discussion(rd):
        renpy.predict_screen("phone_discussion")
        return [ ]
    
    def _phone_execute_init(rv):
        for statement in rv.statements:
            if isinstance(statement, _RawPhonePython):
                renpy.python.create_store(statement.store)

    renpy.register_statement(
        "phone discussion",
        block="possible",
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
        video = False
        nosave = False
        
        while not l.eol():
            state = l.checkpoint()
            thing = l.word()

            if thing == "video":
                if video:
                    l.revert(state)
                    l.error("video clause already given")
                else:
                    video = True

            elif thing == "nosave":
                if nosave:
                    l.revert(state)
                    l.error("nosave clause already given")
                else:
                    nosave = True
            
            else:
                l.revert(state)
                l.error("unknown property %s" % thing)
        

        l.expect_eol()
        l.expect_noblock("phone call")
        return rv, video, nosave

    def _execute_phone_call(tu):
        c = character.character(eval(tu[0], store.__dict__))
        calls.call(c, tu[1], tu[2])
    
    def _predict_phone_call(tu):
        renpy.predict_screen("phone_call", video=tu[1])
        return [ ]

    def _lint_phone_call(tu):
        _lint.character(tu[0])

    renpy.register_statement(
        "phone call",
        parse=_parse_phone_call,
        execute=_execute_phone_call,
        predict=_predict_phone_call,
        lint=_lint_phone_call
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
        if l.init:
            # set the pos to the beginning of the statement
            # makes the error message clearer
            l.unadvance()
            l.advance()
            l.error("the `phone register` statement can't be used during init. see the `init phone register` statement instead.")
        
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
        translation_strings=_translation_strings_phone_register,
        lint=cds_utils.lint
    ) 

    ########################################################

    # soooooooooooooooooooooooooooooooooooooooooooooooo clunky
    class _RawInitPhoneRegister(_RawPhoneRegister):
        __slots__ = ("name", "icon", "key", "chars", "transient", "default_statement")

        def __init__(self, gc, statements, name, icon, key, chars, transient, default_statement):
            super(_RawInitPhoneRegister, self).__init__(gc, statements)
            self.name = name
            self.icon = icon
            self.key = key
            self.chars = chars
            self.transient = transient
            self.default_statement = default_statement

        def execute(self):
            if self.default_statement is not None:
                self.default_statement.execute()
            execute_default(self._execute, ("phone define gc", self.gc if self.gc is not None else str(self.key)))
        
        def _execute(self):
            gc = None

            globals = store.__dict__
            if self.default_statement is not None:
                gc = getattr(store, self.default_statement.varname)
            else:
                if self.name is not None:
                    gc = group_chat.GroupChat(self.name, eval(self.icon, globals), eval(self.key, globals), transient=self.transient)
            
            if gc is not None:
                for char in self.chars:
                    gc.add_character(character.character(eval(char, globals)))

            super(_RawInitPhoneRegister, self).execute()
        
        def get_translatable_strings(self):
            rv = super(_RawInitPhoneRegister, self).get_translatable_strings()
            if self.name is not None:
                rv.insert(0, self.name)
            return rv
    
        def lint(self):
            _lint.eval(self.icon)
            _lint.eval(self.key)
            for char in self.chars:
                _lint.character(char)
    
    ############################

    _INIT_PHONE_REGISTER_PRIORITY = 700

    def _parse_init_phone_register(l):
        gc = l.simple_expression()

        no_gc = gc is None

        l.require(":")
        l.expect_eol()
        l.expect_block("init phone register")
        ll = l.subblock_lexer(init=True)
        
        name = None
        key = None
        icon = None
        chars = [ ]
        transient = False
        _as = None
        default_statement = None

        if no_gc:
            ll.advance()
            ll.require("define")

            name = ll.require(ll.string)

            ll.require(":")
            ll.expect_eol()
            ll.expect_block("define group chat")

            dl = ll.subblock_lexer()

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

                    elif p == "transient":
                        if transient:
                            dl.error("'transient' property already given")
                        transient = True

                    elif p == "as":
                        if _as is not None:
                            dl.error("'as' property already given")
                        _as = dl.require(dl.dotted_name)

                    else:
                        dl.revert(state)
                        dl.error("unknown property '{}'".format(p))

            if key is None:
                dl.error("expected 'key' property")
                        
            if icon is None:
                icon = 'phone.asset("default_icon.png")'
            
            if _as is not None:
                filename, linenumber = l.get_location()

                global _INIT_PHONE_REGISTER_PRIORITY
                string = "{init} {_as} = phone.group_chat.GroupChat('{name}', {icon}, {key}, transient={transient})" \
                        .format(
                            init=_INIT_PHONE_REGISTER_PRIORITY,
                            _as=_as,
                            name=name,
                            icon=icon,
                            key=key,
                            transient=transient,
                        )

                lexer = cds_utils.Lexer(
                    [(filename, linenumber, string, None)], True
                )
                lexer.advance()

                default_statement = renpy.parser.default_statement(lexer, (filename, linenumber))

        statements = _get_phone_statements(ll, False)
        
        if not statements and not no_gc:
            ll.error("expected at least one statement")
        
        return _RawInitPhoneRegister(gc, statements, name, icon, key, chars, transient, default_statement)
    
    def _translation_strings_init_phone_register(ripr):
        rv = _translation_strings_phone_register(ripr)
        if ripr.name is not None:
            rv.insert(0, ripr.name)
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