from core.input_functions import create_new_client
from core.validations import validate_option


def program_options(db) -> bool:
    option = validate_option("Escolha uma opção: ")

    match option:
        case 1:
            create_new_client(db)
            return True
        
        case 2:
            return False
        
        case _:
            print("Opção inválida.")
            return True
