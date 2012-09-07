import logging
import sys

from PyQt4 import QtGui

import audio
from db import DB
from dirwatcher import DirWatcher
from mainwindow import MainWindow
from playlist import Playlist

class DrinkApp(QtGui.QApplication):
    def __init__(self, argv):
        super(DrinkApp, self).__init__(argv)
        
        self.__window = MainWindow()
        self.__player = audio.Player()
        self.__dirWatcher = DirWatcher('/Users/dbenamy/Music')
        self.__db = DB()

        self.__player.songDone.connect(lambda: logging.debug('player song done'))
        self.__window.newPlaylist.connect(lambda songs: logging.debug('window new playlist %s' % songs))
        self.__window.controls.playButton.clicked.connect(lambda: logging.debug('window play'))
        self.__window.controls.nextButton.clicked.connect(lambda: logging.debug('window next'))

        self.__player.songDone.connect(self.playNextRandSong)
        self.__window.controls.playButton.clicked.connect(self.playNextRandSong)
        self.__window.controls.nextButton.clicked.connect(self.playNextRandSong)

    def playNextRandSong(self):
        self.__player.play_file(self.__db.randSong())

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = DrinkApp(sys.argv)
    sys.exit(app.exec_())
