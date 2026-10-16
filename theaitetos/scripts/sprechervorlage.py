"""Karaoke guide for recording the narration yourself.

    python scripts/sprechervorlage.py          # plan, karaoke subtitles and guide video
    python scripts/sprechervorlage.py plan     # only src/data/sprechplan.json
    python scripts/sprechervorlage.py ass      # only video/karaoke.ass (needs the plan)
    python scripts/sprechervorlage.py video    # only out/sprechervorlage.mp4 (needs the ass)

The plan says when the current narration of video/Theaitetos.mp4 speaks every sentence and
word: Whisper transcribes the video's soundtrack (cached in out/eigene_stimme/), the words
are matched to src/data/script.json, and sentence starts are set on the voice onset. The
karaoke subtitles light every word up at that moment, so a speaker who follows them stays
in sync with the animation; scripts/stimme_ersetzen.py lays a recording onto the same plan.
Needs faster-whisper, num2words, scipy (as for scripts/tts.py, in a virtual environment).
"""

import argparse
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eigene_stimme as es  # noqa: E402
from srt import chunks, wrap  # noqa: E402

ASS = os.path.join(es.ROOT, 'video', 'karaoke.ass')
GUIDE = os.path.join(es.ROOT, 'out', 'sprechervorlage.mp4')
VOICE_DELAY = 0.05    # Piper starts speaking this long after a segment's first frame

LEAD = 0.8            # a line appears this long before its first word
HOLD = 0.35           # and stays this long after its last word
NEXT_WINDOW = 6.0     # show the following line if it starts within this many seconds


# ------------------------------------------------------------ the plan
def voice_envelope(audio):
    """Envelope above 1.5 kHz: the ambient pad is low-passed at 1.5 kHz (scripts/music.py),
    so only the voice is left there (pad alone: about −100 dB, voice: about −35 dB)."""
    from scipy.signal import butter, sosfiltfilt
    sos = butter(4, 1500, 'highpass', fs=es.RATE, output='sos')
    return es.envelope(sosfiltfilt(sos, audio).astype(np.float32))


def build_plan(model):
    segs = es.segments()
    words = es.take_words(es.VIDEO, None, model)
    found = es.locate([(s['id'], s['sentences']) for s in segs], words)
    env = voice_envelope(es.load(es.VIDEO))
    total = len(env) * es.HOP

    # every sentence starts with the first voice after the pause that follows the one before;
    # Whisper often lets a word begin inside the pause in front of it
    seq, missing = [], []
    for seg in segs:
        f = found.get(seg['id'])
        if f is None or any(sp is None for sp in f['spans']):
            missing.append(seg['id'])
            continue
        for k, (t0, t1, head) in enumerate(f['spans']):
            seq.append((seg['id'], k, t0, t1, head, f['tokens'][k]))
    timed, prev = {}, None
    for i, (sid, k, t0, t1, head, heard) in enumerate(seq):
        lo = t0 - 0.3 if prev is None else max(prev['start'] + 0.3, min(prev['t1'], t0) - 0.6)
        p = es.pause_near(env, lo, min(t1, head + 0.6), head, min_len=0.15)
        on = es.first_loud(env, p if p is not None else max(lo, t0 - 0.3), head + 0.3)
        if on is None:                          # the first word was dated far too early
            on = es.first_loud(env, p if p is not None else lo, t1)
        timed[(sid, k)] = prev = {'start': on if on is not None else t0, 'pause': p, 't1': t1, 'heard': heard}
    keys = list(timed)
    for a, b in zip(keys, keys[1:] + [None]):
        stop = timed[b]['pause'] if b and timed[b]['pause'] else (timed[b]['start'] - 0.1 if b else timed[a]['t1'] + 0.5)
        off = es.last_loud(env, timed[a]['start'], stop)
        timed[a]['end'] = off if off is not None else timed[a]['t1']

    out = []
    for seg in segs:
        if seg['id'] in missing:                # fall back to the even layout of scripts/srt.py
            sents = even_layout(seg)
        else:
            sents = [{'text': text, **timed[(seg['id'], k)]} for k, text in enumerate(seg['sentences'])]
        for s in sents:
            weights = [max(1, len(''.join(es.norm_words(t)))) for t in s['text'].split()]
            heard = s.get('heard') or [None] * len(weights)
            heard = [t if t is None or s['start'] < t < s['end'] else None for t in heard]
            heard[0] = s['start']
            for key in ('heard', 'pause', 't1'):
                s.pop(key, None)
            s['words'] = [round(t, 3) for t in es.fill_times(heard, s['start'], s['end'], weights)]
            s['start'], s['end'] = round(s['start'], 3), round(s['end'], 3)
        out.append({'id': seg['id'], 'scene': seg['scene'], 'scene_id': seg['scene_id'],
                    'chapter': seg['chapter'], 'title': seg['title'], 'sentences': sents})
    plan = {'source': 'video/Theaitetos.mp4, Whisper ' + model, 'total': round(total, 3), 'segments': out}
    with open(es.PLAN, 'w', encoding='utf-8') as fh:
        json.dump(plan, fh, ensure_ascii=False, indent=1)
    print(f'{es.PLAN}: {len(out)} Abschnitte, {sum(len(s["sentences"]) for s in out)} Sätze'
          + (f'; nach Schätzung (Whisper unsicher): {", ".join(missing)}' if missing else ''))
    return plan


def even_layout(seg):
    """Sentences spread over the segment as scripts/srt.py does (0.38 s pauses)."""
    pause = 0.38
    speak = seg['secs'] - pause * (len(seg['sentences']) - 1)
    total = sum(len(s) for s in seg['sentences'])
    t, out = seg['start'] + VOICE_DELAY, []
    for text in seg['sentences']:
        d = speak * len(text) / total
        out.append({'text': text, 'start': t, 'end': t + d})
        t += d + pause
    return out


def load_plan():
    with open(es.PLAN, encoding='utf-8') as fh:
        return json.load(fh)


# ------------------------------------------------------------ karaoke subtitles
HEADER = """[Script Info]
Title: Sprechervorlage – Theaitetos
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Inter,58,&H006BB5D9,&H00D9E6EC,&H30150F0D,&H00000000,-1,0,0,0,100,100,0,0,3,16,0,2,80,80,120,1
Style: Naechste,Inter,36,&H008C969A,&H008C969A,&H30150F0D,&H00000000,0,0,0,0,100,100,0,0,3,10,0,2,80,80,30,1
Style: Info,Inter,30,&H006BB5D9,&H006BB5D9,&H30150F0D,&H00000000,-1,0,0,0,100,100,0,0,3,10,0,9,40,40,30,1
Style: Pause,Inter,52,&H00D9E6EC,&H00D9E6EC,&H30150F0D,&H00000000,-1,0,0,0,100,100,0,0,3,18,0,5,40,40,40,1

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


def build_lines(plan):
    lines = []
    for seg in plan['segments']:
        for s in seg['sentences']:
            toks, times, k = s['text'].split(), s['words'], 0
            for piece in chunks(s['text']):
                n = len(piece.split())
                items = list(zip(toks[k:k + n], times[k:k + n]))
                end = times[k + n] if k + n < len(times) else s['end']
                lines.append({'start': items[0][1], 'end': end, 'items': items, 'text': piece})
                k += n
    return lines


def karaoke_text(line, shown_from):
    """\\kf tags in centiseconds; a silent lead-in before the first word, line breaks as in the SRT."""
    wrapped = wrap(line['text'])
    first_line_words = len(wrapped.split('\n')[0].split())
    parts = [f'{{\\k{int(round((line["items"][0][1] - shown_from) * 100))}}}']
    items = line['items']
    for i, (word, t0) in enumerate(items):
        t1 = items[i + 1][1] if i + 1 < len(items) else line['end']
        sep = '\\N' if i + 1 == first_line_words and '\n' in wrapped else (' ' if i + 1 < len(items) else '')
        parts.append(f'{{\\kf{max(1, int(round((t1 - t0) * 100)))}}}{_esc(word)}{sep}')
    return ''.join(parts)


def write_ass(plan):
    lines = build_lines(plan)
    events, shown = [], []
    for i, ln in enumerate(lines):
        start = ln['start'] - LEAD
        if shown:
            start = max(start, shown[-1][1])
        nxt = lines[i + 1]['start'] - LEAD if i + 1 < len(lines) else ln['end'] + HOLD
        shown.append((start, min(ln['end'] + HOLD, max(nxt, ln['end']))))
    for i, (ln, (start, end)) in enumerate(zip(lines, shown)):
        events.append(f'Dialogue: 1,{_t(start)},{_t(end)},Karaoke,,0,0,0,,{karaoke_text(ln, start)}')
        if i + 1 < len(lines) and lines[i + 1]['start'] - ln['end'] < NEXT_WINDOW:
            events.append(f'Dialogue: 0,{_t(start)},{_t(end)},Naechste,,0,0,0,,{_esc(lines[i + 1]["text"])}')
    prev_end = 0.0
    for seg in plan['segments']:
        a, b = seg['sentences'][0]['start'], seg['sentences'][-1]['end']
        label = f'Abschnitt {seg["id"]} · {seg["title"]}'
        if a - prev_end >= 1.5:                  # announce a segment after a longer pause
            events.append(f'Dialogue: 0,{_t(max(prev_end, a - 2.0))},{_t(a)},Info,,0,0,0,,gleich: {_esc(label)}')
        events.append(f'Dialogue: 0,{_t(a)},{_t(b)},Info,,0,0,0,,{_esc(label)}')
        prev_end = b
    events.append(f'Dialogue: 0,{_t(prev_end + 1.0)},{_t(plan["total"])},Pause,,0,0,0,,Abspann – Ende der Aufnahme')
    with open(ASS, 'w', encoding='utf-8') as f:
        f.write(HEADER + '\n'.join(events) + '\n')
    print(f'{ASS} ({len(lines)} Zeilen, {plan["total"] / 60:.1f} min)')


def burn_video():
    os.makedirs(os.path.dirname(GUIDE), exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', es.VIDEO, '-an',
                    '-vf', f'scale=1280:720,ass={ASS}',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart', GUIDE], check=True)
    print(GUIDE)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('schritt', nargs='?', choices=['plan', 'ass', 'video'])
    ap.add_argument('--modell', default='small', help='Whisper-Modell (Standard: small)')
    args = ap.parse_args()
    if args.schritt in (None, 'plan'):
        plan = build_plan(args.modell)
    if args.schritt in (None, 'ass'):
        write_ass(plan if args.schritt is None else load_plan())
    if args.schritt in (None, 'video'):
        burn_video()


if __name__ == '__main__':
    main()
