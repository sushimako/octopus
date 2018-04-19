from __future__ import division
import dsp
import config
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

#N_FFT_BINS = 24
#MIC_RATE = 44100
#FPS = 60
#N_ROLLING_HISTORY = 2
#MIN_FREQUENCY = 200
#MAX_FREQUENCY = 12000

gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                     alpha_decay=0.001, alpha_rise=0.99)
mel_gain = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.01, alpha_rise=0.99)
mel_smoothing = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.5, alpha_rise=0.99)
fft_window = np.hamming(int(config.MIC_RATE / config.FPS) * config.N_ROLLING_HISTORY)

# Number of audio samples to read every time frame
samples_per_frame = int(config.MIC_RATE / config.FPS)

# Array containing the rolling audio sample window
y_roll = np.random.rand(config.N_ROLLING_HISTORY, samples_per_frame) / 1e16


def bands_maxvals(y):
    # here be dragons
    y = y**2.0
    gain.update(y)
    y /= gain.value
    y *= 255.0
    low = int(np.max(y[:len(y) // 3]))
    mid = int(np.max(y[len(y) // 3: 2 * len(y) // 3]))
    hig = int(np.max(y[2 * len(y) // 3:]))
    return low, mid, hig

def band_data(audio_samples):
    global y_roll, prev_rms, prev_exp
    # Normalize samples between 0 and 1
    y = audio_samples / 2.0**15
    # Construct a rolling window of audio samples
    y_roll[:-1] = y_roll[1:]
    y_roll[-1, :] = np.copy(y)
    y_data = np.concatenate(y_roll, axis=0).astype(np.float32)
    
    # Transform audio input into the frequency domain
    N = len(y_data)
    N_zeros = 2**int(np.ceil(np.log2(N))) - N
    # Pad with zeros until the next power of two
    y_data *= fft_window
    y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
    YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
    # Construct a Mel filterbank from the FFT data
    mel = np.atleast_2d(YS).T * dsp.mel_y.T
    # Scale data to values more suitable for visualization
    # mel = np.sum(mel, axis=0)
    mel = np.sum(mel, axis=0)
    mel = mel**2.0
    # Gain normalization
    mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
    mel /= mel_gain.value
    mel = mel_smoothing.update(mel)
    #x = np.linspace(config.MIN_FREQUENCY, config.MAX_FREQUENCY, len(mel))

    #print (bands_maxvals(mel))
    #if bands_maxvals(mel)[0] > 120:
    #    print('BEAT')
    return bands_maxvals(mel)




#def start_stream(callback):
#    p = pyaudio.PyAudio()
#    frames_per_buffer = int(config.MIC_RATE / config.FPS)
#    stream = p.open(format=pyaudio.paInt16,
#                    channels=1,
#                    rate=config.MIC_RATE,
#                    input=True,
#                    frames_per_buffer=frames_per_buffer)
#    overflows = 0
#    prev_ovf_time = time.time()
#    while True:
#        try:
#            y = np.fromstring(stream.read(frames_per_buffer), dtype=np.int16)
#            y = y.astype(np.float32)
#            callback(y)
#        except IOError:
#            overflows += 1
#            if time.time() > prev_ovf_time + 1:
#                prev_ovf_time = time.time()
#                print('Audio buffer has overflowed {} times'.format(overflows))
#    stream.stop_stream()
#    stream.close()
#    p.terminate()


