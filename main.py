from core.crud import create_client, get_client, get_all_clients, update_client
from core.models import Client
from core.database import get_db
from datetime import date


def main():
    db = get_db()

    # # TEST: Creating new Client - Success!
    # birthdate_client1_str = "1982-02-10"
    # birthdate = date.fromisoformat(birthdate_client1_str)
    # new_client = Client(
    #     name="Fulano da Silva", 
    #     cpf=12345678900,
    #     birthdate=birthdate,
    #     address="Rua X, número 123, prédio Y",
    #     phone=41987659174,
    #     email="fulano@mail.com"
    # )
    # created_client = create_client(db, new_client)
    # print(f"Cliente criado com sucesso! ID: {created_client.id}")

    # birthdate_client1_str = "1987-07-07"
    # birthdate = date.fromisoformat(birthdate_client1_str)
    # new_client = Client(
    #     name="Beltrano da Silva", 
    #     cpf=12345678900,
    #     birthdate=birthdate,
    #     address="Rua Y, número 321, prédio Z",
    #     phone=41987659174,
    #     email="beltrano@mail.com"
    # )
    # created_client = create_client(db, new_client)
    # print(f"Cliente criado com sucesso! ID: {created_client.id}")


    # TEST: Fetch all Clients
    clients = get_all_clients(db)

    if clients:
        print("Lista de todos os clientes:")
        for client in clients:
            print(f"- {client.name} (ID: {client.id})")
    else:
        print("Nenhum cliente encontrado.")


    # TEST: Fetching a Client by ID - Success!
    # client_id = 1
    # client = get_client(db, client_id)
    # if client:
    #     print(f"Cliente encontrado: {client.name}")
    # else:
    #     print(f"Cliente com ID {client_id} não encontrado.")


    ## TEST: Update Client by ID - Success!
    # client_id = 1  # Replace with the actual ID of the client you want to update

    # # Fetch the client to update
    # client = get_client(db, client_id)
    # if not client:
    #     print(f"Cliente com ID {client_id} não encontrado.")
    #     return

    # # Update client information (modify these as needed)
    # client.name = "Ciclano dos Santos"
    # client.email = "ciclano@mail.com"
    # client.phone = 41598763210

    # # Update the client in the database
    # update_client(db, client)

    # print(f"Cliente com ID {client_id} atualizado com sucesso!")


    db.close()


if __name__ == "__main__":
    main()
