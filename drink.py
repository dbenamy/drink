import logging
import sys

from PyQt4 import QtGui

import audio
from db import DB
from dirwatcher import DirWatcher
from mainwindow import MainWindow
from playlist import Playlist

MUSIC_DIR = '/Users/dbenamy/Music'

class DrinkApp(QtGui.QApplication):
    def __init__(self, argv):
        super(DrinkApp, self).__init__(argv)
        
        self.__window = MainWindow(MUSIC_DIR)
        self.__player = audio.Player()
        self.__dirWatcher = DirWatcher(MUSIC_DIR)
        self.__db = DB()

        self.__player.songDone.connect(lambda: logging.debug('player song done'))
        self.__window.playSong.connect(lambda path: logging.debug('window play song %s' % path))
        self.__window.controls.playButton.clicked.connect(lambda: logging.debug('window play'))
        self.__window.controls.nextButton.clicked.connect(lambda: logging.debug('window next'))

        self.__player.songDone.connect(self.playNextRandSong)
        self.__window.playSong.connect(self.__player.play_file)
        self.__window.controls.playButton.clicked.connect(self.playNextRandSong)
        self.__window.controls.nextButton.clicked.connect(self.playNextRandSong)

    def playNextRandSong(self):
        self.__player.play_file(self.__db.randSong())

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = DrinkApp(sys.argv)
    sys.exit(app.exec_())
