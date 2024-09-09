import os


def clear_screen() -> None:
    """
    Esta função limpa a tela do terminal baseado no sistema operacional.

    Parâmetros:
        Nenhum

    Retorno:
        Não há retorno, apenas limpa a tela do terminal.
    """

    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

