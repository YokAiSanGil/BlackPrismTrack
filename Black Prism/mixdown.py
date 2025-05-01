from pydub import AudioSegment

# Load all stem files
rain = AudioSegment.from_wav("black_prism_true_rain.wav")
pad = AudioSegment.from_wav("pad_cminor.wav")
drums = AudioSegment.from_wav("drums_core.wav")
bass = AudioSegment.from_wav("bassline_dark.wav")
lead = AudioSegment.from_wav("lead_melody.wav")

# Match lengths
min_len = min(len(rain), len(pad), len(drums), len(bass), len(lead))
rain = rain[:min_len]
pad = pad[:min_len]
drums = drums[:min_len]
bass = bass[:min_len]
lead = lead[:min_len]

# Adjust volumes for blend (in dB)
rain = rain - 14
pad = pad - 6
drums = drums - 3
bass = bass - 4
lead = lead - 2

# Revised Black Prism structure — emotional focus
final_duration_ms = 80_000  # 2:30

def loop_trim(audio, target_ms):
    loops = (target_ms // len(audio)) + 1
    return (audio * loops)[:target_ms]

rain = loop_trim(rain, final_duration_ms) - 3
lead = loop_trim(lead, final_duration_ms) - 0  # Louder lead
bass = loop_trim(bass, final_duration_ms) - 14  # Softer bass
drums = loop_trim(drums, final_duration_ms) - 6

sec = 1000

# Build sections with timing tweaks
s0 = rain[:10*sec].fade_in(3000)                                 # 0–10s: Rain only
s1 = rain[10*sec:20*sec].overlay(lead[:10*sec])                  # 10–20s: Rain + Lead
s2 = lead[10*sec:30*sec].overlay(drums[:20*sec])                 # 20–40s: Add beat
s3 = lead[30*sec:50*sec].overlay(bass[:20*sec]) \
     .overlay(drums[20*sec:40*sec])                              # 40–60s: Bass joins
s4 = lead[50*sec:80*sec].overlay(bass[20*sec:50*sec]) \
     .overlay(drums[40*sec:70*sec])                              # 60–90s: Evolve
s5 = lead[80*sec:120*sec].overlay(bass[50*sec:90*sec]) \
     .overlay(drums[70*sec:110*sec])                             # 90–120s: Full pulse
s6 = lead[110*sec:150*sec].overlay(bass[90*sec:130*sec]) \
     .overlay(drums[110*sec:150*sec]).fade_out(6000)             # 120–150s: Fade out

final_mix = s0 + s1 + s2 + s3 + s4 + s5 + s6

# Export
final_mix_path = "01black_prism_mixdown.wav"
final_mix.export(final_mix_path, format="wav")