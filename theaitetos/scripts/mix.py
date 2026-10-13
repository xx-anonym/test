"""Build the final soundtrack and mux it with the rendered video.

1. Places every narration segment at its frame position (same layout as
   src/timeline.ts) -> out/voice.wav
2. Mixes in the looped ambient pad, ducked under the voice, normalises to
   -16 LUFS and muxes with the video stream -> out/theaitetos.mp4

usage: python3 scripts/mix.py out/theaitetos_voice.mp4 [--music-db -24]
"""

import argparse
import json
import math
import os
import subprocess
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
CARD = round(2.6 * FPS)
LEAD = round(0.5 * FPS)
GAP = math.floor(0.55 * FPS + 0.5)
TAIL = round(1.1 * FPS)
CREDITS = round(26 * FPS)


def build_voice(timing_path: str | None = None) -> tuple[str, float]:
    script = json.load(open(os.path.join(ROOT, 'src/data/script.json'), encoding='utf-8'))
    # Positions must follow the timing the video was rendered with.
    timing = json.load(open(timing_path or os.path.join(ROOT, 'src/data/timing.json')))
    placements, cursor, rate = [], 0, None
    for scene in script['scenes']:
        t = (CARD if scene.get('chapter') else 0) + LEAD
        for i, secs in enumerate(timing[scene['id']]):
            placements.append(((cursor + t) / FPS, os.path.join(ROOT, 'public/audio', f"{scene['id']}-{i}.wav")))
            t += math.ceil(secs * FPS) + GAP
        cursor += t - GAP + TAIL
    total = (cursor + CREDITS) / FPS
    track = None
    for start, path in placements:
        with wave.open(path) as w:
            rate = rate or w.getframerate()
            if track is None:
                track = np.zeros(int(total * rate) + rate, dtype=np.int32)
            data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        a = int(round(start * rate))
        track[a : a + len(data)] += data
    out = os.path.join(ROOT, 'out', 'voice.wav')
    with wave.open(out, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(np.clip(track, -32768, 32767).astype(np.int16).tobytes())
    return out, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('--music-db', type=float, default=-24.0, help='pad gain relative to its own level')
    ap.add_argument('--out', default=os.path.join(ROOT, 'out', 'theaitetos.mp4'))
    ap.add_argument('--timing', help='timing.json used for the video render (default: src/data/timing.json)')
    args = ap.parse_args()

    voice, total = build_voice(args.timing)
    pad = os.path.join(ROOT, 'public/music/pad.wav')
    gain = 10 ** (args.music_db / 20)
    graph = (
        '[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[v][sc];'
        f'[2:a]aresample=48000,highpass=f=70,volume={gain:.4f},atrim=0:{total:.3f},'
        f'afade=t=in:d=5,afade=t=out:st={total - 10:.3f}:d=10[m];'
        '[m][sc]sidechaincompress=threshold=0.02:ratio=5:attack=200:release=1500:makeup=1[md];'
        '[v][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]'
    )
    cmd = [
        'ffmpeg', '-y', '-v', 'error', '-stats',
        '-i', args.video, '-i', voice, '-stream_loop', '-1', '-i', pad,
        '-filter_complex', graph,
        '-map', '0:v', '-map', '[a]',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
        '-t', f'{total:.3f}', args.out,
    ]
    subprocess.run(cmd, check=True)
    print(args.out)


if __name__ == '__main__':
    main()
