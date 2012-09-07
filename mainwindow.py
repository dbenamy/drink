import random

from PyQt4 import QtGui
from PyQt4 import QtCore

class MainWindow(QtGui.QMainWindow):
    newPlaylist = QtCore.pyqtSignal(list)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(400, 150)
        self.move(0, 0)
        self.setWindowTitle('Drink')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
 
        self.nextButton = QtGui.QPushButton('Next', self)
        self.setCentralWidget(self.nextButton)

        openAction = QtGui.QAction('Open', self)
        openAction.triggered.connect(self.open)
 
        menubar = self.menuBar()
        file = menubar.addAction(openAction)
 
        self.show()

    def open(self):
        try:
            fileNames = QtGui.QFileDialog.getOpenFileNames(
                self, "Open", "/Users/dbenamy/Music", "Mp3 Files (*.mp3)")
            playlist = [str(fn) for fn in fileNames]
            random.shuffle(playlist)
            self.newPlaylist.emit(playlist)
        except Exception, e:
            QtGui.QMessageBox.critical(self, "Open error", e.message)
