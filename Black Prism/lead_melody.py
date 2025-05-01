# Generate a lead melody with sine wave motif (lead_melody.py)

import numpy as np
from scipy.io.wavfile import write

# Setup
sample_rate = 44100
bpm = 68
beat_duration = 60 / bpm
bars = 4
beats_per_bar = 4
duration = beat_duration * beats_per_bar * bars
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
lead = np.zeros_like(t)

# Melody: Eb4 → C4 → Ab3 → G3 (minor 6th logic)
melody_freqs = [311.13, 261.63, 207.65, 196.00]  # Hz
note_duration = beat_duration * 2  # 2 beats per note
samples_per_note = int(sample_rate * note_duration)

# Generate notes
for i, freq in enumerate(melody_freqs):
    start = i * samples_per_note * 1.5  # space between notes
    end = start + samples_per_note
    local_t = np.linspace(0, note_duration, samples_per_note, endpoint=False)
    wave = 0.25 * np.sin(2 * np.pi * freq * local_t) * np.exp(-3 * local_t)
    lead[start:end] += wave[:len(lead[start:end])]

# Normalize and export
lead = np.clip(lead, -1, 1)
lead_out = np.int16(lead * 32767)
lead_path = "lead_melody.wav"
write(lead_path, sample_rate, lead_out)

lead_path