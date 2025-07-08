import gc
from views.game_board_view import FillominoPuzzleView

class LoadingViewController:
    def __init__(self, view, board_index, max_polyomino_size_index):
        self.view = view
        self.board_index = board_index
        self.max_polyomino_size_index = max_polyomino_size_index

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
        if self.max_polyomino_size_index == 0:
            max_k = 6
        elif self.max_polyomino_size_index == 1:
            max_k = 7
        elif self.max_polyomino_size_index == 2:
            max_k = 8
        elif self.max_polyomino_size_index == 3:
            max_k = 9

        old_view = self.view
        self.view = FillominoPuzzleView(max_i, max_j, max_k)
        self.view.move(old_view.pos())
        self.view.show()
        old_view.setParent(None)
        old_view.deleteLater()
        old_view.close()
        del old_view
        gc.collect()



