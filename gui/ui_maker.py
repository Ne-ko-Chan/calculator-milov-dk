# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calculatorGui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 116)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mainTitle = QLabel(self.centralwidget)
        self.mainTitle.setObjectName(u"mainTitle")
        self.mainTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.mainTitle)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.isFloat = QCheckBox(self.centralwidget)
        self.isFloat.setObjectName(u"isFloat")

        self.horizontalLayout.addWidget(self.isFloat)

        self.sendButton = QPushButton(self.centralwidget)
        self.sendButton.setObjectName(u"sendButton")

        self.horizontalLayout.addWidget(self.sendButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.responseLayout = QVBoxLayout()
        self.responseLayout.setObjectName(u"responseLayout")
        self.responseTitle = QLabel(self.centralwidget)
        self.responseTitle.setObjectName(u"responseTitle")
        self.responseTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.responseLayout.addWidget(self.responseTitle)

        self.responseText = QLabel(self.centralwidget)
        self.responseText.setObjectName(u"responseText")

        self.responseLayout.addWidget(self.responseText)


        self.verticalLayout_2.addLayout(self.responseLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440", None))
        self.mainTitle.setText(QCoreApplication.translate("MainWindow", u"TITLE", None))
        self.isFloat.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.sendButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", None))
        self.responseTitle.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0432\u0435\u0442 \u0441\u0435\u0440\u0432\u0435\u0440\u0430", None))
        self.responseText.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

