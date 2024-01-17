init -100 python in phone.calendar:
    from renpy import store
    from store import _, At, _fits, phone
    from store.phone import system, config
    import calendar

    MONDAY = calendar.MONDAY
    TUESDAY = calendar.TUESDAY
    WEDNESDAY = calendar.WEDNESDAY
    THURSDAY = calendar.THURSDAY
    FRIDAY = calendar.FRIDAY
    SATURDAY = calendar.SATURDAY
    SUNDAY = calendar.SUNDAY

    renpy.const("phone.calendar.MONDAY")
    renpy.const("phone.calendar.TUESDAY")
    renpy.const("phone.calendar.WEDNESDAY")
    renpy.const("phone.calendar.THURSDAY")
    renpy.const("phone.calendar.FRIDAY")
    renpy.const("phone.calendar.SATURDAY")
    renpy.const("phone.calendar.SUNDAY")

    days = (
        _("Monday"),
        _("Tuesday"),
        _("Wednesday"),
        _("Thursday"),
        _("Friday"),
        _("Saturday"),
        _("Sunday")
    )

    renpy.const("phone.calendar.days")

    months = (
        "",
        _("January"),
        _("February"),
        _("March"),
        _("April"),
        _("May"),
        _("June"),
        _("July"),
        _("August"),
        _("September"),
        _("October"),
        _("November"),
        _("December")
    )

    renpy.const("phone.calendar.months")
    
    class _CalendarEntry(object):
        def __init__(self, day):
            self.day = day
            self.description = None
        
    class Calendar(calendar.Calendar):
        def __init__(self, month, year=2017, first_day=SUNDAY):
            super(Calendar, self).__init__(first_day)
            
            self.month = month
            self.month_name = months[month]
            self.year = year 
    
            self.__days = [ ]
            self.start_offset = self.end_offset = 0
    
            end = False
            for d in self.itermonthdays(year, month):
                if d == 0:
                    self.__days.append(None)
                    if not end:
                        self.start_offset += 1
                    else:
                        self.end_offset += 1
                else:
                    self.__days.append(_CalendarEntry(d))
                    end = True
        
        def is_day_passed(self, day):
            if not 0 < day <= self.lenght(): return False
            date = system.get_date()
            return (self.year, self.month, day) < (date.year, date.month, date.day)
        
        def lenght(self, offsets=False):
            if offsets: return len(self.__days)
            return self.lenght(True) - self.end_offset - self.start_offset
        
        def get_week_days(self):
            return get_week_days(self.firstweekday)
        
        @property
        def rows(self):
            return self.lenght(True) // 7
        
        def __getitem__(self, i):
            return self.__days[self.start_offset:self.lenght(True) - self.end_offset][i - 1]
        
        def __iter__(self):
            return iter(self.__days)
    
    def get_week_days(first_day=SUNDAY):
        for i in range(first_day, 7):
            yield days[i]
        
        for i in range(0, first_day):
            yield days[i]
    
    def day_name(year, month, day):
        return days[calendar.weekday(year, month, day)]
    
    def add_calendar(year, month, key=None, first_day=SUNDAY):
        if renpy.is_init_phase():
            phone.execute_default(renpy.partial(add_calendar, year=year, month=month, key=key, first_day=first_day), ("_phone_add_calendar", month, year, key))
        else:
            key = character.character(key).key

            if get_calendar(year=year, month=month, key=key) is not None:
                raise Exception("a calendar for the year {} and month {} already exists for the *character* {}" \
                    .format(year, month, key))

            calendars = store.phone.data[key]["calendars"]
            calendars.append(Calendar(year=year, month=month, first_day=first_day))

            calendars.sort(key=lambda c: (c.year, c.month))

    def add_calendar_to_all_characters(year, month, first_day=SUNDAY):
        if renpy.is_init_phase():
            phone.execute_default(renpy.partial(add_calendar_to_all_characters, year=year, month=month, first_day=first_day), ("_phone_add_calendar", month, year))
        else:
            for key in character._characters:
                add_calendar(year=year, month=month, first_day=first_day, key=key)

    _calendar_button_background = At(config.basedir + "circle.png", store._fits(None))

    def get_calendar(year, month, key=None):
        key = character.character(key).key
        for calendar in data[key]["calendars"]:
            if calendar.year == year and calendar.month == month:
                return calendar
        return None

    def _calendar_default_index(m):
        n = config.default_calendar_index

        if n is True:
            pov_key = store.pov_key
            date = system.get_date()

            c = get_calendar(year=date.year, month=date.month, key=pov_key)

            if c is None:
                raise Exception("no calendar with the year {} and month {} exists for the *character* {}".format(year, month, pov_key))

            n = phone.data[pov_key]["calendars"].index(c)

        elif n < 0:
            n = m + n
                
        return n

screen phone_calendars():
    default calendars = phone.data[pov_key]["calendars"]
    default m = len(calendars) - 1
    default n = phone.calendar._calendar_default_index(m + 1)
    default selected_entry = None
    default yadj = ui.adjustment()

    $ calendar = calendars[n]

    use _phone():
        style_prefix "phone_calendar"

        side "t c":
            use app_base():
                style_prefix "app_base"
                text _("Calendar") xalign 0.5 text_align 0.5
            
            grid 7 calendar.rows + 1 at Flatten xalign 0.5:
                for day in calendar.get_week_days():
                    text __(day)[0] style "phone_calendar_days_text"

                for entry in calendar:
                    if entry is None:
                        null width gui.phone_calendar_button_size
                    else:
                        button:
                            at transform:
                                subpixel True yoffset -15
                                on idle:
                                    matrixcolor BrightnessMatrix(0.0)
                                on hover, selected_idle:
                                    matrixcolor BrightnessMatrix(-0.1)
                                on selected_hover:
                                    matrixcolor BrightnessMatrix(-0.2)

                            if calendar.is_day_passed(entry.day):
                                background Transform(phone.calendar._calendar_button_background, matrixcolor=TintMatrix("#9e9e9e"))
                            else:
                                hover_background Transform(phone.calendar._calendar_button_background, matrixcolor=TintMatrix("#e0e0e0"))
                                selected_background Transform(phone.calendar._calendar_button_background, matrixcolor=TintMatrix("#e0e0e0"))

                            action (
                                If(
                                    selected_entry is not entry,
                                    SetScreenVariable("selected_entry", entry),
                                    SetScreenVariable("selected_entry", None)
                                ),
                                Function(yadj.change, 0),
                                SelectedIf(selected_entry is entry)
                            )
                                
                            text str(entry.day) style "phone_calendar_button_text"

                            if entry.description is not None:
                                frame style "empty" align (1.0, 0.0) xysize (16, 16):
                                    background Transform(phone.calendar._calendar_button_background, matrixcolor=TintMatrix("#8f8f8fff"))
                                    text "?" style "phone_calendar_button_text_special":
                                        at transform:
                                            subpixel True

        vbox style_prefix "phone_calendar_notes" yalign 1.0:
            spacing 5

            side "l c r" xalign 0.5:
                textbutton "<" action If(n != 0, (SetScreenVariable("n", n - 1), SetScreenVariable("selected_entry", None)))
                text _("[calendar.month_name!t]-[calendar.year]") size 25 xalign 0.5 text_align 0.5
                textbutton ">" action If(n != m, (SetScreenVariable("n", n + 1), SetScreenVariable("selected_entry", None)))
            
            frame at CurriedRoundedCorners(radius=(0, 25, 0, 25)):
                vbox spacing 3 at Flatten:
                    text _("Notes:") size 22

                    viewport:
                        draggable True mousewheel True
                        yadjustment yadj

                        if selected_entry is not None:
                            if selected_entry.description is not None:
                                text selected_entry.description
                            else:
                                text _("No description provided.")

style phone_calendar_side is empty:
    yfill True xfill True

style phone_calendar_grid is empty:
    spacing 10

style phone_calendar_button is empty:
    xysize (gui.phone_calendar_button_size, gui.phone_calendar_button_size)

style phone_calendar_button_text is empty:
    color "#000"
    outlines []
    size 16
    align (0.5, 0.5) text_align 0.5 
    font phone.asset("Aller_Rg.ttf")

style phone_calendar_button_text_special is phone_calendar_button_text:
    size 12

style phone_calendar_days_text is phone_calendar_button_text:
    size 17

style phone_calendar_notes_side is empty:
    xsize 0.9 xfill True

style phone_calendar_notes_text is empty:
    font "DejaVuSans.ttf"
    color "#000" outlines []
    size 18

style phone_calendar_notes_button is empty:
    yalign 0.5
style phone_calendar_notes_button_text is phone_calendar_notes_text:
    size 21

style phone_calendar_notes_frame is empty:
    background "#e0e0e0"
    padding (13, 7, 13, 0)
    xfill True ysize 180

style phone_calendar_notes_vbox is empty:
    xfill True

init -50 python in phone.calendar:
    from store.phone import character

init python in phone:
    renpy_config.start_callbacks.append(lambda: setattr(calendar, "data", data))