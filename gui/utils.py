from PySide6.QtWidgets import QLineEdit


def toggle_password_visibility(self):
    if self.new_password_input.echoMode() == QLineEdit.Password:
        self.new_password_input.setEchoMode(QLineEdit.Normal)
    else:
        self.new_password_input.setEchoMode(QLineEdit.Password)

