import numpy as np
import soundfile as sf
from scipy.signal import stft, istft

# 1. Load audio file

x, fs = sf.read("input.wav")

# Convert stereo to mono using L-R (center channel removal)
if x.ndim > 1:
    L = x[:, 0]
    R = x[:, 1]
    x = (L - R) * 0.5  # prevent amplitude blow-up

# 2. Apply STFT

f, t, Zxx = stft(
    x,
    fs=fs,
    nperseg=1024,
    noverlap=512,
    window='hann'
)

# 3. Create smooth frequency mask

M = np.ones_like(Zxx)

alpha = 0.1  # attenuation factor

for i, freq in enumerate(f):
    # Smooth transition (avoid hard cutoff)
    if 150 < freq < 200:
        M[i, :] = np.linspace(1, alpha, Zxx.shape[1])
    elif 200 <= freq <= 3000:
        M[i, :] = alpha
    elif 3000 < freq < 3500:
        M[i, :] = np.linspace(alpha, 1, Zxx.shape[1])

# 4. Apply mask

Zxx_filtered = Zxx * M

# 5. Inverse STFT

_, y = istft(
    Zxx_filtered,
    fs=fs,
    nperseg=1024,
    noverlap=512,
    window='hann'
)

# 6. Normalize (avoid clipping)

y = y / np.max(np.abs(y) + 1e-6)

# 7. Save output

sf.write("output.wav", y, fs)
