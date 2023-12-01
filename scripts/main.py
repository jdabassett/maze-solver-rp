import argparse
import pathlib
import json

from src.graphs.solver import solve_all
from src.models.maze import Maze
from src.view.renderer import SVGRenderer
from src.generate.create_maze import create_maze


def load_messages() -> dict:
    """
    load prompts for client interaction
    :return: dict
    """
    cwd = pathlib.Path.cwd()
    path_messages = cwd.joinpath('resources/text/messages.json')
    with path_messages.open("r") as file:
        messages = json.load(file)
    return messages


def solve_maze() -> None:
    maze = Maze.load(parse_path())
    solutions = solve_all(maze)
    if solutions:
        renderer = SVGRenderer()
        for solution in solutions:
            renderer.render(maze, solution).preview()
    else:
        print("No solution found")


def parse_path() -> pathlib.Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=pathlib.Path)
    return parser.parse_args().path


def main() -> None:
    create_maze()


if __name__ == "__main__":
    main()
