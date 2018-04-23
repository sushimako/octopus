import time
import random
import colors
import numpy as np

def rainbow(state, prev=None, beat=False, colorscheme=colors.ocean):
    # shift the whole state by one pixel
    state[:, 1:] = state[:, :-1]
    if beat:
        # insert a new pixel at position one
        state[:, 0] = random.choice(colorscheme)
    else:
        # leaft position one empty
        state[:, 0] = np.tile(0, (1, 3))
    return state

def shifter(state, prev=None, beat=False):
    # simply shifts whatever shate it gets by one. 
    # can be used in combination with other filters
    # to combine the effects
    state[:, 1:] = state[:, :-1]
    state[:, 0] = np.tile(0, (1, 3))
    return state


def segment_shade(state, segments=2):
    #state_len = len(state)
    #segment_len= state_len / segments
    #for idx in range(0, state_len, segment_len*2):
    #    #print idx
    #    state[0, idx: idx+segment_len] = 0
    #    state[1, idx: idx+segment_len] = 0
    #    state[2, idx: idx+segment_len] = 0
    state[0, 0:75] = 0
    state[1, 0:75] = 0
    state[2, 0:75] = 0
    return state

def rolling_shift(state, localstate=0, beat=False):
    if not beat:
        return state, localstate
    localstate += 1 #int(beat*4)
    state = np.roll(state, localstate, axis=1)
    return state, localstate

def allglow(state, beat=False, localstate=0, colorscheme=colors.darkblue):
    fade = colorscheme + colorscheme[::-1]
    if localstate:
        localstate -= 1
        idx = len(fade) - localstate - 1
        state[0, :] = fade[idx][0]
        state[1, :] = fade[idx][1]
        state[2, :] = fade[idx][2]
        return state, localstate
    else:
        # reset state to dark
        state.fill(0)
    if beat:
        localstate = len(fade)
        state[0, :] = fade[0][0]
        state[1, :] = fade[0][1]
        state[2, :] = fade[0][2]
    return state, localstate

def strobe(state, prev=None, beat=False, localstate=0, color=(0xf5, 0, 0x57)):
    if localstate:
        localstate -= 1
        return state, localstate
    else:
        # reset state to dark
        state.fill(0)
    if beat:
        # set all leds in our state to #f50057
        state[0, :] = color[0]
        state[1, :] = color[1]
        state[2, :] = color[2]
        # keep it for the next 4 iterations
        localstate = 4
    return state, localstate

def glow(state, prev=None, beat=False, localstate=None, colorscheme=colors.ocean, width=1):
    if not localstate:
        localstate = {}

    shape_len = max(state.shape)
    if beat:
        ## initialize a  glow on a random position
        #localstate[random.choice(range(max(state.shape)))] = 1
        idx = random.choice(range(shape_len))
        localstate[idx] = 1

    # we'll be modifying localstate, so make a copy before we iterate
    # over it. 
    cpy = localstate.copy()
    for idx, val in cpy.items():
        color = None
        if val < len(colorscheme):
            if abs(val) > 0:
                color = colorscheme[abs(val)]
                localstate[idx] = val + 1
            else:
                #del localstate[idx]
                color = [0, 0, 0]
            state[0, idx:min(shape_len, idx+width)] = color[0]
            state[1, idx:min(shape_len, idx+width)] = color[1]
            state[2, idx:min(shape_len, idx+width)] = color[2]
        elif val == len(colorscheme):
            localstate[idx] = -(val-1)
    return state, localstate
