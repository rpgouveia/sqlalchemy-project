from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from core.models import Base


# Setup SQLite Database
engine: Engine = create_engine("sqlite:///insurance.db", echo=False)

# Session Factory
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def connect_db() -> Session:
    db: Session = session_local()
    return db


Base.metadata.create_all(engine)
