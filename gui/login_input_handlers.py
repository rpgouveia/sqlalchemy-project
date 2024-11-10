from PySide6.QtWidgets import QMessageBox
from core.models import Users
from sqlalchemy import select


def handle_login(self):
    """Gerencia o processo de login"""
    username = self.username_input.text().strip()
    password = self.password_input.text()

    if not username or not password:
        QMessageBox.warning(
            self,
            "Erro de Login",
            "Por favor, preencha todos os campos.",
            QMessageBox.Ok
        )
        return

    try:
        # Busca o usuário usando a conexão existente
        query_stmt = select(Users).where(Users.username == username)
        user = self.db.scalar(query_stmt)

        if user and user.check_password(password):
            # Login bem sucedido
            self.current_user = user
            self.is_admin = user.access_level == "admin"
            
            welcome_msg = f"Bem-vindo, {user.fullname}!"
            QMessageBox.information(
                self,
                "Login Bem Sucedido",
                welcome_msg,
                QMessageBox.Ok
            )

            # Redireciona baseado no nível de acesso
            if self.is_admin:
                self.stacked_widget.setCurrentIndex(1)
            else:
                self.stacked_widget.setCurrentIndex(5)

            # Limpa os campos de login
            self.username_input.clear()
            self.password_input.clear()

        else:
            QMessageBox.warning(
                self,
                "Erro de Login",
                "Usuário ou senha incorretos.",
                QMessageBox.Ok
            )
            self.password_input.clear()

    except Exception as e:
        QMessageBox.critical(
            self,
            "Erro de Sistema",
            "Ocorreu um erro ao tentar fazer login. Por favor, tente novamente.",
            QMessageBox.Ok
        )
        print(f"Erro de login: {str(e)}")

