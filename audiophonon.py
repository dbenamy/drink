import logging
import platform
import sys
import time

from PyQt4.phonon import Phonon
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QBuffer

class Player(QtCore.QObject):
    songDone = QtCore.pyqtSignal() 

    def __init__(self):
        super(Player, self).__init__()
        
        self.mediaObject = Phonon.MediaObject(self)
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        
        self.mediaObject.stateChanged.connect(self.stateChanged)
        self.mediaObject.finished.connect(self.songDone.emit)

    def stateChanged(self, newState, oldState):
        logging.debug('mediaObject state changed from %s to %s' % (oldState, newState))
        if newState == Phonon.ErrorState:
            source = self.mediaObject.currentSource().fileName()
            logging.error(
                "Could not play %s: %s - %s" %
                (source.toLocal8Bit().data(), self.mediaObject.errorType(),
                 self.mediaObject.errorString()))

    def playFile(self, path):
        logging.debug("Player playing %s" % path)
        self.stop()
        logging.debug("Player stopped.")

        if platform.system().lower() == 'windows':
            # On windows, directshow blows up if id3 tags aren't just right. Read
            # the data into memory and strip out the id3 tag before playing it.
            # Thanks to http://stackoverflow.com/questions/10560349/direct-show-9-phonon-error-pins-cannot-connect
            data = file(path, 'rb').read()
            data = self.__stripId3(data)
            qbuffer = QBuffer(self.mediaObject)
            qbuffer.setData(data)
            logging.debug("Player loaded song and stripped id3 tags.")
            self.mediaObject.setCurrentSource(Phonon.MediaSource(qbuffer))
            # Phonon only reports the DS error when reading from path, not from
            # buffer, so to reproduce, use the following version.
        else:
            # On my linux box, it occasionally hangs when playing from a
            # QBuffer so play directly from file.
            # To reproduce, use the above code and hold down next.
            self.mediaObject.setCurrentSource(Phonon.MediaSource(path))
        
        logging.debug("Player playing.")
        self.mediaObject.play()

    def stop(self):
        if self.mediaObject.state() == Phonon.PlayingState:
            self.mediaObject.stop()

    def __stripId3(self, data):
        # ID3 v1.x
        if data[-128:-125] == 'TAG':
            data = data[:-128]

        # ID3 v2
        if data[:3] == 'ID3':
            tagSize = self.__bin2dec(self.__bytes2bin(data[6:10], 7)) + 10 # 10 is a magic number from eyeD3
            data = data[tagSize:]

        return data

    # Accepts a string of bytes (chars) and returns an array of bits
    # representing the bytes in big endian byte (Most significant byte/bit first)
    # order.  Each byte can have it's higher bits ignored by passing an sz arg.
    # From eyeD3
    def __bytes2bin(self, bytes, sz = 8):
       if sz < 1 or sz > 8:
          raise ValueError("Invalid sz value: " + str(sz))

       retVal = []
       for b in bytes:
          bits = []
          b = ord(b)
          while b > 0:
             bits.append(b & 1)
             b >>= 1

          if len(bits) < sz:
             bits.extend([0] * (sz - len(bits)))
          elif len(bits) > sz:
             bits = bits[:sz]

          # Big endian byte order.
          bits.reverse()
          retVal.extend(bits)

       if len(retVal) == 0:
          retVal = [0]
       return retVal

    # Convert and array of "bits" (MSB first) to it's decimal value.
    # From eyeD3
    def __bin2dec(self, x):
       bits = []
       bits.extend(x)
       bits.reverse()

       multi = 1
       value = long(0)
       for b in bits:
          value += b * multi
          multi *= 2
       return value
