import sys
import time

from PySide6.QtWidgets import QApplication
from matplotlib.backends.backend_qt import MainWindow

from views.game_board_view import FillominoPuzzleView
from views.menu_view import MenuView
from views.winned_game_view import WinnedGameView

app = QApplication(sys.argv)
app.setApplicationName("FillominoPuzzle")
time0 = time.time()
window = MenuView()
window.show()
time1 = time.time()
print(time1 - time0)
sys.exit(app.exec())