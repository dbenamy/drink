import random
import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

import audio

# When I'm ready to save settings and/or db, create a qt settings object, set the format to ini, save it, get its path, and create a sqlite db in the same dir.
# http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qsettings.html

player = audio.Player()

class MainWindow(QtGui.QMainWindow):
 
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.resize(400, 150)
        self.move(0, 0)
        self.setWindowTitle('Drink')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
 
        self.__nextButton = QtGui.QPushButton('Next', self)
        self.__nextButton.clicked.connect(player.next)
        self.setCentralWidget(self.__nextButton)

        openAction = QtGui.QAction('Open', self)
        openAction.triggered.connect(self.open)
 
        menubar = self.menuBar()
        file = menubar.addAction(openAction)
 
        self.show()

    def open(self):
        try:
            fileNames = QtGui.QFileDialog.getOpenFileNames(
                self, "Open", "/Users/dbenamy/Music", "Mp3 Files (*.mp3)")
            self.__playlist = [str(fn) for fn in fileNames]
            if self.__playlist == []:
                return

            random.shuffle(self.__playlist)
            player.play_files(self.__playlist)
        except Exception, e:
            QtGui.QMessageBox.critical(self, "Open error", e.message)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
