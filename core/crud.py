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
    return db.query(Client).filter(Client.id == client_id).first()


def update_client(db: Session, client: Client) -> Client:
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int) -> None:
    client: Union[Client | None] = db.query(Client).filter(Client.id == client_id).first()
    db.delete(client)
    db.commit()


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()


def get_user(db: Session, user_id: int) -> Union[User | None]:
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user: User) -> User:
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user: Union[User | None] = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()

