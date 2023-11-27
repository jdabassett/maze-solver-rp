# parent to data classes that are expected by only contain and modify their own data
from dataclasses import dataclass
# to iterate over iterable and reduce to single element
from functools import reduce
# type hinting iterator
from typing import Iterator

from src.maze_solver.models.role import Role
from src.maze_solver.models.square import Square


@dataclass(frozen=True)
class Solution:
    """
    Immutable dataclass of maze solution
    Contains tuple of squares that form path of solution
    """
    squares: tuple[Square, ...]

    def __post_init__(self) -> None:
        """
        Post initialization tests to verify that solution could be a valid one
        :return: None
        """
        # raise assertion if first square doesn't have role of entrance
        assert self.squares[0].role is Role.ENTRANCE
        # raise assertion if last square doesn't have role of exit
        assert self.squares[-1].role is Role.EXIT
        # check that all adjacent squares either share a row or column value
        reduce(validate_corridor, self.squares)

    def __iter__(self) -> Iterator[Square]:
        """
        Transform solutions dataclass into iterable
        :return: iterator
        """
        return iter(self.squares)

    def __getitem__(self, index: int) -> Square:
        """
        Input index and return square at index from solution dataclass
        :param index:
        :return:
        """
        return self.squares[index]

    def __len__(self) -> int:
        """
        Return length of solution
        :return: integer
        """
        return len(self.squares)


def validate_corridor(current: Square, following: Square) -> Square:
    """
    Check that all adjacent squares either share a row or column value
    Will raise assertion if ever false
    :param current:
    :param following:
    :return: Square
    """
    assert any(
        [current.row == following.row, current.column == following.column]
    ), "Squares must lie in the same row or column"
    return following
