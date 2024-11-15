from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QGroupBox,
    QRadioButton,
    QDateEdit,
    QFormLayout,
    QTableWidget,
    QHeaderView,
)
from gui.client_input_handlers import (
    save_new_client,
    search_client,
    search_client_for_update,
    update_client_data,
    update_clients_table,
    confirm_delete,
)
from gui.login_input_handler import handle_login
from gui.user_input_handlers import (
    save_new_user,
    update_users_table,
    confirm_delete_user,
)
from gui.utils import toggle_password_visibility
from gui.permissions import (
    show_register_page_with_permission,
    show_update_page_with_permission,
    show_delete_page_with_permission
)


def create_login_page(self):
    """Cria a página de login"""
    login_page = QWidget()
    layout = QVBoxLayout()

    # Título
    title_label = QLabel("Login")
    title_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(title_label)

    # Campos de login
    form_layout = QFormLayout()

    self.username_input = QLineEdit()
    self.password_input = QLineEdit()
    self.password_input.setEchoMode(QLineEdit.Password)

    form_layout.addRow("Usuário:", self.username_input)
    form_layout.addRow("Senha:", self.password_input)

    layout.addLayout(form_layout)

    # Botão de login
    login_button = QPushButton("Entrar")
    login_button.clicked.connect(lambda: handle_login(self))

    # Botão de Sair do Programa
    exit_button = QPushButton("Sair do programa")
    exit_button.clicked.connect(self.close)

    layout.addWidget(login_button)
    layout.addWidget(exit_button)

    login_page.setLayout(layout)
    self.stacked_widget.addWidget(login_page)


def create_admin_menu(self):
    """Cria o menu de administrador"""
    admin_menu = QWidget()
    layout = QVBoxLayout()

    # Título
    title_label = QLabel("Menu do Administrador")
    title_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(title_label)

    # Botões do menu admin
    create_user_button = QPushButton("Criar Novo Usuário")
    list_users_button = QPushButton("Listar Usuários")
    delete_user_button = QPushButton("Excluir Usuário")

    # Botão para acessar o sistema principal
    access_system_button = QPushButton("Acessar Sistema Principal")
    logout_button = QPushButton("Sair")

    # Conectando os botões às funções
    create_user_button.clicked.connect(self.show_create_user_page)
    list_users_button.clicked.connect(self.show_list_users_page)
    delete_user_button.clicked.connect(self.show_delete_user_page)
    access_system_button.clicked.connect(self.show_main_menu)
    logout_button.clicked.connect(self.show_login_page)

    # Adicionando os botões ao layout
    layout.addWidget(create_user_button)
    layout.addWidget(list_users_button)
    layout.addWidget(delete_user_button)
    layout.addWidget(access_system_button)
    layout.addWidget(logout_button)

    admin_menu.setLayout(layout)
    self.stacked_widget.addWidget(admin_menu)


def create_user_page(self):
    """Cria a página de cadastro de usuário"""
    create_user_page = QWidget()
    layout = QVBoxLayout()

    # Título
    title_label = QLabel("Criar Novo Usuário")
    title_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(title_label)

    # Form
    form_layout = QFormLayout()

    self.new_username_input = QLineEdit()
    self.new_fullname_input = QLineEdit()
    self.new_phone_input = QLineEdit()
    self.new_email_input = QLineEdit()
    self.new_password_input = QLineEdit()
    self.new_password_input.setEchoMode(QLineEdit.Password)

    # Grupo de radio buttons para os cargos
    role_group = QGroupBox("Cargo do Usuário")
    role_layout = QVBoxLayout()

    self.admin_radio = QRadioButton("Administrador")
    self.user_radio = QRadioButton("Usuário")
    self.guest_radio = QRadioButton("Convidado")

    # Definir o cargo "Usuário" como padrão
    self.user_radio.setChecked(True)

    self.admin_radio.setToolTip("Acesso total ao sistema")
    self.user_radio.setToolTip("Acesso para operações regulares")
    self.guest_radio.setToolTip("Acesso limitado apenas para visualização")

    role_layout.addWidget(self.admin_radio)
    role_layout.addWidget(self.user_radio)
    role_layout.addWidget(self.guest_radio)
    role_group.setLayout(role_layout)

    password_layout = QHBoxLayout()
    show_password_button = QPushButton("👁")
    show_password_button.setFixedWidth(30)
    show_password_button.clicked.connect(lambda: toggle_password_visibility(self))
    password_layout.addWidget(self.new_password_input)
    password_layout.addWidget(show_password_button)

    form_layout.addRow("Nome de Usuário:", self.new_username_input)
    form_layout.addRow("Nome completo:", self.new_fullname_input)
    form_layout.addRow("Telefone (com DDD):", self.new_phone_input)
    form_layout.addRow("E-mail:", self.new_email_input)
    form_layout.addRow("Senha:", password_layout)
    form_layout.addRow(role_group)

    layout.addLayout(form_layout)

    # Botões
    save_button = QPushButton("Salvar Usuário")
    return_button = QPushButton("Voltar")

    save_button.clicked.connect(lambda: save_new_user(self))
    return_button.clicked.connect(self.show_admin_menu)

    layout.addWidget(save_button)
    layout.addWidget(return_button)

    create_user_page.setLayout(layout)
    self.stacked_widget.addWidget(create_user_page)


def list_users_page(self):
    """Cria a página de listagem de usuários"""
    if hasattr(self, "list_users_page"):
        self.users_table.clearContents()
    else:
        self.list_users_page = QWidget()
        layout = QVBoxLayout()

        # Título
        title_label = QLabel("Lista de Usuários")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tabela de usuários
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(
            ["ID", "Usuário", "Nome Completo", "Telefone", "E-mail", "Nível de Acesso"]
        )

        # Configurando a tabela
        self.users_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.users_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        self.users_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(
            5, QHeaderView.ResizeToContents
        )
        self.users_table.setSortingEnabled(True)

        layout.addWidget(self.users_table)

        # Botão de retorno
        return_button = QPushButton("Voltar")
        return_button.clicked.connect(self.show_admin_menu)
        layout.addWidget(return_button)

        self.list_users_page.setLayout(layout)
        self.stacked_widget.addWidget(self.list_users_page)

    # Busca e exibe os dados atualizados
    update_users_table(self)


def delete_user_page(self):
    """Cria a página para deletar usuários"""
    delete_user_page = QWidget()
    layout = QVBoxLayout()

    # Título
    title_label = QLabel("Excluir Usuário")
    title_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(title_label)

    # Campo para ID do usuário
    form_layout = QFormLayout()
    self.delete_user_id_input = QLineEdit()
    form_layout.addRow("ID do Usuário:", self.delete_user_id_input)
    layout.addLayout(form_layout)

    # Botões
    delete_button = QPushButton("Excluir")
    return_button = QPushButton("Voltar")

    delete_button.clicked.connect(
        lambda: confirm_delete_user(self, self.delete_user_id_input.text())
    )
    return_button.clicked.connect(self.show_admin_menu)

    layout.addWidget(delete_button)
    layout.addWidget(return_button)

    delete_user_page.setLayout(layout)
    self.stacked_widget.addWidget(delete_user_page)


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
    register_button.clicked.connect(lambda: show_register_page_with_permission(self))
    list_all_clients_button.clicked.connect(self.show_list_clients_page)
    retrieve_client_button.clicked.connect(self.show_retrieve_client_data_page)
    update_client_button.clicked.connect(lambda: show_update_page_with_permission(self))
    delete_client_button.clicked.connect(lambda: show_delete_page_with_permission(self))
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
    if hasattr(self, "list_clients_page"):
        self.table.clearContents()
    else:
        self.list_clients_page = QWidget()
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
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
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
        self.list_clients_page.setLayout(layout)
        self.stacked_widget.addWidget(self.list_clients_page)

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
    search_button.clicked.connect(lambda: search_client(self))
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
    search_button.clicked.connect(lambda: search_client_for_update(self))
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
    save_button.clicked.connect(lambda: update_client_data(self))
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
    delete_button.clicked.connect(lambda: confirm_delete(self, id_input.text()))

    # Define o layout da página
    delete_page.setLayout(layout)
    self.stacked_widget.addWidget(delete_page)
