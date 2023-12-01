import array
import pathlib
from typing import Iterator

from src.models.border import Border
from src.models.role import Role
from src.models.square import Square
from src.persistence.file_format import FileBody, FileHeader

FORMAT_VERSION: int = 1


def dump_squares(
    width: int,
    height: int,
    squares: tuple[Square, ...],
    path: pathlib.Path,
) -> None:
    """
    Input maze width, height, squares, and file path with filename to write binary file
    :param width:
    :param height:
    :param squares:
    :param path:
    :return: None
    """
    # create FileHeader and FileBody instances
    header, body = serialize(width, height, squares)
    # open code block in write binary mode to write file using FileHeader and FileBody methods
    with path.open(mode="wb") as file:
        header.write(file)
        body.write(file)


def load_squares(path: pathlib.Path) -> Iterator[Square]:
    """

    :param path:
    :return:
    """
    with path.open("rb") as file:
        # extract header from file
        header = FileHeader.read(file)
        # if not valid header format version, raise exception
        if header.format_version != FORMAT_VERSION:
            raise ValueError("Unsupported file format version")
        # extract body from rest of file, remember pointer is currently pointing after header
        body = FileBody.read(header, file)
        return deserialize(header, body)


def serialize(
    width: int, height: int, squares: tuple[Square, ...]
) -> tuple[FileHeader, FileBody]:
    """
    Creates instances of FileHeader and FileBody from maze width, height, and squares
    Returns each
    :param width:
    :param height:
    :param squares:
    :return:
    """
    header = FileHeader(FORMAT_VERSION, width, height)
    body = FileBody(array.array("B", map(compress, squares)))
    return header, body


def deserialize(header: FileHeader, body: FileBody) -> Iterator[Square]:
    """
    Input header and body instances from imported file
    Output is iterator generator
    :param header:
    :param body:
    :return: Iterator
    """
    for index, square_value in enumerate(body.square_values):
        # create row and column values from index value
        row, column = divmod(index, header.width)
        # extract border and role instances from binary value of square
        border, role = decompress(square_value)
        yield Square(index, row, column, border, role)


def compress(square: Square) -> int:
    """
    Compress the role and border values into integer that will become one binary
    :param square:
    :return:
    """
    # shift role to the left and bitmask with border value to preserve both in new binary value
    return (square.role << 4) | square.border.value


def decompress(square_value: int) -> tuple[Border, Role]:
    """
    Decompress the role and border values from the compressed integer from the binary file
    :param square_value:
    :return:
    """
    # retrieve border value and create new border instance with it to return
    # shift input and use remainder to create instance of role to return
    return Border(square_value & 0xF), Role(square_value >> 4)


# to test run the following in a shell
# from pathlib import Path
#
# from src.maze_solver.models.border import Border
# from src.maze_solver.models.maze import Maze
# from src.maze_solver.models.role import Role
# from src.maze_solver.models.square import Square
# from src.maze_solver.persistence.serializer import dump_squares, load_squares
#
# maze = Maze(
#     squares=(
#         Square(0, 0, 0, Border.TOP | Border.LEFT),
#         Square(1, 0, 1, Border.TOP | Border.RIGHT),
#         Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
#         Square(3, 0, 3, Border.TOP | Border.LEFT | Border.RIGHT),
#         Square(4, 1, 0, Border.BOTTOM | Border.LEFT | Border.RIGHT),
#         Square(5, 1, 1, Border.LEFT | Border.RIGHT),
#         Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
#         Square(7, 1, 3, Border.RIGHT),
#         Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
#         Square(9, 2, 1, Border.BOTTOM),
#         Square(10, 2, 2, Border.TOP | Border.BOTTOM),
#         Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
#     )
# )
#
# path = Path("miniature.maze")
#
# dump_squares(maze.width, maze.height, maze.squares, path)
# load_squares(path) == maze
# load_squares(path) is maze