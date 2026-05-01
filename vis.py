import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.signal import stft

# ======================
# Load files
# ======================
x_in, fs = sf.read("input.wav")
x_out, _ = sf.read("output.wav")
# Limit duration to avoid OOM (use only first 10 seconds)
x_in = x_in[:fs*10]
x_out = x_out[:fs*10]

# mono 변환
if x_in.ndim > 1:
    x_in = x_in[:,0]
if x_out.ndim > 1:
    x_out = x_out[:,0]

# ======================
# STFT function
# ======================
def compute_spectrogram(x):
    f, t, Z = stft(x, fs=fs, nperseg=512, noverlap=256)
    S = 20*np.log10(np.abs(Z) + 1e-6)
    return f, t, S

f1, t1, S1 = compute_spectrogram(x_in)
f2, t2, S2 = compute_spectrogram(x_out)

# ======================
# Plot
# ======================
plt.figure(figsize=(12,8))

# Input waveform
plt.subplot(2,2,1)
plt.plot(x_in)
plt.title("Input Waveform")

# Output waveform
plt.subplot(2,2,2)
plt.plot(x_out)
plt.title("Output Waveform")

# Input spectrogram
plt.subplot(2,2,3)
plt.pcolormesh(t1, f1, S1, shading='gouraud')
plt.title("Input Spectrogram")
plt.ylabel("Frequency (Hz)")
plt.xlabel("Time (s)")

# Output spectrogram
plt.subplot(2,2,4)
plt.pcolormesh(t2, f2, S2, shading='gouraud')
plt.title("Output Spectrogram")
plt.ylabel("Frequency (Hz)")
plt.xlabel("Time (s)")

plt.tight_layout()
plt.savefig("result.png")
