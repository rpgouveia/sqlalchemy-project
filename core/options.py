from core.validations import validate_integer_number
from sqlalchemy.orm import Session
from core.input_functions import (
    create_new_client, 
    read_all_clients, 
    read_client_by_id, 
    update_client_by_id,
    delete_client_by_id
)


def program_options(db: Session) -> bool:
    options: str = """
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
            read_client_by_id(db)
            return True

        case 4:
            update_client_by_id(db)
            return True

        case 5:
            delete_client_by_id(db)
            return True

        case 6:
            print("Saindo do programa.")
            return False

        case _:
            print("Opção inválida.")
            return True
