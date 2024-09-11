from sqlalchemy.orm import Session
from core.options import program_options
from core.database import connect_db


def main() -> None:
    db: Session = connect_db()

    status: bool = True
    while (status):
        print("Programa de Cadastro de Clientes")
        status = program_options(db)

    db.close()


if __name__ == "__main__":
    main()
