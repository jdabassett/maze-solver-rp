import time
import pathlib
import json
import argparse

from src.graphs.solver import solve_all
from src.models.maze import Maze
from src.view.renderer import SVGRenderer
from menu.menu_classes import (
    Menu,
    TransitMixin,
    SolveMazeMixin,
    CreateMazeMixin,
    LoadMazeMixin,
    SaveMazeMixin,
    QuittingMixin)

sleep_in_seconds = 0.2


def sleep(multiple):
    """"""
    time.sleep(sleep_in_seconds*multiple)


def import_data() -> Menu:
    """"""
    cwd = pathlib.Path.cwd()
    path_messages = cwd.joinpath("resources","text","menu_objects.json")
    with path_messages.open("r") as file:
        data = json.load(file)
        return_object = create_menu_objects(data)
    return return_object

def create_menu_objects(dict_import: dict) -> Menu:
    dict_menu = {}
    for key,value in dict_import.items():
        if value.get("mixin") == "TransitMixin":
            menu_new = type("TransitMenu", (Menu, TransitMixin), {})
            dict_menu[key] = menu_new(**value)
        elif value.get("mixin") == "CreateMazeMixin":
            menu_new = type("CreateMazeMenu", (Menu, CreateMazeMixin), {})
            dict_menu[key] = menu_new(**value)
        elif value.get("mixin") == "SolveMazeMixin":
            menu_new = type("SolveMazeMenu", (Menu, SolveMazeMixin), {})
            dict_menu[key] = menu_new(**value)
        elif value.get("mixin") == "LoadMazeMixin":
            menu_new = type("LoadMazeMenu", (Menu, LoadMazeMixin), {})
            dict_menu[key] = menu_new(**value)
        elif value.get("mixin") == "SaveMazeMixin":
            menu_new = type("SaveMazeMenu", (Menu, SaveMazeMixin), {})
            dict_menu[key] = menu_new(**value)
        elif value.get("mixin") == "QuittingMixin":
            menu_new = type("QuittingMenu", (Menu, QuittingMixin), {})
            dict_menu[key] = menu_new(**value)

    for menu in dict_menu.values():
        list_children = {}
        for name, child in menu.children.items():
            list_children[name] = dict_menu.get(name)
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


# if __name__=="__main__":
#     intro = load_intro()

