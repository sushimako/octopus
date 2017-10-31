import numpy as np
import os.path

_gamma = np.load(os.path.join(os.path.dirname(__file__), 'gamma_table.npy'))

## wireformat: 
##  [16 bit: led address][8 bit Red][8 bit Blue][8 bit Green] == 40bit
def decode_pos(left, right):
    return (ord(left) << 8) | ord(right)

def encode_pos(pos):
    return chr((pos >> 8 ) & 0xff) + chr(pos & 0xff)

def update_strip(pixels, socket, last_state=None):
    # pixels is a numpy ndarray of dimension (3, 900), with 8bit R, G, and B values
    # for each of the (hardcoded) 900 LEDs. The wireformat addresses the leds by their 
    # integer address from 0-899. See https://www.pjrc.com/teensy/td_libs_OctoWS2811.html for
    # details on the addressing scheme
    bytes_per_pixel = 5 # 2x for address + 3x1 for RGB 
    max_payload = 30 # send max 30 leds per serial send
    pixels = np.clip(pixels, 0, 255).astype(int) 
    # Optionally apply gamma correc tio
    #pixels = _gamma[pixels]

    # packet is what is sent over the serial to the teensy
    packet = ''
    for i in range(900):
        if last_state is not None and np.array_equal(pixels[:, i], last_state[:, i]):
            # nothing changed on that pixel, continue
            continue
        packet += encode_pos(i) + chr(pixels[0][i]) + chr(pixels[1][i]) + chr(pixels[2][i])
        if (len(packet)/bytes_per_pixel) + 1 > max_payload:
            socket.write(packet)
            packet = ''
    if packet:
        # send the rest
        socket.write(packet)


# receives numpy arrays, convertes them into the searial wireformat and sends it over serial
class MockSerial(object):
    def write(self, packet):
        #print 'received packet', len(packet), list(packet)
        step = 5 #bytes per pixel
        for i in range(0, len(packet), step):
            pos = decode_pos(packet[i:i+1], packet[i+1:i+2])
            r, g, b = [ord(val) for val in packet[i+2:i+step]]
            #print 'setting pixel <{}> to ({} {} {})'.format(pos, r, g, b)

    def close(self):
        pass
