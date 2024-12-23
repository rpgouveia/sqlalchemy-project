from typing import List, Union
from sqlalchemy.orm import Session
from core.models import Client, User


def create_client(db: Session, client: Client) -> Client:
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_all_clients(db: Session) -> List[Client]:
    return db.query(Client).all()


def get_client(db: Session, client_id: int) -> Union[Client | None]:
    return get_by_id(db, Client, client_id)


def update_client(db: Session, client: Client) -> Client:
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int) -> None:
    client: Union[Client | None] = db.query(Client).filter(Client.id == client_id).first()
    db.delete(client)
    db.commit()


def get_clients_by_city(db: Session, city: str) -> List[Client]:
    clients = db.query(Client).filter(Client.city == city).all()
    if clients:
        return clients
    else:
        return db.query(Client).all()


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()


def get_user(db: Session, user_id: int) -> Union[User | None]:
    return get_by_id(db, User, user_id)


def update_user(db: Session, user: User) -> User:
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user: Union[User | None] = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()


def get_by_id(db: Session, model, record_id: int):
    return db.query(model).filter(model.id == record_id).first()
