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
        clear_fields(self)

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


def search_client_generic(
    self,
    client_id_input,
    result_label, 
    editable_fields=None
):
    """Função genérica para buscar cliente no banco de dados pelo ID inserido."""
    client_id = client_id_input.text().strip()

    if not client_id.isdigit():
        QMessageBox.warning(
            self.stacked_widget, "Erro", "Por favor, insira um ID válido."
        )
        return

    client = get_client(self.db, int(client_id))

    if client:
        if editable_fields:
            editable_fields["name"].setText(client.name)
            editable_fields["email"].setText(client.email)
            editable_fields["phone"].setText(client.phone)
            result_label.setText(
                f"Cliente com ID {client_id} carregado para atualização."
            )
        else:
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
            result_label.setText(client_data)
    else:
        QMessageBox.warning(
            self.stacked_widget,
            "Erro",
            f"Cliente com ID {client_id} não encontrado.",
        )
        result_label.setText("")


def search_client(self):
    """Função para buscar cliente para visualização."""
    search_client_generic(self, self.id_input, self.result_label)


def search_client_for_update(self):
    """Função para buscar cliente para atualização."""
    editable_fields = {
        "name": self.name_input_update,
        "email": self.email_input_update,
        "phone": self.phone_input_update,
    }
    search_client_generic(
        self,
        self.id_input_update,
        self.result_label_update,
        editable_fields,
    )


def update_client_data(self):
    """Função para salvar as alterações no banco de dados"""
    client_id = self.id_input_update.text().strip()

    if not client_id.isdigit():
        QMessageBox.warning(self.stacked_widget, "Erro", "ID inválido.")
        return

    client = get_client(self.db, int(client_id))

    if client:
        # Atualiza os dados do cliente com base no input
        client.name = self.name_input_update.text().strip()
        client.email = validate_email(self.email_input_update.text().strip())
        client.phone = validate_phone(self.phone_input_update.text().strip())

        try:
            update_client(self.db, client)  # Atualiza o cliente no banco de dados
            self.result_label_update.setText(
                f"Cliente com ID {client.id} atualizado com sucesso!"
            )
        except IntegrityError as ie:
            self.db.rollback()
            if "client.email" in str(ie.orig):
                self.result_label_update.setText(
                    f"Erro: O e-mail {client.email} já está cadastrado."
                )
            else:
                self.result_label_update.setText(
                    f"Erro de integridade no banco de dados: {ie}"
                )
        except Exception as e:
            self.result_label_update.setText(f"Ocorreu um erro: {e}")
    else:
        self.result_label_update.setText(
            f"Cliente com ID {client_id} não encontrado."
        )


def update_clients_table(self):
    """Atualiza a tabela de clientes com os dados mais recentes do banco"""
    # Função para buscar todos os clientes no banco de dados
    clients = get_all_clients(self.db)

    # Define o número de linhas com base no número de clientes
    self.table.setRowCount(len(clients))

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
        self.table.setItem(row, 0, id_item)
        self.table.setItem(row, 1, name_item)
        self.table.setItem(row, 2, cpf_item)
        self.table.setItem(row, 3, age_item)
        self.table.setItem(row, 4, city_item)
        self.table.setItem(row, 5, email_item)


def confirm_delete(self, id):
    """Confirma e executa a exclusão do cliente"""
    if not id.isdigit():
        QMessageBox.warning(self, "Erro", "O ID deve ser um número válido.")
        return

    client_id = int(id)

    # Busca o cliente no banco de dados
    client = self.db.query(Client).filter(Client.id == client_id).first()

    if not client:
        QMessageBox.warning(
            self, "Erro", f"Cliente com ID {client_id} não encontrado."
        )
        return

    # Confirmação antes de deletar
    confirm = QMessageBox.question(
        self,
        "Confirmação",
        f"Tem certeza que deseja deletar o cliente com ID {client.id} ({client.name})?",
        QMessageBox.Yes | QMessageBox.No,
    )

    if confirm == QMessageBox.Yes:
        # Deletar o cliente
        delete_client(self.db, client_id)
        QMessageBox.information(self, "Sucesso", "Cliente deletado com sucesso.")
    else:
        QMessageBox.information(
            self, "Cancelado", "Operação de exclusão cancelada."
        )
