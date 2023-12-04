import argparse
import pathlib
from rich.console import Console
from rich.prompt import Prompt

from src.graphs.solver import solve_all
from src.models.maze import Maze
from src.view.renderer import SVGRenderer
from menu.menu_classes import Menu
from menu.menu_functions import sleep, import_data, solve_maze
from src.generate.create_maze import create_maze

# global
console = Console()


def main() -> None:
    level = import_data("resources/text/menu_objects.json")
    console.print(level.message_prompt, style="bold green")
    level = level.children[0]

    while True:
        sleep(2)
        if level.actionable:
            level = level.action()
        else:
            level = level.transit()
        if level.level == "quitting":
            level = level.children[-1]
            break
    sleep(2)
    console.print(level, style="bold magenta")


if __name__ == "__main__":
    main()