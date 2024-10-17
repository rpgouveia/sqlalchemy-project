import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt

class MainWindowApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programa de Cadastro de Clientes")

        # Sketch for Main Menu
        """
        1 - Cadastrar um novo cliente
        2 - Listar todos os clientes
        3 - Ler um cliente por ID
        4 - Atualizar um cliente por ID
        5 - Deletar um cliente por ID
        6 - Sair do programa
        """

        # Layout
        # Each option change the main window?

        # Connect buttons to functions?

    # Define functions for each option?


# Startup Application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindowApp()
    window.show()

    sys.exit(app.exec())

