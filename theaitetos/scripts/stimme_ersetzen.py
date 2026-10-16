"""Replace the synthetic narration with your own recording and build the updated video.

    python scripts/stimme_ersetzen.py aufnahme.m4a        # one take of the whole video
    python scripts/stimme_ersetzen.py aufnahmen/          # a folder of takes (see below)

Takes may be any format ffmpeg reads (wav, mp3, m4a, flac, …). In a folder the file
name says where a take belongs:

    szene_05.wav, 05.m4a, mathematik.wav     → scene 5 (scene 1 is the intro; or the scene id)
    5.3.wav, abschnitt_5.3.wav               → segment 3 of scene 5 (e.g. a retake)
    anything else (only if it is the only file) → the whole video

Whisper transcribes each take and its words are matched against the script, so every
sentence is found wherever it is in the take. The take is cut in the pauses between
sentences and each sentence is laid onto the moment the animation expects it – the
timing of src/data/sprechplan.json, which the karaoke guide shows (scripts/sprechervorlage.py).
Nothing is stretched; where sentences run longer than their slots, they move apart just
enough (least squares) to keep a natural pause. A segment take replaces that segment of a
scene or whole-video take. The ambient pad is mixed in as in scripts/mix.py (ducked under
the voice, −16 LUFS). Transcripts are cached in out/eigene_stimme/.

Result (picture from video/Theaitetos.mp4, unchanged):
    out/theaitetos_eigene_stimme.mp4   video with your voice
    out/theaitetos_eigene_stimme.srt   subtitles timed to your voice
"""

import argparse
import os
import re
import subprocess
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eigene_stimme as es  # noqa: E402
from sprechervorlage import load_plan  # noqa: E402
from srt import chunks, ts, wrap  # noqa: E402

OUT = os.path.join(es.ROOT, 'out', 'theaitetos_eigene_stimme.mp4')
PAD = os.path.join(es.ROOT, 'public', 'music', 'pad.wav')
AUDIO_EXT = ('.wav', '.mp3', '.m4a', '.aac', '.flac', '.ogg', '.opus', '.aiff', '.aif', '.wma', '.mp4', '.mov')

MIN_PAUSE = 0.35      # shortest pause between two sentences when one runs long
SEG_PAUSE = 0.6       # … between two segments
PAD_S = 0.4           # pause kept before and after each piece of a take


# ------------------------------------------------------------ which take is which
def classify(paths, plan):
    scene_ids = {seg['scene_id']: seg['scene'] for seg in plan['segments']}
    scenes = set(scene_ids.values())
    takes = []
    for path in paths:
        stem = os.path.splitext(os.path.basename(path))[0].strip().lower()
        m = re.match(r'^(?:abschnitt[ _-]*)?(\d{1,2})\.(\d{1,2})$', stem)
        if m:
            takes.append(('abschnitt', f'{int(m.group(1))}.{int(m.group(2))}', path))
            continue
        m = re.match(r'^(?:szene|kapitel|kap|s)?[ _-]*0*(\d{1,2})(?:[ _-].*)?$', stem)
        if m and int(m.group(1)) in scenes:
            takes.append(('szene', int(m.group(1)), path))
            continue
        if stem in scene_ids:
            takes.append(('szene', scene_ids[stem], path))
            continue
        takes.append(('gesamt', None, path))
    whole = [t for t in takes if t[0] == 'gesamt']
    if len(whole) > 1 or (whole and any(t[0] == 'szene' for t in takes)):
        names = ', '.join(os.path.basename(t[2]) for t in whole)
        raise SystemExit(f'Nicht eindeutig zuzuordnen: {names}. Entweder eine Gesamtaufnahme oder Szenen-'
                         'aufnahmen (z. B. szene_05.wav); Nachaufnahmen einzelner Abschnitte heißen z. B. 5.3.wav.')
    return takes


def scope(plan, kind, key, path):
    segs = plan['segments']
    if kind == 'gesamt':
        return segs
    if kind == 'szene':
        return [s for s in segs if s['scene'] == key]
    hit = [s for s in segs if s['id'] == key]
    if not hit:
        raise SystemExit(f'Abschnitt {key} gibt es im Skript nicht ({os.path.basename(path)}).')
    return hit


def summarize(ids, plan):
    """'Szene 1, 3–4, 6–31; Abschnitt 5.2' instead of every segment id."""
    per_scene = {}
    for seg in plan['segments']:
        per_scene.setdefault(seg['scene'], []).append(seg['id'])
    whole = [n for n, sids in per_scene.items() if all(x in ids for x in sids)]
    single = [x for x in ids if int(x.split('.')[0]) not in whole]
    runs = []
    for n in whole:
        if runs and n == runs[-1][1] + 1:
            runs[-1][1] = n
        else:
            runs.append([n, n])
    parts = []
    if runs:
        parts.append('Szene ' + ', '.join(f'{a}' if a == b else f'{a}–{b}' for a, b in runs))
    if single:
        parts.append('Abschnitt ' + ', '.join(single))
    return '; '.join(parts)


# ------------------------------------------------------------ cutting and laying out
def cut(segs, audio, found, words):
    """Pieces of a take, cut in the speaker's pauses between sentences (always between
    segments); each knows where its voice starts and ends and when it is due."""
    env = es.envelope(audio)
    dur = len(audio) / es.RATE
    seq = [(seg['id'], k, seg['sentences'][k]['start']) + span
           for seg in segs if seg['id'] in found
           for k, span in enumerate(found[seg['id']]['spans']) if span]
    pieces = []
    for idx, (sid, k, due, t0, t1, head) in enumerate(seq):
        if idx:
            psid, _, _, _, p1, _ = seq[idx - 1]
            hi = max(min(p1, t0) + 0.2, head - 0.1)
            if any(p1 + 0.05 < w[1] < t0 - 0.1 for w in words):
                # words heard in between that are not in the script (an addition, a repeat):
                # they stay with the sentence before, the cut goes right before the next one
                c = es.pause_near(env, min(p1, t0) - 0.25, hi, t0, min_len=0.1, near=0.3)
            else:
                # nothing heard in between: Whisper dates the end of a sentence more reliably
                # than the start of the next (it misses words after a pause), so of similar
                # pauses the one nearest that end wins
                c = es.pause_near(env, min(p1, t0) - 0.25, hi, p1, min_len=0.1, near=0.6)
            if c is None and psid == sid:       # no pause: the sentences stay together
                pieces[-1]['t1'] = t1
                pieces[-1]['ks'].append(k)
                continue
            if c is None:                       # new segment without a pause: cut between words
                c = es.quietest(env, min(p1, t0) - 0.5, max(p1, t0) + 0.5)
            pieces[-1]['cut1'] = c
        cut0 = pieces[-1]['cut1'] if pieces else max(0.0, t0 - 1.0)
        pieces.append({'sid': sid, 'k': k, 'ks': [k], 'cut0': cut0, 't0': t0, 't1': t1, 'head': head,
                       'due': due, 'plan': due})
    if pieces:
        pieces[-1]['cut1'] = min(dur, pieces[-1]['t1'] + 1.0)
    for pc in pieces:
        on = es.first_loud(env, max(pc['cut0'], pc['t0'] - 0.3), max(pc['head'], pc['t0'] + 0.3))
        if on is None:
            on = es.first_loud(env, pc['cut0'], pc['t1'])
        off = es.last_loud(env, pc['t1'] - 0.3, min(pc['cut1'], pc['t1'] + 0.5))
        on = on if on is not None else pc['t0']
        off = max(on + 0.1, off if off is not None else pc['t1'])
        # Whisper sometimes misses words at the start or end of a sentence: voice running on
        # into it belongs to it, and nothing spoken between the two cuts is thrown away
        pc['on'], pc['off'] = es.spread(env, on, off, pc['cut0'], pc['cut1'], gap=0.8)
        first = es.first_voice(env, pc['cut0'], pc['cut1'])
        last = es.last_voice(env, pc['cut0'], pc['cut1'])
        pc['c0'] = max(pc['cut0'], min(pc['on'], first if first is not None else pc['on']) - PAD_S)
        pc['last'] = max(pc['off'], last if last is not None else pc['off'])   # end of everything said
        pc['c1'] = min(pc['cut1'], pc['last'] + PAD_S)
        pc['audio'], pc['env'] = audio, env
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


def assemble(pieces, track):
    """Lay the pieces onto the track in order, each as close to when it is due as possible
    (least squares: a sentence that runs long moves itself a little earlier and the next
    ones a little later) but never closer to its neighbour than the minimum pause.
    Sets each piece's 'shift' (take → video) and 'late' (against the animation)."""
    items = sorted(pieces, key=lambda p: p['due'])
    cum, y, w = 0.0, [], []
    for i, it in enumerate(items):
        if i:
            prev = items[i - 1]
            cum += prev['last'] - prev['on'] + (MIN_PAUSE if prev['sid'] == it['sid'] else SEG_PAUSE)
        # start_i = x_i + cum_i keeps every gap iff x is non-decreasing
        y.append(it['due'] - cum)
        w.append(3.0 if it['k'] == 0 else 1.0)  # segment starts weigh more: the picture changes there
        it['cum'] = cum
    prev_end = -1e9
    for it, x in zip(items, _pava(y, w)):
        shift = x + it['cum'] - it['on']
        it['late'] = it['on'] + shift - it['plan']
        it['shift'] = shift
        c0 = max(it['c0'], prev_end + 0.05 - shift)
        # voice lost because the lead-in had to give way to the sentence before (should be none)
        it['trimmed'] = float((it['env'][int(it['c0'] / es.HOP):int(c0 / es.HOP)] > es.LOUD).sum() * es.HOP)
        seg = es.fade(it['audio'][int(c0 * es.RATE):int(it['c1'] * es.RATE)].copy(), 0.04)
        i0 = int(round((c0 + shift) * es.RATE))
        lo, hi = max(0, i0), min(len(track), i0 + len(seg))
        if hi > lo:
            track[lo:hi] += seg[lo - i0:hi - i0]
        prev_end = it['last'] + shift


# ------------------------------------------------------------ subtitles from the new voice
def subtitles(plan, placed, track):
    """Cues as in scripts/srt.py, timed to the new voice. placed: {segment id: (found, pieces)}."""
    cues = []
    for seg in plan['segments']:
        f, ps = placed.get(seg['id'], (None, []))
        for k, s in enumerate(seg['sentences']):
            toks = s['text'].split()
            mine = [p for p in ps if k in p['ks']]
            if f and f['spans'][k] and mine:
                pc, ks = mine[0], mine[0]['ks']
                sh = pc['shift']
                start = pc['on'] + sh if k == pc['k'] else f['spans'][k][0] + sh
                end = pc['off'] + sh if k == ks[-1] else f['spans'][ks[ks.index(k) + 1]][0] + sh
                heard = [t + sh if t is not None else None for t in f['tokens'][k]]
                heard = [t if t is None or start - 0.1 <= t <= end else None for t in heard]
                heard[0] = start
                weights = [max(1, len(''.join(es.norm_words(t)))) for t in toks]
                times = es.fill_times(heard, start, end, weights)
            else:                               # no take for it: keep the plan's timing
                times, end = s['words'], s['end']
            j = 0
            for piece in chunks(s['text']):
                n = len(piece.split())
                a = times[j]
                b = times[j + n] if j + n < len(times) else max(end, a + 0.5)
                cues.append((a, b, piece))
                j += n
    cues.sort(key=lambda c: c[0])
    for i in range(len(cues) - 1):              # no overlaps, at least a short display
        a, b, txt = cues[i]
        cues[i] = (a, max(a + 0.3, min(max(b, a + 0.7), cues[i + 1][0])), txt)
    return cues


def write_srt(path, cues):
    with open(path, 'w', encoding='utf-8') as fh:
        for i, (a, b, text) in enumerate(cues, 1):
            fh.write(f'{i}\n{ts(a)} --> {ts(b - 0.05)}\n{wrap(text)}\n\n')


# ------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('aufnahme', help='Audiodatei oder Ordner mit Aufnahmen')
    ap.add_argument('--modell', default='small', help='Whisper-Modell (Standard: small)')
    ap.add_argument('--ziel', default=OUT, help='Ausgabedatei (Standard: out/theaitetos_eigene_stimme.mp4)')
    ap.add_argument('--music-db', type=float, default=-24.0, help='Musikpegel wie in scripts/mix.py')
    ap.add_argument('--ohne-feinabgleich', action='store_true',
                    help='jede Aufnahme nur als Ganzes versetzen, die Sätze nicht einzeln anlegen')
    args = ap.parse_args()
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        raise SystemExit('faster-whisper fehlt: pip install faster-whisper num2words scipy')
    if not os.path.exists(es.PLAN):
        raise SystemExit('src/data/sprechplan.json fehlt: python scripts/sprechervorlage.py plan')
    plan = load_plan()

    src = args.aufnahme
    if os.path.isdir(src):
        paths = sorted(os.path.join(src, f) for f in os.listdir(src) if f.lower().endswith(AUDIO_EXT))
    else:
        paths = [src]
    if not paths:
        raise SystemExit(f'Keine Aufnahmen gefunden in {src}')
    takes = classify(paths, plan)
    takes.sort(key=lambda t: {'gesamt': 0, 'szene': 1, 'abschnitt': 2}[t[0]])   # retakes last, so they win

    by_seg, placed, notes = {}, {}, []
    label = {'gesamt': 'ganzes Video', 'szene': 'Szene', 'abschnitt': 'Abschnitt'}
    for kind, key, path in takes:
        name = os.path.basename(path)
        print(f'{name}: Whisper hört zu …', flush=True)
        audio = es.load(path)
        words = es.take_words(path, audio, args.modell)
        segs = scope(plan, kind, key, path)
        found = es.locate([(s['id'], [x['text'] for x in s['sentences']]) for s in segs], words)
        pieces = cut(segs, audio, found, words)
        where = label[kind] + ('' if key is None else f' {key}')
        if not pieces:
            notes.append(f'{name}: nichts aus {where} erkannt – nicht verwendet')
            continue
        drift = np.array([pc['due'] - pc['on'] for pc in pieces])
        offset = float(np.median(drift))
        if args.ohne_feinabgleich:
            for pc in pieces:
                pc['due'] = pc['on'] + offset
        for sid in found:
            mine = [pc for pc in pieces if pc['sid'] == sid]
            if mine:
                by_seg[sid] = mine
                placed[sid] = (found[sid], mine)
        n_sent = sum(len(s['sentences']) for s in segs)
        n_found = sum(1 for f in found.values() for s in f['spans'] if s)
        dev = np.abs(drift - offset)
        worst = pieces[int(np.argmax(dev))]
        start = f'bei {es.clock(offset)} im Video' if offset >= 0 else f'{-offset:.1f} s vor dem Video'
        print(f'  {where}: Aufnahme beginnt {start}; {len(found)} von {len(segs)} Abschnitten, '
              f'{n_found} von {n_sent} Sätzen gefunden')
        print(f'  Abweichung vom Takt der Vorlage: Median {np.median(dev):.2f} s, größte {dev.max():.2f} s '
              f'(Abschnitt {worst["sid"]}, Satz {worst["k"] + 1})'
              + ('' if args.ohne_feinabgleich else ' – wird angeglichen'))
        lost = [s['id'] for s in segs if s['id'] not in found]
        if lost:
            notes.append(f'{name}: nicht gefunden, bitte anhören: ' + summarize(lost, plan))
        gaps = [f'{sid}/{k + 1}' for sid, f in found.items() for k, s in enumerate(f['spans']) if s is None]
        if gaps:
            notes.append(f'{name}: Sätze kaum erkannt (bleiben am Satz davor): ' + ', '.join(gaps))
        extra = [f'{sid} (ab {es.clock(words[f["lo"]][1])})' for sid, f in found.items() if f['surplus'] >= 25]
        if extra:
            notes.append(f'{name}: mehr Wörter als im Skript – Versprecher oder Wiederholung? Abschnitt '
                         + ', '.join(extra))

    order = [s['id'] for s in plan['segments']]
    pieces = [pc for ps in by_seg.values() for pc in ps]
    total = plan['total']
    track = np.zeros(int(round(total * es.RATE)) + es.RATE, dtype=np.float32)
    assemble(pieces, track)
    moved = {}
    for pc in pieces:
        if abs(pc['late']) > 0.5 and abs(pc['late']) > abs(moved.get(pc['sid'], 0.0)):
            moved[pc['sid']] = pc['late']
    if pieces:
        dev = np.abs([pc['late'] for pc in pieces])
        print(f'Sätze im Video gegenüber der Animation: {np.mean(dev < 0.1):.0%} genau'
              + (f', sonst im Median {np.median(dev[dev >= 0.1]):.2f} s daneben' if (dev >= 0.1).any() else ''))
    cut_off = [f'{pc["sid"]} ({pc["trimmed"]:.1f} s)' for pc in pieces if pc['trimmed'] > 0.3]
    if cut_off:
        notes.append('Stimme beim Anlegen abgeschnitten, bitte anhören: Abschnitt ' + ', '.join(cut_off))
    if moved:
        notes.append(('weicht um mehr als 0,5 s von der Animation ab: Abschnitt ' if args.ohne_feinabgleich
                      else 'länger gesprochen als Platz war, um mehr als 0,5 s verschoben: Abschnitt ')
                     + ', '.join(f'{s} ({v:+.1f} s)' for s, v in sorted(moved.items(), key=lambda x: order.index(x[0]))))
    silent = [sid for sid in order if sid not in by_seg]
    if silent:
        notes.append('ohne Aufnahme (dort ist jetzt nur Musik): ' + summarize(silent, plan))
    for line in notes:
        print('Hinweis: ' + line)

    os.makedirs(es.WORK, exist_ok=True)
    voice = os.path.join(es.WORK, 'stimme.wav')
    with wave.open(voice, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(es.RATE)
        w.writeframes((np.clip(track[:int(round(total * es.RATE))], -1, 1) * 32767).astype(np.int16).tobytes())
    if not os.path.exists(PAD):
        subprocess.run([sys.executable, os.path.join(es.ROOT, 'scripts', 'music.py')], check=True)
    mix(voice, total, args.music_db, args.ziel)
    print(f'Video mit eigener Stimme: {args.ziel}')

    srt = os.path.splitext(args.ziel)[0] + '.srt'
    cues = subtitles(plan, placed, track)
    write_srt(srt, cues)
    print(f'Untertitel: {srt} ({len(cues)})')


def mix(voice, total, music_db, out):
    """Voice + ambient pad as in scripts/mix.py, with the picture of video/Theaitetos.mp4."""
    gain = 10 ** (music_db / 20)
    graph = (
        '[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[v][sc];'
        f'[2:a]aresample=48000,highpass=f=70,volume={gain:.4f},atrim=0:{total:.3f},'
        f'afade=t=in:d=5,afade=t=out:st={total - 10:.3f}:d=10[m];'
        '[m][sc]sidechaincompress=threshold=0.02:ratio=5:attack=200:release=1500:makeup=1[md];'
        '[v]highpass=f=70[vh];[vh][md]amix=inputs=2:duration=first:normalize=0,'
        'loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]'
    )
    tmp = os.path.join(es.WORK, 'neu.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', es.VIDEO, '-i', voice, '-stream_loop', '-1', '-i', PAD,
                    '-filter_complex', graph, '-map', '0:v', '-map', '[a]',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
                    '-t', f'{total:.3f}', tmp], check=True)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    os.replace(tmp, out)


if __name__ == '__main__':
    sys.exit(main())
