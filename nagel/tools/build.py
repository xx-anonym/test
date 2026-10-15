"""Assemble chapters: narration track, subtitles, and the muxed video.

    python tools/build.py scene 3        # audio + srt + mp4 for chapter 3
    python tools/build.py final          # join all chapters into output/

The audio track and the subtitles are laid out from the same schedule that
drives the Manim scene (tools/timeline.py), so they line up by construction.
"""

import argparse
import json
import math
import os
import re
import subprocess
import wave

import numpy as np

from timeline import FPS, schedule

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARRATION = os.path.join(ROOT, 'audio', 'narration')
SCENE_AUDIO = os.path.join(ROOT, 'audio', 'scenes')
BUILD = os.path.join(ROOT, 'output', 'scenes')
RATE = 48000

SCENE_FILES = {
    0: 's00_prolog', 1: 's01_warum', 2: 's02_kontext', 3: 's03_kernthese', 4: 's04_argument',
    5: 's05_nicht', 6: 's06_vorlaeufer', 7: 's07_wirkung', 8: 's08_einwaende', 9: 's09_biologie',
    10: 's10_weg', 11: 's11_gegenwart', 12: 's12_fazit', 13: 's13_abspann',
}


def read_wav(path):
    with wave.open(path) as w:
        rate, ch = w.getframerate(), w.getnchannels()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1:
        a = a.reshape(-1, ch).mean(axis=1)
    if rate != RATE:
        from scipy.signal import resample_poly
        g = math.gcd(rate, RATE)
        a = resample_poly(a, RATE // g, rate // g).astype(np.float32)
    return a


def write_wav(path, a):
    a = np.clip(a, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes((a * 32767).astype(np.int16).tobytes())


def scene_audio(n):
    s = schedule(n)
    track = np.zeros(int(math.ceil(s['end'] * RATE)) + RATE, dtype=np.float32)

    def place(a, t):
        i = int(round(t * RATE))
        track[i:i + len(a)] += a[:len(track) - i]

    for p in s['paragraphs']:
        place(read_wav(os.path.join(NARRATION, f"{p['id']}.wav")), p['start'])
        if p['clip']:
            clip = read_wav(os.path.join(ROOT, p['clip']['file']))
            fade = int(0.05 * RATE)
            clip[:fade] *= np.linspace(0, 1, fade)
            clip[-fade:] *= np.linspace(1, 0, fade)
            place(clip * 0.9, p['clip']['start'])
    track = track[:int(round(s['end'] * RATE))]
    os.makedirs(SCENE_AUDIO, exist_ok=True)
    path = os.path.join(SCENE_AUDIO, f'{SCENE_FILES[n]}.wav')
    write_wav(path, track)
    return path, s


# ---------------------------------------------------------------- subtitles
MAX_CHARS = 80   # per cue (two lines)
LINE = 42        # per line


def _pieces(sentence):
    if len(sentence) <= MAX_CHARS:
        return [sentence]
    out, cur = [], ''
    for piece in re.split(r'(?<=[,;:–])\s+', sentence):
        if cur and len(cur) + 1 + len(piece) > MAX_CHARS:
            out.append(cur)
            cur = piece
        else:
            cur = f'{cur} {piece}'.strip()
    if cur:
        out.append(cur)
    # Every cue must wrap into two lines of at most LINE characters;
    # otherwise split it at the word boundary nearest its middle.
    final = []

    def add(p):
        if all(len(line) <= LINE for line in _wrap(p).split('\n')) or ' ' not in p:
            final.append(p)
            return
        mid = len(p) // 2
        cut = min((i for i, c in enumerate(p) if c == ' '), key=lambda i: abs(i - mid))
        add(p[:cut])
        add(p[cut + 1:])

    for p in out:
        add(p)
    return final


def _wrap(text):
    if len(text) <= LINE:
        return text
    words, best = text.split(), None
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        score = max(len(a), len(b))
        if best is None or score < best[0]:
            best = (score, f'{a}\n{b}')
    return best[1]


def cues(s, offset=0.0):
    out = []
    for p in s['paragraphs']:
        for sent in p['sentences']:
            pieces = _pieces(sent['text'])
            total = sum(len(x) for x in pieces)
            t = sent['start']
            for x in pieces:
                d = (sent['end'] - sent['start']) * len(x) / total
                out.append((offset + t, offset + t + d, _wrap(x)))
                t += d
    return out


def ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


def write_srt(path, items):
    with open(path, 'w', encoding='utf-8') as f:
        for i, (a, b, text) in enumerate(items, 1):
            f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{text}\n\n')


# --------------------------------------------------------------------- mux
def video_path(n):
    name = SCENE_FILES[n]
    return os.path.join(ROOT, 'media', 'videos', name, '1080p30', f'{name}.mp4')


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def build_scene(n):
    audio, s = scene_audio(n)
    os.makedirs(BUILD, exist_ok=True)
    name = SCENE_FILES[n]
    srt = os.path.join(BUILD, f'{name}.srt')
    write_srt(srt, cues(s))
    video = video_path(n)
    vdur = duration(video)
    if abs(vdur - s['end']) > 1.5 / FPS:
        print(f'WARNUNG: Video {vdur:.3f} s, Zeitplan {s["end"]:.3f} s')
    out = os.path.join(BUILD, f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', audio,
                    '-filter:a', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(RATE), '-ac', '2',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
    print(f'{out}  ({duration(out):.2f} s, Zeitplan {s["end"]:.2f} s)')
    print(srt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['scene', 'final'])
    ap.add_argument('chapters', nargs='*', type=int)
    args = ap.parse_args()
    if args.what == 'scene':
        for n in args.chapters:
            build_scene(n)
    else:
        raise SystemExit('final: folgt in der Produktionsphase')


if __name__ == '__main__':
    main()
