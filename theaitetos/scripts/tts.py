"""Synthesise the narration with Piper and record segment durations.

Reads src/data/script.json, writes public/audio/<scene>-<n>.wav and
src/data/timing.json ({scene id: [seconds per segment]}). Segments whose text
has not changed since the last run are reused.

Usage: PIPER_PYTHON=/path/to/venv/bin/python python3 scripts/tts.py
   or: /path/to/venv/bin/python scripts/tts.py --model voice.onnx
"""

import argparse
import hashlib
import json
import os
import re
import wave

import numpy as np
from piper import PiperVoice, SynthesisConfig

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'src', 'data', 'script.json')
TIMING = os.path.join(ROOT, 'src', 'data', 'timing.json')
AUDIO = os.path.join(ROOT, 'public', 'audio')
MANIFEST = os.path.join(AUDIO, 'manifest.json')

# Pause between sentences inside one segment, in seconds.
SENTENCE_PAUSE = 0.38
# How the synthesiser should pronounce words it would otherwise mangle.
# Only the spoken text changes; the script keeps the proper spelling.
PRONUNCIATION = {
    'G. E. L. Owen': 'Oh-in',
    'Phainarete': 'Phai-naréte',
    'Theaitetos': 'Theai-tetos',
    'Kyrene': 'Kürehne',
    'Gettier': 'Gettjer',
    'Burnyeat': 'Börnjet',
    'Myles': 'Mails',
    'Sedley': 'Seddli',
    'Geach': 'Gietsch',
    'Ryle': 'Rail',
    'Jones': 'Dschohns',
    'Kitharaspieler': 'Kithara-Spieler',
    'Gail Fine': 'Gejl Fain',
}


def spoken(text: str) -> str:
    for word, say in PRONUNCIATION.items():
        text = text.replace(word, say)
    # Typographic quotes and dashes confuse the phonemizer.
    text = re.sub(r'[„“”‚‘’»«]', '', text)
    return text.replace('–', ', ')


def synthesize(voice: PiperVoice, text: str, config: SynthesisConfig) -> np.ndarray:
    rate = voice.config.sample_rate
    pause = np.zeros(int(SENTENCE_PAUSE * rate), dtype=np.int16)
    parts = []
    for chunk in voice.synthesize(spoken(text), syn_config=config):
        if parts:
            parts.append(pause)
        parts.append(chunk.audio_int16_array)
    return np.concatenate(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--length-scale', type=float, default=1.06)
    args = parser.parse_args()

    os.makedirs(AUDIO, exist_ok=True)
    script = json.load(open(SCRIPT, encoding='utf-8'))
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    voice = PiperVoice.load(args.model)
    config = SynthesisConfig(length_scale=args.length_scale, noise_scale=0.6, noise_w_scale=0.8)
    # Only the text actually spoken (after pronunciation fixes) decides whether a
    # segment must be re-synthesised; Piper is not deterministic, so unchanged
    # segments must keep their audio and timing.
    key_extra = f'{os.path.basename(args.model)}|{args.length_scale}|{SENTENCE_PAUSE}'

    timing = {}
    for scene in script['scenes']:
        durations = []
        for i, seg in enumerate(scene['segments']):
            name = f"{scene['id']}-{i}.wav"
            path = os.path.join(AUDIO, name)
            digest = hashlib.sha1((spoken(seg['text']) + key_extra).encode()).hexdigest()
            if manifest.get(name, {}).get('hash') != digest or not os.path.exists(path):
                audio = synthesize(voice, seg['text'], config)
                with wave.open(path, 'wb') as w:
                    w.setnchannels(1)
                    w.setsampwidth(2)
                    w.setframerate(voice.config.sample_rate)
                    w.writeframes(audio.tobytes())
                manifest[name] = {'hash': digest, 'seconds': len(audio) / voice.config.sample_rate}
                print(f'synthesised {name}: {manifest[name]["seconds"]:.1f}s')
            durations.append(round(manifest[name]['seconds'], 3))
        timing[scene['id']] = durations

    json.dump(manifest, open(MANIFEST, 'w'), indent=1)
    json.dump(timing, open(TIMING, 'w'), indent=1)
    total = sum(sum(v) for v in timing.values())
    print(f'total narration: {total / 60:.1f} min')


if __name__ == '__main__':
    main()
