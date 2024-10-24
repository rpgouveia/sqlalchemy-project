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


def create_main_menu(main_window):
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
    register_button.clicked.connect(main_window.show_register_client_page)
    list_all_clients_button.clicked.connect(main_window.show_list_clients_page)
    retrieve_client_button.clicked.connect(main_window.show_retrieve_client_data_page)
    update_client_button.clicked.connect(main_window.show_update_client_data_page)
    delete_client_button.clicked.connect(main_window.show_delete_client_page)
    exit_button.clicked.connect(main_window.close)

    # Adicionando os botões ao layout
    layout.addWidget(register_button)
    layout.addWidget(list_all_clients_button)
    layout.addWidget(retrieve_client_button)
    layout.addWidget(update_client_button)
    layout.addWidget(delete_client_button)
    layout.addWidget(exit_button)

    # Definindo Layout do menu principal
    main_menu.setLayout(layout)
    main_window.stacked_widget.addWidget(main_menu)


def create_register_client_page(main_window):
    """Cria a página de cadastro de cliente"""
    register_page = QWidget()
    layout = QVBoxLayout()
    form_layout = QFormLayout()

    # Criando os campos de entrada
    main_window.name_input = QLineEdit()
    main_window.cpf_input = QLineEdit()
    main_window.birthdate_input = QDateEdit()
    main_window.birthdate_input.setCalendarPopup(True)
    main_window.birthdate_input.setDate(QDate.currentDate())
    main_window.address_1_input = QLineEdit()
    main_window.address_2_input = QLineEdit()
    main_window.post_code_input = QLineEdit()
    main_window.city_input = QLineEdit()
    main_window.state_input = QLineEdit()
    main_window.country_input = QLineEdit()
    main_window.phone_input = QLineEdit()
    main_window.email_input = QLineEdit()

    # Adicionando campos ao layout de formulário
    form_layout.addRow("Nome Completo:", main_window.name_input)
    form_layout.addRow("CPF:", main_window.cpf_input)
    form_layout.addRow("Data de Nascimento:", main_window.birthdate_input)
    form_layout.addRow("Endereço Principal:", main_window.address_1_input)
    form_layout.addRow("Complemento:", main_window.address_2_input)
    form_layout.addRow("CEP:", main_window.post_code_input)
    form_layout.addRow("Cidade:", main_window.city_input)
    form_layout.addRow("Estado (Ex: PR):", main_window.state_input)
    form_layout.addRow("País (Ex: BR):", main_window.country_input)
    form_layout.addRow("Telefone (com DDD):", main_window.phone_input)
    form_layout.addRow("Email:", main_window.email_input)

    # Botão para salvar o cliente
    submit_button = QPushButton("Cadastrar Cliente")
    submit_button.clicked.connect(lambda: save_new_client(main_window))

    # Botão para voltar ao menu
    return_button = QPushButton("Voltar para o Menu")
    return_button.clicked.connect(main_window.show_main_menu)

    # Construindo o Layout da Página
    layout.addLayout(form_layout)
    layout.addWidget(submit_button)
    layout.addWidget(return_button)

    # Definindo Layout da Página
    register_page.setLayout(layout)
    main_window.stacked_widget.addWidget(register_page)


def list_all_clients_page(main_window):
    """Cria a página de listagem de clientes"""
    # Verifica se a página de listagem já foi criada
    if hasattr(main_window, "list_page"):
        main_window.table.clearContents()
    else:
        main_window.list_page = QWidget()
        layout = QVBoxLayout()

        # Título
        label = QLabel("Lista de Clientes")

        # Cria a tabela para exibir os clientes
        main_window.table = QTableWidget()
        main_window.table.setColumnCount(6)
        main_window.table.setHorizontalHeaderLabels(
            ["ID", "Nome", "CPF", "Idade", "Cidade", "Email"]
        )

        # Definindo uma largura mínima para as colunas
        main_window.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        main_window.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        main_window.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        main_window.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        main_window.table.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.Stretch
        )
        main_window.table.horizontalHeader().setSectionResizeMode(
            5, QHeaderView.Stretch
        )
        # Ordenação
        main_window.table.setSortingEnabled(True)

        # Botão para voltar ao menu principal
        return_button = QPushButton("Voltar para o Menu")
        return_button.clicked.connect(main_window.show_main_menu)

        # Adiciona os widgets ao layout
        layout.addWidget(label)
        layout.addWidget(main_window.table)
        layout.addWidget(return_button)

        # Configura o layout da página
        main_window.list_page.setLayout(layout)
        main_window.stacked_widget.addWidget(main_window.list_page)

    # Busca e exibe os dados atualizados
    update_clients_table(main_window)


def retrieve_client_data_page(main_window):
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
    main_window.id_input = QLineEdit()
    main_window.id_input.setFixedWidth(50)
    search_id_layout.addWidget(main_window.id_input)

    # Botão para buscar cliente
    search_button = QPushButton("Buscar Cliente")
    search_button.setFixedWidth(100)
    search_button.clicked.connect(
        lambda: search_client(main_window)
    )
    search_id_layout.addWidget(search_button)

    # Adiciona o layout horizontal ao layout da janela
    layout.addLayout(search_id_layout)

    # Label para exibir os dados do cliente
    main_window.result_label = QLabel()
    layout.addWidget(main_window.result_label)

    # Botão para voltar ao menu principal
    return_button = QPushButton("Voltar para o Menu")
    return_button.clicked.connect(main_window.show_main_menu)
    layout.addWidget(return_button)

    # Configura o layout da página
    retrieve_page.setLayout(layout)
    main_window.stacked_widget.addWidget(retrieve_page)


def update_client_data_page(main_window):
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
    main_window.id_input_update = QLineEdit()
    main_window.id_input_update.setFixedWidth(50)
    search_id_layout.addWidget(main_window.id_input_update)

    # Botão para buscar cliente
    search_button = QPushButton("Buscar Cliente")
    search_button.setFixedWidth(100)
    search_button.clicked.connect(
        lambda: search_client_for_update(main_window)
    )
    search_id_layout.addWidget(search_button)

    # Adiciona o layout horizontal ao layout da janela
    layout.addLayout(search_id_layout)

    # Campos editáveis para os dados do cliente
    main_window.name_input_update = QLineEdit()
    main_window.email_input_update = QLineEdit()
    main_window.phone_input_update = QLineEdit()

    layout.addWidget(QLabel("Nome:"))
    layout.addWidget(main_window.name_input_update)

    layout.addWidget(QLabel("E-mail:"))
    layout.addWidget(main_window.email_input_update)

    layout.addWidget(QLabel("Telefone:"))
    layout.addWidget(main_window.phone_input_update)

    # Botão para salvar as alterações
    save_button = QPushButton("Salvar Alterações")
    save_button.clicked.connect(
        lambda: update_client_data(main_window)
    )
    layout.addWidget(save_button)

    # Label para feedback de status
    main_window.result_label_update = QLabel()
    layout.addWidget(main_window.result_label_update)

    # Botão para voltar ao menu principal
    return_button = QPushButton("Voltar para o Menu")
    return_button.clicked.connect(main_window.show_main_menu)
    layout.addWidget(return_button)

    # Configura o layout da página
    update_page.setLayout(layout)
    main_window.stacked_widget.addWidget(update_page)


def delete_client_page(main_window):
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
    return_button.clicked.connect(main_window.show_main_menu)

    # Ação para deletar o cliente ao clicar no botão
    delete_button.clicked.connect(
        lambda: confirm_delete(main_window, id_input.text())
    )

    # Define o layout da página
    delete_page.setLayout(layout)
    main_window.stacked_widget.addWidget(delete_page)
