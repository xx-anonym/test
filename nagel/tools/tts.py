"""Synthesise the narration with Piper, one sentence at a time.

Writes audio/narration/<paragraph>.wav and audio/timing.json:

    {"3.1": {"duration": 18.4,
             "sentences": [{"text": "…", "start": 0.0, "end": 9.1}, …]}, …}

Sentence times let scenes and subtitles follow the voice closely. Piper is
not deterministic, so a paragraph is only re-synthesised when its spoken text
(or the voice settings) changed; otherwise the cached audio and timing stay.

Usage:
    python tools/tts.py --model de_DE-thorsten-high.onnx [--chapters 3 4] [--verify] [--force]

--verify: synthesise each sentence up to three times and keep the take that
Whisper (medium) transcribes closest to the script; sentences that never
come out clean are listed in audio/asr_report.txt for listening.
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import wave

import numpy as np
from piper import PiperVoice, SynthesisConfig

from script_parse import parse
from textnorm import PRONUNCIATION, spoken

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'audio', 'narration')
TIMING = os.path.join(ROOT, 'audio', 'timing.json')

LENGTH_SCALE = 1.06   # slightly slower than Piper's default
SENTENCE_PAUSE = 0.38  # seconds of silence between sentences
TRIM_DB = -50          # trim leading/trailing silence below this level


def _trim(a: np.ndarray, rate: int) -> np.ndarray:
    """Remove silence at both ends, keeping 30 ms of margin."""
    level = np.abs(a.astype(np.float32)) / 32768.0
    loud = np.flatnonzero(level > 10 ** (TRIM_DB / 20))
    if not len(loud):
        return a
    margin = int(0.03 * rate)
    return a[max(0, loud[0] - margin): loud[-1] + margin]


class Judge:
    """Scores a synthesised sentence by how well Whisper recovers the script.

    Names with a phonetic respelling are left out of the comparison, since
    Whisper cannot be expected to spell them as in the script.
    """

    ATTEMPTS = 3

    def __init__(self, model: str = 'medium'):
        from faster_whisper import WhisperModel
        from scipy.signal import resample_poly
        self.model = WhisperModel(model, device='cpu', compute_type='int8')
        self.resample = resample_poly
        self.skip = {w for k, v in PRONUNCIATION.items() if k != v for w in _words(k)}
        self.report = []

    def score(self, sentence: str, audio: np.ndarray, rate: int):
        a = audio.astype(np.float32) / 32768
        g = np.gcd(rate, 16000)
        a = self.resample(a, 16000 // g, rate // g).astype(np.float32)
        hyp = ' '.join(s.text.strip() for s in self.model.transcribe(a, language='de', beam_size=5)[0])
        # Share of script words that Whisper recovers in order. Extra words in
        # the transcript (e.g. "Nägel" for the English "Nagel") do not count.
        ref = [w for w in _words(sentence) if w not in self.skip]
        got = _words(hyp)
        matched = sum(b.size for b in difflib.SequenceMatcher(a=ref, b=got, autojunk=False).get_matching_blocks())
        return (matched / len(ref) if ref else 1.0), hyp


def _words(text: str):
    return re.sub(r'[^\wÄÖÜäöüß\s]', ' ', text.lower().replace('-', ' ')).split()


def synth_sentence(voice, config, sentence, judge=None, pid=''):
    rate = voice.config.sample_rate
    best = None
    for attempt in range(judge.ATTEMPTS if judge else 1):
        chunks = [c.audio_int16_array for c in voice.synthesize(spoken(sentence), syn_config=config)]
        audio = _trim(np.concatenate(chunks), rate)
        if not judge:
            return audio
        score, hyp = judge.score(sentence, audio, rate)
        if best is None or score > best[0]:
            best = (score, audio, hyp)
        if score >= 0.999:
            break
    if best[0] < 0.999:
        judge.report.append(f'{pid} | {best[0]:.2f} | Skript: {sentence}\n      | gehört: {best[2]}')
    return best[1]


def synth_paragraph(voice, config, sentences, judge=None, pid=''):
    rate = voice.config.sample_rate
    pause = np.zeros(int(SENTENCE_PAUSE * rate), dtype=np.int16)
    parts, times, t = [], [], 0.0
    for i, sent in enumerate(sentences):
        audio = synth_sentence(voice, config, sent, judge, pid)
        if i:
            parts.append(pause)
            t += SENTENCE_PAUSE
        parts.append(audio)
        dur = len(audio) / rate
        times.append({'text': sent, 'start': round(t, 3), 'end': round(t + dur, 3)})
        t += dur
    return np.concatenate(parts), times


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True)
    ap.add_argument('--chapters', nargs='*', type=int)
    ap.add_argument('--paragraphs', nargs='*', help='only these paragraph ids, e.g. 4.5 9.2')
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--force', action='store_true', help='re-synthesise even if cached')
    args = ap.parse_args()
    judge = Judge() if args.verify else None

    os.makedirs(OUT, exist_ok=True)
    timing = json.load(open(TIMING)) if os.path.exists(TIMING) else {}
    voice = PiperVoice.load(args.model)
    config = SynthesisConfig(length_scale=LENGTH_SCALE, noise_scale=0.6, noise_w_scale=0.8)
    settings = f'{os.path.basename(args.model)}|{LENGTH_SCALE}|{SENTENCE_PAUSE}|{TRIM_DB}'

    for chap in parse():
        if args.chapters and chap['n'] not in args.chapters:
            continue
        for p in chap['paragraphs']:
            pid = p['id']
            if args.paragraphs and pid not in args.paragraphs:
                continue
            key = hashlib.sha1(('\n'.join(spoken(s) for s in p['sentences']) + settings).encode()).hexdigest()
            path = os.path.join(OUT, f'{pid}.wav')
            if not args.force and timing.get(pid, {}).get('hash') == key and os.path.exists(path):
                # Subtitle text may change without changing the spoken text.
                for s, txt in zip(timing[pid]['sentences'], p['sentences']):
                    s['text'] = txt
                continue
            audio, times = synth_paragraph(voice, config, p['sentences'], judge, pid)
            with wave.open(path, 'wb') as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(voice.config.sample_rate)
                w.writeframes(audio.tobytes())
            timing[pid] = {'hash': key, 'duration': round(len(audio) / voice.config.sample_rate, 3),
                           'sentences': times}
            print(f'{pid}: {timing[pid]["duration"]:.1f} s')
            json.dump(timing, open(TIMING, 'w'), ensure_ascii=False, indent=1)

    json.dump(timing, open(TIMING, 'w'), ensure_ascii=False, indent=1)
    if judge:
        report = os.path.join(ROOT, 'audio', 'asr_report.txt')
        with open(report, 'w', encoding='utf-8') as f:
            f.write('Sätze, die Whisper nicht wortgleich erkannt hat (bitte anhören):\n\n')
            f.write('\n'.join(judge.report) + '\n')
        print(f'{len(judge.report)} Sätze im Prüfbericht {report}')
    total = sum(v['duration'] for v in timing.values())
    print(f'Sprechzeit (alle synthetisierten Absätze): {total / 60:.1f} min')


if __name__ == '__main__':
    main()
