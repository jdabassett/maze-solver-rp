from rich.console import Console
from menu.menu_functions import sleep, import_data

# global
console = Console()


def main() -> None:
    level = import_data("resources/text/menu_objects.json")
    console.print(level.message_prompt, style="bold green")
    level = next(level)

    while True:
        sleep(2)
        level = level.action()
        if level.level == "quitting":
            level = next(level)
            break
    sleep(2)
    console.print(level, style="bold magenta")


if __name__ == "__main__":
    main()
