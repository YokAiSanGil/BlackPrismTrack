# Create a pad synth in C minor using layered waveforms

import numpy as np
from scipy.io.wavfile import write

# Setup
sample_rate = 44100
duration = 32  # match rain
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Frequencies for C minor chord: C2, Eb2, G2
freqs = [65.41, 77.78, 98.00]  # in Hz

# Layer pad tones using sine + saw blend with gentle modulation
pad = np.zeros_like(t)
for f in freqs:
    # Base tones
    sine = 0.3 * np.sin(2 * np.pi * f * t)
    saw = 0.15 * 2 * (f * t - np.floor(f * t + 0.5))
    # Slight LFO for movement
    lfo = 0.8 + 0.2 * np.sin(2 * np.pi * 0.1 * t + np.random.rand())
    voice = (sine + saw) * lfo
    pad += voice

# Normalize and convert
pad = np.clip(pad, -1, 1)
pad_out = np.int16(pad * 32767)

# Export
pad_path = "pad_cminor_san.wav"
write(pad_path, sample_rate, pad_out)

pad_path