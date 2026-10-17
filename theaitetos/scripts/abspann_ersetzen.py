"""Picture of video/Theaitetos.mp4 with the credits rendered anew from the current source
(src/scenes/credits.tsx) → out/theaitetos_bild.mp4 (no sound). scripts/stimme_ersetzen.py
takes its picture from there when the file exists.

    python3 scripts/abspann_ersetzen.py [--chrome /path/to/chrome-headless-shell]

Everything before the credits is copied unchanged; from the first keyframe of the credits
on, the frames are rendered with Remotion (needs `npm install`) and encoded to match.
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO = os.path.join(ROOT, 'video', 'Theaitetos.mp4')
OUT = os.path.join(ROOT, 'out', 'theaitetos_bild.mp4')
FPS = 30
CREDITS = round(26 * FPS)


def credits_from_source():
    """First credits frame as src/timeline.ts computes it from the current timing."""
    script = json.load(open(os.path.join(ROOT, 'src', 'data', 'script.json'), encoding='utf-8'))
    timing = json.load(open(os.path.join(ROOT, 'src', 'data', 'timing.json')))
    card, lead, gap, tail = round(2.6 * FPS), round(0.5 * FPS), math.floor(0.55 * FPS + 0.5), round(1.1 * FPS)
    cursor = 0
    for sc in script['scenes']:
        t = (card if sc.get('chapter') else 0) + lead
        for secs in timing[sc['id']]:
            t += math.ceil(secs * FPS) + gap
        cursor += t - gap + tail
    return cursor


def probe(*args):
    return subprocess.run(['ffprobe', '-v', 'error', *args], capture_output=True, text=True, check=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chrome', help='Chrome headless shell for Remotion (default: Remotion downloads one)')
    args = ap.parse_args()

    frames = int(probe('-select_streams', 'v:0', '-count_packets', '-show_entries', 'stream=nb_read_packets',
                       '-of', 'default=nw=1:nk=1', VIDEO).strip())
    start = frames - CREDITS                    # first credits frame in the rendered video
    keys = [round(float(t) * FPS) for t in probe('-select_streams', 'v:0', '-read_intervals',
                                                   f'{start / FPS - 1}%{frames / FPS}', '-skip_frame', 'nokey',
                                                   '-show_entries', 'frame=pts_time', '-of', 'default=nw=1:nk=1',
                                                   VIDEO).split()]
    key = min(k for k in keys if k >= start)    # copy everything before it unchanged
    src0 = credits_from_source() + (key - start)
    count = frames - key
    with tempfile.TemporaryDirectory() as tmp:
        head, raw, tail = (os.path.join(tmp, n) for n in ('head.mp4', 'raw.mp4', 'tail.mp4'))
        # by frame count: a time limit would also take the keyframe and the frame after it
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VIDEO, '-map', '0:v', '-c', 'copy',
                        '-frames:v', str(key), head], check=True)
        render = ['npx', 'remotion', 'render', 'Theaitetos', raw, f'--frames={src0}-{src0 + count - 1}',
                  '--codec=h264', '--crf=1', '--log=error']
        if args.chrome:
            render.append(f'--browser-executable={args.chrome}')
        subprocess.run(render, cwd=ROOT, check=True)
        timescale = probe('-select_streams', 'v:0', '-show_entries', 'stream=time_base', '-of', 'default=nw=1:nk=1',
                          VIDEO).strip().split('/')[1]
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-c:v', 'libx264', '-profile:v', 'high',
                        '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-r', str(FPS),
                        '-video_track_timescale', timescale, tail], check=True)
        lst = os.path.join(tmp, 'list.txt')
        with open(lst, 'w') as fh:
            fh.write(f"file '{head}'\nfile '{tail}'\n")
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                        '-movflags', '+faststart', OUT], check=True)
    n = int(probe('-select_streams', 'v:0', '-count_packets', '-show_entries', 'stream=nb_read_packets',
                  '-of', 'default=nw=1:nk=1', OUT).strip())
    print(f'{OUT}: {n} Bilder (Original {frames}), Abspann neu ab Bild {key}')
    if n != frames:
        raise SystemExit('Bildzahl weicht ab – nicht verwenden.')


if __name__ == '__main__':
    shutil.which('npx') or print('npx fehlt (Node.js).')
    main()
