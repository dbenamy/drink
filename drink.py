#!/usr/bin/python

import logging
import sys

from PyQt4.QtGui import QApplication, QMessageBox

# import audiopymedia as audio It's less well supported but I'm hanging on to it until I'm sure that phonon works well.
import audiophonon as audio
from db import DB
from indexer import Indexer
from mainwindow import MainWindow

MUSIC_DIR = u'/Users/dbenamy/Music'

class DrinkApp(QApplication):
    def __init__(self, argv):
        super(DrinkApp, self).__init__(argv)
        
        self.__window = MainWindow(MUSIC_DIR)
        self.__player = audio.Player()
        self.__dirWatcher = Indexer(MUSIC_DIR)
        self.__db = DB()

        self.__player.songDone.connect(lambda: logging.debug('player song done'))
        self.__window.playSong.connect(lambda path: logging.debug('window play song %s' % path))
        self.__window.controls.playPauseButton.clicked.connect(lambda: logging.debug('window play'))
        self.__window.controls.nextButton.clicked.connect(lambda: logging.debug('window next'))

        self.__player.songDone.connect(self.playNextRandSong)
        self.__window.playSong.connect(self.__player.playFile)
        self.__window.controls.playPauseButton.clicked.connect(self.playNextRandSong)
        self.__window.controls.nextButton.clicked.connect(self.playNextRandSong)
        self.__dirWatcher.foundSongs.connect(self.foundSongs)

    def playNextRandSong(self):
        song = self.__db.randSong()
        if song is None:
            time.sleep(0.1) # Give indexer a chance to add songs to db.
            song = self.__db.randSong()
        if song is None:
            QMessageBox.critical(
                self.__window, "No songs",
                "Drink doesn't know about your music. Make sure the MUSIC_DIR "
                "variable in drink.py is set right.")
            return
        self.__player.playFile(song)

    def foundSongs(self, pathList):
        for path in pathList:
            try:
                self.__db.addSong(path)
            except:
                logging.exception("Skipping %s" % path)
        self.__db.commit()
        logging.info("%s songs in db" % self.__db.numSongs())


if __name__ == '__main__':
    logging.basicConfig(level=(logging.DEBUG if '-v' in sys.argv else logging.INFO))
    app = DrinkApp(sys.argv)
    sys.exit(app.exec_())
