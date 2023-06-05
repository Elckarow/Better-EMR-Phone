init -100 python in phone.group_chat:
    from renpy import store
    from store import __, phone
    import datetime

    # The max lenght of a *group chat*'s name shortened.
    short_name_length = 9

    # How many messages we display at the same time.
    messages_displayed = 175

    # If the next "load" of messages contains this many or less messages, add those messages to the current load.
    messages_fill_if_lower = 15

    class GroupChat(object):    
        def __init__(self, name, icon, key):
            global _group_chats
            _group_chats[key] = self

            self.name = name
            self.icon = icon
            self.date = datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0)

            self.unread = True

            self._characters = set()            
            self._payloads = [ ]
            self._page = 0
            
            if key is None: raise ValueError("key may not be 'None'")
            self.key = key
        
        @property
        def short_name(self):
            global short_name_length
            name = __(self.name)
            if len(name) > short_name_length:
                name = name[:short_name_length - 3] + "..."
            
            return name
        
        def add_character(self, char):
            if isinstance(char, list):
                for c in char:
                    self.add_character(c)
            else:
                char = character(char).key
                self._characters.add(char)

                global data
                if self.key not in data[char]["group_chats"]:
                    data[char]["group_chats"].append(self.key)
            
            return self
        
        def remove_character(self, char):
            char = character(char).key
            if char not in self._characters: return
            self._characters.remove(char)

            global data
            data[char]["group_chats"].remove(self.key)
        
        def number_of_messages_sent(self, char):
            if char is not None: key = charcter(char).key
            else: key = char

            rv = 0
            for p in self._payloads:
                if (p.type in (_PayloadTypes.TEXT, _PayloadTypes.IMAGE, _PayloadTypes.AUDIO, _PayloadTypes.VIDEO)
                    and (key is None or p.source == key)
                ): rv += 1
            return rv
        
        @property
        def number_of_messages(self):
            return self.number_of_messages_sent(None)
        
        def _can_load_more(self):
            if not self._payloads: return False         
            return next(self._get_messages()) is not self._payloads[0]
        
        def _get_display_last_message(self):
            italic = True

            if not self._payloads:
                sender = None
                message = __("Empty group chat")
            
            else:
                p = self._payloads[-1]

                sender = p.source
                if sender is not None: sender = character(sender)

                _type = p.type

                if _type == _PayloadTypes.TEXT:
                    message = renpy.substitute(p.data)
                    italic = False

                elif _type == _PayloadTypes.IMAGE:
                    message = __("Image sent")
                
                elif _type == _PayloadTypes.LABEL:
                    message = renpy.substitute(p.data)
                
                elif _type == _PayloadTypes.DATE:
                    message = p.data
                
                elif _type == _PayloadTypes.AUDIO:
                    message = __("Audio sent")
                
                elif _type == _PayloadTypes.VIDEO:
                    message = __("Video sent")

            message = remove_text_tags(message)

            LIMIT = 27
            if len(message) >= LIMIT:
                message = message[:LIMIT - 3] + "..."
            
            if italic:
                message = "{i}" + message + "{/i}"
            
            return (sender, message)
        
        def _get_messages(self):
            global messages_displayed
            min_x = self._page * messages_displayed
            max_x = min_x + messages_displayed

            global messages_fill_if_lower
            remaining = len(self._payloads) - max_x
            if remaining <= messages_fill_if_lower:
                max_x += remaining

            return reversed(self._payloads[::-1][min_x:max_x])
        
        @property
        def _date_text(self):
            date = self.date
            return format_date(date.month, date.day, date.year)
        
        @property
        def _hour_text(self):
            date = self.date
            return format_time(date.hour, date.minute)
        
        def _save_payload(self, p, check_source=True):
            if check_source and p.source not in self._characters:
                raise Exception("sender '{}' isn't in group chat".format(p.source))

            if p.type == _PayloadTypes._DUMMY:
                raise Exception("can't save dummy message")
            elif p.type == _PayloadTypes._MENU:
                raise Exception("can't save menu")

            self._payloads.append(p)

            self.unread = phone.discussion._group_chat is not self 
        
        def _page_up(self):
            self._page += 1
            
        def _page_down(self):
            self._page -= 1
            
        def __iter__(self):
            return reversed(self._payloads)
        
        def __len__(self):
            return len(self._payloads)

        def __hash__(self):
            return hash(self.key)
    
    def group_chat(x):
        if isinstance(x, GroupChat): return x
        global _group_chats
        return _group_chats[x]
    
    def has_group_chat(key):
        global _group_chats
        return key in _group_chats
    
default -100 phone.group_chat._group_chats = { }

init python in phone.group_chat:
    from store.phone.character import character
    from store.phone.discussion import _PayloadTypes, remove_text_tags
    from store.phone import format_time, format_date

init python in phone:
    renpy_config.start_callbacks.append(lambda: setattr(group_chat, "data", data))