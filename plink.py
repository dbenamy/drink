# from multiprocessing import freeze_support, Process
import random
import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

import audio

# When I'm ready to save settings and/or db, create a qt settings object, set the format to ini, save it, get its path, and create a sqlite db in the same dir.
# http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qsettings.html

hidden_window = None
window = None
fileName = ""
# player_proc = None
player = audio.Player()


class MainWindow(QtGui.QMainWindow):
 
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.resize(400, 150)
        self.move(0, 0)
        self.setWindowTitle('Plink')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
 
        self.__nextButton = QtGui.QPushButton('Next', self)
        self.__nextButton.clicked.connect(self.next)
        self.setCentralWidget(self.__nextButton)

        openAction = QtGui.QAction('Open', self)
        openAction.triggered.connect(self.open)
 
        menubar = self.menuBar()
        file = menubar.addAction(openAction)
 
        self.minimizing = False

        self.show()

    def open(self):
        global player
        try:
            fileNames = QtGui.QFileDialog.getOpenFileNames(
                self, "Open", "/Users/dbenamy/Music", "Mp3 Files (*.mp3)")
            self.__playlist = [str(fn) for fn in fileNames]
            if self.__playlist == []:
                return

            random.shuffle(self.__playlist)

            # if player_proc:
            #     player_proc.terminate()
            # player_proc = Process(target=audio.play_files, args=(self.__playlist,))
            # player_proc.start()
            player.play_files(self.__playlist)
        except Exception, e:
            QtGui.QMessageBox.critical(self, "Open error", e.message)

    def next(self, event):
        player.next()

    def changeEvent(self, event):
        if (event.type() == QtCore.QEvent.WindowStateChange and
            self.windowState() & QtCore.Qt.WindowMinimized):
            self.minimizing = True
            self.close()
        QtGui.QWidget.changeEvent(self, event)

    def closeEvent(self, event):
        if self.minimizing:
            window = None
        else:
            QtCore.QCoreApplication.instance().quit()


class Tray:

    def __init__(self, parent):
        self.sysTray = QtGui.QSystemTrayIcon(parent=parent)
        self.sysTray.setIcon(QtGui.QIcon('icon.png'))
        self.sysTray.setVisible(True)
        window.connect(self.sysTray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.sysTrayClicked)

    def sysTrayClicked(self, reason):
        global window
        if window is None:
            window = MainWindow(parent=hidden_window)


if __name__ == '__main__':
    # freeze_support() # needed for py2exe

    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    global hidden_window, window, tray #, player_proc
    hidden_window = QtGui.QMainWindow()
    window = MainWindow(parent=hidden_window)
    tray = Tray(parent=hidden_window)
 
    ret = app.exec_()
    # if player_proc:
    #     player_proc.terminate()
    sys.exit(ret)
