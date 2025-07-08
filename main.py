import sys
import time
from PySide6.QtWidgets import QApplication
from views.menu_view import MenuView

app = QApplication(sys.argv)
app.setApplicationName("FillominoPuzzle")
time0 = time.time()
window = MenuView()
window.show()
time1 = time.time()
print(time1 - time0)
sys.exit(app.exec())
