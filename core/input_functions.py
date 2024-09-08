from core.validations import validate_cpf, validate_phone, validate_birthdate, validate_option
from sqlalchemy.orm import Session
from core.models import Client
from typing import List, Union
from core.crud import (
    create_client,
    get_all_clients,
    get_client,
    update_client,
    delete_client
)


def create_new_client(db: Session) -> None:
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


def read_all_clients(db: Session) -> None:
    clients: List[Client] = get_all_clients(db)

    if clients:
        print("Lista de todos os clientes:")
        for client in clients:
            print(f"- {client.name} (ID: {client.id})")
    else:
        print("Nenhum cliente encontrado.")


def read_client(db: Session) -> None:
    client_id: int = validate_option("Digite o id do cliente: ")
    client: Union[Client | None] = get_client(db, client_id)

    if client:
        print(f"Cliente encontrado: {client.name}")
    else:
        print(f"Cliente com ID {client_id} não encontrado.")


def update_client(db: Session) -> None:
    # Validate ID
    client_id: int = validate_option("Digite o id do cliente: ")
    client: Union[Client | None] = get_client(db, client_id)
    if not client:
        print(f"Cliente com ID {client_id} não encontrado.")
        return

    # Update client information
    client.name = "Ciclano dos Santos"
    client.email = "ciclano@mail.com"
    client.phone = 41598763210

    # Update the client in the database
    update_client(db, client)
    print(f"Cliente com ID {client_id} atualizado com sucesso!")


def delete_client(db: Session) -> None:
    # Validate ID
    client_id: int = validate_option("Digite o id do cliente: ")
    client: Union[Client | None] = get_client(db, client_id)
    if not client:
        print(f"Cliente com ID {client_id} não encontrado.")
        return

    # Confirm deletion
    confirmation = input(f"Tem certeza que deseja deletar o cliente com ID {client_id}? (s/n): ")
    if confirmation.lower() != 's':
        print("Cancelando a operação.")
        return

    # Delete client
    delete_client(db, client_id)
    print("Cliente deletado com sucesso.")
