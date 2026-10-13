"""Generate a quiet ambient pad (public/music/pad.wav) to sit under the narration.

Slowly cross-fading chords built from soft sine partials, a gentle
low-pass and a simple synthetic reverb. Deterministic (fixed seed).
"""

import os
import wave

import numpy as np

SR = 44100
CHORD_SECONDS = 16.0
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public', 'music', 'pad.wav')

# MIDI notes: Dm9 – Bbmaj7 – Fmaj9 – C(add9)/E – Gm9 – Bbmaj7 – Dm(add9) – A7sus4
CHORDS = [
    [38, 50, 53, 57, 64],
    [34, 46, 50, 53, 57],
    [41, 53, 57, 60, 67],
    [40, 48, 55, 60, 62],
    [43, 55, 58, 62, 69],
    [34, 46, 53, 57, 62],
    [38, 50, 57, 62, 64],
    [33, 45, 52, 57, 62],
]


def hz(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def chord(notes, seconds, rng):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for k, m in enumerate(notes):
        f0 = hz(m)
        amp = 0.22 if k == 0 else 0.13
        for h, ha in [(1, 1.0), (2, 0.28), (3, 0.08)]:
            for det, pan in [(-0.06, 0.25), (0.06, 0.75)]:
                ph = rng.uniform(0, 2 * np.pi)
                lfo = 1 + 0.15 * np.sin(2 * np.pi * rng.uniform(0.03, 0.08) * t + ph)
                sig = np.sin(2 * np.pi * (f0 * h + det * h) * t + ph) * amp * ha * lfo
                out[:, 0] += sig * (1 - pan)
                out[:, 1] += sig * pan
    # slow swell envelope
    env = np.sin(np.pi * np.clip(t / seconds, 0, 1)) ** 1.6
    return out * env[:, None]


def lowpass(x, cutoff=1800.0):
    """Gentle 2nd-order-like roll-off applied in the frequency domain."""
    freqs = np.fft.rfftfreq(len(x), 1 / SR)
    gain = 1 / np.sqrt(1 + (freqs / cutoff) ** 4)
    return np.stack([np.fft.irfft(np.fft.rfft(x[:, c]) * gain, len(x)) for c in range(x.shape[1])], axis=1)


def reverb(x, rng, seconds=4.5, mix=0.45):
    n = int(seconds * SR)
    ir_t = np.arange(n) / SR
    out = np.zeros((len(x) + n, 2))
    for c in range(2):
        ir = rng.normal(0, 1, n) * np.exp(-ir_t * 6.9 / seconds)
        ir /= np.sqrt(np.sum(ir**2))
        wet = np.fft.irfft(np.fft.rfft(x[:, c], len(x) + n) * np.fft.rfft(ir, len(x) + n), len(x) + n)
        out[:, c] = wet * mix
    out[: len(x)] += x * (1 - mix)
    return out


def main():
    rng = np.random.default_rng(399)
    step = int(CHORD_SECONDS * SR)
    seg_len = int(CHORD_SECONDS * 1.6 * SR)
    total = step * len(CHORDS) + seg_len
    mix = np.zeros((total, 2))
    for i, notes in enumerate(CHORDS):
        c = chord(notes, CHORD_SECONDS * 1.6, rng)
        mix[i * step : i * step + len(c)] += c
    # make the loop seamless: fold the tail back onto the start
    loop_len = step * len(CHORDS)
    mix[: total - loop_len] += mix[loop_len:]
    mix = mix[:loop_len]
    mix = lowpass(mix, 1500.0)
    wet = reverb(mix, rng)
    wet[: len(wet) - loop_len] += wet[loop_len:]
    wet = wet[:loop_len]
    wet /= np.max(np.abs(wet)) / 0.7
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with wave.open(OUT, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((wet * 32767).astype(np.int16).tobytes())
    print(f'{OUT}: {loop_len / SR:.0f}s loop')


if __name__ == '__main__':
    main()
