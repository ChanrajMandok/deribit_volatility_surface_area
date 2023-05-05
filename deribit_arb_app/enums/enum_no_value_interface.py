from enum import Enum

    ##################################################
    # Interface provdes no value interface for Enums #
    ##################################################

class NoValue(Enum):

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)
