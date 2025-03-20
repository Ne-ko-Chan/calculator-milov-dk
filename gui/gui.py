import sys
import http.client

from PySide6.QtCore import QObject, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QApplication, QMainWindow

from ui_maker import Ui_MainWindow


class MyGuiApp(QObject):
    def __init__(self, address, port) -> None:
        self.address = address
        self.port = port
        self.conn = http.client.HTTPConnection(self.address, self.port, timeout=1)
        self.app = QApplication(sys.argv)
        self.mainWindow = QMainWindow()
        self.uiMaker = Ui_MainWindow()
        self.uiMaker.setupUi(self.mainWindow)

        self.uiMaker.lineEdit.setValidator(
            QRegularExpressionValidator(
                regularExpression=QRegularExpression(r"^[0-9()+\-*/]+$")
            )
        )

        self.uiMaker.sendButton.clicked.connect(self.sendPressed)
        self.uiMaker.lineEdit.returnPressed.connect(self.sendPressed)

    def sendPressed(self):
        if self.isWaitingMode:
            return

        self.setMode(True)
        self.sendRequest(self.uiMaker.lineEdit.text(), 3000)
        self.setMode(False)

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

    def sendRequest(self, string: str, timeout):
        try:
            self.conn.request(
                "POST",
                "/calc",
                body='"' + string + '"',
                headers={"Content-Type": "application/json"},
            )
            response = self.conn.getresponse()
            responseBytes = response.read()
            self.uiMaker.responseText.setText(responseBytes.decode("utf-8").strip('"'))
            self.conn.close()
        except Exception as e:
            print(e)

    isWaitingMode = False


if __name__ == "__main__":
    app = MyGuiApp("localhost", 8000)
    app.run()
