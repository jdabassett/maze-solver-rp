from rich.console import Console
from menu.menu_functions import sleep, import_data

# global
console = Console()


def main() -> None:
    level = import_data()
    console.print(level.message_prompt, style="bold green")
    level = next(level)

    while True:
        sleep(2)
        print("")
        if level.level == "good_bye":
            level.action()
            break
        level = level.action()


if __name__ == "__main__":
    main()
