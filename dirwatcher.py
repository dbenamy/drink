import fnmatch
import logging
import os
import sqlite3
import threading

from PyQt4 import QtCore

from db import DB

# http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
# http://packages.python.org/watchdog/quickstart.html#quickstart
# fs_watcher = QtCore.QFileSystemWatcher(['/Users/dbenamy/'])
# fs_watcher.directoryChanged.connect(lambda d: logging.debug('dir changed %s' % d))

class DirWatcher(QtCore.QObject):
    def __init__(self, root):
        super(DirWatcher, self).__init__()
        self.__thread = threading.Thread(target=self.scanDir, args=(root,))
        self.__thread.daemon = True
        self.__thread.start()
        
    def scanDir(self, root_dir):
        db = DB()
        print "%s songs in db" % db.numSongs()

        for root, dirnames, filenames in os.walk(root_dir):
            for filename in fnmatch.filter(filenames, '*.mp3'):
                path = os.path.join(root, filename)
                print "Adding to db (if not there): %s" % path
                try:
                    db.addSong(path)
                except:
                    logging.exception("Skipping %s" % path)

        print "%s songs in db" % db.numSongs()
