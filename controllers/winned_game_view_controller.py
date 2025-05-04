
class WinnedGameController:
    def __init__(self, view):
        self.view = view

    def back_to_menu_button_clicked(self):
        from views.menu_view import MenuView
        self.view.main_menu = MenuView()
        self.view.main_menu.move(self.view.pos())
        self.view.main_menu.show()
        self.view.close()