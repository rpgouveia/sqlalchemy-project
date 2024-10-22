import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt

class SetOperationsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Set Operations Interface')

        # Widgets creation
        self.setA_label = QLabel('Enter Set A:')
        self.setA_input = QLineEdit(self)

        self.setB_label = QLabel('Enter Set B:')
        self.setB_input = QLineEdit(self)

        self.union_button = QPushButton('Union')
        self.intersection_button = QPushButton('Intersection')
        self.difference_button = QPushButton('Difference')

        self.result_label = QLabel('Result:')
        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.setA_label)
        layout.addWidget(self.setA_input)
        layout.addWidget(self.setB_label)
        layout.addWidget(self.setB_input)
        layout.addWidget(self.union_button)
        layout.addWidget(self.intersection_button)
        layout.addWidget(self.difference_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

        # Connect buttons to functions
        self.union_button.clicked.connect(self.perform_union)
        self.intersection_button.clicked.connect(self.perform_intersection)
        self.difference_button.clicked.connect(self.perform_difference)

    # Operation functions
    def get_sets(self):
        setA = set(self.setA_input.text().split(','))
        setB = set(self.setB_input.text().split(','))
        return setA, setB

    def perform_union(self):
        setA, setB = self.get_sets()
        result = setA.union(setB)
        self.result_display.setText(f'Union: {result}')

    def perform_intersection(self):
        setA, setB = self.get_sets()
        result = setA.intersection(setB)
        self.result_display.setText(f'Intersection: {result}')

    def perform_difference(self):
        setA, setB = self.get_sets()
        result = setA.difference(setB)
        self.result_display.setText(f'Difference: {result}')

# Application initialization
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = SetOperationsApp()
    window.show()

    sys.exit(app.exec())
