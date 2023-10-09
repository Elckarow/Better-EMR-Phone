Click effects
=============

The framework comes with a built-in click effects that shows a displayable whenever a click/drag/release occurs.

It uses three variables

* ``phone_on_click_effect``
* ``phone_on_drag_effect``
* ``phone_on_release_effect``

which are, if not ``None``, a 2-tuple containing a displayable and a float.

Whenever the corresponding mouse event occurs

* a left/right click for ``phone_on_click_effect``
* moving the mouse while holding click for ``phone_on_drag_effect``
* releasing a click for ``phone_on_release_effect``

the corresponding displayable will be added to the screen and then hidden after the amout of time passed as second element of the tuple.

say you have this ::

    define phone_on_click_effect = (Solid("#f00", xysize=(50, 50)), 2)

left/right clicking will add a 50x50 red square to the screen that will be hidden after 2 seconds.