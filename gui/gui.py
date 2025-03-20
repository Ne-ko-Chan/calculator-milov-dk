import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from ui_maker import Ui_MainWindow


app = QApplication(sys.argv)
mainWindow = QMainWindow()
uiMaker = Ui_MainWindow()
uiMaker.setupUi(mainWindow)
mainWindow.show()
app.exec()
