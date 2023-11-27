# to create integer enumeration constants
from enum import IntEnum, auto


class Role(IntEnum):
    """
    Class int-enum for square roles
    """
    NONE = 0
    ENEMY = auto()
    ENTRANCE = auto()
    EXIT = auto()
    EXTERIOR = auto()
    REWARD = auto()
    WALL = auto()
