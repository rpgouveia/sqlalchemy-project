from sqlalchemy.orm import Session
from core.options import program_options
from core.database import connect_db



def main():
    db: Session = connect_db()

    status = True
    while (status):
        status = program_options(db)

    db.close()


if __name__ == "__main__":
    main()
