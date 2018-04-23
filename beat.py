import time
import random
from datetime import timedelta


class SkipCycleBeat(object):
    def __init__(self, cycles=20):
        self.state = 0
        self.skip_cycles = cycles

    def tick(self):
        self.state = (self.state+1) % self.skip_cycles
        return 1 if self.state == 0 else 0


class LowPassBeat(object):
    def __init__(self, stream, thresh=0.47):
        self.stream = stream
        self.thresh = thresh

    def tick(self):
        band = self.stream.bands[0]
        return band if band > self.thresh else 0

class MidPassBeat(object):
    def __init__(self, stream, thresh=0.47):
        self.stream = stream
        self.thresh = thresh

    def tick(self):
        band = self.stream.bands[1]
        return band if band > self.thresh else 0

class HighPassBeat(object):
    def __init__(self, stream, thresh=0.47):
        self.stream = stream
        self.thresh = thresh

    def tick(self):
        band = self.stream.bands[2]
        return band if band > self.thresh else 0


class RandomBeat(object):
    def __init__(self, probability=0.05):
        self.probability = probability

    def tick(self):
        return 1 if random.random() < self.probability else 0

class TimedBeat(object):
    def __init__(self, ms, duration=200):
        self.ms = ms
        self.duration = duration
        self.last_tick = time.time() * 1000.0

    def tick(self):
        now = time.time() * 1000.0
        if now > (self.last_tick + self.ms):
            self.last_tick = now
            return 1
        if now < (self.last_tick + self.duration):
            return 1
        return 0




class EnergyBeat(object):
    def __init__(self, stream, thresh=0):
        self.stream = stream
        self.thresh = thresh

    def tick(self):
        val = max(self.stream.bands)
        return val if val > self.thresh else 0


