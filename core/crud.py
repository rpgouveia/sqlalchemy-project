from sqlalchemy.orm import Session
from core.database import session_local
from core.models import Base, Client, Apartment, Insurance, Accidents


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def create_client(db: Session, client: Client):
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()


def update_client(db: Session, client: Client):
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    db.delete(client)
    db.commit()
