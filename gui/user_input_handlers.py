from PySide6.QtWidgets import (
    QMessageBox,
)
from core.validations import (
    validate_phone,
    validate_email,
)
from core.crud import (
    create_user,
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


def list_users(self):
    ...


def delete_user(self):
    ...