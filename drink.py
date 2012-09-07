import logging
import sys
import time

from PyQt4 import QtCore, QtGui

import audio
from db import DB
from dirwatcher import DirWatcher
from mainwindow import MainWindow
from playlist import Playlist

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = QtGui.QApplication(sys.argv)
    
    window = MainWindow()
    playlist = Playlist()
    player = audio.Player()
    dirWatcher = DirWatcher('/Users/dbenamy/Music')
    db = DB()

    if db.numSongs() == 0:
        print("There are no songs in the database. We'll wait 1/2 a sec to see "
              "if some show up so we can play them.")
        time.sleep(0.5)

    playlist.newSong.connect(lambda song: logging.debug('playlist new song %s' % song))
    playlist.done.connect(lambda: logging.debug('playlist done'))
    player.songDone.connect(lambda: logging.debug('player song done'))
    window.newPlaylist.connect(lambda songs: logging.debug('window new playlist %s' % songs))
    window.controls.nextButton.clicked.connect(lambda: logging.debug('window next'))
    window.controls.playButton.clicked.connect(lambda: logging.debug('window play'))

    playlist.newSong.connect(player.play_file)
    playlist.done.connect(player.stop)
    player.songDone.connect(playlist.next)
    window.newPlaylist.connect(playlist.setSongs)
    window.controls.nextButton.clicked.connect(playlist.next)
    # TODO rand "playlist"
    window.controls.playButton.clicked.connect(lambda: player.play_file(db.randSong()))

    ret = app.exec_()
    sys.exit(ret)
