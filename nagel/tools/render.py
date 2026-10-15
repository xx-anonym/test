"""Build one or more chapters end to end: voice, animation, audio, subtitles.

    python tools/render.py 3            # chapter 3
    python tools/render.py 3 4 --verify # with Whisper check of the voice

Needs the Piper voice at voices/de_DE-thorsten-high.onnx (see README) or the
path in the environment variable PIPER_MODEL.
"""

import argparse
import os
import subprocess
import sys

from build import SCENE_FILES, build_scene

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('chapters', nargs='+', type=int)
    ap.add_argument('--verify', action='store_true', help='check every sentence with Whisper')
    ap.add_argument('--skip-tts', action='store_true')
    args = ap.parse_args()
    model = os.environ.get('PIPER_MODEL', os.path.join(ROOT, 'voices', 'de_DE-thorsten-high.onnx'))
    if not args.skip_tts:
        cmd = [PY, os.path.join(ROOT, 'tools', 'tts.py'), '--model', model, '--chapters', *map(str, args.chapters)]
        subprocess.run(cmd + (['--verify'] if args.verify else []), check=True)
    for n in args.chapters:
        name = SCENE_FILES[n]
        cls = f'Kapitel{n}'
        subprocess.run([PY, '-m', 'manim', 'render', '--config_file', 'manim.cfg', '--progress_bar', 'none',
                        '-o', name, f'{name}.py', cls], cwd=os.path.join(ROOT, 'scenes'), check=True)
        build_scene(n)


if __name__ == '__main__':
    main()
