#!/bin/env python

import time, wave, string, os, sys, threading

import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound
import pymedia.muxer as muxer

class StopPlayThread(Exception):
    pass

class Player:
    def __init__(self):
        self.__thread = None
        self.__stop_file_event = threading.Event()
        self.__stop_all_files_event = threading.Event()

    def play_files(self, filenames):
        if self.__thread and self.__thread.is_alive():
            self.__stop_all_files_event.set()
            while self.__thread.is_alive():
                time.sleep(0.01)
        self.__thread = threading.Thread(target=self._play_files_thread, args=(filenames,))
        self.__thread.daemon = True
        self.__thread.start()

    def next(self):
        self.__stop_file_event.set()

    def _play_files_thread(self, filenames):
        try:
            for fn in filenames:
                self._play_file(fn)
        except StopPlayThread:
            pass

    def _play_file(self, filename):
        extension = str.split(filename, '.')[-1].lower()
        demux = muxer.Demuxer(extension)
        decoder = None
        snd = None
        f = open(filename, 'rb')

        while True:
            audio_data = f.read(20000)
            if len(audio_data) == 0:
                break

            frames_encoded = demux.parse(audio_data)
            for frame_encoded in frames_encoded:
                # Can't access demux.streams[0] until we access a frame
                if decoder == None:
                    decoder = acodec.Decoder(demux.streams[0])
                frame_pcm = decoder.decode(frame_encoded[1])
                if frame_pcm and frame_pcm.data:
                    if snd == None:
                        snd = sound.Output(frame_pcm.sample_rate, frame_pcm.channels, sound.AFMT_S16_LE)
                    snd.play(frame_pcm.data)

                    if self.__stop_file_event.is_set():
                        self.__stop_file_event.clear()
                        return
                    if self.__stop_all_files_event.is_set():
                        self.__stop_all_files_event.clear()
                        raise StopPlayThread()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s <filename>" % sys.argv[0]
    else:
        Player()._play_file(sys.argv[1])
