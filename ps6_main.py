import sys
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QStackedWidget,
    QLineEdit,
    QDateEdit,
    QFormLayout,
    QMessageBox,
)
from core.validations import (
    validate_cpf,
    validate_phone,
    validate_birthdate,
    validate_email,
    validate_post_code,
    validate_country,
    validate_state,
)
from PySide6.QtCore import QDate
from sqlalchemy.orm import Session
from core.database import connect_db
from core.crud import create_client
from core.models import Client
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date


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

        # Definindo Layout do menu principal
        main_menu.setLayout(layout)
        self.stacked_widget.addWidget(main_menu)

    def create_register_client_page(self):
        """Cria a página de cadastro de cliente"""
        register_page = QWidget()
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Criando os campos de entrada (QLineEdit, QDateEdit, etc.)
        self.name_input = QLineEdit()
        self.cpf_input = QLineEdit()
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)  # Permite escolher a data
        self.birthdate_input.setDate(QDate.currentDate())  # Data padrão
        self.address_1_input = QLineEdit()
        self.address_2_input = QLineEdit()
        self.post_code_input = QLineEdit()
        self.city_input = QLineEdit()
        self.state_input = QLineEdit()
        self.country_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        # Adicionando campos ao layout de formulário
        form_layout.addRow("Nome Completo:", self.name_input)
        form_layout.addRow("CPF:", self.cpf_input)
        form_layout.addRow("Data de Nascimento:", self.birthdate_input)
        form_layout.addRow("Endereço Principal:", self.address_1_input)
        form_layout.addRow("Complemento:", self.address_2_input)
        form_layout.addRow("CEP:", self.post_code_input)
        form_layout.addRow("Cidade:", self.city_input)
        form_layout.addRow("Estado (Ex: PR):", self.state_input)
        form_layout.addRow("País (Ex: BR):", self.country_input)
        form_layout.addRow("Telefone (com DDD):", self.phone_input)
        form_layout.addRow("Email:", self.email_input)

        # Botão para salvar o cliente
        submit_button = QPushButton("Cadastrar Cliente")
        submit_button.clicked.connect(self.save_new_client)

        # Botão para voltar ao menu
        return_button = QPushButton("Voltar para o Menu")
        return_button.clicked.connect(self.show_main_menu)

        # Construindo o Layout da Página
        layout.addLayout(form_layout)
        layout.addWidget(submit_button)
        layout.addWidget(return_button)

        # Definindo Layout da Página
        register_page.setLayout(layout)
        self.stacked_widget.addWidget(register_page)

    def clear_fields(self):
        """Limpa os campos de entrada do formulário"""
        self.name_input.clear()
        self.cpf_input.clear()
        self.birthdate_input.clear()
        self.address_1_input.clear()
        self.address_2_input.clear()
        self.post_code_input.clear()
        self.city_input.clear()
        self.state_input.clear()
        self.country_input.clear()
        self.phone_input.clear()
        self.email_input.clear()

    def save_new_client(self):
        """Salva o cliente no banco de dados após validar os dados"""
        try:
            # Capturar dados dos campos
            name = self.name_input.text()
            cpf = validate_cpf(self.cpf_input.text())
            birthdate = validate_birthdate(
                self.birthdate_input.date().toString("yyyy-MM-dd")
            )
            address_1 = self.address_1_input.text()
            address_2 = self.address_2_input.text() or None
            post_code = validate_post_code(self.post_code_input.text())
            city = self.city_input.text()
            state = validate_state(self.state_input.text())
            country = validate_country(self.country_input.text())
            phone = validate_phone(self.phone_input.text())
            email = validate_email(self.email_input.text())

            # Criando o novo objeto Client
            new_client = Client(
                name=name,
                cpf=cpf,
                birthdate=birthdate,
                address_1=address_1,
                address_2=address_2,
                post_code=post_code,
                city=city,
                state=state,
                country=country,
                phone=phone,
                email=email,
            )

            # Salvar no banco de dados
            create_client(self.db, new_client)
            QMessageBox.information(self, "Sucesso", "Cliente cadastrado com sucesso!")

            # Limpa os campos após cadastro
            self.clear_fields()

        except IntegrityError as ie:
            self.db.rollback()
            if "client.cpf" in str(ie.orig):
                QMessageBox.warning(
                    self, "Erro", f"O CPF {cpf} já está cadastrado no sistema."
                )
            elif "client.email" in str(ie.orig):
                QMessageBox.warning(
                    self, "Erro", f"O e-mail {email} já está cadastrado no sistema."
                )
            else:
                QMessageBox.critical(
                    self, "Erro", f"Erro de integridade no banco de dados: {ie}"
                )
        except ValueError as ve:
            QMessageBox.warning(self, "Erro de Validação", f"Erro: {ve}")
        except Exception as e:
            QMessageBox.critical(
                self, "Erro Inesperado", f"Ocorreu um erro inesperado: {e}"
            )

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
