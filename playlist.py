from PyQt4 import QtCore

class Playlist(QtCore.QObject):
    currentChanged = QtCore.pyqtSignal()
    newSong = QtCore.pyqtSignal(str) # path to song
    done = QtCore.pyqtSignal()

    def __init__(self):
        super(Playlist, self).__init__()
        self._songs = []
        self._current = 0

    def getSongs(self):
        return self._songs
    def setSongs(self, songs):
        self._songs = songs
        self._current = -1
        self.next()
    songs = property(getSongs, setSongs)

    def getCurrent(self):
        return self._current
    def setCurrent(self, newCurrent):
        self._current = newCurrent
        self.currentChanged.emit()
    current = property(getCurrent, setCurrent)

    def next(self):
        self._current += 1
        if self._current < len(self._songs):
            song = self._songs[self._current]
            self.newSong.emit(song)
        else:
            self.done.emit()
