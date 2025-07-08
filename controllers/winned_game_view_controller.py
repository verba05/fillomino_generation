import gc

class WinnedGameController:
    def __init__(self, view):
        self.view = view

    def back_to_menu_button_clicked(self):
        from views.menu_view import MenuView
        old_view = self.view
        self.view = MenuView()
        self.view.move(self.view.pos())
        self.view.show()
        old_view.setParent(None)
        old_view.deleteLater()
        old_view.close()
        del old_view
        gc.collect()