"""Shared pieces for recording the narration yourself (scripts/sprechervorlage.py,
scripts/stimme_ersetzen.py): the segments of the rendered video, Whisper transcripts,
matching heard words to the script, and a few audio helpers.

Numbering for speakers: scene 1 is the intro, scene 2 is chapter I, …; "5.3" is the
third segment of scene 5.
"""

import difflib
import functools
import hashlib
import json
import math
import os
import re
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO = os.path.join(ROOT, 'video', 'Theaitetos.mp4')
SCRIPT = os.path.join(ROOT, 'src', 'data', 'script.json')
TIMING = os.path.join(ROOT, 'src', 'data', 'timing.json')
PLAN = os.path.join(ROOT, 'src', 'data', 'sprechplan.json')
WORK = os.path.join(ROOT, 'out', 'eigene_stimme')

RATE = 48000
FPS = 30
CARD = round(2.6 * FPS)
LEAD = round(0.5 * FPS)
GAP = math.floor(0.55 * FPS + 0.5)  # JS Math.round
TAIL = round(1.1 * FPS)
CREDITS = round(26 * FPS)
HOP = 0.02            # envelope resolution (s)
LOUD = 0.3            # envelope level that counts as voice

# Written one way, spoken (and transcribed) another.
EXPAND = {'v. Chr.': 'vor Christus', 'n. Chr.': 'nach Christus', 'z. B.': 'zum Beispiel',
          'd. h.': 'das heißt', 'u. a.': 'unter anderem'}


# ------------------------------------------------------------ the script and its layout
def split_sentences(text):
    """As in scripts/srt.py, but initials (G. E. L. Owen) do not end a sentence."""
    return [s for s in re.split(r'(?<=[.!?])(?<!\s[A-Z]\.)\s+(?=[A-ZÄÖÜ„])', text) if s]


def segments():
    """All narration segments in order: id ('5.3'), scene number, scene id, title,
    nominal start (s, from src/data/timing.json) and sentences."""
    script = json.load(open(SCRIPT, encoding='utf-8'))
    timing = json.load(open(TIMING))
    out, cursor = [], 0
    for n, scene in enumerate(script['scenes'], 1):
        t = (CARD if scene.get('chapter') else 0) + LEAD
        for k, (seg, secs) in enumerate(zip(scene['segments'], timing[scene['id']]), 1):
            out.append({'id': f'{n}.{k}', 'scene': n, 'scene_id': scene['id'], 'chapter': scene.get('chapter'),
                        'title': scene['title'], 'start': (cursor + t) / FPS, 'secs': secs,
                        'text': seg['text'], 'sentences': split_sentences(seg['text'])})
            t += math.ceil(secs * FPS) + GAP
        cursor += t - GAP + TAIL
    return out


# ------------------------------------------------------------ audio helpers
def load(path):
    """Any audio (or video) file → mono float32 at RATE, via ffmpeg."""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vn', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def envelope(a):
    """Speech activity per 20 ms frame, 0…1, robust to recording level and noise floor."""
    hop = int(HOP * RATE)
    n = len(a) // hop
    if n == 0:
        return np.zeros(1)
    rms = np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    live = db[db > -90]                         # ignore digital silence (gaps, noise gates)
    if len(live) < 10:
        live = db
    floor, top = np.percentile(live, 15), np.percentile(live, 97)
    return np.clip((db - floor - 6) / max(6.0, top - floor - 6), 0, 1)


def fade(a, sec=0.02):
    k = min(len(a) // 2, int(sec * RATE))
    if k:
        a[:k] *= np.linspace(0, 1, k)
        a[-k:] *= np.linspace(1, 0, k)
    return a


def pause_near(env, t0, t1, mid, min_len=0.12):
    """Middle of the longest pause (at least min_len) between t0 and t1, nearest to mid if
    several are equally long; None if the speaker did not pause there."""
    i0, i1 = max(0, int(t0 / HOP)), min(len(env), int(t1 / HOP))
    if i1 - i0 < 3:
        return None
    quiet = np.convolve(env[i0:i1], np.ones(3) / 3, mode='same') < 0.15
    runs, k = [], 0
    while k < len(quiet):
        if quiet[k]:
            j = k
            while j < len(quiet) and quiet[j]:
                j += 1
            if (j - k) * HOP >= min_len:
                c = (i0 + (k + j) / 2) * HOP
                runs.append((j - k, -abs(c - mid), c))
            k = j
        else:
            k += 1
    return max(runs)[2] if runs else None


def quietest(env, t0, t1):
    i0, i1 = max(0, int(t0 / HOP)), min(len(env), int(t1 / HOP))
    if i1 - i0 < 3:
        return (t0 + t1) / 2
    smooth = np.convolve(env[i0:i1], np.ones(3) / 3, mode='same')
    return (i0 + int(np.argmin(smooth[1:-1])) + 1.5) * HOP


def first_loud(env, t0, t1):
    i0 = max(0, int(t0 / HOP))
    idx = np.flatnonzero(env[i0:max(i0, int(t1 / HOP))] > LOUD)
    return (i0 + idx[0]) * HOP if len(idx) else None


def last_loud(env, t0, t1):
    i0 = max(0, int(t0 / HOP))
    idx = np.flatnonzero(env[i0:max(i0, int(t1 / HOP))] > LOUD)
    return (i0 + idx[-1] + 1) * HOP if len(idx) else None


def clock(t):
    return f'{int(t // 60)}:{t % 60:04.1f}'


# ------------------------------------------------------------ what was said when (Whisper)
def take_words(path, audio, model_name):
    """[(word, start, end)] of a recording, seconds from its beginning; cached per file and model."""
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    cache = os.path.join(WORK, f'woerter_{h.hexdigest()[:16]}_{model_name}.json')
    if os.path.exists(cache):
        with open(cache) as f:
            return [tuple(w) for w in json.load(f)]
    from faster_whisper import WhisperModel
    from scipy.signal import resample_poly
    model = WhisperModel(model_name, device='cpu', compute_type='int8')
    a16 = resample_poly(audio if audio is not None else load(path), 1, RATE // 16000).astype(np.float32)
    segs, _ = model.transcribe(a16, language='de', beam_size=5, word_timestamps=True,
                               condition_on_previous_text=False, vad_filter=True)
    words = [(w.word.strip(), round(w.start, 3), round(w.end, 3)) for s in segs for w in (s.words or [])]
    os.makedirs(WORK, exist_ok=True)
    with open(cache, 'w') as f:
        json.dump(words, f, ensure_ascii=False)
    return words


def norm_words(text):
    """Lower-case letter sequences; numbers spelled out; hyphens split words."""
    from num2words import num2words
    for short, full in EXPAND.items():
        text = text.replace(short, full)
    text = text.lower().replace('-', ' ')
    text = re.sub(r'\d+', lambda m: num2words(int(m.group(0)), lang='de'), text)
    return re.sub(r'[^a-zäöüß\s]', ' ', text).split()


@functools.lru_cache(maxsize=None)
def similar(a, b):
    return a == b or difflib.SequenceMatcher(a=a, b=b).ratio() >= 0.7


def subwords(sentences):
    """Script words of a list of sentences: [(normalised word, sentence index, token index)],
    token = whitespace-separated word of that sentence."""
    out = []
    for k, s in enumerate(sentences):
        for j, tok in enumerate(s.split()):
            for w in norm_words(tok):
                out.append((w, k, j))
    return out


def fit(ref, hyp):
    """Semi-global alignment: all of ref, somewhere inside hyp (extra words before and after
    it are free). Returns {ref index: hyp index} for the words that match."""
    n, m = len(ref), len(hyp)
    rows = [[0.0] * (m + 1)]
    for i in range(1, n + 1):
        prev, row, r = rows[-1], [-float(i)] + [0.0] * m, ref[i - 1]
        for j in range(1, m + 1):
            d = prev[j - 1] + (2 if similar(r, hyp[j - 1]) else -1)
            u, le = prev[j] - 1, row[j - 1] - 1
            row[j] = d if d >= u and d >= le else (u if u >= le else le)
        rows.append(row)
    pairs, i, j = {}, n, int(np.argmax(rows[n]))
    while i > 0 and j > 0:
        hit = similar(ref[i - 1], hyp[j - 1])
        if rows[i][j] == rows[i - 1][j - 1] + (2 if hit else -1):
            if hit:
                pairs[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif rows[i][j] == rows[i - 1][j] - 1:
            i -= 1
        else:
            j -= 1
    return pairs


def locate(units, words):
    """Find the units (segments), in order, in a recording's words.

    units: [(id, [sentences])]. For each unit found: per sentence (start, end, head) or None –
    head is when the voice has certainly started (end of the first recognised word, or its
    start if the sentence's first words were not recognised) –, per sentence the start time
    of every whitespace token (None where Whisper did not hear it), the unit's word range in
    `words`, and how many more letters were heard than the script has (slips, repeats)."""
    flat = [(x, i) for i, (w, _, _) in enumerate(words) for x in norm_words(w)]
    found, ptr = {}, 0
    for uid, sents in units:
        subs = subwords(sents)
        if not subs:
            continue
        window = flat[ptr:ptr + 2 * len(subs) + 60]
        pairs = fit([w for w, _, _ in subs], [w for w, _ in window])
        if len(pairs) < 0.4 * len(subs):
            continue                            # not in the recording (or not recognisable)
        word = lambda i: words[window[pairs[i]][1]]     # noqa: E731
        i_first, i_last = min(pairs), max(pairs)
        rate = (word(i_last)[2] - word(i_first)[1]) / max(1, sum(len(w) for w, _, _ in subs[i_first:i_last + 1]))
        rate = min(max(rate, 0.03), 0.15)       # seconds per letter, for words Whisper missed
        spans, tokens = [], []
        for k, s in enumerate(sents):
            mine = [i for i in range(len(subs)) if subs[i][1] == k]
            hits = [i for i in mine if i in pairs]
            toks = [None] * len(s.split())
            for i in hits:
                j = subs[i][2]
                if toks[j] is None:
                    toks[j] = word(i)[1]
            tokens.append(toks)
            if len(hits) < max(1, 0.25 * len(mine)):
                spans.append(None)
                continue
            i0, i1 = hits[0], hits[-1]
            t0 = word(i0)[1] - rate * sum(len(subs[i][0]) for i in mine if i < i0)
            t1 = word(i1)[2] + rate * sum(len(subs[i][0]) for i in mine if i > i1)
            spans.append((t0, t1, word(i0)[2] if i0 == mine[0] else word(i0)[1]))
        found[uid] = {'spans': spans, 'tokens': tokens, 'lo': window[pairs[i_first]][1],
                      'hi': window[pairs[i_last]][1] + 1, 'letters': sum(len(w) for w, _, _ in subs)}
        ptr += pairs[i_last] + 1
    # words heard between two units but not matched go to the nearer one
    order = [uid for uid, _ in units if uid in found]
    for p, q in zip(order, order[1:]):
        a, b = found[p], found[q]
        end_p, start_q, k = words[a['hi'] - 1][2], words[b['lo']][1], a['hi']
        while k < b['lo'] and words[k][1] - end_p < start_q - words[k][2]:
            k += 1
        a['hi'], b['lo'] = k, k
    for f in found.values():
        heard = sum(len(x) for w, _, _ in words[f['lo']:f['hi']] for x in norm_words(w))
        f['surplus'] = heard - f['letters']
    return found


def fill_times(times, start, end, weights):
    """Fill None entries by interpolating between known ones (by spoken length), keep order."""
    times = list(times)
    if times and times[0] is None:
        times[0] = start
    anchors = [k for k, t in enumerate(times) if t is not None] + [len(times)]
    for a, b in zip(anchors[:-1], anchors[1:]):
        t0, t1 = times[a], times[b] if b < len(times) else end
        span = sum(weights[a:b]) or 1
        acc = 0
        for k in range(a + 1, b):
            acc += weights[k - 1]
            times[k] = t0 + (t1 - t0) * acc / span
    for k in range(1, len(times)):
        times[k] = max(times[k], times[k - 1] + 0.05)
    return times
