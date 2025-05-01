# Generate a Moog-style bassline in C minor (bassline_dark.py)

import numpy as np
from scipy.io.wavfile import write

# Setup
sample_rate = 44100
bpm = 68
beat_duration = 60 / bpm
beats_per_bar = 4
bars = 4
duration = beat_duration * beats_per_bar * bars
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
bass = np.zeros_like(t)

# Note sequence (C2, G1, C2, Ab1)
note_sequence = [65.41, 49.00, 65.41, 51.91]  # Hz
note_duration = beat_duration * 2
samples_per_note = int(sample_rate * note_duration)

# Generate bassline
for i, freq in enumerate(note_sequence * 2):  # repeat to fill 4 bars
    start = i * samples_per_note
    end = start + samples_per_note
    local_t = np.linspace(0, note_duration, samples_per_note, endpoint=False)
    wave = 0.4 * np.sign(np.sin(2 * np.pi * freq * local_t)) * np.exp(-2 * local_t)
    bass[start:end] += wave[:len(bass[start:end])]

# Normalize and export
bass = np.clip(bass, -1, 1)
bass_out = np.int16(bass * 32767)
bass_path = "bassline_dark.wav"
write(bass_path, sample_rate, bass_out)

bass_path
