import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt

class MainWindowApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programa de Cadastro de Clientes")

        # Sketch for Main Menu
        """
        1 - Cadastrar um novo cliente
        2 - Listar todos os clientes
        3 - Ler um cliente por ID
        4 - Atualizar um cliente por ID
        5 - Deletar um cliente por ID
        6 - Sair do programa
        """

        # Configuração do layout principal
        self.layout = QVBoxLayout()

        # Criando um widget empilhado (para navegação entre telas)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Criar as páginas (Menu Principal e as demais opções)
        self.create_main_menu()
        self.create_cadastro_cliente_page()
        self.create_hello_world_page()

        # Definir o layout da janela principal
        self.setLayout(self.layout)

    def create_main_menu(self):
        """Cria o menu principal com botões para diferentes funcionalidades"""
        main_menu = QWidget()
        layout = QVBoxLayout()

        # Botões do menu
        cadastro_button = QPushButton("Cadastrar um novo cliente")
        hello_world_button = QPushButton("Hello World (teste)")
        sair_button = QPushButton("Sair do programa")

        # Conectando os botões às funções que alteram as páginas
        cadastro_button.clicked.connect(self.show_cadastro_cliente_page)
        hello_world_button.clicked.connect(self.show_hello_world_page)
        sair_button.clicked.connect(self.close)

        # Adicionando os botões ao layout
        layout.addWidget(cadastro_button)
        layout.addWidget(hello_world_button)
        layout.addWidget(sair_button)

        main_menu.setLayout(layout)
        self.stacked_widget.addWidget(main_menu)

    def create_cadastro_cliente_page(self):
        """Cria a página de cadastro de cliente"""
        cadastro_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Página de Cadastro de Cliente")
        voltar_button = QPushButton("Voltar para o Menu")
        voltar_button.clicked.connect(self.show_main_menu)

        layout.addWidget(label)
        layout.addWidget(voltar_button)

        cadastro_page.setLayout(layout)
        self.stacked_widget.addWidget(cadastro_page)

    def create_hello_world_page(self):
        """Cria a página de Hello World"""
        hello_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Hello World!")
        voltar_button = QPushButton("Voltar para o Menu")
        voltar_button.clicked.connect(self.show_main_menu)

        layout.addWidget(label)
        layout.addWidget(voltar_button)

        hello_page.setLayout(layout)
        self.stacked_widget.addWidget(hello_page)

    def show_main_menu(self):
        """Exibe o menu principal"""
        self.stacked_widget.setCurrentIndex(0)

    def show_cadastro_cliente_page(self):
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

