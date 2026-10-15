"""Quality check: transcribe the synthesised narration with Whisper and list
words that differ from the script, to catch mispronunciations.

Usage: python tools/asr_check.py 3.1 3.2 …   (or a chapter: --chapter 3)

Differences are hints, not errors: Whisper also mishears names or writes
numbers as digits. Every flagged word should be listened to.
"""

import argparse
import difflib
import json
import os
import re
import wave

import numpy as np
from scipy.signal import resample_poly

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARRATION = os.path.join(ROOT, 'audio', 'narration')
TIMING = os.path.join(ROOT, 'audio', 'timing.json')


def load(path: str) -> np.ndarray:
    with wave.open(path) as w:
        rate = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    g = np.gcd(rate, 16000)
    return resample_poly(a, 16000 // g, rate // g).astype(np.float32)


def words(text: str):
    text = re.sub(r'[^\wÄÖÜäöüß\s-]', ' ', text.lower())
    return text.replace('-', ' ').split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ids', nargs='*')
    ap.add_argument('--chapter', type=int)
    ap.add_argument('--model', default='small')
    args = ap.parse_args()

    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device='cpu', compute_type='int8')
    timing = json.load(open(TIMING))
    ids = args.ids or [k for k in timing if args.chapter is not None and k.split('.')[0] == str(args.chapter)]
    for pid in ids:
        ref = ' '.join(s['text'] for s in timing[pid]['sentences'])
        segs, _ = model.transcribe(load(os.path.join(NARRATION, f'{pid}.wav')), language='de', beam_size=5)
        hyp = ' '.join(s.text.strip() for s in segs)
        a, b = words(ref), words(hyp)
        diffs = [(' '.join(a[i1:i2]), ' '.join(b[j1:j2]))
                 for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes() if op != 'equal']
        print(f'## {pid}  ({len(diffs)} Abweichungen)')
        print('   gehört:', hyp)
        for r, h in diffs:
            print(f'   Skript „{r}“  →  Whisper „{h}“')


if __name__ == '__main__':
    main()
