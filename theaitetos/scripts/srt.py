"""Write German subtitles (out/theaitetos.srt) from the script and measured timing.

Mirrors the frame layout in src/timeline.ts; within a segment, time is shared
between sentences in proportion to their length.
"""

import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
CARD = round(2.6 * FPS)
LEAD = round(0.5 * FPS)
GAP = math.floor(0.55 * FPS + 0.5)  # JS Math.round
TAIL = round(1.1 * FPS)
PAUSE = 0.38  # sentence pause used by scripts/tts.py
MAX_CHARS = 84


def ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


def chunks(sentence: str):
    """Split long sentences at commas/semicolons into readable pieces."""
    if len(sentence) <= MAX_CHARS:
        return [sentence]
    parts, cur = [], ''
    for piece in re.split(r'(?<=[,;:])\s+', sentence):
        if cur and len(cur) + len(piece) + 1 > MAX_CHARS:
            parts.append(cur)
            cur = piece
        else:
            cur = f'{cur} {piece}'.strip()
    if cur:
        parts.append(cur)
    return parts


def wrap(text: str) -> str:
    if len(text) <= 42:
        return text
    words, best = text.split(), None
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        score = max(len(a), len(b))
        if best is None or score < best[0]:
            best = (score, f'{a}\n{b}')
    return best[1]


def main():
    script = json.load(open(os.path.join(ROOT, 'src/data/script.json'), encoding='utf-8'))
    timing = json.load(open(os.path.join(ROOT, 'src/data/timing.json')))
    cues = []
    cursor = 0
    for scene in script['scenes']:
        t = (CARD if scene.get('chapter') else 0) + LEAD
        for seg, secs in zip(scene['segments'], timing[scene['id']]):
            start = (cursor + t) / FPS
            sentences = [s for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„])', seg['text']) if s]
            speak = secs - PAUSE * (len(sentences) - 1)
            total_chars = sum(len(s) for s in sentences)
            clock = start
            for sen in sentences:
                dur = speak * len(sen) / total_chars
                pieces = chunks(sen)
                pc = sum(len(p) for p in pieces)
                for p in pieces:
                    d = dur * len(p) / pc
                    cues.append((clock, clock + d, p))
                    clock += d
                clock += PAUSE
            t += math.ceil(secs * FPS) + GAP
        cursor += t - GAP + TAIL
    out = os.path.join(ROOT, 'out', 'theaitetos.srt')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as fh:
        for i, (a, b, text) in enumerate(cues, 1):
            fh.write(f'{i}\n{ts(a)} --> {ts(b - 0.05)}\n{wrap(text)}\n\n')
    print(f'{out}: {len(cues)} cues, last ends {ts(cues[-1][1])}, video narration ends ~{ts(cursor / FPS)}')


if __name__ == '__main__':
    main()
