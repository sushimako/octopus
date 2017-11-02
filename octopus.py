#! /usr/bin/env python
import sys
import time
import random
import serial
import numpy as np

import dsp
import beat
import colors
import effects

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
    strips = [
            range(149, -1, -1) + range(150, 300), 
            range(449, 299, -1) + range(450, 600),
            range(899, 749, -1) + range(600, 750),
            ]

    # we want to create effects for each mapped strip individually. Thus we need to 
    # keep a state for each 300-strip, which is then modified by whatever effect we 
    # feed it to:

    # initialize each strip's state with zeroes
    state1 = np.tile(0, (3, len(strips[0])))
    state2 = np.tile(0, (3, len(strips[1])))
    state3 = np.tile(0, (3, len(strips[2])))

    # some effects expect a localtate object to be passed along with each iteration. 
    # each effecn can decide what it uses it for. Check out effects.glow to see how it 
    # might be used
    localstate1 = localstate2 = None

    # enter mainloop
    while True:
        try:
            # decide there was a "beat" on each strip. Effects expect a beat parameter
            # and can choose to act upon it. Here we are simply creating random beats, i.e. 
            # "beat" if a random number is below an arbitrary treshold. 
            beat1 = beat.rnd(0.05)
            beat2 = beat.rnd(0.03)
            beat3 = beat.rnd(0.05)
            
            # calculate this iteration's pattern for each strip
            state1, localstate1 = effects.glow(state1, beat=beat1, localstate=localstate1, colorscheme=colors.darkblue)
            state2 = effects.rainbow(state2, beat=beat2, colorscheme=colors.realred)
            state3, localstate2 = effects.strobe(state3, beat=beat3, localstate=localstate2)


            # project the per-strip states back into the send-buffer. 
            send_buffer[:, strips[0]] = state1
            send_buffer[:, strips[1]] = state2
            send_buffer[:, strips[2]] = state3

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
            #time.sleep(0.04)

        except KeyboardInterrupt:
            print('abort')
            break
    socket.close()


if __name__ == '__main__':
    main()
