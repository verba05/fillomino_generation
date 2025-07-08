import gc

from PySide6.QtCore import QTimer

from views.loading_view import LoadingView


class MenuController:
    def __init__(self, view):
        self.view = view

    def start_button_clicked(self):
        old_view = self.view
        self.view = LoadingView(self.view.board_size_menu.currentIndex(), self.view.max_size_polyomino.currentIndex())
        self.view.move(self.view.pos())
        self.view.resize(self.view.size())
        self.view.show()
        old_view.setParent(None)
        old_view.deleteLater()
        old_view.close()
        del old_view
        gc.collect()

