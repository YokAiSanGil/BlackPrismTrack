# Generate kick, snare, and hi-hat at 68 BPM using synthesis (drums_core.py)

import numpy as np
from scipy.io.wavfile import write

# Setup
sample_rate = 44100
bpm = 68
beat_duration = 60 / bpm  # seconds per beat
loop_bars = 4
beats_per_bar = 4
total_beats = loop_bars * beats_per_bar
duration = beat_duration * total_beats
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Empty drum track
drums = np.zeros_like(t)

# Utility: place sound at specific time
def place_sound(base, sound, start_time):
    start_index = int(start_time * sample_rate)
    end_index = start_index + len(sound)
    if end_index > len(base):
        end_index = len(base)
        sound = sound[:end_index - start_index]
    base[start_index:end_index] += sound
    return base

# Kick: 60Hz sine burst with decay
kick_t = np.linspace(0, 0.3, int(sample_rate * 0.3), endpoint=False)
kick = 0.6 * np.sin(2 * np.pi * 60 * kick_t) * np.exp(-20 * kick_t)

# Snare: white noise + 180Hz sine click
snare_t = np.linspace(0, 0.25, int(sample_rate * 0.25), endpoint=False)
snare = (0.4 * np.random.normal(0, 1, len(snare_t)) + 0.2 * np.sin(2 * np.pi * 180 * snare_t)) * np.exp(-10 * snare_t)

# Hi-hat: short white noise burst
hat_t = np.linspace(0, 0.05, int(sample_rate * 0.05), endpoint=False)
hat = 0.2 * np.random.normal(0, 1, len(hat_t)) * np.exp(-100 * hat_t)

# Place drums
for i in range(total_beats):
    current_time = i * beat_duration
    drums = place_sound(drums, kick, current_time)
    if i % 4 == 2:  # beat 2 and 4
        drums = place_sound(drums, snare, current_time)

# Place hi-hats on 8th notes
for i in range(total_beats * 2):
    current_time = i * (beat_duration / 2)
    drums = place_sound(drums, hat, current_time)

# Normalize and export
drums = np.clip(drums, -1, 1)
drum_out = np.int16(drums * 32767)
drum_path = "drums_core.wav"
write(drum_path, sample_rate, drum_out)

drum_path