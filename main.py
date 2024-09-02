from core.crud import get_client, create_client
from core.models import Client
from core.database import get_db
from datetime import date


def main():
    db = get_db()

    # TEST: Creating new Client - Success!
    birthdate_client1_str = "1982-02-10"
    birthdate = date.fromisoformat(birthdate_client1_str)
    new_client = Client(
        name="Fulano da Silva", 
        cpf=99999999999,
        birthdate=birthdate,
        address="Rua X, número 123, prédio Y",
        phone=41987659174,
        email="fulano@mail.com"
    )
    created_client = create_client(db, new_client)
    print(f"Cliente criado com sucesso! ID: {created_client.id}")

    # TEST: Fetching a Client by ID - Success!
    client_id = 1
    client = get_client(db, client_id)
    if client:
        print(f"Cliente encontrado: {client.name}")
    else:
        print(f"Cliente com ID {client_id} não encontrado.")

    db.close()

if __name__ == "__main__":
    main()
