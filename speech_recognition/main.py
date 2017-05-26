import sys
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui_mainwin import Ui_MainWindow
from worker import RecThread, GoogleSTTThread

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        self._recoding = False
        self._translate = QCoreApplication.translate
        self._speechRecWorker = RecThread()
        self._speechRecWorker.speechReady.connect(self.recordReady)

        self._speechRegWorker = GoogleSTTThread()
        self._speechRegWorker.textReady.connect(self.sttReady)

    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            return

        if e.key() == Qt.Key_R and not self._recoding:
            self.pbRecord.setText(self._translate("MainWindow", "Recording"))
            self._recoding = True
            self.pteDebug.appendPlainText('recoding is activated')
            self._speechRecWorker.record()
            e.accept()
        else:
            super(MainWindow, self).keyPressEvent(e)

    @pyqtSlot(str)
    def recordReady(self, filename):
        self.pteDebug.appendPlainText('sound is recorded to {}'.format(filename))
        self._recoding = False
        self.pbRecord.setText(self._translate("MainWindow", "Record"))

        # trigger goolge Speech-2-Text
        self._speechRegWorker.speechToText(filename, self._speechRecWorker.encoding)

    @pyqtSlot(list)
    def sttReady(self, texts):
        self.teSTT.clear()
        self.teSTT.append('Speech To Text:')
        for text in texts:
            self.teSTT.append(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())