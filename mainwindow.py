import random

from PyQt4.QtGui import (
    QWidget, QHBoxLayout, QPushButton, QMainWindow, QIcon, QAction, QShortcut,
    QKeySequence, QFileDialog, QMessageBox)
from PyQt4 import QtCore

class Controls(QWidget):
    def __init__(self, parent):        
        super(Controls, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.openButton = QPushButton('Open', self)
        self.layout.addWidget(self.openButton)

        self.playPauseButton = QPushButton('Play', self) # TODO implement pausing
        self.layout.addWidget(self.playPauseButton)

        self.nextButton = QPushButton('Next', self)
        self.layout.addWidget(self.nextButton)
        
        self.__nextShortcut = QShortcut(QKeySequence.MoveToNextChar, self)
        self.__nextShortcut.activated.connect(self.nextButton.click)

        self.__playPauseShortcut = QShortcut(QKeySequence.fromString(' '), self)
        self.__playPauseShortcut.activated.connect(self.playPauseButton.click)


class MainWindow(QMainWindow):
    playSong = QtCore.pyqtSignal(str) # arg is path to file

    def __init__(self, music_dir):
        super(MainWindow, self).__init__()

        self.__music_dir = music_dir

        self.resize(400, 70)
        self.move(0, 0)
        self.setWindowTitle('Drink')
        self.setWindowIcon(QIcon('icon.png'))
 
        self.controls = Controls(self)
        self.setCentralWidget(self.controls)

        self.controls.openButton.clicked.connect(self.open)

        self.show()

    def open(self):
        try:
            fileName = QFileDialog.getOpenFileName(
                self, "Open", self.__music_dir, "Mp3 Files (*.mp3)")
            self.playSong.emit(fileName)
        except Exception, e:
            QMessageBox.critical(self, "Open error", e.message)
