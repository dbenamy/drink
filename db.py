import os
import sqlite3

from PyQt4 import QtCore

class DB():
    def __init__(self, path):
        self.__conn = sqlite3.connect(path)
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS songs (path text unique);')

    def commit(self):
        self.__conn.commit()

    def numSongs(self):
        self.__cursor.execute('SELECT COUNT(*) FROM songs;')
        return self.__cursor.fetchone()[0]

    def addSong(self, path):
        try:
            print(type(path))
            self.__cursor.execute('INSERT INTO songs (path) VALUES (?);', (path,))
        except sqlite3.IntegrityError as error:
            if 'column path is not unique' in str(error):
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