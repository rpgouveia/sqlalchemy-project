import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select, and_

# Configuração do Banco de Dados
engine = create_engine("sqlite:///library.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Definição do Modelo
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    access_level = Column(String, nullable=False)  # ex: 'admin', 'guest'

# Função para inicializar o banco com dados padrões
def initialize_database():
    # Verifica se já existem usuários no banco de dados
    existing_users = session.query(User).count()
    
    if existing_users == 0:
        # Cria os usuários iniciais com diferentes níveis de acesso
        default_users = [
            User(username="admin_user", access_level="admin"),
            User(username="standard_user", access_level="user"),
            User(username="guest_user", access_level="guest"),
        ]
        
        session.add_all(default_users)
        session.commit()
        print("Usuários iniciais adicionados com sucesso.")

# Inicialização do Banco de Dados e da Aplicação
Base.metadata.create_all(engine)
initialize_database()  # Chama a função para inicializar os dados

# Classe principal da Interface Gráfica
class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)
        
    def add_book(self, title, author, user):
        # Controle de Acesso
        if user.access_level != 'admin':
            QMessageBox.warning(self, "Acesso Negado", "Você não tem permissão para adicionar livros.")
            return

        # Transação de Banco de Dados
        try:
            new_book = Book(title=title, author=author)
            session.add(new_book)
            session.commit()
            QMessageBox.information(self, "Sucesso", "Livro adicionado com sucesso!")
        except SQLAlchemyError as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", f"Erro ao adicionar o livro: {e}")

    def view_books(self, user):
        # Consulta usando Álgebra Relacional (Seleção e Projeção)
        try:
            if user.access_level in ('admin', 'guest'):
                books = session.execute(select(Book)).scalars().all()
                # Aqui você pode carregar os dados dos livros para um QTableView ou similar
                for book in books:
                    print(f"Title: {book.title}, Author: {book.author}")
        except SQLAlchemyError as e:
            QMessageBox.critical(self, "Erro", f"Erro ao consultar livros: {e}")

# Inicialização da Aplicação
def main():
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
