"""Replace the synthetic narration with your own recording and build the updated video.

    python tools/stimme_ersetzen.py aufnahme.wav          # one take of the whole video
    python tools/stimme_ersetzen.py aufnahmen/            # a folder of takes (see below)

Takes may be any format ffmpeg reads (wav, mp3, m4a, flac, …). In a folder the file
name says where a take belongs:

    kapitel_04.wav, kap4.m4a, 04.wav, s04_argument.wav  → chapter 4
    4.2.wav, absatz_4.2.wav                              → paragraph 4.2 (e.g. a retake)
    anything else (only if it is the only file)          → the whole video

Each take is placed automatically: its speech/pause pattern is matched against the
pattern of the current narration (which the karaoke guide follows), so it does not
matter when you pressed record. A paragraph take replaces that paragraph inside a
chapter or whole-video take. The sound example in chapter 9 is mixed in as before.

Result:
    output/nagel_fledermaus.mp4   video with your voice (loudness −16 LUFS)
    output/untertitel.srt         subtitles timed to your voice (Whisper; skip with --schnell)
                                  (with --ziel X.mp4 the subtitles go to X.srt instead)
The picture is taken from output/nagel_fledermaus_piper.mp4 (the version with the synthetic
voice, refreshed by `tools/build.py final`); it is created from the current video if missing.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

import numpy as np

from build import RATE, NARRATION, SCENE_FILES, _pieces, _wrap, chapter_layout, read_wav, write_srt, write_wav
from timeline import schedule

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'output')
FINAL = os.path.join(OUT, 'nagel_fledermaus.mp4')
BACKUP = os.path.join(OUT, 'nagel_fledermaus_piper.mp4')
SRT = os.path.join(OUT, 'untertitel.srt')
WORK = os.path.join(ROOT, 'audio', 'eigene_stimme')
AUDIO_EXT = ('.wav', '.mp3', '.m4a', '.aac', '.flac', '.ogg', '.opus', '.aiff', '.aif', '.wma', '.mp4', '.mov')

HOP = 0.02            # envelope resolution (s)
CREDITS = 13          # no narration in the credits


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


def best_lag(rec, ref, max_lag, center=0):
    """Lag (frames) by which rec must be shifted to match ref – searched within
    center ± max_lag – and a 0…1 match score."""
    r = rec - rec.mean()
    f = ref - ref.mean()
    size = 1 << int(np.ceil(np.log2(len(r) + len(f) + 2 * abs(center) + 1)))
    corr = np.fft.irfft(np.fft.rfft(f, size) * np.conj(np.fft.rfft(r, size)), size)
    lags = np.arange(center - max_lag, center + max_lag + 1)
    vals = corr[lags % size]
    i = int(np.argmax(vals))
    norm = np.sqrt(np.sum(r ** 2) * np.sum(f ** 2)) + 1e-9
    return int(lags[i]), float(vals[i] / norm)


def fade(a, sec=0.02):
    k = min(len(a) // 2, int(sec * RATE))
    if k:
        a[:k] *= np.linspace(0, 1, k)
        a[-k:] *= np.linspace(1, 0, k)
    return a


# ------------------------------------------------------------ the old narration as reference
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
                    self.clips.append((p['clip']['file'], off + p['clip']['start']))

    def reference(self, start, end):
        """The current narration between start and end (seconds in the final video)."""
        out = np.zeros(int(round((end - start) * RATE)), dtype=np.float32)
        for pid, (n, a, b, p) in self.paragraphs.items():
            if b < start or a > end:
                continue
            voice = read_wav(os.path.join(NARRATION, f'{pid}.wav'))
            i = int(round((a - start) * RATE))
            lo, hi = max(0, i), min(len(out), i + len(voice))
            if hi > lo:
                out[lo:hi] += voice[lo - i:hi - i]
        return out


# ------------------------------------------------------------ placing the takes
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


def paragraph_reference(tl, pid, start, end):
    """The old narration of one paragraph alone, between start and end."""
    _, a, _, _ = tl.paragraphs[pid]
    out = np.zeros(int(round((end - start) * RATE)), dtype=np.float32)
    voice = read_wav(os.path.join(NARRATION, f'{pid}.wav'))
    i = int(round((a - start) * RATE))
    lo, hi = max(0, i), min(len(out), i + len(voice))
    out[lo:hi] = voice[lo - i:hi - i]
    return out


def speech_frames(env):
    idx = np.flatnonzero(env > 0.3)
    return (idx[0] * HOP, (idx[-1] + 1) * HOP) if len(idx) else (0.0, 0.0)


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


def sentence_reference(tl, pid, k, start, end):
    """The old narration of one sentence alone, between start and end."""
    _, a, _, p = tl.paragraphs[pid]
    s = p['sentences'][k]
    voice = read_wav(os.path.join(NARRATION, f'{pid}.wav'))
    local = s['start'] - p['sentences'][0]['start']
    v0 = int(max(0.0, local - 0.05) * RATE)
    v1 = int((local + (s['end'] - s['start']) + 0.05) * RATE)
    piece = voice[v0:v1]
    out = np.zeros(int(round((end - start) * RATE)), dtype=np.float32)
    i = int(round((a + local - 0.05 - start) * RATE))
    lo, hi = max(0, i), min(len(out), i + len(piece))
    if hi > lo:
        out[lo:hi] = piece[lo - i:hi - i]
    return out


def put(track, seg, at):
    seg = fade(seg.copy())
    i = int(round(at * RATE))
    lo, hi = max(0, i), min(len(track), i + len(seg))
    if hi > lo:
        track[lo:hi] += seg[lo - i:hi - i]


def place(tl, take, kind, key, path, track, report, fine=True):
    """Put one take where its speech pattern matches the old narration (which the animation
    follows); with fine=True each paragraph of a longer take is then aligned on its own."""
    if kind == 'gesamt':
        start, end, search = 0.0, tl.total, 180.0
    elif kind == 'kapitel':
        off, length, _ = tl.chapters[key]
        start, end, search = off, off + length, 60.0
    else:
        if key not in tl.paragraphs:
            raise SystemExit(f'Absatz {key} gibt es im Skript nicht ({os.path.basename(path)}).')
        _, a, b, _ = tl.paragraphs[key]
        start, end, search = a - 0.35, b + 0.35, 8.0
    env = envelope(take)
    lag, score = best_lag(env, envelope(tl.reference(start, end)), int(search / HOP))
    at = start + lag * HOP                      # where the take's first sample lands
    name = os.path.basename(path)

    if kind == 'absatz':                        # a retake replaces that paragraph
        track[int(start * RATE):int(end * RATE)] = 0
        state = {'prev_end': -1e9, 'shifts': [], 'crowded': []}
        if fine:
            place_sentences(tl, key, take, at, at, track, state)
        else:
            put(track, take, at)
        f0, f1 = speech_frames(env)
        late = max(0.0, at + f1 - end) + max(0.0, start - (at + f0))
        report.append((name, kind, key, at - start, score, late, (state['shifts'], []) if fine else None))
        return

    pids = sorted((p for p, v in tl.paragraphs.items() if start <= v[1] and v[2] <= end),
                  key=lambda p: tl.paragraphs[p][1])
    if not fine or not pids:
        lo = max(start, at)
        seg = take[int(round((lo - at) * RATE)):int(round((end - at) * RATE))]
        put(track, seg, lo)
        report.append((name, kind, key, at - start, score, 0.0, None))
        return

    # cut the take in the pauses between paragraphs …
    cuts = [max(0.0, tl.paragraphs[pids[0]][1] - at - 1.0)]
    for p, q in zip(pids[:-1], pids[1:]):
        mid = (tl.paragraphs[p][2] + tl.paragraphs[q][1]) / 2 - at
        cut = pause_near(env, mid - 1.0, mid + 1.0, mid, min_len=0.2)
        cuts.append(cut if cut is not None else mid)
    cuts.append(min(len(take) / RATE, tl.paragraphs[pids[-1]][2] - at + 1.5))
    # … lay each paragraph onto its place in the animation, then each sentence inside it
    state = {'prev_end': -1e9, 'shifts': [], 'crowded': []}
    for pid, c0, c1 in zip(pids, cuts[:-1], cuts[1:]):
        if c1 - c0 < 0.2:
            continue
        seg = take[int(c0 * RATE):int(c1 * RATE)]
        nominal = at + c0
        _, a, b, _ = tl.paragraphs[pid]
        pos = align(seg, lambda r0, r1: paragraph_reference(tl, pid, r0, r1), nominal, 1.5)
        place_sentences(tl, pid, seg, pos, nominal, track, state)
    report.append((name, kind, key, at - start, score, 0.0, (state['shifts'], state['crowded'])))


def align(seg, reference, nominal, search):
    """Best position (s) of seg near nominal, matched against reference(r0, r1); nominal if unsure."""
    dur = len(seg) / RATE
    r0 = nominal - search - 0.5
    ref = reference(r0, nominal + dur + search + 0.5)
    lag, sc = best_lag(envelope(seg), envelope(ref), int(search / HOP), center=int(round((nominal - r0) / HOP)))
    pos = r0 + lag * HOP
    return pos if sc >= 0.3 else nominal


def place_sentences(tl, pid, seg, pos, nominal, track, state, gap=0.15):
    """Split a paragraph take at the speaker's pauses near the sentence boundaries and align
    each piece to its sentence; pieces never overlap and keep at least `gap` of pause."""
    _, a, _, p = tl.paragraphs[pid]
    sents = p['sentences']
    env = envelope(seg)
    bounds = [0.0]
    groups = [[0]]
    for k in range(1, len(sents)):
        mid = (sents[k - 1]['end'] + sents[k]['start']) / 2 - p['start'] + a - pos
        cut = pause_near(env, mid - 0.6, mid + 0.6, mid)
        if cut is None or cut <= bounds[-1] + 0.2:
            groups[-1].append(k)            # no pause there: keep the sentences together
        else:
            bounds.append(cut)
            groups.append([k])
    bounds.append(len(seg) / RATE)
    for ks, b0, b1 in zip(groups, bounds[:-1], bounds[1:]):
        piece = seg[int(b0 * RATE):int(b1 * RATE)]
        if len(piece) < int(0.1 * RATE):
            continue

        def ref(r0, r1, ks=ks):
            return sum(sentence_reference(tl, pid, k, r0, r1) for k in ks)
        spos = align(piece, ref, pos + b0, 0.6)
        f0, f1 = speech_frames(envelope(piece))
        if spos + f0 < state['prev_end'] + gap:
            if spos + f0 < state['prev_end'] - 0.05 and pid not in state['crowded']:
                state['crowded'].append(pid)
            spos = state['prev_end'] + gap - f0
        put(track, piece, spos)
        state['shifts'].append(spos - (nominal + b0))
        state['prev_end'] = spos + f1


# ------------------------------------------------------------ subtitles from the new voice
def subtitles(tl, track, model_name):
    from faster_whisper import WhisperModel
    from scipy.signal import resample_poly
    from karaoke import token_times
    model = WhisperModel(model_name, device='cpu', compute_type='int8')
    items = []
    for pid in sorted(tl.paragraphs, key=lambda k: [int(x) for x in k.split('.')]):
        n, a, b, p = tl.paragraphs[pid]
        w0, w1 = max(0.0, a - 0.8), min(tl.total, b + 1.2)
        seg = track[int(w0 * RATE):int(w1 * RATE)]
        seg16 = resample_poly(seg, 1, RATE // 16000).astype(np.float32)
        segments, _ = model.transcribe(seg16, language='de', beam_size=5, word_timestamps=True,
                                       condition_on_previous_text=False)
        hyp = [(w.word.strip(), w0 + w.start, w0 + w.end) for s in segments for w in (s.words or [])]
        sents = [s['text'] for s in p['sentences']]
        if not hyp:      # nothing recognised: keep the old timing
            for s in p['sentences']:
                pieces = _pieces(s['text'])
                total = sum(len(x) for x in pieces)
                t = tl.chapters[n][0] + s['start']
                for x in pieces:
                    d = (s['end'] - s['start']) * len(x) / total
                    items.append((t, t + d, _wrap(x)))
                    t += d
            print(f'  {pid}: keine Sprache erkannt – alte Zeiten', flush=True)
            continue
        text = ' '.join(sents)
        times = token_times(text, hyp[0][1], hyp[-1][2], hyp)
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
        print(f'  {pid}: {len(hyp)} Wörter erkannt', flush=True)
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
    loud = env > 0.3
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
    ap.add_argument('--schnell', action='store_true', help='Untertitel nicht neu an die Stimme anpassen')
    ap.add_argument('--modell', default='small', help='Whisper-Modell für die Untertitel (Standard: small)')
    ap.add_argument('--ziel', default=FINAL, help='Ausgabedatei (Standard: output/nagel_fledermaus.mp4)')
    ap.add_argument('--ohne-feinabgleich', action='store_true',
                    help='Aufnahmen nur als Ganzes anlegen, Absätze nicht einzeln nachziehen')
    args = ap.parse_args()

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
    track = np.zeros(int(round(tl.total * RATE)) + RATE, dtype=np.float32)
    report = []
    for kind, key, path in takes:
        print(f'lege an: {os.path.basename(path)} ({kind}{"" if key is None else " " + str(key)})', flush=True)
        place(tl, load(path), kind, key, path, track, report, fine=not args.ohne_feinabgleich)
    retakes = {key for k, key, _ in takes if k == 'absatz'}
    covered = set(tl.chapters) if any(k == 'gesamt' for k, _, _ in takes) else {key for k, key, _ in takes if k == 'kapitel'}
    missing = [n for n in tl.chapters if n not in covered
               and not all(pid in retakes for pid, v in tl.paragraphs.items() if v[0] == n)]

    for name, kind, key, shift, score, late, fine in report:
        warn = []
        if score < 0.3:
            warn.append('Zuordnung unsicher – bitte anhören')
        if late > 0.3:
            warn.append(f'ragt {late:.1f} s über den Absatz hinaus')
        line = (f'  {name:24s} {kind:8s} {"" if key is None else key!s:5s} Versatz {shift:+7.2f} s  '
                f'Übereinstimmung {score:.2f}')
        if fine:
            shifts, crowded = fine
            line += f'  Feinabgleich (Absätze, Sätze): max. {max(map(abs, shifts), default=0):.2f} s'
            if crowded:
                warn.append('zu lang gesprochen, nach hinten verschoben: ' + ', '.join(crowded))
        print(line + (f'  – {"; ".join(warn)}' if warn else ''))
    if missing:
        print('Hinweis: ohne Aufnahme (dort ist jetzt Stille): Kapitel ' + ', '.join(map(str, missing)))

    # the sound example in chapter 9 stays
    for f, at in tl.clips:
        clip = fade(read_wav(os.path.join(ROOT, f)) * 0.9, 0.05)
        i = int(round(at * RATE))
        track[i:i + len(clip)] += clip[:len(track) - i]
    track = track[:int(round(tl.total * RATE))]

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

    if args.schnell:
        print('Untertitel unverändert (--schnell).')
        return
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        print('faster-whisper ist nicht installiert – Untertitel unverändert.')
        return
    print('Untertitel an die neue Stimme anpassen (Whisper) …', flush=True)
    items = subtitles(tl, track, args.modell)
    srt = SRT if os.path.abspath(args.ziel) == os.path.abspath(FINAL) else os.path.splitext(args.ziel)[0] + '.srt'
    write_srt(srt, items)
    print(f'Untertitel: {srt} ({len(items)})')


if __name__ == '__main__':
    sys.exit(main())
