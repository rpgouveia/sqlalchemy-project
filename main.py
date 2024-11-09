import sys
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QStackedWidget,
)
from sqlalchemy.orm import Session
from core.database import connect_db
from sqlalchemy.orm import Session
from gui.interface import (
    create_main_menu,
    create_register_client_page,
    list_all_clients_page,
    retrieve_client_data_page,
    update_client_data_page,
    delete_client_page,
    create_login_page,
    create_admin_menu,
    create_user_page,
    list_users_page,
    delete_user_page
)


class MainWindowApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Programa de Cadastro de Clientes")

        # Configuração inicial
        self.current_user = None
        self.is_admin = False

        try:
            self.db: Session = connect_db()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.db = None

        self.layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.create_all_pages()
        self.setLayout(self.layout)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Sobrescreve o evento de fechamento para garantir que o banco seja desconectado"""
        if self.db:
            self.db.close()
        event.accept()

    def create_all_pages(self):
        """Cria todas as páginas do sistema"""
        # Páginas de autenticação e admin
        create_login_page(self)
        create_admin_menu(self)
        create_user_page(self)
        list_users_page(self)
        delete_user_page(self)
        
        # Páginas do sistema principal
        create_main_menu(self)
        create_register_client_page(self)
        list_all_clients_page(self)
        retrieve_client_data_page(self)
        update_client_data_page(self)
        delete_client_page(self)

    # Funções para mostrar as páginas
    def show_login_page(self):
        """Exibe a página de login"""
        self.current_user = None
        self.is_admin = False
        self.stacked_widget.setCurrentIndex(self.login_page_index)

    def show_admin_menu(self):
        """Exibe o menu de administrador"""
        self.stacked_widget.setCurrentIndex(self.admin_menu_index)

    def show_create_user_page(self):
        """Exibe a página de criação de usuário"""
        self.stacked_widget.setCurrentIndex(self.create_user_index)

    def show_list_users_page(self):
        """Exibe a página de listagem de usuários"""
        self.stacked_widget.setCurrentIndex(self.list_users_index)

    def show_delete_user_page(self):
        """Exibe a página de exclusão de usuário"""
        self.stacked_widget.setCurrentIndex(self.delete_user_index)

    def show_main_menu(self):
        """Exibe o menu principal"""
        self.stacked_widget.setCurrentIndex(self.main_menu_index)

    def show_register_client_page(self):
        """Exibe a página de cadastro de cliente"""
        self.stacked_widget.setCurrentIndex(self.register_client_index)

    def show_list_clients_page(self):
        """Exibe a página de listagem de clientes"""
        # Atualiza a tabela de clientes antes de exibir a página
        list_all_clients_page(self)
        self.stacked_widget.setCurrentIndex(self.list_clients_index)

    def show_retrieve_client_data_page(self):
        """Exibe a página de dados do cliente"""
        self.stacked_widget.setCurrentIndex(self.retrieve_client_data_index)

    def show_update_client_data_page(self):
        """Exibe a página de dados do cliente"""
        self.stacked_widget.setCurrentIndex(self.update_client_data_index)

    def show_delete_client_page(self):
        """Exibe a página de dados do cliente"""
        self.stacked_widget.setCurrentIndex(self.delete_client_index)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindowApp()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
