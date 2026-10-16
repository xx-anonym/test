"""Spectrogram of the CC0 recording „Bat feeding buzz.wav“ (Kaldari 2020) for scene 9.5.

Writes assets/img/spectrogram_buzz.png: the bare spectrogram (no axes, no margins),
time 0–7.0 s (as heard, 10× slowed) left to right, frequency 0–8 kHz (as heard)
bottom to top. The scene draws the axes itself, with both scales (heard / real × 10).

    python tools/make_spectrogram.py
"""

import os

import numpy as np
from matplotlib import cm
from PIL import Image
from scipy.io import wavfile
from scipy.signal import spectrogram

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'audio', 'bat_feeding_buzz.wav')
OUT = os.path.join(ROOT, 'assets', 'img', 'spectrogram_buzz.png')
F_MAX = 8000.0     # Hz, as heard
DURATION = 7.0     # s, as heard
W, H = 1400, 500   # pixels


def main():
    rate, x = wavfile.read(SRC)
    x = x.astype(np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    x = x[: int(DURATION * rate)]
    f, t, s = spectrogram(x, fs=rate, nperseg=1024, noverlap=896, window='hann', mode='magnitude')
    keep = f <= F_MAX
    f, s = f[keep], s[keep]
    db = 20 * np.log10(s + 1e-12)
    top = np.percentile(db, 99.7)
    db = np.clip((db - (top - 45)) / 45, 0, 1)            # 45 dB dynamic range
    # resample onto a regular pixel grid
    ti = np.linspace(0, DURATION, W)
    fi = np.linspace(0, F_MAX, H)
    cols = np.clip(np.searchsorted(t, ti), 0, len(t) - 1)
    rows = np.clip(np.searchsorted(f, fi), 0, len(f) - 1)
    img = db[np.ix_(rows, cols)][::-1]                    # low frequencies at the bottom
    rgba = (cm.magma(img) * 255).astype(np.uint8)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    Image.fromarray(rgba).save(OUT)
    print(OUT, rgba.shape)


if __name__ == '__main__':
    main()
