init -100 python in phone.application:
    from renpy import store
    from store import (
        Gradient, RoundedCorners, Transform,
        Text, phone, NullAction, Fixed, gui, Null, Flatten
    )
    from store.phone import config

    def IconBackground(d, **kwargs):
        return RoundedCorners(
            d, radius=gui.phone_application_rounded_corners_radius,
            xysize=(gui.phone_application_icon_size, gui.phone_application_icon_size),
            **kwargs
        )
    
    def GradientBackground(start_color, end_color, theta=0):
        return IconBackground(Gradient(start_color, end_color, theta))
    
    def Icon(d, size=None, background=None):
        d = Transform(d, align=(0.5, 0.5), subpixel=True, fit="contain", xysize=(size, size))
        bg = renpy.easy.displayable_or_none(background) or Null()
        rv = Fixed(bg, d, style="empty", xysize=(gui.phone_application_icon_size, gui.phone_application_icon_size))
        return Flatten(rv)

    class Application(object):
        def __init__(self, name, icon, action):
            self.name = name
            self.icon = icon
            self.action = action
        
    _cols = 4
    _rows = 5 

    def _generate_applications_page():
        return [[None for x in range(_cols)] for y in range(_rows)]
    
    def _generate_bottom_applications_page():
        return [[None for x in range(_cols)]]

    def get_app_dict(key=None):
        key = phone.character.character(key).key
        return phone.data[key]["applications"]

    def get_app_page(page, key=None):
        return get_app_dict(key)[page]
        
    def get_application(page, col, row, key=None):
        return get_app_page(page, key)[row][col]

    def move_application(start, end, key=None):
        if start == end: return

        start_page, start_col, start_row = start
        end_page, end_col, end_row = end

        start_app_page = get_app_page(start_page, key)    
        end_app_page = get_app_page(end_page, key)    

        app1 = start_app_page[start_row][start_col]
        if app1 is None: return

        app2 = end_app_page[end_row][end_col]

        end_app_page[end_row][end_col] = app1
        start_app_page[start_row][start_col] = app2

        _set_new_max(key)
    
    def add_application(app, page=0, key=None):
        """
        Returns `True` if added, `False` if it failed, or `None` if renpy is still init phase and we can't know.
        """
        if renpy.is_init_phase():
            phone.execute_default(renpy.partial(add_application, app, page, key), ("_phone_add_app", app.name, page, key))
            return None

        if not isinstance(app, Application):
            raise TypeError("expected Application, got %r" % app)

        def add(page):
            app_page = get_app_page(page, key)
            for y, row in enumerate(app_page):
                for x, _app in enumerate(row):
                    if _app is None:
                        app_page[y][x] = app
                        return True
            return False

        if add(page):
            _set_new_max(key)
            return True

        if page is None: return False

        for i in range((phone.config.applications_pages - 1) - page): # try to add it on the right
            if add(page + (i + 1)):
                _set_new_max(key)
                return True
        
        for i in range(page): # try to add it on the left
            if add(page - (i + 1)): return True
        
        return False

    def add_app_to_all_characters(app, page=0):
        if renpy.is_init_phase():
            phone.execute_default(renpy.partial(add_app_to_all_characters, app, page), ("_phone_add_app", app.name, page))
            return None
        
        rv = False
        
        for key in store.phone.character._characters:
            rv |= add_application(app, page=page, key=key)
        
        return rv
    
    def _set_new_max(key):
        d = get_app_dict(key)
        for i in range(phone.config.applications_pages - 1, -1, -1):
            if any(any(row) for row in d[i]):
                d["max"] = i
                return                
        d["max"] = 0

screen phone():
    default current_page = 0
    default coords_to_move = None

    python:
        max_page = min(
            phone.application.get_app_dict(None)["max"] + (coords_to_move is not None),
            phone.config.applications_pages - 1
        )
        current_page = min(current_page, max_page)

    fixed style_prefix "phone_main":
        button style "empty" xysize (1.0, 1.0) action If(coords_to_move is None, PhoneReturn(), SetScreenVariable("coords_to_move", None))

        if coords_to_move is not None:
            key "K_ESCAPE" action SetScreenVariable("coords_to_move", None)

        if current_page != 0:
            button:
                at transform:
                    subpixel True anchor (0.5, 0.5) pos (0.35, 0.45)
                    rotate -90 transform_anchor True
                    xysize (150, 30) matrixcolor TintMatrix("#474343ee")
                action SetScreenVariable("current_page", current_page - 1)
                add phone.asset("arrow_icon.png")

        if current_page != max_page:
            button:
                at transform:
                    subpixel True anchor (0.5, 0.5) pos (0.65, 0.45)
                    rotate 90 transform_anchor True
                    xysize (150, 30) matrixcolor TintMatrix("#474343ee")
                action SetScreenVariable("current_page", current_page + 1)
                add phone.asset("arrow_icon.png")

    use _phone():
        style_prefix "phone_main"

        add (phone.data[store.pov_key]["background_image"] or Gradient("#0a8be7", "#32F5EE")):
            at transform:
                ease 0.2 blur (0.0 if coords_to_move is None else 10.0)

        side "t b":
            frame:
                top_padding (int(gui.phone_application_frame_padding * 0.5) + gui.phone_status_bar_height if phone.config.status_bar else gui.phone_application_frame_padding)

                grid phone.application._cols phone.application._rows:
                    xalign 0.5
                    for y, app_row in enumerate(phone.application.get_app_page(current_page)):
                        for x, app in enumerate(app_row):
                            use _phone_application_button(app, (current_page, x, y), coords_to_move)

            vbox:
                hbox xalign 0.5 spacing 13:
                    for i in range(max_page + 1):
                        add phone.asset("circle.png"):
                            at transform:
                                subpixel True xysize (10, 10)
                                matrixcolor TintMatrix("#4e4e4e")
                                alpha (0.8 if i == current_page else 0.4)

                frame style "phone_main_frame_bottom":
                    hbox xalign 0.5:
                        for by, b_app_row in enumerate(phone.application.get_app_page(None)):
                            for bx, b_app in enumerate(b_app_row):
                                use _phone_application_button(b_app, (None, bx, by), coords_to_move)

style phone_main_text is empty:
    font "DejaVuSans.ttf"
    color "#fff" outlines []
    size 22

style phone_main_button is empty                
style phone_main_button_text is phone_main_text

style phone_main_side is empty:
    xfill True yfill True

style phone_main_box is empty:
    spacing 22

style phone_main_hbox is phone_main_box
style phone_main_grid is phone_main_box:
    yspacing 15

style phone_main_vbox is empty:
    spacing 5 xfill True

style phone_main_frame is empty:
    bottom_padding gui.phone_application_frame_padding
    xfill True

style phone_main_frame_bottom is phone_main_frame:
    top_padding gui.phone_application_frame_padding
    background "#ffffff62"
    
screen _phone_application_button(app, app_coords, coords_to_move):
    style_prefix "_phone_application_button"

    fixed:
        if app is None:
            null:
                width gui.phone_application_icon_size
                height ( # cursed
                    gui.phone_application_icon_size +
                    style._phone_application_button_vbox.spacing +
                    style._phone_application_button_text.size + 
                    1 # dunno why it's one pixel off
                )
        else:
            button at _phone_application_button:
                vbox:
                    add app.icon at _fits(None)
                    text app.name

                sensitive (coords_to_move is None)
                action app.action,
                alternate SetScreenVariable("coords_to_move", app_coords)

        if coords_to_move is not None:
            button:
                at (_phone_move_application_selected if app_coords == coords_to_move else _phone_move_application)

                add phone.application.IconBackground("#ffffffcc")

                action [
                    Function(phone.application.move_application, coords_to_move, app_coords),
                    SetScreenVariable("coords_to_move", None)
                ] 
    
transform _phone_application_button:
    on idle:
        matrixcolor BrightnessMatrix(0.0)
    on hover:
        matrixcolor BrightnessMatrix(0.1)

transform _phone_move_application:
    subpixel True
    on idle:
        alpha (0.5 * (not renpy.variant("pc")))
    on hover:
        alpha 1.0

transform _phone_move_application_selected:
    subpixel True
    on idle:
        block:
            pause 0.4
            easeout 0.5 alpha 0.0
            easein 0.5 alpha 1.0
            repeat
    on hover:
        alpha 1.0

style _phone_application_button_button is empty:
    xsize gui.phone_application_icon_size

style _phone_application_button_vbox is empty:
    spacing 3

style _phone_application_button_text is empty:
    text_align 0.5 xalign 0.5
    outlines [ ] color "#000"
    size 12 font phone.asset("Metropolis-Regular.otf")
    line_spacing 0

style _phone_application_button_fixed is empty:
    fit_first True

init -10 python in phone.application:
    from store import PhoneMenu, ShowMenu, TintMatrix

    message_app = Application(
        _("message"),
        Icon(
            config.basedir + "message_icon.png",
            0.9,
            GradientBackground("#5bf676", "#04be25")
        ),
        PhoneMenu("phone_contacts")
    )

    calendar_app = Application(
        _("calendar"),
        Icon( # cancer
            Fixed(
                Transform(
                    Text(
                        "WED", style="empty",
                        color="#f00", size=21, xalign=0.5, text_align=0.5,
                        ypos=0.12, font="DejaVuSans.ttf"
                    ),
                    subpixel=True,
                    gl_pixel_perfect=True
                ),
                Transform(
                    Text(
                        "10", style="empty",
                        color="#141414", size=60, xalign=0.5, text_align=0.5,
                        ypos=0.35, font=config.basedir + "Metropolis-Regular.otf"
                    ),
                    subpixel=True,
                    gl_pixel_perfect=True
                ),
                style="empty",
                xysize=(100, 100)
            ),
            background=IconBackground("#f5f5f5")
        ),
        PhoneMenu("phone_calendars")
    )

    call_history_app = Application(
        _("call"),
        Icon(
            config.basedir + "call_icon.png",
            0.9,
            GradientBackground("#5bf676", "#04be25")
        ),
        PhoneMenu("phone_call_history")
    )
    
    