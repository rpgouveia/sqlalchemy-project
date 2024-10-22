import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hello World", "Olá Mundo", "Hallo Welt", "Salut Monde", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
    
    def closeEvent(self, event):
        print("Fechando a janela.")
        # Verifica se há algum processo em segundo plano
        # ...
        # Fecha todos os arquivos e conexões
        # ...
        event.accept()  # Permite que a janela seja fechada


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    # Conectar um sinal ao evento de fechamento
    app.aboutToQuit.connect(lambda: print("Fechando aplicação..."))

    # Executar o loop principal da aplicação
    sys.exit(app.exec())