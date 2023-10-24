GUI Variables
=============

*Please note that this framework was developed on a 1280x720 project.*

These variables can be found in the ``phone_stuff.rpy`` file.

``gui.phone_xsize = 389``
    The width available for the phone screens.

``gui.phone_ysize = 803``
    The height available for the phone screens.

``gui.phone_margin = (15, 81, 15, 94)``
    Margins added to the left / top / right / bottom of the phone's available area, respectively.

*If you take* **gui.phone_margin** *to be* **(l, t, r, b)** *,* **l + r + gui.phone_xsize** *and* **t + b + gui.phone_ysize** *should match the phone's background image's dimensions (the one at* **phone.config.basedir + "background.png"** *).*

``gui.phone_zoom = 0.8``
    The level of zoom applied to the phone. If your project uses a different aspect ratio than 1280x720, you might want to consider modifying this variable.

*Other GUI variables exist but should not be changed by creators.*