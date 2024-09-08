from core.validations import validate_integer_number
from core.input_functions import (
    create_new_client, 
    read_all_clients, 
    read_client, 
    update_client
)


def program_options(db) -> bool:
    options = """
    1 - Cadastrar um novo cliente
    2 - Listar todos os clientes
    3 - Ler um cliente por ID
    4 - Atualizar um cliente por ID
    5 - Deletar um cliente por ID
    6 - Sair do programa
    """

    print(options)

    option: int = validate_integer_number("Escolha uma opção: ")

    match option:
        case 1:
            create_new_client(db)
            return True

        case 2:
            read_all_clients(db)
            return True

        case 3:
            read_client(db)
            return True

        case 4:
            update_client(db)
            return True

        case 5:
            ...
            return True

        case 6:
            print("Saindo do programa.")
            return False

        case _:
            print("Opção inválida.")
            return True
