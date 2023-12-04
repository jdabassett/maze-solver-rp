import time
import pathlib
import json
import argparse

from src.graphs.solver import solve_all
from src.models.maze import Maze
from src.view.renderer import SVGRenderer
from menu.menu_classes import Menu

sleep_in_seconds = 0.2


def sleep(multiple):
    """"""
    time.sleep(sleep_in_seconds*multiple)


def import_data(relative_path) -> Menu:
    """"""
    cwd = pathlib.Path.cwd()
    path_messages = cwd.joinpath(relative_path)
    with path_messages.open("r") as file:
        data = json.load(file)
        if "menu" in relative_path:
            return_object = create_menu_objects(data)
    return return_object

def create_menu_objects(dict_import: dict) -> Menu:
    dict_menu = {}
    for key,value in dict_import.items():
        value["actionable"] = value.get('actionable')=="True"
        dict_menu[key] = Menu(**value)

    for menu in dict_menu.values():
        list_children = []
        for child in menu.children:
            retrieve_menu = dict_menu.get(child)
            list_children.append(retrieve_menu)
        menu.children = list_children

    return dict_menu.get("intro")



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


if __name__=="__main__":
    intro = load_intro()
    # print(type(intro.actionable))
    # print(intro.actionable)
#     main = intro.children[0]
#     create_maze = main.children[0]
#     print(create_maze)
