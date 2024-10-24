from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QDateEdit,
    QFormLayout,
    QTableWidget,
    QHeaderView,
)
from gui.input_handlers import (
    save_new_client,
    search_client,
    search_client_for_update,
    update_client_data,
    update_clients_table,
    confirm_delete,
)


def create_main_menu(self):
    """Cria o menu principal com botões para diferentes funcionalidades"""

    main_menu = QWidget()
    layout = QVBoxLayout()

    # Botões do menu principal
    register_button = QPushButton("Cadastrar um novo cliente")
    list_all_clients_button = QPushButton("Listar todos os clientes")
    retrieve_client_button = QPushButton("Visualizar dados de um cliente")
    update_client_button = QPushButton("Atualizar dados de um cliente")
    delete_client_button = QPushButton("Excluir um cliente")
    exit_button = QPushButton("Sair do programa")

    # Conectando os botões às funções que alteram as páginas
    register_button.clicked.connect(self.show_register_client_page)
    list_all_clients_button.clicked.connect(self.show_list_clients_page)
    retrieve_client_button.clicked.connect(self.show_retrieve_client_data_page)
    update_client_button.clicked.connect(self.show_update_client_data_page)
    delete_client_button.clicked.connect(self.show_delete_client_page)
    exit_button.clicked.connect(self.close)

    # Adicionando os botões ao layout
    layout.addWidget(register_button)
    layout.addWidget(list_all_clients_button)
    layout.addWidget(retrieve_client_button)
    layout.addWidget(update_client_button)
    layout.addWidget(delete_client_button)
    layout.addWidget(exit_button)

    # Definindo Layout do menu principal
    main_menu.setLayout(layout)
    self.stacked_widget.addWidget(main_menu)


def create_register_client_page(self):
    """Cria a página de cadastro de cliente"""
    register_page = QWidget()
    layout = QVBoxLayout()
    form_layout = QFormLayout()

    # Criando os campos de entrada
    self.name_input = QLineEdit()
    self.cpf_input = QLineEdit()
    self.birthdate_input = QDateEdit()
    self.birthdate_input.setCalendarPopup(True)
    self.birthdate_input.setDate(QDate.currentDate())
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
    submit_button.clicked.connect(lambda: save_new_client(self))

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


def list_all_clients_page(self):
    """Cria a página de listagem de clientes"""
    # Verifica se a página de listagem já foi criada
    if hasattr(self, "list_page"):
        self.table.clearContents()
    else:
        self.list_page = QWidget()
        layout = QVBoxLayout()

        # Título
        label = QLabel("Lista de Clientes")

        # Cria a tabela para exibir os clientes
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nome", "CPF", "Idade", "Cidade", "Email"]
        )

        # Definindo uma largura mínima para as colunas
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            5, QHeaderView.Stretch
        )
        # Ordenação
        self.table.setSortingEnabled(True)

        # Botão para voltar ao menu principal
        return_button = QPushButton("Voltar para o Menu")
        return_button.clicked.connect(self.show_main_menu)

        # Adiciona os widgets ao layout
        layout.addWidget(label)
        layout.addWidget(self.table)
        layout.addWidget(return_button)

        # Configura o layout da página
        self.list_page.setLayout(layout)
        self.stacked_widget.addWidget(self.list_page)

    # Busca e exibe os dados atualizados
    update_clients_table(self)


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
    search_button.clicked.connect(
        lambda: search_client(self)
    )
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


def update_client_data_page(self):
    """Cria a página de atualização de cliente pelo ID"""
    # Cria o widget da página
    update_page = QWidget()
    layout = QVBoxLayout()

    # Título
    label = QLabel("Atualizar dados do Cliente por ID")
    layout.addWidget(label, alignment=Qt.AlignTop)

    # Cria um layout horizontal
    search_id_layout = QHBoxLayout()

    # Entrada do ID do cliente
    search_id_label = QLabel("Digite o ID do Cliente:")
    search_id_layout.addWidget(search_id_label)
    # Campo de entrada para busca do ID
    self.id_input_update = QLineEdit()
    self.id_input_update.setFixedWidth(50)
    search_id_layout.addWidget(self.id_input_update)

    # Botão para buscar cliente
    search_button = QPushButton("Buscar Cliente")
    search_button.setFixedWidth(100)
    search_button.clicked.connect(
        lambda: search_client_for_update(self)
    )
    search_id_layout.addWidget(search_button)

    # Adiciona o layout horizontal ao layout da janela
    layout.addLayout(search_id_layout)

    # Campos editáveis para os dados do cliente
    self.name_input_update = QLineEdit()
    self.email_input_update = QLineEdit()
    self.phone_input_update = QLineEdit()

    layout.addWidget(QLabel("Nome:"))
    layout.addWidget(self.name_input_update)

    layout.addWidget(QLabel("E-mail:"))
    layout.addWidget(self.email_input_update)

    layout.addWidget(QLabel("Telefone:"))
    layout.addWidget(self.phone_input_update)

    # Botão para salvar as alterações
    save_button = QPushButton("Salvar Alterações")
    save_button.clicked.connect(
        lambda: update_client_data(self)
    )
    layout.addWidget(save_button)

    # Label para feedback de status
    self.result_label_update = QLabel()
    layout.addWidget(self.result_label_update)

    # Botão para voltar ao menu principal
    return_button = QPushButton("Voltar para o Menu")
    return_button.clicked.connect(self.show_main_menu)
    layout.addWidget(return_button)

    # Configura o layout da página
    update_page.setLayout(layout)
    self.stacked_widget.addWidget(update_page)


def delete_client_page(self):
    """Cria a página para deletar um cliente pelo ID"""
    # Cria o widget da página
    delete_page = QWidget()
    layout = QVBoxLayout()

    # Título
    label = QLabel("Deletar Cliente")
    layout.addWidget(label)

    # Campo para inserir o ID do cliente
    id_label = QLabel("Informe o ID do Cliente:")
    layout.addWidget(id_label)

    id_input = QLineEdit()
    id_input.setPlaceholderText("ID do Cliente")
    layout.addWidget(id_input)

    # Botão de Excluir
    delete_button = QPushButton("Excluir Cliente")
    layout.addWidget(delete_button)

    # Botão de Voltar ao Menu
    return_button = QPushButton("Voltar para o Menu")
    layout.addWidget(return_button)

    # Ação para voltar ao menu principal
    return_button.clicked.connect(self.show_main_menu)

    # Ação para deletar o cliente ao clicar no botão
    delete_button.clicked.connect(
        lambda: confirm_delete(self, id_input.text())
    )

    # Define o layout da página
    delete_page.setLayout(layout)
    self.stacked_widget.addWidget(delete_page)
