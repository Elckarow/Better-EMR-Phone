define gui.phone_zoom = 0.8
define gui.phone_xsize = 389
define gui.phone_ysize = 803

define gui.phone_call_xpos = 0.07

define gui.phone_message_frame_padding = (8, 8, 8, 8)
define gui.phone_message_label_null_height = 4

init 10 python:
    config.gl2 = True # required
    config.developer = True

    config.start_callbacks.append(lambda: renpy.run(Preference("rollback side", "left")))

init -10 python:
    import collections
    import datetime
    import time

    # RoundedFrame by pseurae
    # https://gist.github.com/Pseurae/661e6084f756fc917b2889a386b16664
    # modified by yours truly (i don't know shit about OpenGL)

    class RoundedFrame(renpy.display.image.Frame):
        def __init__(self, image, *args, **kwargs):
            radius = kwargs.pop("radius", 0.0)
            super(RoundedFrame, self).__init__(image, *args, **kwargs)
            
            if not isinstance(radius, tuple):
                radius = (radius,) * 4

            self.radius = radius

        def render(self, width, height, st, at):
            rv = super(RoundedFrame, self).render(width, height, st, at)

            if self.radius:
                rv.mesh = True
                rv.add_property("gl_pixel_perfect", True)
                rv.add_property("gl_mipmap", False)
                rv.add_shader("shader.rounded_corners")
                rv.add_uniform("u_radius", self.radius)
                rv.add_property("texture_scaling", "nearest")

            return rv

    renpy.register_shader("shader.rounded_corners", variables="""
        uniform vec4 u_radius;
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec2 res0;
        uniform vec2 u_model_size;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_functions="""
        // https://www.iquilezles.org/www/articles/distfunctions/distfunctions2d.htm
        float rounded_rectangle(in vec2 p, in vec2 b, in vec4 r)
        {
            r.xy = (p.x > 0.0) ? r.xy : r.zw;
            r.x  = (p.y > 0.0) ? r.x  : r.y;
            vec2 q = abs(p) - b + r.x;
            return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r.x;
        }
    """, fragment_200="""
        vec2 center = u_model_size.xy / 2.0;
        vec2 uv = (v_tex_coord.xy * u_model_size.xy);
        float crop = rounded_rectangle(uv - center, center, u_radius);
        vec4 color = texture2D(tex0, v_tex_coord);
        gl_FragColor = mix(vec4(0.0), color, smoothstep(1.0, 0.0, crop));
    """)