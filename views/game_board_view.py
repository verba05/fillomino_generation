from PySide6.QtGui import QKeyEvent, Qt
from PySide6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,
)

from controllers.game_board_view_controller import GameBoardController
from widgets.board_cell import BoardCell
from widgets.number_selection_cell import NumberSelectionCell


class FillominoPuzzleView(QWidget):
    def __init__(self, max_i, max_j):
        super().__init__()

        self.controller = GameBoardController(self, max_i, max_j)
        self.setWindowTitle("Fillomino Puzzle")

        self.window_layout = QVBoxLayout()
        self.board_layout = QGridLayout()
        self.board_layout.setSpacing(0)

        self.cells = []

        for i in range(max_i):
            for j in range(max_j):
                cell = BoardCell(j, i)
                self.board_layout.addWidget(cell, i, j)
                self.cells.append(cell)
                cell.clicked.connect(lambda checked, cell_index = i * max_j + j : self.controller.boardCellClickedHandler(cell_index))


        self.selection_number_buttons = []

        self.number_selection_layout = QHBoxLayout()
        self.number_selection_layout.setSpacing(0)
        self.number_selection_layout.setContentsMargins(0, 0, 0, 0)
        for i in range(2, 10):
            button = NumberSelectionCell()
            button.setText(str(i))
            button.clicked.connect(lambda checked, number = i : self.controller.numberSelectionChangeHandler(number))
            spacing = (max_j - 8) / 2
            self.number_selection_layout.addWidget(button)
            self.selection_number_buttons.append(button)

        self.window_layout.addLayout(self.board_layout)
        self.window_layout.addLayout(self.number_selection_layout)



        self.controller.generate_board()
        self.selection_number_buttons[0].changeState()
        self.setFixedSize(self.sizeHint())

        self.clear_errors_button = QPushButton("Clear Errors")
        self.clear_errors_button.clicked.connect(self.controller.clear_errors_button_clicked)
        self.window_layout.addWidget(self.clear_errors_button, alignment=Qt.AlignLeft)
        self.setLayout(self.window_layout)



    def keyPressEvent(self, event: QKeyEvent):
        if event.text() not in ("0", "1"):
            self.controller.numberSelectionChangeHandler(int(event.text()))

