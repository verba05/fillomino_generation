import sys

from PySide6.QtWidgets import QApplication

from views.game_board_view import FillominoPuzzle

app = QApplication(sys.argv)
window = FillominoPuzzle(10, 10)
window.show()
sys.exit(app.exec())
