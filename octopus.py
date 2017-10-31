#! /usr/bin/env python

# Use pyaudio to open the microphone and run aubio.pitch on the stream of
# incoming samples. If a filename is given as the first argument, it will
# record 5 seconds of audio to this location. Otherwise, the script will
# run until Ctrl+C is pressed.

# Examples:
#    $ ./python/demos/demo_pyaudio.py
#    $ ./python/demos/demo_pyaudio.py /tmp/recording.wav

import pyaudio
import sys
import numpy as np
import serial
import time
import aubio
import dsp
import random
import colors

# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
#buffer_size = 1024
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
#pyaudio_format = pyaudio.paInt16
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size,
                input_device_index=6,
                )

# setup pitch
tolerance = 0.8
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)


# read from audiofile
#s = aubio.source('/home/flo/music/nikolo-2014.mp3', samplerate, hop_s)
#samplerate = s.samplerate
#o = aubio.tempo("specdiff", win_s, hop_s, samplerate)



# setup beat detector?
#samplerate, win_s, hop_s = 44100, 1024, 512
#tempo_o = aubio.tempo("specdiff", win_s, hop_s, samplerate)
tempo_o = aubio.tempo("specdiff", win_s, hop_s, samplerate)
#tempo_o.set_tolerance(tolerance)
print("*** starting recording")

#set strips
from ledstrip import MockSerial, update_strip
from effects import rainbow, sparkle, shifter, strobe, glow
#strips = (Strip(1, 300), Strip(2, 300), Strip(3, 300))
num_pixels = 300

strips = [
        range(149, -1, -1) + range(150, 300),
        range(449, 299, -1) + range(450, 600),
        range(899, 749, -1) + range(600, 750),
        ]

def scale_pixels(l, data):
    cpy = data.copy()
    for i, px in enumerate(data.T):
        #print i
        cpy = np.insert(cpy, i*l, np.tile(data[:, i], (l-1, 1)), axis=1)
    #print 'done'
    return cpy


fps_last_update = time.time()
time_prev = time.time() * 1000.0
_fps = dsp.ExpFilter(val=40, alpha_decay=0.2, alpha_rise=0.2)

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



class skipbeat(object):
    state = 0

    def beat(self, skips):
        self.state = (self.state+1) % 200
        #print self.state, self.state % skips
        return (self.state % skips) == 0


        


def main(): 
    #socket = MockSerial()
    socket = serial.Serial('/dev/ttyACM0', timeout=0.01)

    #strip1 = np.tile(0, (3, num_pixels))
    #strip2 = np.tile(0, (3, num_pixels))
    #strip3 = np.tile(0, (3, num_pixels))
    state = np.tile(0, (3, num_pixels))
    state_strobe = np.tile(0, (3, num_pixels))
    send_buffer = np.tile(0, (3, 900))
    prev_state = None
    prev_state_strobe = None

    state1 = np.tile(0, (3, 60))
    state2 = np.tile(0, (3, 60))
    state3 = np.tile(0, (3, 60))
    bar = np.tile(0, (3, 3))

    delay = skipbeat()

    metronom = skipbeat()
    local1 = local2 = local3 = None
    while True:
        try:
            audiobuffer = stream.read(buffer_size, exception_on_overflow=False)
            signal = np.fromstring(audiobuffer, dtype=np.float32)

            #read from tile
            #samples, read = s()
            #is_beat = o(samples)


            #pitch = pitch_o(signal)[0]
            #confidence = pitch_o.get_confidence()

            ##is_beat = True
            #is_beat = tempo_o(signal)
            ##print is_beat
	    #    
	
            #if is_beat:
            #    this_beat = tempo_o.get_last_s()
            #    print 'beat',  this_beat
            #is_beat = random.random() < 0.07

            #globalbeat = metronom.beat(3)
            #if globalbeat:
            #    print 'METRONOOOOM'
            #beat3 = metronom.beat(10)
            #if is_beat:
            #    this_beat = tempo_o.get_last_s()
            #    effect.beat()
            #    print this_beat
            #    #beats.append(this_beat)
            #TODO: set mfcc (if this is necessary at all
            # apply effect
            #print 'beat', is_beat

            #pixels = rainbow(pixels, state, is_beat)
            #pixels = sparkle(pixels, state, is_beat)
            #pixels = strobe(pixels, state, is_beat)
            #pixels = shifter(pixels, state, is_beat)
            #state3 = rainbow(state3, beat=is_beat)
            if delay.beat(1):
                #beat1 = metronom.beat(random.choice(17)) and random.random() < 0.5
                #beat1 = random.random() < 0.1
                beat1 = random.random() < 0.05
                beat2 = random.random() < 0.03
                beat3 = random.random() < 0.05
                #beat3 = random.random() < 0.1
                #beat1 = metronom.beat(random.choice(range(13, 20))) and random.random() < 0.05
                #beat3 = metronom.beat(random.choice(range(11, 20))) and random.random() < 0.01
                #state1, local1 = glow(state1, beat=beat1, localstate=local1)
                #state2, local2 = glow(state2, beat=beat2, localstate=local2, colorscheme=colors.red)
                
                #state1 = rainbow(state1, beat=beat1)
                #state1 = rainbow(state1, beat=beat1)
                #state2 = strobe(state2, beat=beat2, colorscheme=colors.darkblue)
                #state3 = rainbow(state3, beat=beat3)
                #state2 = strobe(state2, beat=beat2, colorscheme=colors.darkblue)

                #state1 = rainbow(state1, beat=beat1, colorscheme=random.choice([colors.realred, ]))
                state1, local1 = glow(state1, beat=beat1, localstate=local1, colorscheme=random.choice([colors.darkblue, ]))
                state2 = rainbow(state2, beat=beat2, colorscheme=random.choice([colors.darkblue, ]))
                state3, local3 = glow(state3, beat=beat3, localstate=local3, colorscheme=random.choice([colors.darkblue, ]))
                #state2, local2 = glow(state2, beat=beat2, colorscheme=random.choice([colors.darkblue, ]))
                #state2 = rainbow(state2, beat=(beat2 and random.random<0.4), colorscheme=random.choice([colors.darkblue, ]))
                #state3 = rainbow(state3, beat=beat3, colorscheme=random.choice([colors.realred, ]))
                #state3 = rainbow(state3, beat=beat3)
                #if delay.beat(3):
                #    state2 = rainbow(state2, beat=beat2)
                #state3, local3 = glow(state3, beat=beat3, localstate=local3)
                send_buffer[:, strips[0]] = scale_pixels(5, state2)
                send_buffer[:, strips[1]] = scale_pixels(5, state2)
                send_buffer[:, strips[2]] = scale_pixels(5, state2)
            #for strip in (strips[0], strips[2]):
            #    res = scale_pixels(10, state3)
            #    send_buffer[:, strip] = res
            
            #strobe_beat = random.random() < 0.1
            ##state_strobe = strobe(state_strobe, beat=strobe_beat)
            #state_strobe = rainbow(state_strobe, beat=strobe_beat)
            #send_buffer[:, strips[1]] = state_strobe

            update_strip(send_buffer, socket, last_state=prev_state)
            prev_state = np.copy(send_buffer)
            #time.sleep(.03)
            #confidence = pitch_o.get_confidence()
            #print("{} / {}".format(pitch,confidence))
            #msg = socket.read(200)
            #if msg:
            #    print msg
            #print 'python loop'

            fps = frames_per_second()
            if time.time() - 0.5 > fps_last_update:
                prev_fps_update = time.time()
                print('FPS {:.0f}'.format(fps))


        except KeyboardInterrupt:
            print("*** Ctrl+C pressed, exiting")
            break

    print("*** done recording")
    stream.stop_stream()
    stream.close()
    socket.close()
    p.terminate()



if __name__ == '__main__':
    main()
