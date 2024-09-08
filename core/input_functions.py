from core.validations import validate_cpf, validate_phone, validate_birthdate, validate_integer_number, validate_email
from core.crud import create_client, get_all_clients, get_client, update_client, delete_client
from sqlalchemy.orm import Session
from core.models import Client
from typing import List, Union
from datetime import date


def create_new_client(db: Session) -> None:
    try:
        name: str = input("Digite o nome completo do cliente: ")
        cpf: str = validate_cpf(input("Digite o CPF do cliente: "))
        birthdate: date = validate_birthdate(input("Digite a data de nascimento do cliente (AAAA-MM-DD): "))
        address: str = input("Digite o endereço do cliente: ")
        phone: str = validate_phone(input("Digite o telefone do cliente (com DDD): "))
        email: str = validate_email(input("Digite o e-mail do cliente: "))

        # Create object Client
        new_client: Client = Client(
            name=name,
            cpf=cpf,
            birthdate=birthdate,
            address=address,
            phone=phone,
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


def read_client_by_id(db: Session) -> None:
    client_id: int = validate_integer_number("Digite o id do cliente: ")
    client: Union[Client | None] = get_client(db, client_id)

    if client:
        print(f"Cliente encontrado: {client.name}")
    else:
        print(f"Cliente com ID {client_id} não encontrado.")


def get_client_object_by_id(db: Session) -> Union[Client | None]:
    client_id: int = validate_integer_number("Digite o id do cliente: ")
    client: Union[Client | None] = get_client(db, client_id)
    if client:
        return client
    else:
        print(f"Cliente com ID {client_id} não encontrado.")


def update_client_by_id(db: Session) -> None:
    client: Union[Client | None] = get_client_object_by_id(db)
    if not client:
        return

    # Update client information
    client.name = input("Digite o nome do cliente: ")
    client.email = input("Digite o e-mail do cliente: ")
    client.phone = validate_phone(input("Digite o telefone do cliente (com o DDD): "))

    # Update the client in the database
    update_client(db, client)
    print(f"Cliente com ID {client.id} atualizado com sucesso!")


def delete_client_by_id(db: Session) -> None:
    client: Union[Client | None] = get_client_object_by_id(db)
    if not client:
        return

    # Confirm deletion
    confirmation: str = input(f"Tem certeza que deseja deletar o cliente com ID {client.id}? (s/n): ")
    if confirmation.lower() != 's':
        print("Cancelando a operação.")
        return

    # Delete client
    delete_client(db, client.id)
    print("Cliente deletado com sucesso.")
