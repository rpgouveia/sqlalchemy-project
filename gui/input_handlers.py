from PySide6.QtWidgets import (
    QMessageBox,
    QTableWidgetItem,
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
from PySide6.QtCore import Qt
from core.crud import (
    create_client,
    get_all_clients,
    get_client,
    update_client,
    delete_client,
)
from core.models import Client
from sqlalchemy.exc import IntegrityError


def save_new_client(interface):
    """Salva o cliente no banco de dados após validar os dados"""
    try:
        # Capturar dados dos campos
        name = interface.name_input.text()
        cpf = validate_cpf(interface.cpf_input.text())
        birthdate = validate_birthdate(
            interface.birthdate_input.date().toString("yyyy-MM-dd")
        )
        address_1 = interface.address_1_input.text()
        address_2 = interface.address_2_input.text() or None
        post_code = validate_post_code(interface.post_code_input.text())
        city = interface.city_input.text()
        state = validate_state(interface.state_input.text())
        country = validate_country(interface.country_input.text())
        phone = validate_phone(interface.phone_input.text())
        email = validate_email(interface.email_input.text())

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
        create_client(interface.db, new_client)
        QMessageBox.information(interface, "Sucesso", "Cliente cadastrado com sucesso!")

        # Limpa os campos após cadastro
        clear_fields(interface)

    except IntegrityError as ie:
        interface.db.rollback()
        if "client.cpf" in str(ie.orig):
            QMessageBox.warning(
                interface, "Erro", f"O CPF {cpf} já está cadastrado no sistema."
            )
        elif "client.email" in str(ie.orig):
            QMessageBox.warning(
                interface, "Erro", f"O e-mail {email} já está cadastrado no sistema."
            )
        else:
            QMessageBox.critical(
                interface, "Erro", f"Erro de integridade no banco de dados: {ie}"
            )
    except ValueError as ve:
        QMessageBox.warning(interface, "Erro de Validação", f"Erro: {ve}")
    except Exception as e:
        QMessageBox.critical(
            interface, "Erro Inesperado", f"Ocorreu um erro inesperado: {e}"
        )


def clear_fields(interface):
    """Limpa os campos de entrada do formulário"""
    interface.name_input.clear()
    interface.cpf_input.clear()
    interface.birthdate_input.clear()
    interface.address_1_input.clear()
    interface.address_2_input.clear()
    interface.post_code_input.clear()
    interface.city_input.clear()
    interface.state_input.clear()
    interface.country_input.clear()
    interface.phone_input.clear()
    interface.email_input.clear()


def search_client(interface):
    """Função para buscar cliente no banco de dados pelo ID inserido"""
    client_id = interface.id_input.text().strip()

    if not client_id.isdigit():
        QMessageBox.warning(
            interface.stacked_widget, "Erro", "Por favor, insira um ID válido."
        )
        return

    client = get_client(interface.db, int(client_id))

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
        interface.result_label.setText(client_data)
    else:
        QMessageBox.warning(
            interface.stacked_widget,
            "Erro",
            f"Cliente com ID {client_id} não encontrado.",
        )
        interface.result_label.setText("")


def search_client_for_update(interface):
    """Função para buscar cliente no banco de dados pelo ID inserido (para atualização)"""
    client_id = interface.id_input_update.text().strip()

    if not client_id.isdigit():
        QMessageBox.warning(
            interface.stacked_widget, "Erro", "Por favor, insira um ID válido."
        )
        return

    client = get_client(interface.db, int(client_id))

    if client:
        # Limpar todas as mensagens de atualização anteriores
        interface.result_label_update.setText("")
        # Preenche os campos editáveis com os dados do cliente
        interface.name_input_update.setText(client.name)
        interface.email_input_update.setText(client.email)
        interface.phone_input_update.setText(client.phone)
        interface.result_label_update.setText(
            f"Cliente com ID {client_id} carregado para atualização."
        )
    else:
        QMessageBox.warning(
            interface.stacked_widget,
            "Erro",
            f"Cliente com ID {client_id} não encontrado.",
        )
        interface.result_label_update.setText("")


def update_client_data(interface):
    """Função para salvar as alterações no banco de dados"""
    client_id = interface.id_input_update.text().strip()

    if not client_id.isdigit():
        QMessageBox.warning(interface.stacked_widget, "Erro", "ID inválido.")
        return

    client = get_client(interface.db, int(client_id))

    if client:
        # Atualiza os dados do cliente com base no input
        client.name = interface.name_input_update.text().strip()
        client.email = validate_email(interface.email_input_update.text().strip())
        client.phone = validate_phone(interface.phone_input_update.text().strip())

        try:
            update_client(interface.db, client)  # Atualiza o cliente no banco de dados
            interface.result_label_update.setText(
                f"Cliente com ID {client.id} atualizado com sucesso!"
            )
        except IntegrityError as ie:
            interface.db.rollback()
            if "client.email" in str(ie.orig):
                interface.result_label_update.setText(
                    f"Erro: O e-mail {client.email} já está cadastrado."
                )
            else:
                interface.result_label_update.setText(
                    f"Erro de integridade no banco de dados: {ie}"
                )
        except Exception as e:
            interface.result_label_update.setText(f"Ocorreu um erro: {e}")
    else:
        interface.result_label_update.setText(
            f"Cliente com ID {client_id} não encontrado."
        )


def update_clients_table(interface):
    """Atualiza a tabela de clientes com os dados mais recentes do banco"""
    # Função para buscar todos os clientes no banco de dados
    clients = get_all_clients(interface.db)

    # Define o número de linhas com base no número de clientes
    interface.table.setRowCount(len(clients))

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
        interface.table.setItem(row, 0, id_item)
        interface.table.setItem(row, 1, name_item)
        interface.table.setItem(row, 2, cpf_item)
        interface.table.setItem(row, 3, age_item)
        interface.table.setItem(row, 4, city_item)
        interface.table.setItem(row, 5, email_item)


def confirm_delete(interface, id):
    """Confirma e executa a exclusão do cliente"""
    if not id.isdigit():
        QMessageBox.warning(interface, "Erro", "O ID deve ser um número válido.")
        return

    client_id = int(id)

    # Busca o cliente no banco de dados
    client = interface.db.query(Client).filter(Client.id == client_id).first()

    if not client:
        QMessageBox.warning(
            interface, "Erro", f"Cliente com ID {client_id} não encontrado."
        )
        return

    # Confirmação antes de deletar
    confirm = QMessageBox.question(
        interface,
        "Confirmação",
        f"Tem certeza que deseja deletar o cliente com ID {client.id} ({client.name})?",
        QMessageBox.Yes | QMessageBox.No,
    )

    if confirm == QMessageBox.Yes:
        # Deletar o cliente
        delete_client(interface.db, client_id)
        QMessageBox.information(interface, "Sucesso", "Cliente deletado com sucesso.")
    else:
        QMessageBox.information(
            interface, "Cancelado", "Operação de exclusão cancelada."
        )
