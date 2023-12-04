from dataclasses import dataclass
import importlib
import os
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


class CreateMazeMixin:
    def action(self):
        try:
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
            return self.transfer_maze_and_or_solution(self.children.get("save_file"), maze, None)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)


class LoadMazeMixin:
    def action(self):
        try:
            # if maze already exists
            if self.maze is not None:
                self.what_to_do_with_current_maze("save_maze")

            console.print(self.message_prompt, style="bold green")
            root_dir = os.getcwd()
            maze_dir = os.path.join(root_dir,"resources","mazes")
            maze_files = os.listdir(maze_dir)
            maze_list = [file for file in maze_files if file.endswith(".maze")]
            maze_sorted = sorted(maze_list)
            maze_sorted.append("Cancel")
            options = []
            for index, filename in enumerate(maze_sorted):
                index += 1
                options.append(str(index))
                console.print(f"[{index}] {filename}",style="white")
            input_index = int(Prompt.ask("Choose by number", choices=options, show_choices=False))-1
            input_filename = maze_sorted[input_index]
            maze_file = os.path.join(maze_dir, input_filename)
            if maze_file == "Cancel":
                console.print("Leaving Load Maze.", style="green")
                return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)
            # TODO: load file save to maze and solution
            return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)

        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(self.children.get(self.previous_level), self.maze, self.solution)

class SolveMazeMixin:
    def action(self):
        pass

class SaveMazeMixin:
    def action(self):
        pass

class TransitMixin:
    def action(self):
        console.print(self.message_prompt, style="bold green")
        options_dict = {}
        for index, choice in enumerate([i for i in self.children.values()]):
            index += 1
            options_dict[str(index)] =choice
            console.print(f"[{index}] {choice}", style="white")
        options_keys = [i for i in options_dict.keys()]
        input_str = Prompt.ask("Choose by number", choices=options_keys, show_choices=False)

        return self.transfer_maze_and_or_solution(options_dict.get(input_str), self.maze, self.solution)

class QuittingMixin:
    def action(self):
        #allow user to return, save current maze, or leave
        pass
