import sys
from PySide6.QtWidgets import QApplication
from views.menu_view import MenuView

app = QApplication(sys.argv)
app.setApplicationName("FillominoPuzzle")
window = MenuView()
window.show()
sys.exit(app.exec())
