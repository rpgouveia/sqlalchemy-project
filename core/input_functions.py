from core.validations import (
    validate_cpf, 
    validate_phone, 
    validate_birthdate, 
    validate_integer_number, 
    validate_email, 
    validate_post_code, 
    validate_country, 
    validate_state
)
from core.crud import (
    create_client, 
    get_all_clients, 
    get_client, 
    update_client, 
    delete_client
)
from typing import List, Union, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from core.models import Client
from datetime import date


def create_new_client(db: Session) -> None:
    try:
        name: str = input("Digite o nome completo do cliente: ")
        cpf: str = validate_cpf(input("Digite o CPF do cliente: "))
        birthdate: date = validate_birthdate(input("Digite a data de nascimento do cliente (AAAA-MM-DD): "))
        address_1: str = input("Digite o endereço principal do cliente: ")
        address_2: Optional[str] = input("Digite o complemento do endereço (opcional): ") or None
        post_code: str = validate_post_code(input("Digite o CEP do cliente: "))
        city: str = input("Digite a cidade do cliente: ")
        state: str = validate_state(input("Digite a sigla do estado do cliente (Ex: PR): "))
        country: str = validate_country(input("Digite o código do país do cliente (Ex: BR): "))
        phone: str = validate_phone(input("Digite o telefone do cliente (com DDD): "))
        email: str = validate_email(input("Digite o e-mail do cliente: "))

        new_client: Client = Client(
            name=name,
            cpf=cpf,
            birthdate=birthdate,
            address_1=address_1,
            address_2=address_2,
            post_code=post_code,
            city=city,
            state=state,
            country=country,
            phone=phone,
            email=email
        )

        created_client = create_client(db, new_client)
        print(f"Cliente criado com sucesso! ID: {created_client.id}")

    except IntegrityError as ie:
        db.rollback()
        if "client.cpf" in str(ie.orig):
            print(f"Erro: O CPF {cpf} já está cadastrado no sistema.")
        elif "client.email" in str(ie.orig):
            print(f"Erro: O e-mail {email} já está cadastrado no sistema.")
        else:
            print(f"Erro de integridade no banco de dados: {ie}")
    except ValueError as ve:
        print(f"Erro: {ve}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def read_all_clients(db: Session) -> None:
    clients: List[Client] = get_all_clients(db)

    if clients:
        print("Lista de todos os clientes:")
        for index, client in enumerate(clients, start=1):
            print(f"{index}) {client.name} (ID: {client.id})")
    else:
        print("Nenhum cliente encontrado.")


def read_client_by_id(db: Session) -> None:
    client_id: int = validate_integer_number("Digite o id do cliente: ")
    client: Union[Client, None] = get_client(db, client_id)

    if client:
        print(
            f"\n# Dados do Cliente #\n"
            f"id: {client.id},\n"
            f"Nome: {client.name},\n"
            f"CPF: {client.cpf},\n"
            f"Data de Nascimento: {client.birthdate},\n"
            f"Idade: {client.age},\n"
            f"Endereço 1: {client.address_1},\n"
            f"Endereço 2: {client.address_2 if client.address_2 else 'Não informado'},\n"
            f"CEP: {client.post_code},\n"
            f"Cidade: {client.city},\n"
            f"Estado: {client.state},\n"
            f"País: {client.country},\n"
            f"Telefone: {client.phone},\n"
            f"E-mail: {client.email}\n"
        )
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

    try:
        client.name = input("Digite o nome do cliente: ")
        client.email = validate_email(input("Digite o e-mail do cliente: "))
        client.phone = validate_phone(input("Digite o telefone do cliente (com o DDD): "))

        update_client(db, client)
        print(f"Cliente com ID {client.id} atualizado com sucesso!")
    
    except IntegrityError as ie:
        db.rollback()
        if "client.email" in str(ie.orig):
            print(f"Erro: O e-mail {client.email} já está cadastrado no sistema.")
        else:
            print(f"Erro de integridade no banco de dados: {ie}")
    
    except ValueError as ve:
        print(f"Erro: {ve}")
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def delete_client_by_id(db: Session) -> None:
    client: Union[Client | None] = get_client_object_by_id(db)
    if not client:
        return

    confirmation: str = input(f"Tem certeza que deseja deletar o cliente com ID {client.id}? (s/n): ")
    if confirmation.lower() != 's':
        print("Cancelando a operação.")
        return

    delete_client(db, client.id)
    print("Cliente deletado com sucesso.")
