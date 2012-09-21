#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals
import logging
import os
from os.path import expanduser
import sys

from PyQt4.QtGui import QApplication, QMessageBox
from PyQt4.QtCore import QSettings

# import audiopymedia as audio It's less well supported but I'm hanging on to it until I'm sure that phonon works well.
import audiophonon as audio
from db import DB
from indexer import Indexer
from mainwindow import MainWindow

class DrinkApp(QApplication):
    def __init__(self, argv):
        super(DrinkApp, self).__init__(argv)
        
        self.__settings = QSettings(QSettings.IniFormat, QSettings.UserScope,
                                    "Drink", "Drink")
        musicDir = self.__settings.value('MusicDir')
        if musicDir is None:
            musicDir = expanduser('~/Music')
            self.__settings.setValue('MusicDir', musicDir)
            self.__settings.sync()

        # Settings must be sync()ed so on 1st run, settings dir is created before setting up db.
        settingsDir = os.path.dirname(str(self.__settings.fileName()))
        dbPath = os.path.join(settingsDir, 'Drink Audio.sqlite')

        self.__window = MainWindow(musicDir)
        self.__player = audio.Player()
        self.__dirWatcher = Indexer(musicDir)
        self.__db = DB(dbPath)

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
            time.sleep(0.2) # Give indexer a chance to add songs to db.
            song = self.__db.randSong()
        if song is None:
            QMessageBox.critical(
                self.__window, "No songs",
                "Drink doesn't know about your music. Make sure the "
                "'music dir' setting in '%s' is set right." %
                str(self.__settings.fileName()))
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
