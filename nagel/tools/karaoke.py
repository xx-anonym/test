"""Karaoke subtitles as a guide for recording the narration yourself.

    python tools/karaoke.py words    # word times from the existing recordings (Whisper), cached
    python tools/karaoke.py ass      # output/karaoke.ass for the whole video
    python tools/karaoke.py video    # output/sprechervorlage.mp4: picture + karaoke, no sound
    python tools/karaoke.py          # all three

Every word lights up at the moment the current narration says it, so a speaker who
follows the highlight stays in sync with the animation. Word times come from
faster-whisper word timestamps on each recorded sentence, aligned to the script
words; words Whisper does not recognise are interpolated between their neighbours.
The ASS file shows the line a moment before it is due, the following line dimmed
underneath, the paragraph number top right (for retakes) and a note during the
sound example in chapter 9.
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np
from num2words import num2words

from build import SCENE_FILES, _pieces, _wrap, chapter_layout
from textnorm import spoken
from timeline import schedule

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARRATION = os.path.join(ROOT, 'audio', 'narration')
TIMING = os.path.join(ROOT, 'audio', 'timing.json')
WORDS = os.path.join(ROOT, 'audio', 'words.json')
ASS = os.path.join(ROOT, 'output', 'karaoke.ass')
GUIDE = os.path.join(ROOT, 'output', 'sprechervorlage.mp4')
FINAL = os.path.join(ROOT, 'output', 'nagel_fledermaus.mp4')

LEAD = 0.8        # a line appears this long before its first word
HOLD = 0.35       # and stays this long after its last word
NEXT_WINDOW = 6.0  # show the following line if it starts within this many seconds


# ------------------------------------------------------------ word timing
def _norm_words(text):
    """Lower-case letter sequences; numbers spelled out; hyphens split words."""
    text = text.lower().replace('-', ' ')
    text = re.sub(r'\b(1[89]\d\d|20\d\d)\b', lambda m: num2words(int(m.group(1)), lang='de', to='year'), text)
    text = re.sub(r'\d+', lambda m: num2words(int(m.group(0)), lang='de'), text)
    return re.sub(r'[^a-zäöüß\s]', ' ', text).split()


def _similar(a, b):
    return a == b or difflib.SequenceMatcher(a=a, b=b).ratio() >= 0.7


def _align(ref, hyp):
    """Needleman-Wunsch on word lists; returns {ref index: hyp index} for similar pairs."""
    n, m = len(ref), len(hyp)
    score = np.zeros((n + 1, m + 1))
    score[:, 0] = -np.arange(n + 1)
    score[0, :] = -np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = score[i - 1, j - 1] + (2 if _similar(ref[i - 1], hyp[j - 1]) else -1)
            score[i, j] = max(match, score[i - 1, j] - 1, score[i, j - 1] - 1)
    pairs, i, j = {}, n, m
    while i > 0 and j > 0:
        if score[i, j] == score[i - 1, j - 1] + (2 if _similar(ref[i - 1], hyp[j - 1]) else -1):
            if _similar(ref[i - 1], hyp[j - 1]):
                pairs[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif score[i, j] == score[i - 1, j] - 1:
            i -= 1
        else:
            j -= 1
    return pairs


def token_times(sentence, start, end, hyp_words):
    """Start time of every whitespace token of the sentence (seconds, paragraph-relative).

    hyp_words: [(word, start, end)] from Whisper, already paragraph-relative.
    """
    tokens = sentence.split()
    subs, owner = [], []
    for k, tok in enumerate(tokens):
        for w in _norm_words(spoken(tok)) or ['_']:
            subs.append(w)
            owner.append(k)
    hyp = []
    for w, a, b in hyp_words:
        for x in _norm_words(w) or ['_']:
            hyp.append((x, a, b))
    pairs = _align(subs, [h[0] for h in hyp])
    weight = [max(1, len(''.join(_norm_words(spoken(t))))) for t in tokens]
    known = {}
    for i, j in pairs.items():
        k = owner[i]
        if k not in known and (i == 0 or owner[i - 1] != k):     # first sub-word of the token
            known[k] = hyp[j][1]
    # anchors at both ends, then interpolate by spoken length
    times = [None] * len(tokens)
    for k, t in known.items():
        times[k] = min(max(t, start), end)
    if times[0] is None:
        times[0] = start
    anchors = [k for k, t in enumerate(times) if t is not None] + [len(tokens)]
    tail = end
    for a, b in zip(anchors[:-1], anchors[1:]):
        t0 = times[a]
        t1 = times[b] if b < len(tokens) else tail
        span = sum(weight[a:b])
        acc = 0
        for k in range(a + 1, b):
            acc += weight[k - 1]
            times[k] = t0 + (t1 - t0) * acc / span
    for k in range(1, len(times)):                               # keep them in order
        times[k] = max(times[k], times[k - 1] + 0.05)
    return times


def compute_words(model_name='medium'):
    from faster_whisper import WhisperModel
    from scipy.signal import resample_poly
    timing = json.load(open(TIMING))
    cache = json.load(open(WORDS)) if os.path.exists(WORDS) else {}
    model = None
    for pid, info in sorted(timing.items(), key=lambda kv: [int(x) for x in kv[0].split('.')]):
        if cache.get(pid, {}).get('hash') == info['hash']:
            continue
        if model is None:
            model = WhisperModel(model_name, device='cpu', compute_type='int8')
        with wave.open(os.path.join(NARRATION, f'{pid}.wav')) as w:
            rate = w.getframerate()
            audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        g = np.gcd(rate, 16000)
        sents = []
        for s in info['sentences']:
            a0 = max(0.0, s['start'] - 0.05)
            seg = audio[int(a0 * rate): int((s['end'] + 0.05) * rate)]
            seg = resample_poly(seg, 16000 // g, rate // g).astype(np.float32)
            segments, _ = model.transcribe(seg, language='de', beam_size=5, word_timestamps=True,
                                           condition_on_previous_text=False)
            hyp = [(w.word.strip(), a0 + w.start, a0 + w.end) for sg in segments for w in (sg.words or [])]
            sents.append({'text': s['text'], 'tokens': token_times(s['text'], s['start'], s['end'], hyp),
                          'matched': len(hyp)})
        cache[pid] = {'hash': info['hash'], 'sentences': sents}
        json.dump(cache, open(WORDS, 'w'), ensure_ascii=False, indent=1)
        print(pid, 'ok', flush=True)
    return cache


# ------------------------------------------------------------ ASS
HEADER = """[Script Info]
Title: Sprechervorlage – Wie ist es, eine Fledermaus zu sein?
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Inter,58,&H004BA6DB,&H00DCE6EB,&H30100C0A,&H00000000,-1,0,0,0,100,100,0,0,3,16,0,2,80,80,120,1
Style: Naechste,Inter,36,&H00A1938B,&H00A1938B,&H30100C0A,&H00000000,0,0,0,0,100,100,0,0,3,10,0,2,80,80,30,1
Style: Info,Inter,30,&H004BA6DB,&H004BA6DB,&H30100C0A,&H00000000,-1,0,0,0,100,100,0,0,3,10,0,9,40,40,30,1
Style: Pause,Inter,52,&H00DCE6EB,&H00DCE6EB,&H30100C0A,&H00000000,-1,0,0,0,100,100,0,0,3,18,0,5,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _t(sec):
    cs = int(round(max(0.0, sec) * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f'{h}:{m:02}:{s:02}.{cs:02}'


def _esc(text):
    return text.replace('{', '(').replace('}', ')')


def chapter_offsets():
    layout = chapter_layout()
    return {n: t for n, t, _ in layout}, layout[-1][1] + layout[-1][2]


def build_lines(words):
    """All karaoke cues of the video: (start of first word, end, [(word, start)], paragraph id)."""
    offs, total = chapter_offsets()
    lines, paras, clips = [], [], []
    for n in sorted(SCENE_FILES):
        if n == 13:
            continue
        s = schedule(n)
        for p in s['paragraphs']:
            base = offs[n] + p['start']
            paras.append((p['id'], offs[n] + p['start'], offs[n] + p['end']))
            if p['clip']:
                clips.append((offs[n] + p['clip']['start'], offs[n] + p['clip']['end']))
            for sent, w in zip(p['sentences'], words[p['id']]['sentences']):
                toks = sent['text'].split()
                times = [base + x for x in w['tokens']]
                sent_end = offs[n] + sent['end']
                k = 0
                for piece in _pieces(sent['text']):
                    count = len(piece.split())
                    items = list(zip(toks[k:k + count], times[k:k + count]))
                    end = times[k + count] if k + count < len(times) else sent_end
                    lines.append({'start': items[0][1], 'end': end, 'items': items, 'text': piece, 'pid': p['id']})
                    k += count
    return lines, paras, clips, total


def karaoke_text(line, shown_from):
    """\\kf tags in centiseconds; a silent lead-in before the first word, line breaks as in the SRT."""
    wrapped = _wrap(line['text'])
    first_line_words = len(wrapped.split('\n')[0].split())
    parts = [f'{{\\k{int(round((line["items"][0][1] - shown_from) * 100))}}}']
    items = line['items']
    for i, (word, t0) in enumerate(items):
        t1 = items[i + 1][1] if i + 1 < len(items) else line['end']
        sep = '\\N' if i + 1 == first_line_words and '\n' in wrapped else (' ' if i + 1 < len(items) else '')
        parts.append(f'{{\\kf{max(1, int(round((t1 - t0) * 100)))}}}{_esc(word)}{sep}')
    return ''.join(parts)


def write_ass(words):
    lines, paras, clips, total = build_lines(words)
    events = []
    shown = []
    for i, ln in enumerate(lines):
        start = ln['start'] - LEAD
        if shown:
            start = max(start, shown[-1][1])
        nxt = lines[i + 1]['start'] - LEAD if i + 1 < len(lines) else ln['end'] + HOLD
        end = min(ln['end'] + HOLD, max(nxt, ln['end']))
        shown.append((start, end))
    for i, (ln, (start, end)) in enumerate(zip(lines, shown)):
        events.append(f'Dialogue: 1,{_t(start)},{_t(end)},Karaoke,,0,0,0,,{karaoke_text(ln, start)}')
        if i + 1 < len(lines) and lines[i + 1]['start'] - ln['end'] < NEXT_WINDOW:
            nxt = _esc(lines[i + 1]['text'])
            events.append(f'Dialogue: 0,{_t(start)},{_t(end)},Naechste,,0,0,0,,{nxt}')
    prev_end = 0.0
    for pid, a, b in paras:
        if a - prev_end >= 1.5:                  # announce a paragraph after a longer pause
            events.append(f'Dialogue: 0,{_t(max(prev_end, a - 2.0))},{_t(a)},Info,,0,0,0,,gleich: Absatz {pid}')
        events.append(f'Dialogue: 0,{_t(a)},{_t(b)},Info,,0,0,0,,Absatz {pid}')
        prev_end = b
    for a, b in clips:
        events.append(f'Dialogue: 0,{_t(a - 0.3)},{_t(b)},Pause,,0,0,0,,Hörbeispiel – nicht sprechen')
    os.makedirs(os.path.dirname(ASS), exist_ok=True)
    with open(ASS, 'w', encoding='utf-8') as f:
        f.write(HEADER + '\n'.join(events) + '\n')
    print(ASS, f'({len(lines)} Zeilen, {total / 60:.1f} min)')


def burn_video():
    fonts = os.path.join(ROOT, 'assets', 'fonts')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', FINAL, '-an',
                    '-vf', f"scale=1280:720,ass={ASS}:fontsdir={fonts}",
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart', GUIDE], check=True)
    print(GUIDE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', nargs='?', default='all', choices=['all', 'words', 'ass', 'video'])
    ap.add_argument('--model', default='medium')
    args = ap.parse_args()
    if args.what in ('all', 'words'):
        compute_words(args.model)
    if args.what in ('all', 'ass'):
        write_ass(json.load(open(WORDS)))
    if args.what in ('all', 'video'):
        burn_video()


if __name__ == '__main__':
    main()
