#! /usr/bin/env python
import sys
import time
import random
import serial
import numpy as np

import beat
import colors
import effects
from audio import dsp
from audio.utils import SoundStream

from ledstrip import MockSerial, update_strip


def scale_pixels(l, data):
    cpy = data.copy()
    for i, px in enumerate(data.T):
        cpy = np.insert(cpy, i*l, np.tile(data[:, i], (l-1, 1)), axis=1)
    return cpy


fps_last_update = time.time()
time_prev = time.time() * 1000.0
_fps = dsp.ExpFilter(val=40, alpha_decay=0.2, alpha_rise=0.2)


# you can mostly ignore this. this is just to display at what FPS the script is running
def frames_per_second():
    """Return the estimated frames per second
    
    Returns the current estimate for frames-per-second (FPS).
    FPS is estimated by measured the amount of time that has elapsed since
    this function was previously called. The FPS estimate is low-pass filtered
    to reduce noise.
    
    This function is intended to be called one time for every iteration of
    the program's main loop.
    
    Returns
    -------
    fps : float
        Estimated frames-per-second. This value is low-pass filtered
        to reduce noise.
    """
    global time_prev, _fps
    time_now = time.time() * 1000.0
    dt = time_now - time_prev
    time_prev = time_now
    if dt == 0.0:
        return _fps.value
    return _fps.update(1000.0 / dt)


def main(): 
    # set up serial connection to the teensy via usb
    socket = MockSerial()
    #socket = serial.Serial('/dev/ttyACM0', timeout=0.01)

    # send buffer holds the info that is being sent to the teensy. It is a 
    # ndarray with dimention (3, total_number_of_leds)
    # deduplication efforts (i.e. only send necessary changes to the teensy)
    send_buffer = np.tile(0, (3, 900))

    # here we define the mapping. The low-level wire-format considers all 
    # leds in our setup to be one continuous ledstrip with a lenght of the 
    # total number of leds, indexed from 0 to (numleds-1) (899 in our case)
    # 
    # here we define an (technically arbitrary) mapping of our mega-strip (900 leds)
    # into 3 separate strips of equal length (300). We make use of numpy's ability
    # to pass a list of indxexes when slicing an ndarra. Thus we can do things 
    # like (pseudocode):
    #    >>> arr = [0, 0, 0, 0, 0, 0]
    #    >>> arr[[3,5,2]] = [1, 2, 3]
    #    >>> arr === [0, 0, 3, 1, 0, 2]
    # in this example, our mapping would be [3, 5, 2] and the strip-specifica state [1, 2, 3]
    # 
    # This particular mapping stems from the way our led strips are installed and their 
    # orientation. 
    # Any arbitrary mapping is possible here. 
    #strips = [
    #        range(149, -1, -1) + range(150, 300), 
    #        range(899, 749, -1) + range(600, 750),
    #        ]
    strips = [
            #[0, 1]
            range(0, 150),
            range(150, 300),
            range(300, 450),
            range(600, 750),
            range(750, 900),
            range(450, 525),
            #range(599, 524, -1),
            range(525, 600),
            ]

    # we want to create effects for each mapped strip individually. Thus we need to 
    # keep a state for each 300-strip, which is then modified by whatever effect we 
    # feed it to:

    # initialize each strip's state with zeroes
    state1 = np.tile(0, (3, len(strips[0])))
    state2 = np.tile(0, (3, len(strips[1])))
    state3 = np.tile(0, (3, len(strips[2])))
    state4 = np.tile(0, (3, len(strips[3])))
    state5 = np.tile(0, (3, len(strips[4])))
    state_ring = np.tile(0, (3, len(strips[5])))

    # some effects expect a localtate object to be passed along with each iteration. 
    # each effecn can decide what it uses it for. Check out effects.glow to see how it 
    # might be used
    localstate1 = localstate2 = localstate3 = localstate4 = localstate5 = localstate6 =  None
    shifterstate = 0
    soundstream = SoundStream()

    def beat_gen(key, ticker):
        return lambda: (key, ticker.tick())


    beatmakers = [
            beat_gen('skip5', beat.SkipCycleBeat(5)),
            beat_gen('every20ms', beat.TimedBeat(20)),
            beat_gen('every200ms', beat.TimedBeat(200, duration=100)),
            beat_gen('every1000ms', beat.TimedBeat(1000)),
            soundstream.tick, # doesn't return beat, but calculates soundprofile
            beat_gen('lowpass', beat.LowPassBeat(soundstream)),
            beat_gen('midpass', beat.MidPassBeat(soundstream)),
            beat_gen('highpass', beat.HighPassBeat(soundstream, thresh=0.45)),
            beat_gen('energy', beat.EnergyBeat(soundstream, thresh=0.4))
            ]

    # enter mainloop
    while True:
        try:
            # decide there was a "beat" on each strip. Effects expect a beat parameter
            # and can choose to act upon it. Here we are simply creating random beats, i.e. 
            # "beat" if a random number is below an arbitrary treshold. 
            #print beatmakers
            loop_beats = [b() for b in beatmakers if b]
            loop_beats = dict(b for b in loop_beats if b)
            #print loop_beats

            #beat2 = beat.rnd(0.003)
            #print bands
            #beat3 = beat.rnd(0.05)
            
            bandcolor = [int(x*255.0) for x in soundstream.bands]
            #print loop_beats['lowpass']
            #print bandcolor
            #print soundstream.bands
            # calculate this iteration's pattern for each strip
            #state1 = effects.rainbow(state1, beat=loop_beats['lowpass'], colorscheme=bandcolor)
            #state1, localstate1 = effects.strobe(state1, beat=loop_beats['energy'], localstate=localstate1, color=bandcolor)
            #state2 = effects.rainbow(state2, beat=beat2, colorscheme=colors.darkblue)
            #state2, localstate2 = effects.strobe(state2, beat=beat1, localstate=localstate2, color=bands)
            #state1, localstate1 = effects.glow(state1, beat=loop_beats['energy'], localstate=localstate1, colorscheme=colors.realgreen)
            #print loop_beats['every1000ms']

            #state1, localstate1 = effects.strobe(state1, beat=loop_beats['lowpass'], localstate=localstate1, color=[0xff, 00, 00])
            #state2, localstate2 = effects.strobe(state2, beat=loop_beats['midpass'], localstate=localstate2, color=[00, 0xff, 00])
            #state3, localstate3 = effects.strobe(state3, beat=loop_beats['highpass'], localstate=localstate3, color=[00, 00, 0xff])

            #state2, localstate2 = effects.glow(state2, beat=loop_beats['midpass'], localstate=localstate2, colorscheme=colors.ocean)

            #state1, localstate1 = effects.glow(state1, beat=loop_beats['highpass'], localstate=localstate1, colorscheme=colors.ocean)
            #state2, localstate2 = effects.glow(state2, beat=loop_beats['midpass'], localstate=localstate2, colorscheme=colors.ocean)

            #state1 = effects.rainbow(state1, beat=loop_beats['lowpass'], colorscheme=colors.red)
            #state2 = effects.rainbow(state2, beat=loop_beats['lowpass'], colorscheme=colors.red)
            #state3 = effects.rainbow(state3, beat=loop_beats['lowpass'], colorscheme=colors.yellowgreen)
            #state4 = effects.rainbow(state4, beat=loop_beats['highpass'], colorscheme=colors.darkblue)
            #state5 = effects.rainbow(state5, beat=loop_beats['midpass'], colorscheme=colors.red)
            #state6 = effects.rainbow(state6, beat=loop_beats['midpass'], colorscheme=colors.red)

            state1, localstate1 = effects.glow(state1, beat=loop_beats['lowpass'], localstate=localstate1, colorscheme=colors.red)
            state2, localstate2 = effects.glow(state2, beat=loop_beats['lowpass'], localstate=localstate2, colorscheme=colors.red)
            state3, localstate3 = effects.glow(state3, beat=(loop_beats['lowpass'] or loop_beats['midpass']), localstate=localstate3, colorscheme=colors.red)
            #state4, localstate4 = effects.glow(state4, beat=loop_beats['highpass'], localstate=localstate4, colorscheme=colors.darkblue)
            state4, localstate4 = effects.glow(state4, beat=(loop_beats['lowpass'] or loop_beats['midpass']), localstate=localstate4, colorscheme=colors.red)
            state5, localstate5 = effects.glow(state5, beat=loop_beats['lowpass'], localstate=localstate5, colorscheme=colors.red)

            state_ring, localstate6 = effects.glow(state_ring, width=2, beat=(loop_beats['lowpass'] > 0.87 and not loop_beats['midpass']), localstate=localstate6, colorscheme=colors.red)
            #state_ring, localstate6 = effects.glow(state_ring, beat=loop_beats['highpass'], localstate=localstate6, colorscheme=colors.darkblue, width=3)
            #state_ring = effects.rainbow(state_ring, beat=loop_beats['highpass'], colorscheme=colors.darkblue)

            #state1 = effects.segment_shade(state1, 2)
            #state3, shifterstate = effects.rolling_shift(state3, localstate=shifterstate, beat=loop_beats['lowpass'])


            # project the per-strip states back into the send-buffer. 
            send_buffer[:, strips[0]] = state1
            send_buffer[:, strips[1]] = state2
            send_buffer[:, strips[2]] = state3
            send_buffer[:, strips[3]] = state4
            send_buffer[:, strips[4]] = state5
            send_buffer[:, strips[5]] = state_ring
            send_buffer[:, strips[6]] = state_ring

            # TODO document scale_pixels
            #send_buffer[:, strips[0]] = scale_pixels(5, state2)
            #send_buffer[:, strips[1]] = scale_pixels(5, state2)
            #send_buffer[:, strips[2]] = scale_pixels(5, state2)

            
            # send pixels to teensy
            update_strip(send_buffer, socket)

            fps = frames_per_second()
            if time.time() - 0.5 > fps_last_update:
                prev_fps_update = time.time()
                print('FPS {:.0f}'.format(fps))

            # use this delay to slow it down. Thid delay could use some
            # magic so it will trigger every x ms 
            #time.sleep(0.01)

        except KeyboardInterrupt:
            soundbeat.close()
            print('abort')
            break
    socket.close()


if __name__ == '__main__':
    main()
