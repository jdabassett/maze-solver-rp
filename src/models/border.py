# to create integer and binary compatible enumeration constants
from enum import IntFlag, auto


class Border(IntFlag):
    """
    Class int-flag-enum for square borders
    """
    EMPTY = 0
    TOP = auto()
    LEFT = auto()
    BOTTOM = auto()
    RIGHT = auto()

    @property
    def corner(self) -> bool:
        """
        Will check self if square borders are a corner
        :return: boolean
        """
        return self in (
            self.TOP | self.LEFT,
            self.TOP | self.RIGHT,
            self.BOTTOM | self.LEFT,
            self.BOTTOM | self.RIGHT,
        )

    @property
    def dead_end(self) -> bool:
        """
        Will check self if square borders are a dead-end
        :return: boolean
        """
        return self.bit_count() == 3

    @property
    def intersection(self) -> bool:
        """
        Will check self if square borders are an intersection
        :return: boolean
        """
        return self.bit_count() < 2

    def __getitem__(self, input):
        """
        input string
        returns class attribute
        :param input:
        :return:
        """
        if input == "EMPTY":
            return Border.EMPTY
        elif input == "TOP":
            return Border.TOP
        elif input == "LEFT":
            return Border.LEFT
        elif input == "BOTTOM":
            return Border.BOTTOM
        elif input == "RIGHT":
            return Border.RIGHT
        else:
            raise ValueError("Invalid input for Border subscription.")
