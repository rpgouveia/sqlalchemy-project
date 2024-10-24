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
)


class MainWindowApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Programa de Cadastro de Clientes")

        # Conexão ao banco de dados
        try:
            self.db: Session = connect_db()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.db = None

        # Configuração do layout principal
        self.layout = QVBoxLayout()

        # Criando um widget empilhado para navegação entre telas
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Criar as páginas (Menu Principal e as demais opções)
        create_main_menu(self)
        create_register_client_page(self)
        list_all_clients_page(self)
        retrieve_client_data_page(self)
        update_client_data_page(self)
        delete_client_page(self)

        # Definir o layout da janela principal
        self.setLayout(self.layout)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Sobrescreve o evento de fechamento para garantir que o banco seja desconectado"""
        if self.db:
            self.db.close()
        event.accept()

    # Funções para mostrar as páginas
    def show_main_menu(self):
        """Exibe o menu principal"""
        self.stacked_widget.setCurrentIndex(0)

    def show_register_client_page(self):
        """Exibe a página de cadastro de cliente"""
        self.stacked_widget.setCurrentIndex(1)

    def show_list_clients_page(self):
        """Exibe a página de listagem de clientes"""
        # Atualiza a tabela de clientes antes de exibir a página
        list_all_clients_page(self)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.list_page))

    def show_retrieve_client_data_page(self):
        """Exibe a página de dados do cliente"""
        self.stacked_widget.setCurrentIndex(3)

    def show_update_client_data_page(self):
        """Exibe a página de dados do cliente"""
        self.stacked_widget.setCurrentIndex(4)

    def show_delete_client_page(self):
        """Exibe a página de dados do cliente"""
        self.stacked_widget.setCurrentIndex(5)


# Startup Application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindowApp()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
