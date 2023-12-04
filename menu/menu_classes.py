from dataclasses import dataclass
import importlib
from rich.console import Console
from rich.prompt import Prompt
from src.models.maze import Maze
from src.models.solution import Solution
from src.view.renderer import SVGRenderer

console = Console()
prompt = Prompt()


class TransitMixin:
    def action(self):
        console.print(self.message_prompt, style="bold green")
        options_dict = {}
        for index, choice in enumerate([i for i in self.children.values()]):
            index += 1
            options_dict[str(index)] = choice
            console.print(f"[{index}] {choice}", style="white")
        options_keys = [i for i in options_dict.keys()]
        input_int = Prompt.ask("Choose by number", choices=options_keys, show_choices=False)
        return options_dict.get(input_int)


class CreateMazeMixin:
    def action(self):
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
        try:
            maze = level_callable(**user_input)
            svg = SVGRenderer().render(maze)
            svg.preview()
            console.print("Check your browser for a preview!", style="green")
            level_next = self.children.get("save_file", self)
            level_next.maze = maze
            return level_next
        except:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            return self

class SolveMazeMixin:
    pass

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