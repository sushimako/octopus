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


def strobe(state, prev=None, beat=False, localstate=0):
    if localstate:
        localstate -= 1
        return state, localstate
    else:
        # reset state to dark
        state.fill(0)
    if beat:
        # set all leds in our state to #f50057
        state[0, :] = 0xf5
        state[2, :] = 0x57
        # keep it for the next 4 iterations
        localstate = 4
    return state, localstate

def glow(state, prev=None, beat=False, localstate=None, colorscheme=colors.ocean):
    if not localstate:
        localstate = { 'up': {}, 'down':{}}

    if beat:
        # initialize a  glow on a random position
        localstate[random.choice(range(max(state.shape)))] = 1

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
            state[:, idx] = color
        elif val == len(colorscheme):
            localstate[idx] = -(val-1)
    return state, localstate



#sparklestate = { 'up': True }
#def sparkle(state, prev=None, beat=False):
#    #state[:, 1:] = state[:, :-1]
#    if beat:
#        print 'FLUSHIN'
#        #state.fill(0)
#        sparklestate['up'] = not sparklestate['up']
#    #print state
#    for _ in range(50):
#        pos = (np.random.rand(1, 1)[0][0] * 899).astype(int)
#        print pos
#        if sparklestate['up']:
#            #state[:, pos] = (np.random.rand(1, 3) * 255).astype(int)
#            state[:, pos] = random.choice(colors.ocean)
#        else:
#            state[:, pos].fill(0)
#    #time.sleep(0.1)
#    return state
#    #if beat:
#    #    #state[:, 0] = (np.random.rand(1, 3) * 255).astype(int)
#    #    #state[:, 0] = (np.random.rand(1, 3) * 255).astype(int)
#    #    state[0, 0] = (np.random.rand(1, 3) * 255).astype(int)
#    #else:
#    #    state[:, 0] = np.tile(0, (1, 3))
#    #return state


            

        
        
