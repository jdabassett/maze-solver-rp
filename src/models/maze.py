# parent to data classes that are expected by only contain and modify their own data
from dataclasses import dataclass
# to cache method results to avoid recalculations when recalled
from functools import cached_property
# type hints for iterator
from typing import Iterator
from pathlib import Path

from src.models.role import Role
from src.models.square import Square
from src.persistence.serializer import (
    dump_squares,
    load_squares,
)


@dataclass(frozen=True)
class Maze:
    """
    Immutable dataclass representing maze as tuple of squares
    """
    squares: tuple[Square, ...]

    @classmethod
    def load(cls, path: Path) -> "Maze":
        """
        Input file path
        Output is a maze instance with data from binary maze file
        :param path:
        :return: Maze
        """
        return Maze(tuple(load_squares(path)))

    def dump(self, path: Path) -> None:
        """
        Input file path
        Writes maze self into binary maze file at file path
        :param path:
        :return:
        """
        dump_squares(self.width, self.height, self.squares, path)

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
        :return: iterator
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
    Raises exception if any square index from maze is not valid or in proper order
    :param maze:
    :return: None
    """
    assert [square.index for square in maze] == list(
        range(len(maze.squares))
    ), "Wrong square.index"


def validate_rows_columns(maze: Maze) -> None:
    """
    Raises exception if any square row or column values from maze are not valid or in proper oder
    :param maze:
    :return: None
    """
    for y in range(0, maze.height):
        for x in range(0, maze.width):
            index = y * maze.width + x
            square = maze[index]
            assert square.row == y, "Wrong square.row"
            assert square.column == x, "Wrong square.column"


def validate_entrance(maze: Maze) -> None:
    """
    Raises exception if maze doesn't have exactly one entrance
    :param maze:
    :return: None
    """
    assert 1 == sum(
        1 for square in maze if square.role is Role.ENTRANCE
    ), "Must be exactly one entrance"


def validate_exit(maze: Maze) -> None:
    """
    Raises exception if maze doesn't have exactly one exit
    :param maze:
    :return: None
    """
    assert 1 == sum(
        1 for square in maze if square.role is Role.EXIT
    ), "Must be exactly one exit"



# run the following in shell to test proper functionality
# from src.maze_solver.models.border import Border
# from src.maze_solver.models.maze import Maze
# from src.maze_solver.models.role import Role
# from src.maze_solver.models.square import Square
#
#
if __name__=="__main__":
    from src.models.border import Border
    maze = Maze(
         squares=(
             Square(0, 0, 0, Border.TOP | Border.LEFT),
             Square(1, 0, 1, Border.TOP | Border.RIGHT),
             Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
             Square(3, 0, 3, Border.TOP | Border.LEFT | Border.RIGHT),
             Square(4, 1, 0, Border.BOTTOM | Border.LEFT | Border.RIGHT),
             Square(5, 1, 1, Border.LEFT | Border.RIGHT),
             Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
             Square(7, 1, 3, Border.RIGHT),
             Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
             Square(9, 2, 1, Border.BOTTOM),
             Square(10, 2, 2, Border.TOP | Border.BOTTOM),
             Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
         )
     )


# here is another test
# from pathlib import Path
# from src.maze_solver.models.maze import Maze
# maze = Maze.load(Path("miniature.maze"))
# maze.width, maze.height
# len(maze.squares)
# maze.entrance
# maze.exit


# a more complex one
# from pathlib import Path
# from src.maze_solver.models.maze import Maze
# from src.maze_solver.view.renderer import SVGRenderer
# maze = Maze.load(Path("mazes") / "labyrinth.maze")
# len(maze.squares), maze.height, maze.width
# SVGRenderer().render(maze).preview()
