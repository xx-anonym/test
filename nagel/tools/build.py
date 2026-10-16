"""Assemble chapters: narration track, subtitles, and the muxed video.

    python tools/build.py scene 3        # audio + srt + mp4 for chapter 3
    python tools/build.py final          # join all chapters into output/ (video, srt)

The audio track and the subtitles are laid out from the same schedule that
drives the Manim scene (tools/timeline.py), so they line up by construction.
"""

import argparse
import json
import math
import os
import re
import shutil
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


CREDITS = 13      # the credits have no narration; their length comes from the video


def scene_audio(n):
    if n == CREDITS:
        end = round(duration(video_path(n)) * FPS) / FPS
        s = {'paragraphs': [], 'end': end}
        os.makedirs(SCENE_AUDIO, exist_ok=True)
        path = os.path.join(SCENE_AUDIO, f'{SCENE_FILES[n]}.wav')
        write_wav(path, np.zeros(int(round(end * RATE)), dtype=np.float32))
        return path, s
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
MAX_CHARS = 84   # per cue (two lines)
LINE = 42        # per line


def _pieces(sentence):
    if len(sentence) <= MAX_CHARS:
        out = [sentence]
    else:
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
        spaces = [i for i, c in enumerate(p) if c == ' ']
        commas = [i for i in spaces if p[i - 1] in ',;:' and 0.25 < i / len(p) < 0.75]
        cut = min(commas or spaces, key=lambda i: abs(i - mid))   # prefer a comma near the middle
        add(p[:cut])
        add(p[cut + 1:])

    for p in out:
        add(p)
    # A very short tail („ist offen.“) reads better together with the cue before it.
    merged = []
    for p in final:
        if merged and len(p) < 16:
            both = f'{merged[-1]} {p}'
            if len(both) <= MAX_CHARS and all(len(line) <= LINE for line in _wrap(both).split('\n')):
                merged[-1] = both
                continue
        merged.append(p)
    return merged


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


def frames(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets',
                          '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', path],
                         capture_output=True, text=True, check=True).stdout
    return int(out.strip())


def chapter_layout():
    """[(chapter, start in the final video, length)] from the rendered chapter videos."""
    out, t = [], 0.0
    for n in sorted(SCENE_FILES):
        length = frames(video_path(n)) / FPS
        out.append((n, t, length))
        t += length
    return out


def build_final():
    """Join all chapters: video streams copied, one continuous narration track
    (loudness-normalised once), and one subtitle file with chapter offsets."""
    out_dir = os.path.join(ROOT, 'output')
    parts, track, items, t = [], [], [], 0.0
    for n in sorted(SCENE_FILES):
        video = video_path(n)
        if not os.path.exists(video):
            raise SystemExit(f'Kapitel {n} fehlt: {video}')
        audio, s = scene_audio(n)
        length = frames(video) / FPS
        a = read_wav(audio)
        a = np.pad(a, (0, max(0, int(round(length * RATE)) - len(a))))[:int(round(length * RATE))]
        track.append(a)
        items += cues(s, offset=t)
        parts.append(video)
        print(f'  {SCENE_FILES[n]:16s} {length:7.2f} s   ab {t:7.2f} s')
        t += length
    wav = os.path.join(SCENE_AUDIO, 'gesamt.wav')
    write_wav(wav, np.concatenate(track))
    lst = os.path.join(SCENE_AUDIO, 'concat.txt')
    with open(lst, 'w') as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    silent = os.path.join(SCENE_AUDIO, 'gesamt_video.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-an', '-c', 'copy',
                    silent], check=True)
    final = os.path.join(out_dir, 'nagel_fledermaus.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', wav,
                    '-filter:a', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(RATE), '-ac', '2',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', final],
                   check=True)
    # The synthetic-voice version is also the picture source for tools/stimme_ersetzen.py.
    shutil.copy2(final, os.path.join(out_dir, 'nagel_fledermaus_piper.mp4'))
    srt = os.path.join(out_dir, 'untertitel.srt')
    write_srt(srt, items)
    print(f'{final}  ({duration(final):.2f} s, Summe der Kapitel {t:.2f} s)')
    print(f'{srt}  ({len(items)} Untertitel)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['scene', 'final'])
    ap.add_argument('chapters', nargs='*', type=int)
    args = ap.parse_args()
    if args.what == 'scene':
        for n in args.chapters:
            build_scene(n)
    else:
        build_final()


if __name__ == '__main__':
    main()
