import fnmatch
import logging
import os
import sqlite3
import threading
import time

from PyQt4.QtCore import pyqtSignal, QObject

# Maybe someday I'll do dir watching. If so, these links might be handy. Until
# then, re-indexing once an hour is good enough.
# http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
# http://packages.python.org/watchdog/quickstart.html#quickstart
# fs_watcher = QtCore.QFileSystemWatcher(['/Users/dbenamy/'])
# fs_watcher.directoryChanged.connect(lambda d: logging.debug('dir changed %s' % d))

class Indexer(QObject):
    # Shit does not work well with 2 threads accessing the db, at least in
    # linux. Proxy all inserts through the main thread where they're guarranteed
    # to be serialized with db reads.
    foundSongs = pyqtSignal(list)

    def __init__(self, root):
        super(Indexer, self).__init__()
        self.__rootDir = root
        self.__thread = threading.Thread(target=self.setUpPeriodicScan)
        self.__thread.daemon = True
        self.__thread.start()
    
    def setUpPeriodicScan(self):
        while True:
            self.scanDir()
            oneHour = 60 * 60
            time.sleep(oneHour)

    def scanDir(self):
        logging.info("Indexing %s" % self.__rootDir)
        toAdd = []
        for root, dirnames, filenames in os.walk(self.__rootDir):
            for filename in fnmatch.filter(filenames, '*.mp3'):
                path = os.path.join(root, filename)
                logging.debug("Adding to db (if not there): %s" % path)

                toAdd.append(path)
                if len(toAdd) == 100:
                    self.foundSongs.emit(toAdd)
                    toAdd = []
                    # When it's adding lots of songs, it seems it can starve the
                    # main thread. Sleep for a bit to prevent that.
                    time.sleep(0.1)
        self.foundSongs.emit(toAdd)
