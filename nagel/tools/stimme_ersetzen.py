"""Replace the synthetic narration with your own recording and build the updated video.

    python tools/stimme_ersetzen.py aufnahme.m4a          # one take of the whole video
    python tools/stimme_ersetzen.py aufnahmen/            # a folder of takes (see below)

Takes may be any format ffmpeg reads (wav, mp3, m4a, flac, …). In a folder the file
name says where a take belongs:

    kapitel_04.wav, kap4.m4a, 04.wav, s04_argument.wav  → chapter 4
    4.2.wav, absatz_4.2.wav                              → paragraph 4.2 (e.g. a retake)
    anything else (only if it is the only file)          → the whole video

Whisper transcribes each take and its words are matched against the script, so every
sentence is found wherever it is in the take (it does not matter when you pressed
record). The take is cut in the pauses between sentences and each sentence is laid onto
the moment the animation expects it – the timing the karaoke guide shows. Nothing is
stretched; where sentences run longer than their slots, they move apart just enough
(least squares) to keep a natural pause between them. A
paragraph take replaces that paragraph of a chapter or whole-video take. The sound
example in chapter 9 is mixed in as before. Transcripts are cached in audio/eigene_stimme/.

Result:
    output/nagel_fledermaus.mp4   video with your voice (loudness −16 LUFS)
    output/untertitel.srt         subtitles timed to your voice
                                  (with --ziel X.mp4 the subtitles go to X.srt instead)
The picture is taken from output/nagel_fledermaus_piper.mp4 (the version with the synthetic
voice, refreshed by `tools/build.py final`); it is created from the current video if missing.
"""

import argparse
import functools
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

import numpy as np

from build import RATE, SCENE_FILES, _pieces, _wrap, chapter_layout, read_wav, write_srt, write_wav
from karaoke import _norm_words, _similar, token_times
from textnorm import spoken
from timeline import schedule

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'output')
FINAL = os.path.join(OUT, 'nagel_fledermaus.mp4')
BACKUP = os.path.join(OUT, 'nagel_fledermaus_piper.mp4')
SRT = os.path.join(OUT, 'untertitel.srt')
WORK = os.path.join(ROOT, 'audio', 'eigene_stimme')
AUDIO_EXT = ('.wav', '.mp3', '.m4a', '.aac', '.flac', '.ogg', '.opus', '.aiff', '.aif', '.wma', '.mp4', '.mov')

HOP = 0.02            # envelope resolution (s)
LOUD = 0.3            # envelope level that counts as voice
CREDITS = 13          # no narration in the credits
VOICE_DELAY = 0.05    # the synthetic voice starts this long after a scheduled sentence start
MIN_PAUSE = 0.35      # shortest pause between two sentences when one runs long
PARA_PAUSE = 0.6      # … between two paragraphs
CLIP_GAP = 0.3        # … before and after the sound example
PAD = 0.4             # pause kept before and after each piece of a take


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


def put(track, seg, at):
    seg = fade(seg.copy(), 0.04)
    i = int(round(at * RATE))
    lo, hi = max(0, i), min(len(track), i + len(seg))
    if hi > lo:
        track[lo:hi] += seg[lo - i:hi - i]


def pause_near(env, t0, t1, mid, min_len=0.12):
    """Middle of the longest pause (at least min_len) between t0 and t1, nearest to mid if
    several are equally long; None if the speaker did not pause there (then we don't cut)."""
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


def first_loud(env, t0, t1):
    idx = np.flatnonzero(env[max(0, int(t0 / HOP)):max(0, int(t1 / HOP))] > LOUD)
    return max(0, int(t0 / HOP)) * HOP + idx[0] * HOP if len(idx) else None


def quietest(env, t0, t1):
    i0, i1 = max(0, int(t0 / HOP)), min(len(env), int(t1 / HOP))
    if i1 - i0 < 3:
        return (t0 + t1) / 2
    smooth = np.convolve(env[i0:i1], np.ones(3) / 3, mode='same')
    return (i0 + int(np.argmin(smooth[1:-1])) + 1.5) * HOP


def last_loud(env, t0, t1):
    idx = np.flatnonzero(env[max(0, int(t0 / HOP)):max(0, int(t1 / HOP))] > LOUD)
    return max(0, int(t0 / HOP)) * HOP + (idx[-1] + 1) * HOP if len(idx) else None


def clock(t):
    return f'{int(t // 60)}:{t % 60:04.1f}'


# ------------------------------------------------------------ the animation's timetable
class Timeline:
    def __init__(self):
        self.layout = chapter_layout()
        self.total = self.layout[-1][1] + self.layout[-1][2]
        self.chapters = {}
        self.paragraphs = {}
        self.clips = []
        for n, off, length in self.layout:
            if n == CREDITS:
                continue
            s = schedule(n)
            self.chapters[n] = (off, length, s)
            for p in s['paragraphs']:
                self.paragraphs[p['id']] = (n, off + p['start'], off + p['end'], p)
                if p['clip']:
                    self.clips.append((p['clip']['file'], off + p['clip']['start'], off + p['clip']['end']))
        self.order = sorted(self.paragraphs, key=lambda pid: self.paragraphs[pid][1])

    def due(self, pid, k):
        """When sentence k of paragraph pid is spoken in the animation (seconds in the video)."""
        n, _, _, p = self.paragraphs[pid]
        return self.chapters[n][0] + p['sentences'][k]['start'] + VOICE_DELAY


def classify(paths):
    takes = []
    for path in paths:
        stem = os.path.splitext(os.path.basename(path))[0].strip().lower()
        m = re.match(r'^(?:absatz[ _-]*)?(\d{1,2})\.(\d{1,2})$', stem)
        if m:
            takes.append(('absatz', f'{int(m.group(1))}.{int(m.group(2))}', path))
            continue
        m = re.match(r'^(?:kapitel|kap|k|s)?[ _-]*0*(\d{1,2})(?:[ _-].*)?$', stem)
        if m and int(m.group(1)) in SCENE_FILES:
            takes.append(('kapitel', int(m.group(1)), path))
            continue
        takes.append(('gesamt', None, path))
    whole = [t for t in takes if t[0] == 'gesamt']
    if len(whole) > 1 or (whole and len(takes) > 1 and any(t[0] == 'kapitel' for t in takes)):
        names = ', '.join(os.path.basename(t[2]) for t in whole)
        raise SystemExit(f'Nicht eindeutig zuzuordnen: {names}. Entweder eine Gesamtaufnahme oder Kapitel-'
                         'aufnahmen (z. B. kapitel_04.wav); Nachaufnahmen einzelner Absätze heißen z. B. 4.2.wav.')
    return takes


def scope(tl, kind, key, path):
    if kind == 'gesamt':
        return list(tl.order)
    if kind == 'kapitel':
        return [pid for pid in tl.order if tl.paragraphs[pid][0] == key]
    if key not in tl.paragraphs:
        raise SystemExit(f'Absatz {key} gibt es im Skript nicht ({os.path.basename(path)}).')
    return [key]


# ------------------------------------------------------------ what was said when (Whisper)
def take_words(path, audio, model_name):
    """[(word, start, end)] of a take, seconds from its beginning; cached per file and model."""
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
    a16 = resample_poly(audio, 1, RATE // 16000).astype(np.float32)
    segments, _ = model.transcribe(a16, language='de', beam_size=5, word_timestamps=True,
                                   condition_on_previous_text=False, vad_filter=True)
    words = [(w.word.strip(), round(w.start, 3), round(w.end, 3)) for s in segments for w in (s.words or [])]
    os.makedirs(WORK, exist_ok=True)
    with open(cache, 'w') as f:
        json.dump(words, f, ensure_ascii=False)
    return words


@functools.lru_cache(maxsize=None)
def _sim(a, b):
    return _similar(a, b)


def _fit(ref, hyp):
    """Semi-global alignment: all of ref, somewhere inside hyp (extra words before and after
    it are free). Returns {ref index: hyp index} for the words that match."""
    n, m = len(ref), len(hyp)
    rows = [[0.0] * (m + 1)]
    for i in range(1, n + 1):
        prev, row, r = rows[-1], [-float(i)] + [0.0] * m, ref[i - 1]
        for j in range(1, m + 1):
            d = prev[j - 1] + (2 if _sim(r, hyp[j - 1]) else -1)
            u, le = prev[j] - 1, row[j - 1] - 1
            row[j] = d if d >= u and d >= le else (u if u >= le else le)
        rows.append(row)
    pairs, i, j = {}, n, int(np.argmax(rows[n]))
    while i > 0 and j > 0:
        hit = _sim(ref[i - 1], hyp[j - 1])
        if rows[i][j] == rows[i - 1][j - 1] + (2 if hit else -1):
            if hit:
                pairs[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif rows[i][j] == rows[i - 1][j] - 1:
            i -= 1
        else:
            j -= 1
    return pairs


def locate(tl, pids, words):
    """Find the paragraphs, in order, in a take's words. For each paragraph found:
    sentence spans [(start, end) or None] in the take, its word range and how many
    more words were spoken than the script has (repeats, slips)."""
    flat = [(x, i) for i, (w, _, _) in enumerate(words) for x in (_norm_words(w) or [])]
    found, ptr = {}, 0
    for pid in pids:
        sents = tl.paragraphs[pid][3]['sentences']
        subs, owner = [], []
        for k, s in enumerate(sents):
            for tok in s['text'].split():
                for w in _norm_words(spoken(tok)):
                    subs.append(w)
                    owner.append(k)
        window = flat[ptr:ptr + 2 * len(subs) + 60]
        pairs = _fit(subs, [w for w, _ in window])
        if len(pairs) < 0.4 * len(subs):
            continue                            # not in the take (or not recognisable)
        i_first, i_last = min(pairs), max(pairs)
        t_first = words[window[pairs[i_first]][1]][1]
        t_last = words[window[pairs[i_last]][1]][2]
        rate = (t_last - t_first) / max(1, sum(len(w) for w in subs[i_first:i_last + 1]))
        rate = min(max(rate, 0.03), 0.15)       # seconds per letter, for words Whisper missed
        spans = []
        for k in range(len(sents)):
            mine = [i for i in range(len(subs)) if owner[i] == k]
            hits = [i for i in mine if i in pairs]
            if len(hits) < max(1, 0.25 * len(mine)):
                spans.append(None)
                continue
            i0, i1 = hits[0], hits[-1]
            t0 = words[window[pairs[i0]][1]][1] - rate * sum(len(subs[i]) for i in mine if i < i0)
            t1 = words[window[pairs[i1]][1]][2] + rate * sum(len(subs[i]) for i in mine if i > i1)
            spans.append((t0, t1))
        found[pid] = {'spans': spans, 'lo': window[pairs[i_first]][1], 'hi': window[pairs[i_last]][1] + 1,
                      'letters': sum(len(w) for w in subs)}
        ptr += pairs[i_last] + 1
    # words Whisper heard between two paragraphs but could not match go to the nearer one
    order = [pid for pid in pids if pid in found]
    for p, q in zip(order, order[1:]):
        a, b = found[p], found[q]
        end_p, start_q, k = words[a['hi'] - 1][2], words[b['lo']][1], a['hi']
        while k < b['lo'] and words[k][1] - end_p < start_q - words[k][2]:
            k += 1
        a['hi'], b['lo'] = k, k
    if order:
        a, b = found[order[0]], found[order[-1]]
        while a['lo'] > 0 and words[a['lo']][1] - words[a['lo'] - 1][2] < 1.0:
            a['lo'] -= 1
        while b['hi'] < len(words) and words[b['hi']][1] - words[b['hi'] - 1][2] < 1.0:
            b['hi'] += 1
    for f in found.values():                    # spoken beyond the script (slips, repeats)
        heard = sum(len(x) for w, _, _ in words[f['lo']:f['hi']] for x in _norm_words(w))
        f['surplus'] = heard - f['letters']
    return found


# ------------------------------------------------------------ cutting and laying out
def cut(tl, audio, found):
    """Pieces of a take, cut in the speaker's pauses between sentences (always between
    paragraphs); each knows where its voice starts and ends and when it is due."""
    env = envelope(audio)
    dur = len(audio) / RATE
    seq = [(pid, k) + span for pid in sorted(found, key=tl.order.index)
           for k, span in enumerate(found[pid]['spans']) if span]
    pieces = []
    for idx, (pid, k, t0, t1) in enumerate(seq):
        if idx:
            ppid, _, _, p1 = seq[idx - 1]
            c = pause_near(env, min(p1, t0) - 0.25, max(p1, t0) + 0.25, (p1 + t0) / 2, min_len=0.1)
            if c is None and ppid == pid:       # no pause: the sentences stay together
                pieces[-1]['t1'] = t1
                continue
            if c is None:                       # new paragraph without a pause: cut between words
                c = quietest(env, min(p1, t0) - 0.5, max(p1, t0) + 0.5)
            pieces[-1]['cut1'] = c
        cut0 = pieces[-1]['cut1'] if pieces else max(0.0, t0 - 1.0)
        pieces.append({'pid': pid, 'k': k, 'cut0': cut0, 't0': t0, 't1': t1, 'due': tl.due(pid, k)})
    if pieces:
        pieces[-1]['cut1'] = min(dur, pieces[-1]['t1'] + 1.0)
    for pc in pieces:
        on = first_loud(env, max(pc['cut0'], pc['t0'] - 0.3), pc['t0'] + 0.3)
        off = last_loud(env, pc['t1'] - 0.3, min(pc['cut1'], pc['t1'] + 0.5))
        pc['on'] = on if on is not None else pc['t0']
        pc['off'] = max(pc['on'] + 0.1, off if off is not None else pc['t1'])
        pc['c0'] = max(pc['cut0'], pc['on'] - PAD)
        pc['c1'] = min(pc['cut1'], pc['off'] + PAD)
        pc['audio'] = audio
    return pieces


def _pava(y, w):
    """Non-decreasing weighted least-squares fit to y (pool adjacent violators)."""
    blocks = []
    for yi, wi in zip(y, w):
        blocks.append([yi, wi, 1])
        while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
            m2, w2, c2 = blocks.pop()
            m1, w1, c1 = blocks.pop()
            blocks.append([(m1 * w1 + m2 * w2) / (w1 + w2), w1 + w2, c1 + c2])
    return [m for m, _, c in blocks for _ in range(c)]


def assemble(pieces, track, clips=()):
    """Lay the pieces onto the track in order, each as close to when it is due as possible
    (least squares: a sentence that runs long moves itself a little earlier and the next
    ones a little later) but never closer to its neighbour than the minimum pause; the
    sound example does not move. Sets each piece's 'shift' (take → video) and 'late'."""
    items = sorted(pieces + [{'pid': None, 'on': a, 'off': b, 'due': a, 'clip': True} for a, b in clips],
                   key=lambda p: p['due'])
    cum, y, w = 0.0, [], []
    for i, it in enumerate(items):
        if i:
            prev = items[i - 1]
            if prev.get('clip') or it.get('clip'):
                gap = CLIP_GAP
            else:
                gap = MIN_PAUSE if prev['pid'] == it['pid'] else PARA_PAUSE
            cum += prev['off'] - prev['on'] + gap
        # start_i = x_i + cum_i keeps every gap iff x is non-decreasing
        y.append(it['due'] - cum)
        # paragraph starts weigh more: the picture usually changes with a new paragraph
        w.append(1e6 if it.get('clip') else 3.0 if it['k'] == 0 else 1.0)
        it['cum'] = cum
    prev_end = -1e9
    for it, x in zip(items, _pava(y, w)):
        shift = x + it['cum'] - it['on']
        if not it.get('clip'):
            it['late'] = it['on'] + shift - it['due']
            it['shift'] = shift
            c0 = max(it['c0'], prev_end + 0.05 - shift)
            put(track, it['audio'][int(c0 * RATE):int(it['c1'] * RATE)], c0 + shift)
        prev_end = it['off'] + shift


# ------------------------------------------------------------ subtitles from the new voice
def subtitles(tl, para_words, track):
    """Cues timed to the new voice; para_words: {pid: [(word, start, end)] in video time}."""
    items = []
    for pid in tl.order:
        n, a, b, p = tl.paragraphs[pid]
        sents = [s['text'] for s in p['sentences']]
        hyp = para_words.get(pid)
        if not hyp:      # no take for it: keep the old timing
            for s in p['sentences']:
                pieces = _pieces(s['text'])
                total = sum(len(x) for x in pieces)
                t = tl.chapters[n][0] + s['start']
                for x in pieces:
                    d = (s['end'] - s['start']) * len(x) / total
                    items.append((t, t + d, _wrap(x)))
                    t += d
            continue
        times = token_times(' '.join(sents), hyp[0][1], hyp[-1][2], hyp)
        k = 0
        firsts = []
        for s in sents:
            firsts.append(k)
            k += len(s.split())
        speech_end = hyp[-1][2]
        for si, s in enumerate(sents):
            toks = s.split()
            t_tok = times[firsts[si]:firsts[si] + len(toks)]
            s_end = times[firsts[si + 1]] - 0.15 if si + 1 < len(sents) else speech_end
            j = 0
            for piece in _pieces(s):
                cnt = len(piece.split())
                t0 = t_tok[j]
                t1 = t_tok[j + cnt] if j + cnt < len(t_tok) else max(s_end, t0 + 0.5)
                items.append((t0, t1, _wrap(piece)))
                j += cnt
    items.sort(key=lambda x: x[0])
    items = snap_to_onsets(items, track)
    for i in range(len(items) - 1):             # no overlaps
        a, b, txt = items[i]
        if b > items[i + 1][0]:
            items[i] = (a, max(a + 0.3, items[i + 1][0]), txt)
    return items


def snap_to_onsets(items, track):
    """Whisper reports word starts a little late: where a subtitle begins right at a fresh
    onset of the voice (after a pause), start it there instead."""
    env = envelope(track)
    quiet = np.convolve(env, np.ones(3) / 3, mode='same') < 0.15
    loud = env > LOUD
    onsets = np.array([k * HOP for k in range(8, len(env)) if loud[k] and quiet[k - 8:k].all()])
    out = []
    for a, b, txt in items:
        if len(onsets):
            j = int(np.argmin(np.abs(onsets - a)))
            if -0.35 <= onsets[j] - a <= 0.25:
                a = onsets[j] - 0.05
                b = max(b, a + 0.5)
        out.append((a, b, txt))
    for i in range(len(out) - 1):              # no overlaps
        a, b, txt = out[i]
        if b > out[i + 1][0]:
            out[i] = (a, max(a + 0.3, out[i + 1][0]), txt)
    return out


# ------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('aufnahme', help='Audiodatei oder Ordner mit Aufnahmen')
    ap.add_argument('--modell', default='small', help='Whisper-Modell (Standard: small)')
    ap.add_argument('--ziel', default=FINAL, help='Ausgabedatei (Standard: output/nagel_fledermaus.mp4)')
    ap.add_argument('--ohne-feinabgleich', action='store_true',
                    help='jede Aufnahme nur als Ganzes versetzen, die Sätze nicht einzeln anlegen')
    args = ap.parse_args()
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        raise SystemExit('faster-whisper fehlt: venv/bin/pip install faster-whisper')

    src = args.aufnahme
    if os.path.isdir(src):
        paths = sorted(os.path.join(src, f) for f in os.listdir(src) if f.lower().endswith(AUDIO_EXT))
    else:
        paths = [src]
    if not paths:
        raise SystemExit(f'Keine Aufnahmen gefunden in {src}')
    takes = classify(paths)
    order = {'gesamt': 0, 'kapitel': 1, 'absatz': 2}          # retakes last, so they win
    takes.sort(key=lambda t: order[t[0]])

    tl = Timeline()
    by_pid, words_of, notes = {}, {}, []
    label = {'gesamt': 'ganzes Video', 'kapitel': 'Kapitel', 'absatz': 'Absatz'}
    for kind, key, path in takes:
        name = os.path.basename(path)
        print(f'{name}: Whisper hört zu …', flush=True)
        audio = load(path)
        words = take_words(path, audio, args.modell)
        pids = scope(tl, kind, key, path)
        found = locate(tl, pids, words)
        pieces = cut(tl, audio, found)
        if not pieces:
            where = label[kind] + ('' if key is None else f' {key}')
            notes.append(f'{name}: nichts aus {where} erkannt – nicht verwendet')
            continue
        drift = np.array([pc['due'] - pc['on'] for pc in pieces])
        offset = float(np.median(drift))
        if args.ohne_feinabgleich:
            for pc in pieces:
                pc['due'] = pc['on'] + offset
        for pid in found:
            mine = [pc for pc in pieces if pc['pid'] == pid]
            if mine:
                by_pid[pid] = mine
                words_of[pid] = (words[found[pid]['lo']:found[pid]['hi']], mine)
        n_sent = sum(len(tl.paragraphs[p][3]['sentences']) for p in pids)
        n_found = sum(1 for p in found for s in found[p]['spans'] if s)
        dev = np.abs(drift - offset)
        worst = pieces[int(np.argmax(dev))]
        start = f'bei {clock(offset)} im Video' if offset >= 0 else f'{-offset:.1f} s vor dem Video'
        print(f'  {label[kind]}{"" if key is None else " " + str(key)}: Aufnahme beginnt {start}; '
              f'{len(found)} von {len(pids)} Absätzen, {n_found} von {n_sent} Sätzen gefunden')
        print(f'  Abweichung vom Takt der Vorlage: Median {np.median(dev):.2f} s, größte {dev.max():.2f} s '
              f'(Absatz {worst["pid"]}, Satz {worst["k"] + 1})'
              + ('' if args.ohne_feinabgleich else ' – wird angeglichen'))
        lost = [p for p in pids if p not in found]
        if lost:
            notes.append(f'{name}: nicht gefunden, bitte anhören: Absatz ' + ', '.join(lost))
        gaps = [f'{p}/{k + 1}' for p in found for k, s in enumerate(found[p]['spans']) if s is None]
        if gaps:
            notes.append(f'{name}: Sätze kaum erkannt (bleiben am Satz davor): ' + ', '.join(gaps))
        extra = [f'{p} (ab {clock(words[found[p]["lo"]][1])})' for p in found if found[p]['surplus'] >= 25]
        if extra:
            notes.append(f'{name}: mehr Wörter als im Skript – Versprecher oder Wiederholung? Absatz '
                         + ', '.join(extra))

    pieces = [pc for ps in by_pid.values() for pc in ps]
    track = np.zeros(int(round(tl.total * RATE)) + RATE, dtype=np.float32)
    assemble(pieces, track, [(c0, c1) for _, c0, c1 in tl.clips])
    moved = {}
    for pc in pieces:
        if abs(pc['late']) > 0.5 and abs(pc['late']) > abs(moved.get(pc['pid'], 0.0)):
            moved[pc['pid']] = pc['late']
    if pieces:
        dev = np.abs([pc['late'] for pc in pieces])
        print(f'Sätze im Video gegenüber der Animation: {np.mean(dev < 0.1):.0%} genau, '
              f'sonst im Median {np.median(dev[dev >= 0.1]) if (dev >= 0.1).any() else 0:.2f} s daneben')
    if moved:
        notes.append('länger gesprochen als Platz war, um mehr als 0,5 s verschoben: Absatz '
                     + ', '.join(f'{p} ({s:+.1f} s)' for p, s in sorted(moved.items(), key=lambda x: tl.order.index(x[0]))))
    for f, c0, _ in tl.clips:                   # the sound example in chapter 9 stays
        clip = fade(read_wav(os.path.join(ROOT, f)) * 0.9, 0.05)
        i = int(round(c0 * RATE))
        track[i:i + len(clip)] += clip[:len(track) - i]
    track = track[:int(round(tl.total * RATE))]
    silent = [p for p in tl.order if p not in by_pid]
    if silent:
        notes.append('ohne Aufnahme (dort ist jetzt Stille): Absatz ' + ', '.join(silent))
    for line in notes:
        print('Hinweis: ' + line)

    os.makedirs(WORK, exist_ok=True)
    wav = os.path.join(WORK, 'tonspur.wav')
    write_wav(wav, np.clip(track, -1, 1))
    if not os.path.exists(BACKUP) and os.path.exists(FINAL):
        shutil.copy2(FINAL, BACKUP)
        print(f'Sicherung der bisherigen Fassung: {BACKUP}')
    video = BACKUP if os.path.exists(BACKUP) else FINAL
    tmp = os.path.join(WORK, 'neu.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-map', '0:v:0', '-map', '1:a:0',
                    '-filter:a', 'highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(RATE), '-ac', '2',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', tmp],
                   check=True)
    os.replace(tmp, args.ziel)
    print(f'Video mit eigener Stimme: {args.ziel}')

    para_words = {}
    for pid, (ws, ps) in words_of.items():
        out = []
        for w, a, b in ws:                      # each word moves with the piece it is in
            pc = min(ps, key=lambda p: 0 if p['c0'] <= a < p['c1'] else min(abs(a - p['c0']), abs(a - p['c1'])))
            out.append((w, a + pc['shift'], b + pc['shift']))
        para_words[pid] = out
    items = subtitles(tl, para_words, track)
    srt = SRT if os.path.abspath(args.ziel) == os.path.abspath(FINAL) else os.path.splitext(args.ziel)[0] + '.srt'
    write_srt(srt, items)
    print(f'Untertitel: {srt} ({len(items)})')


if __name__ == '__main__':
    sys.exit(main())
