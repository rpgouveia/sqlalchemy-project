import sys
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QLineEdit,
    QDateEdit,
    QFormLayout,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
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
from PySide6.QtCore import QDate, Qt
from sqlalchemy.orm import Session
from core.database import connect_db
from core.crud import create_client, get_all_clients, get_client
from core.models import Client
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


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
        self.list_all_clients_page()
        self.retrieve_client_data_page()

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
        list_all_clients_button = QPushButton("Listar todos os clientes")
        retrieve_client_button = QPushButton("Visualizar dados de um cliente")
        exit_button = QPushButton("Sair do programa")

        # Conectando os botões às funções que alteram as páginas
        register_button.clicked.connect(self.show_register_client_page)
        list_all_clients_button.clicked.connect(self.show_list_clients_page)
        retrieve_client_button.clicked.connect(self.show_retrieve_client_data_page)
        exit_button.clicked.connect(self.close)

        # Adicionando os botões ao layout
        layout.addWidget(register_button)
        layout.addWidget(list_all_clients_button)
        layout.addWidget(retrieve_client_button)
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

    def list_all_clients_page(self):
        """Cria a página de listagem de clientes"""
        # Cria o widget da página
        list_page = QWidget()
        layout = QVBoxLayout()

        # Título
        label = QLabel("Lista de Clientes")

        # Cria a tabela para exibir os clientes
        table = QTableWidget()
        table.setColumnCount(6)  # Número de colunas
        table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Idade", "Cidade", "Email"])

        # Definindo uma largura mínima para as colunas
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)           # Nome
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)  # CPF
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Idade
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)           # Cidade
        table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)           # Email
        # Ordenação
        table.setSortingEnabled(True)

        # Função para buscar todos os clientes no banco de dados
        clients = get_all_clients(self.db)

        # Define o número de linhas com base no número de clientes
        table.setRowCount(len(clients))

        # Popula a tabela com os dados dos clientes
        for row, client in enumerate(clients):
            id_item = QTableWidgetItem(str(client.id))
            id_item.setTextAlignment(Qt.AlignCenter)

            name_item = QTableWidgetItem(client.name)
            name_item.setTextAlignment(Qt.AlignCenter)

            cpf_item = QTableWidgetItem(client.cpf)
            cpf_item.setTextAlignment(Qt.AlignCenter)

            age_item = QTableWidgetItem(str(client.age))
            age_item.setTextAlignment(Qt.AlignCenter)

            city_item = QTableWidgetItem(client.city)
            city_item.setTextAlignment(Qt.AlignCenter)

            email_item = QTableWidgetItem(client.email)
            email_item.setTextAlignment(Qt.AlignCenter)

            # Adiciona os itens à tabela
            table.setItem(row, 0, id_item)
            table.setItem(row, 1, name_item)
            table.setItem(row, 2, cpf_item)
            table.setItem(row, 3, age_item)
            table.setItem(row, 4, city_item)
            table.setItem(row, 5, email_item)

        # Botão para voltar ao menu principal
        return_button = QPushButton("Voltar para o Menu")
        return_button.clicked.connect(self.show_main_menu)

        # Adiciona os widgets ao layout
        layout.addWidget(label)
        layout.addWidget(table)
        layout.addWidget(return_button)

        # Configura o layout da página
        list_page.setLayout(layout)
        self.stacked_widget.addWidget(list_page)

    def retrieve_client_data_page(self):
        """Cria a página de busca e exibição de cliente pelo ID"""
        # Cria o widget da página
        retrieve_page = QWidget()
        layout = QVBoxLayout()

        # Título
        label = QLabel("Visualizar dados do Cliente por ID")
        layout.addWidget(label, alignment=Qt.AlignTop)

        # Cria um layout horizontal
        search_id_layout = QHBoxLayout()

        # Entrada do ID do cliente
        search_id_label = QLabel("Digite o ID do Cliente:")
        search_id_layout.addWidget(search_id_label)
        # Campo de entrada para busca do ID
        self.id_input = QLineEdit()
        self.id_input.setFixedWidth(50)
        search_id_layout.addWidget(self.id_input)

        # Botão para buscar cliente
        search_button = QPushButton("Buscar Cliente")
        search_button.setFixedWidth(100)
        search_button.clicked.connect(self.search_client)
        search_id_layout.addWidget(search_button)

        # Adiciona o layout horizontal ao layout da janela
        layout.addLayout(search_id_layout)


        # Label para exibir os dados do cliente
        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        # Botão para voltar ao menu principal
        return_button = QPushButton("Voltar para o Menu")
        return_button.clicked.connect(self.show_main_menu)
        layout.addWidget(return_button)

        # Configura o layout da página
        retrieve_page.setLayout(layout)
        self.stacked_widget.addWidget(retrieve_page)

    def search_client(self):
        """Função para buscar cliente no banco de dados pelo ID inserido"""
        client_id = self.id_input.text().strip()

        if not client_id.isdigit():
            QMessageBox.warning(self.stacked_widget, "Erro", "Por favor, insira um ID válido.")
            return

        client = get_client(self.db, int(client_id))

        if client:
            # Exibe os dados do cliente
            client_data = (
                f"ID: {client.id}\n"
                f"Nome: {client.name}\n"
                f"CPF: {client.cpf}\n"
                f"Data de Nascimento: {client.birthdate}\n"
                f"Idade: {client.age}\n"
                f"Endereço 1: {client.address_1}\n"
                f"Endereço 2: {client.address_2 or 'Não informado'}\n"
                f"CEP: {client.post_code}\n"
                f"Cidade: {client.city}\n"
                f"Estado: {client.state}\n"
                f"País: {client.country}\n"
                f"Telefone: {client.phone}\n"
                f"E-mail: {client.email}"
            )
            self.result_label.setText(client_data)
        else:
            QMessageBox.warning(self.stacked_widget, "Erro", f"Cliente com ID {client_id} não encontrado.")
            self.result_label.setText("")

    def show_main_menu(self):
        """Exibe o menu principal"""
        self.stacked_widget.setCurrentIndex(0)

    def show_register_client_page(self):
        """Exibe a página de cadastro de cliente"""
        self.stacked_widget.setCurrentIndex(1)

    def show_list_clients_page(self):
        """Exibe a página de listagem de clientes"""
        self.stacked_widget.setCurrentIndex(2)

    def show_retrieve_client_data_page(self):
        """Exibe a página de dados do cliente"""
        self.stacked_widget.setCurrentIndex(3)

# Startup Application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindowApp()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
