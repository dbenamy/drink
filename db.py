import os
import sqlite3

from PyQt4 import QtCore

class DB():
    def __init__(self):
        settings = QtCore.QSettings(QtCore.QSettings.IniFormat,
                                    QtCore.QSettings.UserScope,
                                    "Daniel Benamy", "Drink")
        settings.setValue('dummy', 0)
        settings.sync() # Ensure settings dir is created.
        settingsDir = os.path.dirname(str(settings.fileName()))
        dbPath = os.path.join(settingsDir, 'Drink Audio.sqlite')
        self.__conn = sqlite3.connect(dbPath)
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS songs (path text unique);')

    def commit(self):
        self.__conn.commit()

    def numSongs(self):
        self.__cursor.execute('SELECT COUNT(*) FROM songs;')
        return self.__cursor.fetchone()[0]

    def addSong(self, path):
        try:
            self.__cursor.execute('INSERT INTO songs (path) VALUES (?);', (path,))
        except sqlite3.IntegrityError, error:
            if 'column path is not unique' in error:
                pass
            else:
                raise

    def randSong(self):
        self.__cursor.execute('SELECT path FROM songs ORDER BY RANDOM() LIMIT 1;')
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return row[0]