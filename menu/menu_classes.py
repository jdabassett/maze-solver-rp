from dataclasses import dataclass
import importlib
import re
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

    @staticmethod
    def what_to_do_with_current_maze() -> str:
        console.print("You have an maze on hand. Would you like to save it first?", style="green")
        console.print("[1] Yes\n[2] No", style="white")
        return Prompt.ask("Choose by number", choices=["1", "2"], show_choices=False)

    @staticmethod
    def transfer_maze_and_or_solution(level_next, maze: Maze | None = None, solution: Solution | None = None):
        level_next.maze = maze
        level_next.solution = solution
        return level_next

    def status_update(self):
        level_str = self.level.replace("_", " ").title()
        maze_exists = "\n[√]maze" if self.maze is not None else ""
        solution_exists = "\n[√]solution" if self.solution is not None else ""
        console.print(f"Location: {level_str}{maze_exists}{solution_exists}", style="green")


class CreateMazeMixin:
    def action(self):
        try:
            self.status_update()
            # if a maze already exists
            if self.maze is not None:
                input_str = self.what_to_do_with_current_maze()
                if input_str == "1":
                    return self.transfer_maze_and_or_solution(self.children.get("save_maze"), self.maze, self.solution)

            # otherwise create a new maze
            level_module_str = self.value.get("module")
            level_callable_str = self.value.get("callable")
            level_callable = getattr(importlib.import_module(level_module_str), level_callable_str)

            user_input = {}
            for key, value in self.parameters.items():
                console.print(f"{key}", style="green")
                # if selecting integer
                if value.get("type") == "int":
                    lower = int(value.get("value").get("lower"))
                    upper = int(value.get("value").get("upper"))
                    increment = int(value.get('value').get("increment"))
                    options = [str(i) for i in range(lower, upper+1, increment)]
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
                input_str = self.what_to_do_with_current_maze()
                if input_str == "1":
                    return self.transfer_maze_and_or_solution(self.children.get("save_maze"), self.maze, self.solution)

            console.print(self.message_prompt, style="green")
            root_dir = Path.cwd()
            maze_dir = root_dir.joinpath("resources", "mazes")
            maze_paths = sorted([item for item in maze_dir.iterdir() if item.is_file() and item.suffix == ".maze"])
            maze_paths.append(root_dir.joinpath("Cancel"))
            options = []
            for index, path in enumerate(maze_paths):
                index += 1
                options.append(str(index))
                console.print(f"[{index}] {str(path.name)}", style="white")
            input_index = int(Prompt.ask("Choose by number", choices=options, show_choices=False))-1
            input_path = maze_paths[input_index]
            if str(input_path.name) == "Cancel":
                console.print("Leaving Load Maze.", style="green")
                return self.transfer_maze_and_or_solution(
                    self.children.get(self.previous_level), self.maze, self.solution)
            maze = Maze.load(input_path) or self.maze
            return self.transfer_maze_and_or_solution(
                self.children.get(self.previous_level), maze, self.solution)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.children.get(self.previous_level), self.maze, self.solution)


class SaveMazeMixin:
    def action(self):
        try:
            self.status_update()
            root_dir = Path.cwd()
            maze_dir = root_dir.joinpath("resources", "mazes")
            console.print(self.message_prompt, style="green")
            console.print(r'Must avoid the following characters: <>:"/\.|?*', style="white")
            input_str = Prompt.ask("Input file name here")
            if is_valid_filename(input_str):
                path = maze_dir.joinpath(f"{input_str}.maze")
                self.maze.dump(path)
                console.print(f"{input_str} was successfully saved!", style="green")
                return self.transfer_maze_and_or_solution(
                    self.children.get(self.previous_level), self.maze, self.solution)
            else:
                console.print("Invalid file name please try again.", style="red")
                return self.transfer_maze_and_or_solution(self, self.maze, self.solution)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.children.get(self.previous_level), self.maze, self.solution)


def is_valid_filename(filename: str) -> bool:
    try:
        Path(filename)
        if re.search(r"[<*>?:/\.|]", filename):
            return False
        else:
            return True
    except (OSError, ValueError):
        return False


class SolveMazeMixin:
    def action(self):
        self.status_update()
        return self.transfer_maze_and_or_solution(
            self.children.get(self.previous_level), self.maze, self.solution)


class TransitMixin:
    def action(self):
        try:
            self.status_update()
            console.print(self.message_prompt, style="green")
            options_dict = {}
            for index, choice in enumerate([i for i in self.children.values()]):
                index += 1
                options_dict[str(index)] = choice
                console.print(f"[{index}] {choice}", style="white")
            options_keys = [i for i in options_dict.keys()]
            input_str = Prompt.ask("Choose by number", choices=options_keys, show_choices=False)

            return self.transfer_maze_and_or_solution(options_dict.get(input_str), self.maze, self.solution)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.children.get(self.previous_level), self.maze, self.solution)


class QuittingMixin:
    def action(self):
        try:
            self.status_update()
            if self.maze is not None:
                input_str = self.what_to_do_with_current_maze()
                if input_str == "1":
                    return self.transfer_maze_and_or_solution(self.children.get("save_maze"), self.maze, self.solution)
            input_dict = {}
            options = []
            index = 1
            for key, value in self.parameters.items():
                options.append(str(index))
                input_dict[str(index)] = value.get("value")
                console.print(f"[{index}] {key}", style="white")
                index += 1
            input_str = Prompt.ask("Choose by number", choices=options, show_choices=False)
            input_level = input_dict[input_str]
            return self.transfer_maze_and_or_solution(self.children.get(input_level), self.maze, self.solution)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(self.children.get(self.next_level), self.maze, self.solution)


class GoodByeMixin:
    def action(self):
        console.print(self, style="magenta")
        return self
