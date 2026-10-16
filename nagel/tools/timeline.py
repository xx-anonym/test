"""One schedule per chapter, shared by the Manim scene, the audio track and
the subtitles, so picture, voice and text cannot drift apart.

A chapter runs:  [card] LEAD  para₁  GAP  para₂ … paraₙ  TAIL
A paragraph with a sound clip is followed by CLIP_PAD, the clip, CLIP_PAD.
All times are seconds from the start of the chapter video.
"""

import json
import os

from script_parse import chapter as load_chapter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMING = os.path.join(ROOT, 'audio', 'timing.json')

FPS = 30
CARD = 3.0        # chapter card (silent)
LEAD = 0.6        # after the card, before the voice starts
GAP = 0.7         # between paragraphs
TAIL = 1.5        # after the last paragraph
CLIP_PAD = 0.6    # silence around a sound clip
TAIL_EXTRA = {12: 3.0}   # let the closing image of the last chapter stand a little longer

# Sound clips by paragraph id: file and length in seconds.
CLIPS = {
    '9.5': {'file': 'assets/audio/bat_feeding_buzz.wav', 'duration': 7.0},
}


def snap(t: float) -> float:
    """Round to the frame grid so audio and video agree exactly."""
    return round(round(t * FPS) / FPS, 4)


def schedule(n: int, timing: dict | None = None) -> dict:
    timing = timing if timing is not None else json.load(open(TIMING))
    chap = load_chapter(n)
    card = n != 0  # the prologue has its own title card instead
    t = (CARD if card else 0.0) + LEAD
    paras = []
    for p in chap['paragraphs']:
        info = timing[p['id']]
        start = snap(t)
        sentences = [{'text': s['text'], 'start': snap(start + s['start']), 'end': snap(start + s['end'])}
                     for s in info['sentences']]
        end = snap(start + info['duration'])
        entry = {'id': p['id'], 'start': start, 'end': end, 'sentences': sentences,
                 'cites': p['cites'], 'quotes': p['quotes'], 'clip': None}
        t = end
        if p['id'] in CLIPS:
            clip = CLIPS[p['id']]
            cs = snap(t + CLIP_PAD)
            entry['clip'] = {'file': clip['file'], 'start': cs, 'end': snap(cs + clip['duration'])}
            t = entry['clip']['end'] + CLIP_PAD
        paras.append(entry)
        t += GAP
    end = snap(t - GAP + TAIL + TAIL_EXTRA.get(n, 0.0))
    return {'chapter': n, 'title': chap['title'], 'card': card, 'card_end': CARD if card else 0.0,
            'paragraphs': paras, 'end': end}


if __name__ == '__main__':
    import sys
    print(json.dumps(schedule(int(sys.argv[1])), ensure_ascii=False, indent=1))
