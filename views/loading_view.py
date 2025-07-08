from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from controllers.loading_view_controller import LoadingViewController


class LoadingView(QWidget):
    def __init__(self, size_index, polyomino_size_index):
        super().__init__()
        self.controller = LoadingViewController(self, size_index, polyomino_size_index)
        loading_message = QLabel("Loading...")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(loading_message)
        self.setLayout(layout)
        self.setFixedSize(300, 300)

        QTimer.singleShot(100, self.controller.start_board_generation)

