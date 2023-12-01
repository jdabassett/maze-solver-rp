from src.models.border import Border
from src.models.square import Square
from src.models.role import Role
from src.models.maze import Maze


def string_to_maze(maze_api) -> Maze:
    """
    Input string maze from mazelib.
    Output formatted maze.
    :param maze_api: string
    :return: Maze
    """
    list_api = string_to_list(maze_api)
    maze_api_dim = find_dim(list_api)
    maze_api_dict = maze_to_dictionary(list_api)
    maze_new = generate_maze(maze_api_dict, maze_api_dim)
    return maze_new


def string_to_list(str_maze) -> list[str]:
    """
    Input string.
    Output list of strings split at "\n".
    :param str_maze: str
    :return: list
    """
    list_maze = str_maze.split("\n")
    return list_maze


def find_dim(list_maze) -> dict:
    """
    Input list of strings.
    Output dictionary with "height" and "width" attributes.
    :param list_maze: list
    :return: dict
    """
    height = len(list_maze)
    width = len(list_maze[0])
    return {"height": height, "width": width}


def maze_to_dictionary(list_maze) -> dict:
    """
    Input list of strings representing maze.
    Output dictionary with each pair representing a border or square.
    :param list_maze: list
    :return: dict
    """
    borders = {}
    for row_index, row in enumerate(list_maze):
        for column, char in enumerate(row):
            borders[f"{row_index},{column}"] = char
    return borders


def generate_maze(maze_dict, maze_dim) -> Maze:
    """
    Input maze as dictionary and dimensions as dictionary.
    Output formatted Maze.
    :param maze_dict: dict
    :param maze_dim: dict
    :return: Maze
    """
    offsets = {"TOP": (-1, 0), "RIGHT": (0, 1), "BOTTOM": (1, 0), "LEFT": (0, -1)}
    index = 0
    row = 0
    squares = []
    for i in range(1, maze_dim["height"], 2):
        column = 0
        for j in range(1, maze_dim["width"], 2):
            role = Role.NONE
            border = Border.EMPTY
            for direction, offset in offsets.items():
                io = i + offset[0]
                jo = j + offset[-1]
                ij = f"{io},{jo}"
                if io < 0 or io >= maze_dim['height'] or jo < 0 or jo >= maze_dim["width"]:
                    continue
                elif ij not in maze_dict:
                    continue
                value = maze_dict[ij]
                if value == "#":
                    if border is not Border.EMPTY:
                        border = border | Border[direction]
                    else:
                        border = Border[direction]
                elif value == "S":
                    role = Role.ENTRANCE
                elif value == "E":
                    role = Role.EXIT
            squares.append(Square(index, row, column, border, role))
            index += 1
            column += 1
        row += 1
    maze_new = Maze(tuple(squares))
    return maze_new


# if __name__ == "__main__":
#     from src.view.renderer import SVGRenderer
#     m = """#########E#
# #   # # #+#
# # ### # #+#
# #+++++++++#
# #+#########
# #+++  # # #
# ###+### # #
# #  +#     #
# # #+### # #
# # #+++  # #
# #####S#####"""
#
#     maze = string_to_maze(m)
#     SVGRenderer().render(maze).preview()
