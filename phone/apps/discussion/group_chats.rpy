init -100 python in phone.group_chat:
    from renpy.store import store, phone
    import datetime

    config = phone.config

    class GroupChat(object):    
        transient = False
        _unread = True
        
        def __init__(self, name, icon, key, transient=False):
            global _group_chats
            _group_chats[key] = self

            self.name = name
            self.icon = icon
            self.date = datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0)
            self.transient = transient

            self._unread = True

            self._characters = set()            
            self._payloads = [ ]
            self._page = 0
            
            if key is None: raise ValueError("key may not be 'None'")
            self.key = key

            # deprecated
            self.short_name = name
        
        @property
        def unread(self):
            if not config.unread_group_chat_pov:
                return self._unread
            return phone.data[store.pov_key]["group_chat_unread_pov"].setdefault(self.key, True)
        
        @unread.setter
        def unread(self, v):
            if not config.unread_group_chat_pov:
                self._unread = v
            else:
                phone.data[store.pov_key]["group_chat_unread_pov"][self.key] = v
                
        def add_character(self, char):
            if isinstance(char, list):
                for c in char:
                    self.add_character(c)
            else:
                char = character(char).key
                self._characters.add(char)

                if self.key not in phone.data[char]["group_chats"]:
                    phone.data[char]["group_chats"].append(self.key)
            
            return self
        
        def remove_character(self, char):
            char = character(char).key
            if char not in self._characters: return
            self._characters.remove(char)

            phone.data[char]["group_chats"].remove(self.key)
        
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
    
        def clear(self):
            self._payloads.clear()
        
        def _can_load_more(self):
            if not self._payloads: return False         
            return self._get_messages()[0] is not self._payloads[0]
        
        def _get_messages(self):
            messages_displayed = config.messages_displayed

            min_x = self._page * messages_displayed
            max_x = min_x + messages_displayed

            l = len(self._payloads)

            remaining = l - max_x
            if remaining <= config.messages_fill_if_lower:
                max_x += remaining

            return self._payloads[l-max_x:l-min_x]
        
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

            if p.type == _PayloadTypes.TYPING:
                raise Exception("can't save typing")
            elif p.type == _PayloadTypes.MENU:
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
        if not has_group_chat(x):
            raise KeyError("no group chat with the key %r exists (check your definitions)" % x)
        return _group_chats[x]
    
    def has_group_chat(key):
        return key in _group_chats

    def get_all():
        return list(_group_chats.values())
    
default -100 phone.group_chat._group_chats = { }

init python in phone.group_chat:
    from store.phone.character import character
    from store.phone.discussion import _PayloadTypes, remove_text_tags
    from store.phone import format_time, format_date