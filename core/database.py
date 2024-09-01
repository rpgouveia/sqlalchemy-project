from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base


# Setup SQLite Database
engine = create_engine("sqlite:///insurance.db", echo=True)

# Session Factory
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
