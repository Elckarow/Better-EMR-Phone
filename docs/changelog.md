# Changelog

A list of all the changes throughout the versions, starting from 3.0.0.

## 3.0.4
- Improved lint.
- `phone.discussion.date` now accepts `None` and `True` values (before, only the `date` phone statement could use `None` values).
- The `image` phone statement and `phone.discussion.image` can now take any displayable.
- Fixed an issue with `gui.phone_message_label_null_height`.

## 3.0.3
- Fixed the `calendar` app layout.

## 3.0.2
- Fixed the `pass` phone discussion statement

## 3.0.1
- Phone messages now respect the `delay` property.
- Phone labels can now accept `None` values.
- The audio icon in the status bar now uses `preferences.get_mixer` on 7.6/8.1+ and `preferences.get_volume` on other Ren'Py versions.
- A new function has been introduced to the `phone.character` namespace: `get_all()`.
- A new function has been introduced to the `phone.group_chat` namespace: `get_all()`.

## 3.0.0
- None