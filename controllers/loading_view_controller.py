from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout

from views.game_board_view import FillominoPuzzleView


class LoadingViewController:
    def __init__(self, view, board_index):
        self.view = view
        self.board_index = board_index

    def start_board_generation(self):
        if self.board_index == 0:
            max_i = 5
            max_j = 10
        elif self.board_index == 1:
            max_i = 8
            max_j = 8
        elif self.board_index == 2:
            max_i = 10
            max_j = 10
        else:
            max_i = 12
            max_j = 12


        self.view.game_view = FillominoPuzzleView(max_i, max_j)
        self.view.game_view.move(self.view.pos())
        self.view.game_view.show()
        self.view.close()



