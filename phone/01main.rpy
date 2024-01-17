python early in phone:
    from renpy import store
    from store import config as renpy_config # phone.config is a substore

    __version__ = (3, 2, 2)
    __author__ = "Elckarow#8399" # smh my head my head

init -150 python in phone:
    class _Data(object):
        def __call__(self):
            return {k: f() for k, f in config.data.items()}
            
    renpy.music.register_channel("phone_audio_message", mixer="phone", loop=False)
    renpy.music.register_channel("phone_music", mixer="phone", loop=True)

    def set_current_screen(_screen_name):
        global _current_screen; _current_screen = _screen_name
    
    def get_current_screen():
        global _current_screen; return _current_screen
    
    import datetime
    def format_date(month, day, year):
        date = datetime.date(month=month, day=day, year=year)
        return date.strftime(__(config.date_format))
    
    import time
    def format_time(hour, minute):
        return time.strftime(__(config.time_format), time.gmtime(hour * 3600 + minute * 60))

transform -150 _fits(size):
    subpixel True xysize (size, size) fit "contain"

transform -150 _xfits(size):
    subpixel True xsize size fit "contain"

transform -150 _yfits(size):
    subpixel True ysize size fit "contain"

# The dictionnary containing all of the data used by the phone.
default -150 phone.data = collections.defaultdict(
    phone._Data()
)

default -100 phone.menu = False

init -100 python in phone:
    from store import Action, Return, With

    class PhoneMenu(Action):
        def __init__(self, screen, *args, **kwargs):
            self.screen = screen
            self.args = args
            self.kwargs = kwargs

        def predict(self):
            if renpy.has_screen(self.screen):
                renpy.predict_screen(self.screen, *self.args, **self.kwargs)

        def __call__(self):
            call_screen(self.screen, *self.args, **self.kwargs)

        def get_selected(self):
            return renpy.get_screen(self.screen) is not None
        
    store.PhoneMenu = PhoneMenu
        
    def call_screen(_screen_name, *args, **kwargs):
        if not renpy.has_screen(_screen_name):
            raise Exception("%r is not a screen." % _screen_name)

        global menu
        menu = True

        global _stack_depth
        first_call = _stack_depth == 0

        needs_rollback = first_call and renpy.game.context().interacting

        if needs_rollback:
            renpy.checkpoint()

        renpy.transition(config.enter_transition if first_call else config.intra_transition)
        store._window_hide(None, True)

        _stack_depth += 1

        current_screen = get_current_screen()
        set_current_screen(_screen_name)

        show_layer_at(_screen_name)
        rv = renpy.invoke_in_new_context(renpy.call_screen, _screen_name, *args, **kwargs)
        show_layer_at(current_screen or [])

        set_current_screen(current_screen)
        _stack_depth -= 1

        menu = not first_call

        if needs_rollback:
            renpy.rollback(force=True, greedy=False)

        return rv
    
    def PhoneReturn(value=None):
        return (Return(value), With(config.exit_transition if _stack_depth == 1 else config.intra_transition))

    store.PhoneReturn = PhoneReturn

    def show_layer_at(at_list, layer="master", camera=True, reset=False):
        if isinstance(at_list, basestring):
            at_list = config.layer_at_transforms.get(at_list, config.layer_at_transforms[None])
        
        if not isinstance(at_list, list):
            at_list = [at_list]
        
        renpy.show_layer_at(at_list=at_list, layer=layer, camera=camera, reset=reset)
    
    def short_name(s, length):
        s = renpy.substitute(s)
        if len(s) > length:
            s = s[:length - 3] + "..."
        
        return s

    import os
    @renpy.pure
    def path_join(*paths):
        return os.path.join(*paths).replace("\\", "/")

    @renpy.pure
    def asset(path):
        return path_join(config.basedir, path)

    def execute_default(f, id):
        def run(load):
            if id not in _defaults_ran:
                _defaults_ran.add(id)
                f()
                if load: renpy.block_rollback()

        renpy_config.start_callbacks.append(renpy.partial(run, load=False))
        renpy_config.after_load_callbacks.append(renpy.partial(run, load=True))

# a set() object
# renamed it because why not
default -999 phone._defaults_ran = phone._id_ran_on_start

default -100 phone._stack_depth = 0
default -100 phone._current_screen = None

# The base screen for all phone screens.
screen _phone(xpos=0.5, xanchor=0.5, ypos=0.1, yanchor=0.1, horizontal=False):
    frame style "empty" modal True:
        at transform:
            subpixel True zoom gui.phone_zoom * (1.3 if horizontal else 1.0)
            xpos xpos xanchor xanchor
            ypos ypos yanchor yanchor
        
        background Transform(
            phone.asset("background.png"),
            subpixel=True,
            align=(0.5, 0.5),
            rotate=-90 * horizontal,
            transform_anchor=horizontal
        )

        if not horizontal:
            padding gui.phone_margin
            xysize (gui.phone_xsize, gui.phone_ysize)
        else:
            padding (gui.phone_margin[1], gui.phone_margin[0], gui.phone_margin[2], gui.phone_margin[3])
            xysize (gui.phone_ysize, gui.phone_xsize)

        fixed style "empty":
            at transform:
                crop (0.0, 0.0, 1.0, 1.0) crop_relative True

            fixed style "empty":
                if phone.system.at_list: # https://github.com/renpy/renpy/issues/4628
                    at phone.system.at_list

                add "#fff"
                transclude

            fixed style "empty":
                for o in phone.config.overlay_screens:
                    use expression o
                        
            # https://www.renpy.org/doc/html/incompatible.html#incompatible-7-5-2
            # the thing just above
            # about config.at_transform_compare_full_context
            $ alpha = 1.0 - phone.system.brightness
            add "#000":
                at transform:
                    alpha alpha
    
    on "hide" action (
        SetVariable("phone.system.at_list", []),
    )

init 1500: 
    # narrator is guarenteed to exist at init 1400
    # see renpy/common/00definitions.rpy
    define _phone_narrator = Character(kind=narrator, screen="phone_say", what_style="phone_say_dialogue")
    define _backup_narrator = narrator

    python in phone:
        if store.PhoneMenu is not PhoneMenu: 
            raise Exception("store.PhoneMenu is a reserved name. (value is %r)" % store.PhoneMenu)
        store.PhoneMenu = PhoneMenu

        if store.PhoneReturn is not PhoneReturn: 
            raise Exception("store.PhoneReturn is a reserved name. (value is %r)" % store.PhoneReturn)
        store.PhoneReturn = PhoneReturn

        if store.is_renpy_version_or_above(7, 6, 0):
            renpy_config.detached_layers.append(config.video_call_layer)
        
        # https://github.com/renpy/renpy/issues/5044
        renpy_config.layer_clipping[config.video_call_layer] = (0, 0, renpy_config.screen_width, renpy_config.screen_height)

# previous name, when the function it's used in was undocumented
default -1000 phone._id_ran_on_start = set()