import time
import random
import colors
import numpy as np



class Effect(object):

    def __init__(self):
        self.beat = False
        self.mfcc = []

    def beat(self):
        # might modify pixel data
        self.beat = True

    def mfcc(self, values):
        self.mfcc = values

    def mfcc_energy(self, mfcc):
        pass

    def energy_to_pixel(self, energy):
        # return (r,g,b) for energy level
        pass

    def tick(self):
        # tick the effect
        pass



def rainbow(state, prev=None, beat=False, colorscheme=None):
    if not colorscheme:
        colorscheme = colors.ocean
    state[:, 1:] = state[:, :-1]
    if beat:
        #state[:, 0] = (np.random.rand(1, 3) * 255).astype(int)
        #state[0, 0] = 255
        state[:, 0] = random.choice(colorscheme)
    else:
        state[:, 0] = np.tile(0, (1, 3))
    return state

def shifter(state, prev=None, beat=False):
    state[:, 1:] = state[:, :-1]
    state[:, 0] = np.tile(0, (1, 3))
    return state


strobestate = 0
def strobe(state, prev=None, beat=False):
    global strobestate
    if strobestate:
        strobestate -= 1
        return state
    else:
        state.fill(0)
    if beat:
        state[0, :] = 0xf5
        state[2, :] = 0x57
        strobestate = 4
    return state



#ocean_colors = [
#        [0xff, 0xff, 0xff],
#        [0xe5, 0xe9, 0xf8],
#        [0xcc, 0xd4, 0xf2],
#        [0xb2, 0xbf, 0xeb],
#        [0x99, 0xaa, 0xe5],
#        [0x7f, 0x95, 0xdf],
#        [0x66, 0x80, 0xd8],
#        [0x4c, 0x6b, 0xd2],
#        [0x33, 0x56, 0xcb],
#        [0x19, 0x41, 0xc5],
#        [0x00, 0x2c, 0xbf],
#        ]





glowstate = { 'up': {}, 'down':{}}
glowstate = { }
def glow(state, prev=None, beat=False, localstate=None, colorscheme=None):
    if not localstate:
        localstate = { 'up': {}, 'down':{}}
    if not colorscheme:
        #colorscheme = colors.red
        colorscheme = colors.ocean

    if beat:
        localstate[random.choice(range(max(state.shape)))] = 1
    cpy = localstate.copy()
    #print cpy
    for idx, val in cpy.items():
        #print abs(val), len(colorscheme)
        color = None
        if val < len(colorscheme):
            if abs(val) > 0:
                color = colorscheme[abs(val)]
                localstate[idx] = val + 1
            else:
                #del localstate[idx]
                color = [0, 0, 0]
            state[:, idx] = color
        elif val == len(colorscheme):
            localstate[idx] = -(val-1)

    return state, localstate



sparklestate = { 'up': True }
def sparkle(state, prev=None, beat=False):
    #state[:, 1:] = state[:, :-1]
    if beat:
        print 'FLUSHIN'
        #state.fill(0)
        sparklestate['up'] = not sparklestate['up']
    #print state
    for _ in range(50):
        pos = (np.random.rand(1, 1)[0][0] * 899).astype(int)
        print pos
        if sparklestate['up']:
            #state[:, pos] = (np.random.rand(1, 3) * 255).astype(int)
            state[:, pos] = random.choice(colors.ocean)
        else:
            state[:, pos].fill(0)
    #time.sleep(0.1)
    return state
    #if beat:
    #    #state[:, 0] = (np.random.rand(1, 3) * 255).astype(int)
    #    #state[:, 0] = (np.random.rand(1, 3) * 255).astype(int)
    #    state[0, 0] = (np.random.rand(1, 3) * 255).astype(int)
    #else:
    #    state[:, 0] = np.tile(0, (1, 3))
    #return state


            

        
        
