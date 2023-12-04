from dataclasses import dataclass
import importlib
import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from src.models.maze import Maze
from src.models.solution import Solution
from src.view.renderer import SVGRenderer

console = Console()
prompt = Prompt()


@dataclass
class Menu:
    """"""
    level: str
    children: dict
    message_pitch: str
    message_prompt: str
    parameters: dict
    value: dict
    previous_level: str
    next_level: str
    mixin: str
    maze: Maze | None = None
    solution: Solution | None = None

    def __str__(self):
        """"""
        return f"{self.message_pitch}"

    def __repr__(self):
        """"""
        return f"{self.message_pitch}"

    def __next__(self):
        """"""
        return self.children.get(self.next_level, self)

    def what_to_do_with_current_maze(self, level_next) -> None:
        if self.maze is not None:
            console.print("You have an maze on hand. Would you like to save it first?", style="bold green")
            input_user = Prompt.ask("[1] Yes\n[2]No", choices=["1", "2"], show_choices=False)
            if input_user == "1":
                self.transfer_maze_and_or_solution(level_next, self.maze, self.solution)

    def transfer_maze_and_or_solution(self, level_next, maze: Maze | None = None, solution: Solution | None = None):
        level_next.maze = maze
        level_next.solution = solution
        return level_next

    def status_update(self):
        level_str = self.level.replace("_"," ").title()
        maze_exists = "\n[√]maze" if self.maze is not None else ""
        solution_exists = "\n[√]solution" if self.maze is not None else ""
        console.print(f"\nLocation: {level_str}{maze_exists}{solution_exists}", style="green")


class CreateMazeMixin:
    def action(self):
        try:
            self.status_update()
            # if a maze already exists
            if self.maze is not None:
                self.what_to_do_with_current_maze("save_maze")

            # otherwise create a new maze
            level_module_str = self.value.get("module")
            level_callable_str = self.value.get("callable")
            level_callable = getattr(importlib.import_module(level_module_str),level_callable_str)

            user_input = {}
            for key,value in self.parameters.items():
                console.print(f"{key}", style="bold green")
                # if selecting integer
                if value.get("type") == "int":
                    lower = int(value.get("value").get("lower"))
                    upper = int(value.get("value").get("upper"))
                    increment = int(value.get('value').get("increment"))
                    options = [str(i) for i in range(lower,upper+1)]
                    input_user = int(Prompt.ask("Choose by number", choices=options, show_choices=False))
                    user_input[value.get("kwarg")] = input_user
                # if selecting callable function or class
                elif value.get("type") == "dict":
                    value_dict = value.get("value")
                    options_dict = {}
                    for index, choice in enumerate([key for key in value_dict.keys()]):
                        index += 1
                        options_dict[str(index)] = value_dict.get(choice)
                        console.print(f"[{index}] {choice}.", style="white")
                    options_keys = [i for i in options_dict.keys()]
                    input_int = Prompt.ask("Choose by number", choices=options_keys, show_choices=False)
                    input_dict = options_dict.get(input_int)
                    input_module_str = input_dict.get("module")
                    input_callable_str = input_dict.get("callable")
                    input_user = getattr(importlib.import_module(input_module_str), input_callable_str)
                    user_input[value.get("kwarg")] = input_user
            maze = level_callable(**user_input)
            svg = SVGRenderer().render(maze)
            svg.preview()
            console.print("Check your browser for a preview!", style="green")
            return self.transfer_maze_and_or_solution(self.children.get("main"), maze, None)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)


class LoadMazeMixin:
    def action(self):
        try:
            self.status_update()
            # if maze already exists
            if self.maze is not None:
                self.what_to_do_with_current_maze("save_maze")

            console.print(self.message_prompt, style="bold green")
            root_dir = Path.cwd()
            maze_dir = root_dir.joinpath("resources","mazes")
            maze_paths = sorted([item for item in maze_dir.iterdir() if item.is_file() and item.suffix == ".maze"])
            maze_paths.append(root_dir.joinpath("Cancel"))
            options = []
            for index, path in enumerate(maze_paths):
                index += 1
                options.append(str(index))
                console.print(f"[{index}] {str(path.name)}",style="white")
            input_index = int(Prompt.ask("Choose by number", choices=options, show_choices=False))-1
            input_path = maze_paths[input_index]
            if str(input_path.name) == "Cancel":
                console.print("Leaving Load Maze.", style="green")
                return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)
            print(str(input_path))
            maze = Maze.load(input_path) | self.maze
            return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), maze, self.solution)

        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)

class SolveMazeMixin:
    def action(self):
        self.status_update()
        return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)

class SaveMazeMixin:
    def action(self):
        self.status_update()
        return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)

class TransitMixin:
    def action(self):
        try:
            self.status_update()
            console.print(self.message_prompt, style="bold green")
            options_dict = {}
            for index, choice in enumerate([i for i in self.children.values()]):
                index += 1
                options_dict[str(index)] =choice
                console.print(f"[{index}] {choice}", style="white")
            options_keys = [i for i in options_dict.keys()]
            input_str = Prompt.ask("Choose by number", choices=options_keys, show_choices=False)

            return self.transfer_maze_and_or_solution(options_dict.get(input_str), self.maze, self.solution)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)


class QuittingMixin:
    def action(self):
        # TODO: allow user to return, save current maze, or leave
        self.status_update()
        return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)
