#!/usr/bin/env python

import logging
import sys

from PyQt4 import QtGui

# import audiopymedia as audio It's less well supported but I'm hanging on to it until I'm sure that phonon works well.
import audiophonon as audio
from db import DB
from dirwatcher import DirWatcher
from mainwindow import MainWindow

MUSIC_DIR = '/home/dbenamy/Music'

class DrinkApp(QtGui.QApplication):
    def __init__(self, argv):
        super(DrinkApp, self).__init__(argv)
        
        self.__window = MainWindow(MUSIC_DIR)
        self.__player = audio.Player()
        self.__dirWatcher = DirWatcher(MUSIC_DIR)
        self.__db = DB()

        self.__player.songDone.connect(lambda: logging.debug('player song done'))
        self.__window.playSong.connect(lambda path: logging.debug('window play song %s' % path))
        self.__window.controls.playPauseButton.clicked.connect(lambda: logging.debug('window play'))
        self.__window.controls.nextButton.clicked.connect(lambda: logging.debug('window next'))

        self.__player.songDone.connect(self.playNextRandSong)
        self.__window.playSong.connect(self.__player.playFile)
        self.__window.controls.playPauseButton.clicked.connect(self.playNextRandSong)
        self.__window.controls.nextButton.clicked.connect(self.playNextRandSong)

    def playNextRandSong(self):
        self.__player.playFile(self.__db.randSong())

if __name__ == '__main__':
    logging.basicConfig(level=(logging.DEBUG if '-v' in sys.argv else logging.INFO))
    app = DrinkApp(sys.argv)
    sys.exit(app.exec_())
