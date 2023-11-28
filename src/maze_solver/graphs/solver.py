import networkx as nx

from src.maze_solver.graphs.converter import make_graph
from src.maze_solver.models.maze import Maze
from src.maze_solver.models.solution import Solution


def solve(maze: Maze) -> Solution | None:
    try:
        # returns solution instance if found
        return Solution(
            squares=tuple(
                # returns list of one of the shortest paths
                nx.shortest_path(
                    # convert maze into graph
                    make_graph(maze),
                    # specify start
                    source=maze.entrance,
                    # specify exit
                    target=maze.exit,
                    weight="weight",
                )
            )
        )
    except nx.NetworkXException:
        return None


def solve_all(maze: Maze) -> list[Solution]:
    try:
        # list comprehension to return list of shortest solutions
        return [
            Solution(squares=tuple(path))
            for path in nx.all_shortest_paths(
                make_graph(maze),
                source=maze.entrance,
                target=maze.exit,
                weight="weight",
            )
        ]
    except nx.NetworkXException:
        return []


# test by running following commands in shell
# from pathlib import Path
# from src.maze_solver.graphs.solver import solve
# from src.maze_solver.models.maze import Maze
# from src.maze_solver.view.renderer import SVGRenderer
#
# maze = Maze.load(Path("mazes") / "miniature.maze")
# solution = solve(maze)
#
# len(solution)
#
#
# [square.index for square in solution]
#
#
# SVGRenderer().render(maze, solution).preview()