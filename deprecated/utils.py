import os


def clear_screen() -> None:
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

