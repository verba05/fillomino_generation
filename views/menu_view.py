from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QLabel, QPushButton, QVBoxLayout, QApplication

from controllers.menu_view_controller import MenuController


class MenuView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = MenuController(self)
        self.board_size_menu = QComboBox()
        self.board_size_menu_label = QLabel("Board size:")
        self.board_size_menu.addItems(["5x10", "8x8", "10x10", "12x12"])
        self.exit_button = QPushButton("Exit")
        layout = QVBoxLayout()
        center_layout = QVBoxLayout()
        layout.addWidget(self.exit_button, alignment=Qt.AlignRight)
        center_layout.addWidget(self.board_size_menu_label, alignment=Qt.AlignCenter)
        center_layout.addWidget(self.board_size_menu, alignment=Qt.AlignCenter)
        center_layout.setSpacing(0)
        center_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(center_layout)
        self.start_button = QPushButton("Start")
        layout.addWidget(self.start_button, alignment=Qt.AlignRight)
        layout.setSpacing(8)
        self.setLayout(layout)
        self.setFixedSize(300, 300)

        self.start_button.clicked.connect(self.controller.start_button_clicked)
        self.exit_button.clicked.connect(QApplication.instance().quit)


