from PySide6.QtWidgets import QMessageBox


def show_register_page_with_permission(self):
    """Verifica permissão antes de mostrar a página de cadastro"""
    if self.access_level == "guest":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Acesso Negado")
        msg.setInformativeText("Você não tem permissão para cadastrar novos clientes. Apenas usuários com nível de acesso 'user' ou 'admin' podem realizar esta operação.")
        msg.setWindowTitle("Erro de Permissão")
        msg.exec_()
    elif self.access_level in ["admin", "user"]:
        self.show_register_client_page()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Erro de Autenticação")
        msg.setInformativeText("Por favor, faça login novamente no sistema.")
        msg.setWindowTitle("Erro")
        msg.exec_()
        self.show_login_page()


def show_update_page_with_permission(self):
    """Verifica permissão antes de mostrar a página de atualização"""
    if self.access_level == "guest":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Acesso Negado")
        msg.setInformativeText("Você não tem permissão para atualizar dados de clientes. Apenas usuários com nível de acesso 'user' ou 'admin' podem realizar esta operação.")
        msg.setWindowTitle("Erro de Permissão")
        msg.exec_()
    elif self.access_level in ["admin", "user"]:
        self.show_update_client_data_page()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Erro de Autenticação")
        msg.setInformativeText("Por favor, faça login novamente no sistema.")
        msg.setWindowTitle("Erro")
        msg.exec_()
        self.show_login_page()


def show_delete_page_with_permission(self):
    """Verifica permissão antes de mostrar a página de exclusão"""
    if self.access_level == "guest":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Acesso Negado")
        msg.setInformativeText("Você não tem permissão para excluir clientes. Apenas usuários com nível de acesso 'user' ou 'admin' podem realizar esta operação.")
        msg.setWindowTitle("Erro de Permissão")
        msg.exec_()
    elif self.access_level in ["admin", "user"]:
        self.show_delete_client_page()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Erro de Autenticação")
        msg.setInformativeText("Por favor, faça login novamente no sistema.")
        msg.setWindowTitle("Erro")
        msg.exec_()
        self.show_login_page()

