from enum import Enum

    ##################################################
    # Interface provdes no value interface for Enums #
    ##################################################

class NoValue(Enum):

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    
    @classmethod
    def get(cls, name):
        return cls._value2member_map_.get(name, None)
