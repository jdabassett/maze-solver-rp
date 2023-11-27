from dataclasses import dataclass
from functools import cached_property
from typing import Iterator

from role import Role
from square import Square


@dataclass(frozen=True)
class Maze:
    """
    Immutable dataclass representing maze as tuple of squares
    """
    squares: tuple[Square, ...]

    def __post_init__(self) -> None:
        """
        Post initialization checks if maze is valid
        """
        # if all square have valid index values
        validate_indices(self)
        # if all squares have valid row and column values
        validate_rows_columns(self)
        # if there is exactly one square with an entrance role per maze
        validate_entrance(self)
        # if there is exactly one square with an exit role per maze
        validate_exit(self)

    def __iter__(self) -> Iterator[Square]:
        """
        Transform maze into an iterable
        :return: Iterator
        """
        return iter(self.squares)

    def __getitem__(self, index: int) -> Square:
        """
        Input index and return square at that index from maze
        :param index:
        :return:
        """
        return self.squares[index]

    @cached_property
    def width(self):
        """
        Returns max width of maze
        :return: integer
        """
        return max(square.column for square in self) + 1

    @cached_property
    def height(self):
        """
        Returns max height of maze
        :return: integer
        """
        return max(square.row for square in self) + 1

    @cached_property
    def entrance(self) -> Square:
        """
        Returns entrance from maze
        :return: Square
        """
        return next(sq for sq in self if sq.role is Role.ENTRANCE)

    @cached_property
    def exit(self) -> Square:
        """
        Returns exit from maze
        :return: Square
        """
        return next(sq for sq in self if sq.role is Role.EXIT)


def validate_indices(maze: Maze) -> None:
    """
    Raises assertion if any square index from maze is not valid or in proper order
    :param maze:
    :return: None
    """
    assert [square.index for square in maze] == list(
        range(len(maze.squares))
    ), "Wrong square.index"


def validate_rows_columns(maze: Maze) -> None:
    """
    Raises assertion if any square row or column values from maze are not valid or in proper oder
    :param maze:
    :return: None
    """
    for y in range(maze.height):
        for x in range(maze.width):
            square = maze[y * maze.width + x]
            assert square.row == y, "Wrong square.row"
            assert square.column == x, "Wrong square.column"


def validate_entrance(maze: Maze) -> None:
    """
    Raises assertion if maze doesn't have exactly one entrance
    :param maze:
    :return: None
    """
    assert 1 == sum(
        1 for square in maze if square.role is Role.ENTRANCE
    ), "Must be exactly one entrance"


def validate_exit(maze: Maze) -> None:
    """
    Raises assertion if maze doesn't have exactly one exit
    :param maze:
    :return: None
    """
    assert 1 == sum(
        1 for square in maze if square.role is Role.EXIT
    ), "Must be exactly one exit"
