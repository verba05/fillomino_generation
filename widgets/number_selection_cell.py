from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPushButton, QSizePolicy


class NumberSelectionCell(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(40, 40)
        self.setFont(QFont('Arial', 15))
        self.setStyleSheet("""
            background-color: yellow;
            border: 2px solid black;
            border-radius: 0px;  
            color: black; 
        """)
        self.selected = False


    def resizeEvent(self, e):
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)

    def changeState(self):
        self.selected = not self.selected
        if self.selected:
            self.setStyleSheet("""
            background-color: red;
            border: 2px solid black;
            color: white; 
        """)
        else:
            self.setStyleSheet("""
            background-color: yellow;
            border: 2px solid black;
            color: black; 
        """)







