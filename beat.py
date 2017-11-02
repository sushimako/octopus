import random

class skip(object):
    state = 0
    def beat(self, skips):
        self.state = (self.state+1) % 200
        return (self.state % skips) == 0

def rnd(threshold):
    return random.random() < 0.05
