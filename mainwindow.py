import random

from PyQt4 import QtGui
from PyQt4 import QtCore

class Controls(QtGui.QWidget):
    def __init__(self, parent):        
        super(Controls, self).__init__(parent)
        self.layout = QtGui.QHBoxLayout(self)

        self.playButton = QtGui.QPushButton('Play', self)
        self.layout.addWidget(self.playButton)

        self.nextButton = QtGui.QPushButton('Next', self)
        self.layout.addWidget(self.nextButton)


class MainWindow(QtGui.QMainWindow):
    playSong = QtCore.pyqtSignal(str) # arg is path to file

    def __init__(self, music_dir):
        super(MainWindow, self).__init__()

        self.__music_dir = music_dir

        self.resize(400, 150)
        self.move(0, 0)
        self.setWindowTitle('Drink')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
 
        openAction = QtGui.QAction('Open', self)
        openAction.triggered.connect(self.open)
 
        menubar = self.menuBar()
        file = menubar.addAction(openAction)

        self.controls = Controls(self)
        self.setCentralWidget(self.controls)
 
        self.show()

    def open(self):
        try:
            fileName = QtGui.QFileDialog.getOpenFileName(
                self, "Open", self.__music_dir, "Mp3 Files (*.mp3)")
            self.playSong.emit(fileName)
        except Exception, e:
            QtGui.QMessageBox.critical(self, "Open error", e.message)
