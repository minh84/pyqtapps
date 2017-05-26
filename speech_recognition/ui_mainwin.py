# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 10, 381, 201))
        self.widget.setObjectName("widget")
        self.pteDebug = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.pteDebug.setGeometry(QtCore.QRect(410, 10, 381, 201))
        self.pteDebug.setReadOnly(True)
        self.pteDebug.setObjectName("pteDebug")
        self.teSTT = QtWidgets.QTextEdit(self.centralwidget)
        self.teSTT.setGeometry(QtCore.QRect(20, 220, 771, 191))
        self.teSTT.setReadOnly(True)
        self.teSTT.setObjectName("teSTT")
        self.lRecord = QtWidgets.QLabel(self.centralwidget)
        self.lRecord.setGeometry(QtCore.QRect(330, 420, 141, 21))
        self.lRecord.setAlignment(QtCore.Qt.AlignCenter)
        self.lRecord.setObjectName("lRecord")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Speech To Text"))
        self.lRecord.setText(_translate("MainWindow", "To Record Press R"))

