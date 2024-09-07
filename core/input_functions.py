from core.validations import validate_cpf, validate_phone, validate_birthdate
from core.models import Client
from core.crud import (
    create_client,
    get_all_clients,
    get_client,
    update_client,
    delete_client
)


def create_new_client(db):
    try:
        name: str = input("Digite o nome completo do cliente: ")
        cpf: str = input("Digite o CPF do cliente: ")
        birthdate_str: str = input("Digite a data de nascimento do cliente (AAAA-MM-DD): ")
        address: str = input("Digite o endereço do cliente: ")
        phone: str = input("Digite o telefone do cliente (com DDD): ")
        email: str = input("Digite o e-mail do cliente: ")

        # Validations
        valid_cpf = validate_cpf(cpf)
        valid_phone = validate_phone(phone)
        valid_birthdate = validate_birthdate(birthdate_str)

        # Create object Client
        new_client: Client = Client(
            name=name,
            cpf=valid_cpf,
            birthdate=valid_birthdate,
            address=address,
            phone=valid_phone,
            email=email
        )

        # Save to database
        created_client = create_client(db, new_client)
        print(f"Cliente criado com sucesso! ID: {created_client.id}")

    except ValueError as ve:
        print(f"Erro: {ve}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
