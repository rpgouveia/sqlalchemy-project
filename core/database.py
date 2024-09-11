from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from core.models import Base


engine: Engine = create_engine("sqlite:///insurance.db", echo=False)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def connect_db() -> Session:
    db: Session = session_local()
    return db

Base.metadata.create_all(engine)
