from PySide6.QtWidgets import QMessageBox


def check_permission(self, required_level, success_callback, access_denied_message):
    """Verifica permissão e exibe a página se permitido, ou mostra mensagem de erro."""
    if self.access_level == "guest":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Acesso Negado!")
        msg.setInformativeText(access_denied_message)
        msg.setWindowTitle("Erro de Permissão")
        msg.exec()
    elif self.access_level in required_level:
        success_callback()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Erro de Autenticação")
        msg.setInformativeText("Por favor, faça login novamente no sistema.")
        msg.setWindowTitle("Erro")
        msg.exec()
        self.show_login_page()

message = (
    "Você não tem permissão para cadastrar novos clientes.\n\n"
    "Apenas usuários com nível de acesso 'user' ou 'admin' "
    "podem realizar esta operação."
)

def show_register_page_with_permission(self):
    """Verifica permissão antes de mostrar a página de cadastro"""
    check_permission(
        self,
        required_level=["admin", "user"],
        success_callback=self.show_register_client_page,
        access_denied_message=message
    )

def show_update_page_with_permission(self):
    """Verifica permissão antes de mostrar a página de atualização"""
    check_permission(
        self,
        required_level=["admin", "user"],
        success_callback=self.show_update_client_data_page,
        access_denied_message=message
    )

def show_delete_page_with_permission(self):
    """Verifica permissão antes de mostrar a página de exclusão"""
    check_permission(
        self,
        required_level=["admin", "user"],
        success_callback=self.show_delete_client_page,
        access_denied_message=message
    )
