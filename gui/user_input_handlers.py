from PySide6.QtWidgets import (
    QMessageBox,
    QTableWidgetItem
)
from core.validations import (
    validate_phone,
    validate_email,
)
from PySide6.QtCore import Qt
from core.crud import (
    create_user,
    get_all_users,
    delete_user
)
from core.models import Users
from sqlalchemy.exc import IntegrityError


def save_new_user(self):
    """ Salva o usuário no banco de dados após validar os dados """
    try:
        username = self.new_username_input.text()
        fullname = self.new_fullname_input.text()
        phone = validate_phone(self.new_phone_input.text())
        email = validate_email(self.new_email_input.text())

        password = self.new_password_input.text()
        if not password:
            QMessageBox.warning(
                self,
                "Erro de Validação",
                "A senha não pode estar vazia!"
            )
            return

        if not all([username, fullname, phone, email]):
            QMessageBox.warning(
                self,
                "Erro de Validação",
                "Todos os campos são obrigatórios!"
            )
            return

        access_level = "admin" if self.is_admin_input.isChecked() else "user"

        new_user = Users(
            username=username,
            fullname=fullname,
            phone=phone,
            email=email,
            access_level=access_level
        )

        new_user.set_password(plaintext_password=password)

        try:
            create_user(self.db, new_user)
            
            QMessageBox.information(
                self,
                "Sucesso",
                f"Usuário {username} criado com sucesso!"
            )

            self.new_username_input.clear()
            self.new_fullname_input.clear()
            self.new_phone_input.clear()
            self.new_email_input.clear()
            self.new_password_input.clear()
            self.is_admin_input.setChecked(False)

        except IntegrityError:
            self.db.rollback()
            QMessageBox.critical(
                self,
                "Erro",
                "Usuário não pode ser criado.\n"
                "Usuário, telefone ou email já existem no sistema."
            )
        except Exception as e:
            self.db.rollback()
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao criar usuário: {str(e)}"
            )

    except ValueError as e:
        QMessageBox.warning(
            self,
            "Erro de Validação",
            str(e)
        )


def update_users_table(self):
    """Atualiza a tabela de clientes com os dados mais recentes do banco"""
    users = get_all_users(self.db)
    self.users_table.setRowCount(len(users))

    for row, user in enumerate(users):
        id_item = QTableWidgetItem(str(user.id))
        id_item.setTextAlignment(Qt.AlignCenter)

        username_item = QTableWidgetItem(user.username)
        username_item.setTextAlignment(Qt.AlignCenter)

        fullname_item = QTableWidgetItem(user.fullname)
        fullname_item.setTextAlignment(Qt.AlignCenter)

        phone_item = QTableWidgetItem(str(user.phone))
        phone_item.setTextAlignment(Qt.AlignCenter)

        email_item = QTableWidgetItem(user.email)
        email_item.setTextAlignment(Qt.AlignCenter)

        access_level_item = QTableWidgetItem(user.access_level)
        access_level_item.setTextAlignment(Qt.AlignCenter)


        # Adiciona os itens à tabela
        self.users_table.setItem(row, 0, id_item)
        self.users_table.setItem(row, 1, username_item)
        self.users_table.setItem(row, 2, fullname_item)
        self.users_table.setItem(row, 3, phone_item)
        self.users_table.setItem(row, 4, email_item)
        self.users_table.setItem(row, 5, access_level_item)


def confirm_delete_user(self, id):
    """Confirma e executa a exclusão do usuário"""
    if not id.isdigit():
        QMessageBox.warning(self, "Erro", "O ID deve ser um número válido.")
        return

    user_id = int(id)
    user = self.db.query(Users).filter(Users.id == user_id).first()

    if not user:
        QMessageBox.warning(
            self, "Erro", f"Usuário com ID {user_id} não encontrado."
        )
        return

    confirm = QMessageBox.question(
        self,
        "Confirmação",
        f"Tem certeza que deseja excluir o usuário com ID {user.id} ({user.fullname})?",
        QMessageBox.Yes | QMessageBox.No,
    )

    if confirm == QMessageBox.Yes:
        delete_user(self.db, user_id)
        QMessageBox.information(self, "Sucesso", "Usuário excluído com sucesso.")
        self.delete_user_id_input.clear()
    else:
        QMessageBox.information(
            self, "Cancelado", "Operação de exclusão cancelada."
        )