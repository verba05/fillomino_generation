from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QFont
from PySide6.QtWidgets import QLineEdit, QPushButton, QSizePolicy


class BoardCell(QPushButton):
    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column
        self.setFixedSize(40, 40)
        self.setFont(QFont('Arial', 15))
        self.setStyleSheet("""
            border: 1px solid black;
            border-radius: 0px;
            background-color: grey;  
        """)
        self.isActive = False
        self.isLocked = False

    def resizeEvent(self, e):
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)

