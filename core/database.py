from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from core.models import Base, Users


engine: Engine = create_engine("sqlite:///insurance.db", echo=False)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def connect_db() -> Session:
    db: Session = session_local()
    return db

def initialize_database():
    db: Session = connect_db()
    try:
        existing_users = db.query(Users).count()

        if existing_users == 0:
            default_users = [
                Users(username="admin", fullname="Administrador", phone="00000000000", email="admin@mail.com", access_level="admin"),
                Users(username="user", fullname="Usuário", phone="00000000001", email="user@mail.com", access_level="user")
            ]

            default_users[0].set_password("admin123")
            default_users[1].set_password("user123")

            db.add_all(default_users)
            db.commit()
            print("Usuários iniciais adicionados com sucesso.")
    finally:
        db.close()

Base.metadata.create_all(engine)
initialize_database()
