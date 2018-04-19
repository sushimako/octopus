import time
import random
import pyaudio
import numpy as np
from audio import utils
from audio import config

class skip(object):
    state = 0
    def beat(self, skips):
        self.state = (self.state+1) % 200
        return (self.state % skips) == 0

def rnd(threshold):
    return random.random() < 0.05

class AudioBeat(object):
    stream = None
    overflows = 0
    prev_ovf_time = None
    frames_per_buffer = int(config.MIC_RATE / config.FPS)

    def __init__(self):
        self.ctx = pyaudio.PyAudio()
        self.stream = self.ctx.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=config.MIC_RATE,
                        input=True,
                        frames_per_buffer=self.frames_per_buffer)
        self.prev_ovf_time = time.time()

    def tick(self):
        try:
            y = np.fromstring(self.stream.read(self.frames_per_buffer), dtype=np.int16)
            y = y.astype(np.float32)
            return y
        except IOError:
            self.overflows += 1
            if time.time() > self.prev_ovf_time + 1:
                self.prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(self.overflows))
            return []

    def bands(self, tick):
        return utils.band_data(tick)

    def is_beat(self, bands):
        return bands[0] > 120

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.ctx.terminate()

if __name__ == '__main__':
    b = AudioBeat()
    while True:
        print b.bands(b.tick())
    b.close()

