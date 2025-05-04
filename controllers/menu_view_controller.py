from PySide6.QtCore import QTimer

from views.loading_view import LoadingView


class MenuController:
    def __init__(self, view):
        self.view = view

    def start_button_clicked(self):
        self.view.loading_view = LoadingView(self.view.board_size_menu.currentIndex())
        self.view.loading_view.move(self.view.pos())
        self.view.loading_view.resize(self.view.size())
        self.view.loading_view.show()
        self.view.close()

