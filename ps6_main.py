import sys
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QStackedWidget
from sqlalchemy.orm import Session
from core.database import connect_db


class MainWindowApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Programa de Cadastro de Clientes")

        # Conexão ao banco de dados
        try:
            self.db: Session = connect_db()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.db = None

        # Configuração do layout principal
        self.layout = QVBoxLayout()

        # Criando um widget empilhado (para navegação entre telas)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Criar as páginas (Menu Principal e as demais opções)
        self.create_main_menu()
        self.create_register_client_page()
        self.create_hello_world_page()

        # Definir o layout da janela principal
        self.setLayout(self.layout)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Sobrescreve o evento de fechamento para garantir que o banco seja desconectado"""
        if self.db:
            self.db.close()
        event.accept()

    def create_main_menu(self):
        """Cria o menu principal com botões para diferentes funcionalidades"""

        # Rascunho do Menu Principal
        """
        1 - Cadastrar um novo cliente
        2 - Listar todos os clientes
        3 - Ler um cliente por ID
        4 - Atualizar um cliente por ID
        5 - Deletar um cliente por ID
        6 - Sair do programa
        """

        main_menu = QWidget()
        layout = QVBoxLayout()

        # Botões do menu principal
        register_button = QPushButton("Cadastrar um novo cliente")
        hello_world_button = QPushButton("Hello World (teste)")
        exit_button = QPushButton("Sair do programa")

        # Conectando os botões às funções que alteram as páginas
        register_button.clicked.connect(self.show_register_client_page)
        hello_world_button.clicked.connect(self.show_hello_world_page)
        exit_button.clicked.connect(self.close)

        # Adicionando os botões ao layout
        layout.addWidget(register_button)
        layout.addWidget(hello_world_button)
        layout.addWidget(exit_button)

        main_menu.setLayout(layout)
        self.stacked_widget.addWidget(main_menu)

    def create_register_client_page(self):
        """Cria a página de cadastro de cliente"""
        register_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Página de Cadastro de Cliente")
        return_button = QPushButton("Voltar para o Menu")
        return_button.clicked.connect(self.show_main_menu)

        layout.addWidget(label)
        layout.addWidget(return_button)

        register_page.setLayout(layout)
        self.stacked_widget.addWidget(register_page)

    def create_hello_world_page(self):
        """Cria a página de Hello World"""
        hello_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Hello World!")
        return_button = QPushButton("Voltar para o Menu")
        return_button.clicked.connect(self.show_main_menu)

        layout.addWidget(label)
        layout.addWidget(return_button)

        hello_page.setLayout(layout)
        self.stacked_widget.addWidget(hello_page)

    def show_main_menu(self):
        """Exibe o menu principal"""
        self.stacked_widget.setCurrentIndex(0)

    def show_register_client_page(self):
        """Exibe a página de cadastro de cliente"""
        self.stacked_widget.setCurrentIndex(1)

    def show_hello_world_page(self):
        """Exibe a página de Hello World"""
        self.stacked_widget.setCurrentIndex(2)

# Startup Application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindowApp()
    window.resize(600, 400)
    window.show()

    sys.exit(app.exec())

