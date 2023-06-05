init -100 python in phone.discussion.audio_messages:
    from renpy import store
    from store import get_pos, TintMatrix, Flatten
    from store.phone import config

    current_p = None

    def reset():
        global current_p
        current_p = None
        renpy.music.stop("phone_audio_message")
        renpy.music.set_pause(False, "phone_audio_message")

    def play_audio(p, audio):        
        global current_p
        if current_p is p:
            if renpy.music.is_playing("phone_audio_message"):
                renpy.music.set_pause(not renpy.music.get_pause("phone_audio_message"), "phone_audio_message")
            else:
                renpy.music.play(audio, "phone_audio_message", loop=False)
        else:
            renpy.music.play(audio, "phone_audio_message", loop=False)
            current_p = p
            
    def button_image(st, at, p):
        global current_p
        if (
            current_p is p
            and renpy.music.is_playing("phone_audio_message")
            and not renpy.music.get_pause("phone_audio_message")
        ):
            image = config.basedir + "pause_icon.png"
        
        else:
            image = config.basedir + "play_icon.png"
        
        return image, 0.0
 
    wave_color = TintMatrix("#727272")(None, 1.0)
    
    class AudioWave(object):
        def __init__(self, p):
            self.p = p
        
        def __call__(self, child):
            return Flatten(_AudioWaveDisplayable(child, self.p))
    
    class _AudioWaveDisplayable(renpy.Displayable):
        def __init__(self, d, p):
            super(_AudioWaveDisplayable, self).__init__()

            self.d = renpy.displayable(d)
            self.p = p

        def render(self, w, h, st, at):
            renpy.redraw(self, 0.0)

            cr = renpy.render(self.d, w, h, st, at)
            
            global current_p
            if current_p is not self.p: return cr

            d = renpy.music.get_duration("phone_audio_message")
            if not d: return cr

            pos = get_pos("phone_audio_message")
            width, height = cr.get_size()
            
            mr = cr.subsurface((0, 0, min(((pos / d) * width), width), height))
            mr.add_shader("renpy.matrixcolor")
            mr.add_uniform("u_renpy_matrixcolor", wave_color)

            rv = renpy.Render(width, height)
            rv.blit(cr, (0, 0))
            rv.blit(mr, (0, 0), main=False)
            return rv
        
        def visit(self):
            return [self.d]