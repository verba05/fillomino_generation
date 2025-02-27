from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt, QSize

from controllers.game_board_controller import GameBoardController
from widgets.custom_cell import CustomCell


class FillominoPuzzle(QWidget):
    def __init__(self, max_i, max_j):
        super().__init__()

        self.controller = GameBoardController(self, max_i, max_j)
        self.setWindowTitle("Fillomino Puzzle")
        self.setFixedSize(QSize(400, 400))

        self.game_board_layout = QGridLayout()
        self.game_board_layout.setContentsMargins(0, 0, 0, 0)

        self.cells = []

        for i in range(max_i):
            for j in range(max_j):
                cell = CustomCell(j, i)
                self.game_board_layout.addWidget(cell, i, j)
                self.cells.append(cell)

        self.setLayout(self.game_board_layout)

        self.controller.generate_board()


