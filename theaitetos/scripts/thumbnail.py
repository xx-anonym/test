"""Render the YouTube thumbnail: scripts/thumbnail.html → out/thumbnail.jpg (1280×720);
the published copy is video/thumbnail.jpg.

Needs `npm install` (fonts from @fontsource), a Chromium/Chrome (the headless shell keeps the
viewport exactly 1920×1080) and ffmpeg.
    python3 scripts/thumbnail.py [--chrome /path/to/chrome]
"""

import argparse
import os
import shutil
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chrome', default=shutil.which('chromium') or shutil.which('google-chrome') or 'chromium')
    ap.add_argument('--out', default=os.path.join(ROOT, 'out', 'thumbnail.jpg'))
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, 'thumbnail.png')
        subprocess.run([args.chrome, '--headless', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
                        '--allow-file-access-from-files', '--force-device-scale-factor=1',
                        '--virtual-time-budget=3000', '--window-size=1920,1080', f'--screenshot={png}',
                        'file://' + os.path.join(ROOT, 'scripts', 'thumbnail.html')],
                       check=True, capture_output=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', png, '-vf', 'scale=1280:720:flags=lanczos',
                        '-q:v', '2', args.out], check=True)
    print(args.out)


if __name__ == '__main__':
    main()
