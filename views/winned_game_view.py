from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton

from controllers.winned_game_view_controller import WinnedGameController


class WinnedGameView(QWidget):
    def __init__(self, time):
        super().__init__()
        self.controller = WinnedGameController(self)
        self.win_msg = QLabel()
        self.win_msg.setAlignment(Qt.AlignCenter)
        self.win_msg.setText("Congratulations, you won!")
        self.time_msg = QLabel()
        self.time_msg.setText("Your time: {:.2f} seconds".format(time))
        self.time_msg.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.win_msg)
        layout.addWidget(self.time_msg)
        self.back_to_menu_button = QPushButton("Back to menu")
        self.back_to_menu_button.clicked.connect(self.controller.back_to_menu_button_clicked)
        layout.addWidget(self.back_to_menu_button)
        self.setLayout(layout)





