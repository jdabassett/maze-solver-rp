from mazelib import Maze as Maze_API
from mazelib.generate import Prims, HuntAndKill, AldousBroder, BacktrackingGenerator, BinaryTree, CellularAutomaton, DungeonRooms, Ellers, GrowingTree, Kruskal, Division, Sidewinder, Wilsons
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

from src.models.maze import Maze
from src.generate.convert_api_maze import string_to_maze


def create_maze(select, dim_row, dim_col) -> Maze:
    """
    Input maze dimensions
    Output formatted maze
    :param select: int
    :param dim_row: int
    :param dim_col: int
    :return: Maze
    """
    maze_string = create_api(select, dim_row, dim_col)
    maze_new = string_to_maze(maze_string)
    return maze_new


def switch_functions(select, dim_row, dim_col):
    """
    Input integers for what maze generator the user wants to use, and the dimensions the maze should take.
    Output maze generator.
    :param select: int
    :param dim_row: int
    :param dim_col: int
    :return: maze generator
    """
    switch_dict = {
        1: AldousBroder.AldousBroder,
        2: BacktrackingGenerator.BacktrackingGenerator,
        3: BinaryTree.BinaryTree,
        4: CellularAutomaton.CellularAutomaton,
        5: Division.Division,
        6: DungeonRooms.DungeonRooms,
        7: Ellers.Ellers,
        8: GrowingTree.GrowingTree,
        9: HuntAndKill.HuntAndKill,
        10: Kruskal.Kruskal,
        11: Prims.Prims,
        12: Sidewinder.Sidewinder,
        13: Wilsons.Wilsons,
    }
    function = switch_dict.get(select, BacktrackingGenerator.BacktrackingGenerator)
    return function(dim_row, dim_col)


def create_api(select, dim_row, dim_col):
    """
    Input maze dimensions.
    Output string representation of the maze.
    :param select: int
    :param dim_row: int
    :param dim_col: int
    :return: str
    """
    m = Maze_API()
    m. generator = switch_functions(select, dim_row, dim_col)
    m.generate()
    m.solver = BacktrackingSolver()
    m.generate_entrances()
    m.solve()
    return m.tostring(entrances=True, solutions=False)


if __name__ == "__main__":
    from src.view.renderer import SVGRenderer
    maze = create_maze(6, 10, 10)
    SVGRenderer(30, 6).render(maze=maze).preview()
