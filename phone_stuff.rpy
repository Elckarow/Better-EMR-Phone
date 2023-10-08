init -999:
    define config.gl2 = True
    define config.early_start_store = False

init -200:
    define gui.phone_margin = (15, 81, 15, 94)
    define gui.phone_zoom = 0.8
    define gui.phone_xsize = 389
    define gui.phone_ysize = 803

    define gui.phone_status_bar_height = 22

    define gui.phone_call_xpos = 0.07

    define gui.phone_message_frame_padding = (8, 8, 8, 8)

    define gui.phone_message_label_null_height = 4

    define gui.phone_application_frame_padding = 16
    define gui.phone_application_icon_size = 65
    define gui.phone_application_rounded_corners_radius = 17

    define gui.phone_calendar_button_size = 40

    define gui.phone_control_center_spacing = 10
    define gui.phone_control_center_block_size = 70
    define gui.phone_control_center_block_scaling_factor = 0.75
    define gui.phone_control_center_block_rounded_corners_radius = 20

python early:
    import collections, pygame_sdl2 as pygame

    @renpy.pure
    def is_renpy_version_or_above(major, minor, patch):
        """
        Checks if the current version of renpy is at least `(major, minor, patch)`.
        If renpy is on a py3 / r8 version, `(major + 1, minor - 5, patch)` is checked.

        I.e., if the game runs on renpy 8 and that this function is called to check for `7.5.0`, `8.0.0` (the py3 / r8 equivalent of `7.5.0`) is checked for.
        """
        current_version = renpy.version_tuple[:3]

        if not renpy.compat.PY2:
            r8version = (major + 1, minor - 5, patch)
            return current_version >= r8version

        return current_version >= (major, minor, patch)
        
    def hyperlink_functions_style(name):
        """
        Hyperlink functions but the style `name` is used.

        `name`: str
            The style to use.
        """
        style_object = getattr(style, name)
        return (lambda target: style_object,) + style.default.hyperlink_functions[1:]

    if is_renpy_version_or_above(7, 6, 0):
        def get_mixer(mixer):
            return preferences.get_mixer(mixer)
    else:
        def get_mixer(mixer):
            return preferences.get_volume(mixer)

    def pause(time=None):
        if time is None:
            ui.saybehavior(afm=" ")
            ui.interact(mouse='pause', type="pause", roll_forward=None)
            return
        if time <= 0: return
        renpy.pause(time)
    
    def get_pos(channel="music"): 
        return renpy.music.get_pos(channel) or 0.0
    
    def normalize_color(col):
        a = col[3] / 255.0        
        r = a * col[0] / 255.0        
        g = a * col[1] / 255.0        
        b = a * col[2] / 255.0        
        return (r, g, b, a)

    # RoundedFrame by pseurae
    # https://gist.github.com/Pseurae/661e6084f756fc917b2889a386b16664
    # modified by yours truly (i don't know shit about OpenGL)
    class RoundedFrame(renpy.display.image.Frame):
        def __init__(self, image, *args, **kwargs):
            radius = kwargs.pop("radius", 0.0)
            outline_width = kwargs.pop("outline_width", 0.0)
            outline_color = kwargs.pop("outline_color", "#fff")

            super(RoundedFrame, self).__init__(image, *args, **kwargs)
            
            if not isinstance(radius, tuple): radius = (radius,) * 4
            self.radius = radius    

            self.outline_width = outline_width
            self.outline_color = normalize_color(Color(outline_color))

        def render(self, w, h, st, at):
            rv = super(RoundedFrame, self).render(w, h, st, at)

            if self.radius:
                rv.mesh = True
                rv.add_property("gl_pixel_perfect", True)
                rv.add_property("gl_mipmap", False)
                rv.add_property("texture_scaling", "nearest")
                rv.add_shader("shader.rounded_corners")
                rv.add_uniform("u_radius", self.radius)
                rv.add_uniform("u_outline_width", self.outline_width)
                rv.add_uniform("u_outline_color", self.outline_color)

            return rv

    renpy.register_shader("shader.rounded_corners", variables="""
        uniform vec4 u_radius;
        uniform float u_outline_width;
        uniform vec4 u_outline_color;
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec2 res0;
        uniform vec2 u_model_size;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_functions="""
        // https://www.iquilezles.org/www/articles/distfunctions/distfunctions2d.htm
        float rounded_rectangle(in vec2 p, in vec2 b, in vec4 r) {
            r.xy = (p.x > 0.0) ? r.xy : r.zw;
            r.x  = (p.y > 0.0) ? r.x  : r.y;
            vec2 q = abs(p) - b + r.x;
            return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r.x;
        }
    """, fragment_200="""
        vec2 center = u_model_size.xy / 2.0;
        vec2 uv = (v_tex_coord.xy * u_model_size.xy);
        vec4 color = texture2D(tex0, v_tex_coord);

        if (u_outline_width > 0.0) {
            vec2 center_outline = center - u_outline_width;

            float crop1 = rounded_rectangle(uv - center, center, vec4(u_radius));
            float crop2 = rounded_rectangle(uv - center, center_outline, vec4(u_radius - u_outline_width));

            float coeff1 = smoothstep(1.0, -1.0, crop1);
            float coeff2 = smoothstep(1.0, -1.0, crop2);

            float outline_coeff = (coeff1 - coeff2);

            gl_FragColor = mix(vec4(0.0), mix(color, u_outline_color, outline_coeff), coeff1);
        } 
        else {
            float crop = rounded_rectangle(uv - center, center, vec4(u_radius));
            gl_FragColor = mix(vec4(0.0), color, smoothstep(1.0, 0.0, crop));
        }
    """)

    # taken from
    # https://github.com/WretchedTeam/WintermuteV3/blob/main/game/mod_code/backend/displayables.rpy
    class ShaderDisplayable(renpy.Displayable):
        """
        A displayable that uses a shader to create an image.
        """
        def __init__(self, shader, uniforms=None, properties=None, **kwargs):
            super(ShaderDisplayable, self).__init__(**kwargs)
            self.style.subpixel = True

            self.shader = shader
            self.uniforms = uniforms or {}
            self.properties = properties or {}
        
        def render(self, w, h, st, at):
            rv = renpy.Render(w, h)
            rv.mesh = renpy.gl2.gl2mesh2.Mesh2.texture_rectangle(
                0, 0, w, h,
                0.0, 0.0, 1.0, 1.0,
            )

            rv.add_shader(self.shader)
            for u_name, uniform in self.expand_dict(self.uniforms):
                rv.add_uniform(u_name, uniform)
            for p_name, property in self.expand_dict(self.properties):
                rv.add_property(p_name, property)
            
            rv.add_property("gl_pixel_perfect", True)
            rv.add_property("gl_mipmap", False)
            return rv
        
        @staticmethod
        def expand_dict(d):
            for k, v in d.items():
                if isinstance(v, ColorMatrix):
                    v = v(None, 1.0)
                yield (k, v)

    # https://github.com/WretchedTeam/WintermuteV3/blob/68415d2e1dd0e9b404361f1bd300084fa39fbfc0/game/mod_code/definitions/shaders/gradient.rpy
    class Gradient(ShaderDisplayable):
        def __init__(self, start_color, end_color, theta=0, start_pos=0.0, end_pos=1.0, **kwargs):
            uniforms = {
                "u_start_color": normalize_color(Color(start_color)),
                "u_end_color": normalize_color(Color(end_color)),
                "u_theta": theta - 90,
                "u_start_pos": start_pos,
                "u_end_pos": end_pos
            }
            properties = {"texture_scaling": "nearest"}
            super(Gradient, self).__init__("shaders.gradient", uniforms, properties, **kwargs)

    renpy.register_shader("shaders.gradient", variables="""
        uniform float u_theta;
        uniform float u_start_pos;
        uniform float u_end_pos;
        uniform vec4 u_start_color;
        uniform vec4 u_end_color;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_functions="""
        mat2 rotate_matrix(float x) {
            return mat2(
                cos(radians(x)), -sin(radians(x)),
                sin(radians(x)), cos(radians(x))
            );
        }
        float map(float value, float min1, float max1, float min2, float max2) {
            return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
        }
    """, fragment_200="""
        // Map it to (-1 and 1)
        vec2 uv = v_tex_coord.xy * 2.0 - 1.0;
        uv *= rotate_matrix(u_theta);
        // Map it back to (0 and 1) 
        uv = (uv + 1.0) / 2.0;
        float coeff = clamp(uv.x, 0.0, 1.0);
        coeff = map(coeff, u_start_pos, u_end_pos, 0.0, 1.0);
        gl_FragColor = mix(u_start_color, u_end_color, clamp(coeff, 0.0, 1.0));
    """)

    # displayable by yours truly
    # shader by the one and only -2
    class CircleDisplayable(ShaderDisplayable):
        def __init__(self, border, radius=None, color="#fff", **kwargs):
            uniforms = {
                "u_border": border,
                "u_color":  normalize_color(Color(color))
            }
            super(CircleDisplayable, self).__init__("shaders.circle", uniforms, **kwargs)

            self.radius = radius
            self.border = self.uniforms["u_border"]

        def render(self, w, h, st, at):
            if self.radius is None:
                radius = min(w, h) / 2.0
            else:
                radius = self.radius
            
            width = height = radius * 2.0
            
            if not self.border: return renpy.Render(width, height)
            return super(CircleDisplayable, self).render(width, height, st, at)
    
    renpy.register_shader("shaders.circle", variables="""
        uniform float u_border;
        uniform vec4 u_color;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec2 u_model_size;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_200="""
        vec2 center = u_model_size.xy / 2.0;
        vec2 uv = (v_tex_coord.xy * u_model_size.xy) - center;

        float d = length(uv);
        float radius = min(u_model_size.x, u_model_size.y) / 2.0 - u_border;
        
        gl_FragColor = mix(vec4(0.0), u_color, 1.0 - smoothstep(0.0, u_border, abs(radius - d)));
    """)