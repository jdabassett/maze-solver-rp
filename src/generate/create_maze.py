from mazelib import Maze as Maze_API
from mazelib.generate import BacktrackingGenerator
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

from src.models.maze import Maze
from src.generate.convert_api_maze import string_to_maze


def create_maze(dim_row=5, dim_col=5, generator=BacktrackingGenerator) -> Maze:
    """
    Input maze dimensions
    Output formatted maze
    :param dim_row: int
    :param dim_col: int
    :param generator: callable
    :return: Maze
    """
    maze_string = create_api(dim_row, dim_col, generator)
    maze_new = string_to_maze(maze_string)
    return maze_new


def create_api(dim_row, dim_col, generator):
    """
    Input maze dimensions.
    Output string representation of the maze.
    :param dim_row: int
    :param dim_col: int
    :param generator:
    :return: str
    """
    m = Maze_API()
    m. generator = generator(dim_row, dim_col)
    m.generate()
    m.solver = BacktrackingSolver()
    m.generate_entrances()
    m.solve()
    return m.tostring(entrances=True, solutions=False)


# if __name__ == "__main__":
#     from src.view.renderer import SVGRenderer
#     maze = create_maze(6, 10, 10)
#     SVGRenderer(30, 6).render(maze=maze).preview()
#     print(type(Wilsons.Wilsons))
