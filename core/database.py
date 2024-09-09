from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from core.models import Base


engine: Engine = create_engine("sqlite:///insurance.db", echo=False)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def connect_db() -> Session:
    """
    Esta função faz a conexão com o banco de dados.

    Parâmetros:
        Nenhum
    
    Retorno:
        db (Session): Retorna um objeto Session.
    """
    db: Session = session_local()
    return db

Base.metadata.create_all(engine)
