#! /usr/bin/env python

import numpy as np
import aubio

sample_rate=44100
x=np.zeros(44100)
for i in range(44100):
    x[i]=np.sin(2. * np.pi * i * 225. / sample_rate)

# create pitch object
p = aubio.pitch("yin", samplerate = sample_rate)
# other examples:
# = aubio.pitch("yinfft", 4096, 512, 44100)
# = aubio.pitch("yin", 2048, 512, 44100)
# = aubio.pitch("mcomb", 4096, 512, 44100)
# = aubio.pitch("schmitt", samplerate = 44100, hop_size = 512, buf_size = 2048)

# pad end of input vector with zeros
pad_length = p.hop_size - x.shape[0] % p.hop_size
x_padded = np.pad(x, (0, pad_length), 'constant', constant_values=0)
# to reshape it in blocks of hop_size
x_padded = x_padded.reshape(-1, p.hop_size)

# input array should be of type aubio.float_type (defaults to float32)
x_padded = x_padded.astype(aubio.float_type)

for frame, i in zip(x_padded, range(len(x_padded))):
    time_str = "%.3f" % (i * p.hop_size/float(sample_rate))
    pitch_candidate = p(frame)[0]
    print (time_str, "%.3f" % pitch_candidate)