from typing import List, Union
from sqlalchemy.orm import Session
from core.models import Client


def create_client(db: Session, client: Client) -> Client:
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_all_clients(db: Session) -> List[Client]:
    return db.query(Client).all()


def get_client(db: Session, client_id: int) -> Union[Client | None]:
    return db.query(Client).filter(Client.id == client_id).first()


def update_client(db: Session, client: Client) -> Client:
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int) -> None:
    client = db.query(Client).filter(Client.id == client_id).first()
    db.delete(client)
    db.commit()

