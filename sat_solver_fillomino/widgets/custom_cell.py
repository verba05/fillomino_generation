from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLineEdit


class CustomCell(QLineEdit):
    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

        self.setValidator(QIntValidator(1, 8))
        self.setStyleSheet("QLineEdit { background-color: rgba(255, 255, 255, 128); }")


