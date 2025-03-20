import sys
from PySide6.QtCore import QObject, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QApplication, QMainWindow

from ui_maker import Ui_MainWindow

class MyGuiApp(QObject):
    def __init__(self) -> None:
        self.app =QApplication(sys.argv)
        self.mainWindow = QMainWindow()
        self.uiMaker = Ui_MainWindow()
        self.uiMaker.setupUi(self.mainWindow)

        self.uiMaker.lineEdit.setValidator(QRegularExpressionValidator(regularExpression=QRegularExpression(r"^[0-9()+\-*/]+$")))

        self.uiMaker.sendButton.clicked.connect(self.sendPressed)

    def sendPressed(self):
        if self.isWaitingMode:
            return

        self.setMode(True)

    def run(self):
        self.mainWindow.show()
        self.app.exec()

    def setMode(self, isWaitingMode):
        if isWaitingMode:
            self.uiMaker.sendButton.setEnabled(False)
            self.uiMaker.lineEdit.setEnabled(False)
            self.uiMaker.isFloat.setEnabled(False)
        else:
            self.uiMaker.sendButton.setEnabled(True)
            self.uiMaker.lineEdit.setEnabled(True)
            self.uiMaker.isFloat.setEnabled(True)

    isWaitingMode = False

if __name__ == "__main__":
    app = MyGuiApp()
    app.run()

