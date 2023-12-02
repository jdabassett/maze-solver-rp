import argparse
import pathlib
import json
from rich.console import Console
from rich.prompt import Prompt
import time

from src.graphs.solver import solve_all
from src.models.maze import Maze
from src.view.renderer import SVGRenderer
from scripts.choose_function import Functions
from src.generate.create_maze import create_maze

# global
sleep_in_seconds = 0.2
console = Console()


def sorry_invalid_input():
    console.print("Sorry that input is not valid.\nPlease try again.", style="bold yellow")


functions = Functions({"create_maze": create_maze}, sorry_invalid_input)


def null_function():
    pass


def sleep(multiple):
    time.sleep(sleep_in_seconds*multiple)


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


def choose_function(messages_all, level):
    # retrieve level
    message = messages_all.get(level)
    # print message from this level
    console.print(message.get('message'))

    # create all options
    prompts = [messages_all.get(prompt) for prompt in message.get("prompts", [])]

    # print all options
    options = []
    for index, prompt in enumerate(prompts):
        index += 1
        options.append(str(index))
        sleep(1)
        console.print(f"[{index}] {prompt.get('message','')}")
    # prompt input
    input_int = int(Prompt.ask("Choose by number", choices=options, show_choices=False))
    # access option
    input_dict = prompts[input_int-1]
    print(input_dict)
    # quitting or continuing
    if input_dict.get('name', "") in ["continuing", "quitting"]:
        return null_function, input_dict.get("name", "main"), level
    # select function
    else:
        function_return = functions[input_dict.get("value", "")]
        return function_return, input_dict.get("name", "main"), level


def choose_arguments():
    return [1, 2, 3], "main_choice", False, False


def main() -> None:
    messages = load_messages()
    level = "intro"
    console.print(messages.get(level).get("message"), style="bold green")
    level = "main"

    while True:
        sleep(2)
        function, level, previous = choose_function(messages, level)
        function()
        if level == "quitting":
            level = "good-bye"
            break
        if level == "continuing":
            level = previous
            continue
        # arguments, message_type, continuing, quitting = choose_arguments()
        # if quitting: break
        # if continuing: continue
        # function(*arguments)
    sleep(3)
    console.print(messages.get(level).get("message"), style="bold magenta")


if __name__ == "__main__":
    main()
