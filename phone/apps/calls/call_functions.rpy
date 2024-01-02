init -100 python in phone.calls:
    from renpy import store
    from store import Transform, BrightnessMatrix, phone
    from store.phone import character, config, show_layer_at, set_current_screen, system
    import time

    config.layer_at_transforms["phone_call"] = Transform(matrixcolor=BrightnessMatrix(-0.21), blur=20)
    config.hide_status_bar_screens.append("phone_call")

    def call(caller, video=False, nosave=False):
        store._window_hide()

        global _current_caller
        if _current_caller is not None:
            raise Exception("can't have 2 phone calls at the same time")
        _current_caller = character.character(caller)
        store.narrator = store._phone_narrator

        set_current_screen("phone_call")
        show_layer_at("phone_call")

        renpy.show_screen("phone_call", video=video)
        renpy.with_statement(config.enter_transition)

        global _nosave
        _nosave = bool(nosave)
    
    def end_call():
        global _current_caller
        if _current_caller is None:
            raise Exception("ending phone call, but no call was ever made")
        
        global _call_time_st
        register_call(character.character(store.pov_key), _current_caller, _call_time_st)
        _current_caller = None
        store.narrator = store._backup_narrator
        _call_time_st = 0.0

        set_current_screen(None)

        show_layer_at([], reset=True)
        renpy.hide_screen("phone_call")
        if store.is_renpy_version_or_above(7, 5, 0):
            renpy.scene(config.video_call_layer)
        renpy.with_statement(config.exit_transition)

        set_current_screen(None)
        store._window_auto = True
    
    class _CallEntry(object):
        def __init__(self, caller, date, duration):
            self.caller = character.character(caller).key
            self.date = date
            self.duration = duration
        
        def _duration_to_str(self):
            if self.duration is None: return ""
            return time.strftime("%M:%S", time.gmtime(self.duration))

    def register_call(char1, char2, duration=None):
        key1 = character.character(char1).key
        key2 = character.character(char2).key

        date = system.get_date()

        global _nosave
        if _nosave is not None and not _nosave:
            _nosave = None
            
            ch1 = phone.data[key1]["call_history"]
            ch1.append(_CallEntry(key2, date, duration))

            while len(ch1) > config.call_history_lenght: ch1.pop(0)

            ch2 = phone.data[key2]["call_history"]
            ch2.append(_CallEntry(key1, date, duration))

            while len(ch2) > config.call_history_lenght: ch2.pop(0)

default -100 phone.calls._current_caller = None
default -100 phone.calls._nosave = None