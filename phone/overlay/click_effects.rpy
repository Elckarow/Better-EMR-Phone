screen _phone_click_effects():
    default _effects = phone.click_effects.ClickEffects(
        phone_on_click_effect,
        phone_on_drag_effect,
        phone_on_release_effect
    )
    add _effects

define phone_click_uptime = 0.3
image phone_click_effect:
    phone.asset("circle.png")
    alpha 0.34 matrixcolor TintMatrix("#464646")
    subpixel True xysize (25, 25)
    easein (phone_click_uptime * 0.4) xysize (50, 50) alpha 0.7
    easeout_quad (phone_click_uptime * 0.6) xysize (0, 0) alpha 0.0
define phone_on_click_effect = ("phone_click_effect", phone_click_uptime)

define phone_drag_uptime = 0.4
image phone_drag_effect:
    phone.asset("circle.png")
    alpha 0.17 matrixcolor TintMatrix("#464646")
    subpixel True xysize (20, 20)
    easeout phone_drag_uptime alpha 0.0 xysize (0, 0)
define phone_on_drag_effect = ("phone_drag_effect", phone_drag_uptime)

define phone_on_release_effect = None

init -100 python in phone.click_effects:
    import pygame_sdl2 as pygame
    # yes i know `SpriteManager`s exist :monikk:
    class ClickEffectDisplayable(object):
        def __init__(self, child, x, y, lifespan, last_st, zorder):
            self.child = child
            self.x = x
            self.y = y
            self.lifespan = lifespan
            self.last_st = last_st
            self.st = 0.0
            self.zorder = zorder
        
        @property
        def dead(self):
            return self.st >= self.lifespan

    class ClickEffects(renpy.Displayable, renpy.python.NoRollback):
        # zorders
        _CLICKED = 3
        _CLICK = 2
        _DRAG = 1

        def __init__(self, on_click, on_drag, on_release):
            super(ClickEffects, self).__init__()

            if on_click is None:
                self.on_click_d = self.on_click_lifespan = None
            else:
                on_click_d, on_click_lifespan = on_click
                self.on_click_lifespan = None if on_click_lifespan < 0.0 else on_click_lifespan
                self.on_click_d = renpy.displayable(on_click_d)

            if on_drag is None:
                self.on_drag_d = self.on_drag_lifespan = None
            else:
                on_drag_d, on_drag_lifespan = on_drag
                self.on_drag_lifespan = None if on_drag_lifespan < 0.0 else on_drag_lifespan
                self.on_drag_d = renpy.displayable(on_drag_d)

            if on_release is None:
                self.on_release_d = self.on_release_lifespan = None
            else:
                on_release_d, on_release_lifespan = on_release
                self.on_release_lifespan = None if on_release_lifespan < 0.0 else on_release_lifespan
                self.on_release_d = renpy.displayable(on_release_d)

            self._clicked = False
            self._dead_child = False
            self._needs_sort = False

            self.width = 0
            self.height = 0

            self.displayables = [ ]
        
        def render(self, w, h, st, at):
            self.width = w
            self.height = h

            rv = renpy.Render(w, h)

            if not self.displayables: return rv

            if self._dead_child:
                self.displayables[:] = [d for d in self.displayables if not d.dead]
                self._dead_child = False
            
            if self._needs_sort: # only sort when needed
                self.displayables.sort(key=lambda d: d.zorder)
                self._needs_sort = False

            for d in self.displayables:
                delta = st - d.last_st
                d.last_st = st
                d.st += delta
                self._dead_child |= d.dead

                cr = renpy.render(d.child, w, h, d.st, at)
                cr_w, cr_h = cr.get_size()

                rv.subpixel_blit(cr, (d.x - (cr_w / 2.0), d.y - (cr_h / 2.0)), main=False)
                        
            renpy.redraw(self, 0.0)
            return rv
        
        def event(self, ev, x, y, st):
            # checking for mousewheel
            if getattr(ev, "button", None) in (4, 5): return None

            create_displayable = (0 <= x <= self.width and 0 <= y <= self.height)

            if ev.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                self._clicked = True
                if create_displayable: self._create(self.on_click_d, x, y, self.on_click_lifespan, st, self._CLICK)
            
            elif ev.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                self._clicked = False
                if create_displayable: self._create(self.on_release_d, x, y, self.on_release_lifespan, st, self._CLICKED)
            
            elif ev.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION) and self._clicked:
                if create_displayable: self._create(self.on_drag_d, x, y, self.on_drag_lifespan, st, self._DRAG)

            return None
        
        def _create(self, d, x, y, lifespan, st, zorder):
            if d is None or lifespan is None: return

            if d._duplicatable:
                d = d._duplicate(None)
                d._unique()

            self.displayables.append(ClickEffectDisplayable(d, x, y, lifespan, st, zorder))
            self._needs_sort = True
            renpy.redraw(self, 0.0)
    
        def visit(self):
            return list(set(d.child for d in self.displayables))

init 1500 python in phone.config:    
    overlay_screens.append("_phone_click_effects")