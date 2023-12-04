from dataclasses import dataclass
from rich.console import Console
from rich.prompt import Prompt

console = Console()
prompt = Prompt()

@dataclass
class Menu:
    """"""
    level: str
    children: list
    message_pitch: str
    message_prompt: str
    parameters: dict
    actionable: bool = False

    def __str__(self):
        """"""
        return f"{self.message_pitch}"

    def __repr__(self):
        """"""
        return f"{self.message_pitch}"

    def action(self):
        """"""
        for key,value in self.parameters.items():
            console.print(f"{key}", style="bold green")
            if value.get("type") == "int":
                lower = int(value.get("value").get("lower"))
                upper = int(value.get("value").get("upper"))
                increment = int(value.get('value').get("increment"))
                options = [str(i) for i in range(lower,upper+1)]
                input_int = int(Prompt.ask("Choose by number", choices=options, show_choices=False))
                print("input_user",input_int)
            elif value.get("type") == "dict":
                value_dict = value.get("value")
                keys_list = [key for key in value_dict.keys()]
                loop_dict = {}
                options = []
                for index, choice in enumerate(keys_list):
                    index += 1
                    loop_dict[str(index)] = value_dict.get(choice)
                    options.append(str(index))
                    console.print(f"[{index}] {choice}.", style="white")

                input_int = Prompt.ask("Choose by number", choices=options, show_choices=False)
                input_obj = loop_dict.get(input_int)
                print("input_user", input_obj)

    def transit(self):
        """"""
        console.print(self.message_prompt, style="bold green")
        options = []
        length = len(self.children)
        for index, choice in enumerate(self.children):
            index += 1
            options.append(str(index))
            if index == (length-1):
                console.print(f"[{index}] Return to {choice}.", style="white")
            else:
                console.print(f"[{index}] {choice}.", style="white")

        input_int = int(Prompt.ask("Choose by number", choices=options, show_choices=False))
        input_obj = self.children[input_int - 1]
        return input_obj


    def __next__(self):
        """"""
        return self.children[-2]