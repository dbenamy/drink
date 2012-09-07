import logging
import sys

from PyQt4 import QtGui

import audio
from mainwindow import MainWindow
from playlist import Playlist

# When I'm ready to save settings and/or db, create a qt settings object, set the format to ini, save it, get its path, and create a sqlite db in the same dir.
# http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qsettings.html

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = QtGui.QApplication(sys.argv)
    
    window = MainWindow()
    playlist = Playlist()
    player = audio.Player()

    playlist.newSong.connect(lambda song: logging.debug('playlist new song %s' % song))
    playlist.done.connect(lambda: logging.debug('playlist done'))
    player.songDone.connect(lambda: logging.debug('player song done'))
    window.newPlaylist.connect(lambda songs: logging.debug('window new playlist %s' % songs))
    window.nextButton.clicked.connect(lambda: logging.debug('window next'))

    playlist.newSong.connect(player.play_file)
    playlist.done.connect(player.stop)
    player.songDone.connect(playlist.next)
    window.newPlaylist.connect(playlist.setSongs)
    window.nextButton.clicked.connect(playlist.next)

    ret = app.exec_()
    sys.exit(ret)
