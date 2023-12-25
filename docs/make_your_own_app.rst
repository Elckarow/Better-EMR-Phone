Wanna make your own app?
========================

In order to do that, you need **two** things:

* A phone screen
* A ``phone.application.Application`` object (not necessary but if you want your app to appear on the ``phone`` screen then yes you need this)

The ``_phone`` screen
---------------------

To create a phone screen, simply ``use`` the ``_phone`` screen, intended as base for all phone screen. ::

    screen my_phone_screen():
        use _phone():
            # your screen code goes there

The ``_phone`` screen has 5 parameters:

* ``xpos`` The xpos of the phone.
* ``ypos`` The ypos of the phone.
* ``xanchor`` The xanchor of the phone.
* ``yanchor`` The yanchor of the phone.
* ``horizontal`` If true, the phone is displayed horizontally. If false, it is displayed vertically.

Once you've coded your screen, simply call it with ``phone.call_screen`` or the ``PhoneMenu`` action and there you go!

Applications
------------

If you want your app to appear on the ``phone`` screen, you need to create a ``phone.application.Application`` object and add it to your ``*character*``\s.

*The following functions and classes are defined in the* **phone.application** *namespace.*

``class Application(object)``

``def __init__(self, name, icon, action)``

* ``name`` A string. The name of the app.
* ``icon`` A ``phone.application.Icon`` or ``phone.application.GradientBackground`` object.
* ``action`` An action to run when clicking on the app (most of the time it's a ``PhoneMenu`` action, but any valid action works).

``def Icon(d, size=None, background=None)``
    Retuns a displayable used as icon for applications.
    ``d`` is a displayable to add on to the icon. ``size`` is the size that displayable takes.
    ``background``, if not ``None``, is a ``phone.application.IconBackground`` or ``phone.application.GradientBackground`` object displayed behind ``d``.

``def GradientBackground(start_color, end_color, theta=0)``
    Retuns a ``phone.application.IconBackground`` object with a ``Gradient`` as displayable.

``def IconBackground(d, **kwargs)``
    Returns ``d`` with rounded corners of size ``gui.phone_application_icon_size``.

Example
-------
::

    init python:
        my_app = phone.application.Application(
            "my application",
            phone.application.GradientBackground("#5bf676", "#04be25"),
            PhoneMenu("my_phone_screen")
        ) 

Now that you've done this, it's time to add the app to the ``*character*``\s you've defined, using those two functions.

``def add_application(app, page=0, key=None)``
    Adds the application ``app`` to the known applications for ``*character*`` ``key``. Returns ``True`` if it succesfully added the app, ``False`` if it failed, or ``None`` if Ren'Py is still in init phase.

``def add_app_to_all_characters(app, page=0)``
    Same as above but for every ``*character*`` known at execution time.

To add the app you've created, simply ::

    phone.application.add_app_to_all_characters(my_app)

and ta-da, your app should appear on the ``phone`` screen.

Functions
---------

``def move_application(start, end, key=None)``
    ``start``/``end`` are 3-tuples containing a page, a column and a row. They represent the start/end point. This function swaps the application of coordinates ``start`` with the one of coordinates ``end``.