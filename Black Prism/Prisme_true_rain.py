# Re-import numpy in case the session lost its state
import numpy as np
from scipy.io.wavfile import write

# Confirm numpy is now available and functional
"numpy reloaded and ready"

# Define audio settings and time vector
sample_rate = 44100
duration = 32  # duration in seconds
t_long = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Final rain architecture: fully desynchronized noise with staggered modulation and no smoothing

# Layer 1: baseline granular static
noise1 = np.random.normal(0, 0.07, len(t_long))
mod1 = np.random.uniform(0.4, 1.0, len(t_long))
layer1 = noise1 * mod1

# Layer 2: high detail texture with jitter
noise2 = np.random.normal(0, 0.04, len(t_long))
jitter_points = np.random.randint(0, len(t_long), size=4000)
mod2 = np.ones(len(t_long))
mod2[jitter_points] = np.random.uniform(0.2, 1.5, size=len(jitter_points))
layer2 = noise2 * mod2

# Layer 3: rumble — long, slow randomness
noise3 = np.random.normal(0, 0.03, len(t_long))
random_chunks = np.split(noise3, 64)
mod3 = np.concatenate([chunk * np.random.uniform(0.5, 1.5) for chunk in random_chunks])
layer3 = mod3[:len(t_long)]

# Combine all noise layers
true_rain = layer1 + layer2 + layer3
true_rain = np.clip(true_rain, -1, 1)
true_rain_out = np.int16(true_rain * 32767)

# Export final de-patterned rain
true_rain_path = "black_prism_true_rain.wav"
write(true_rain_path, sample_rate, true_rain_out)

true_rain_path