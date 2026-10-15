"""Read script/skript.md into chapters and paragraphs.

The approved script is the single source of truth for what is spoken and
which citations appear on screen. Each paragraph block looks like:

    #### 3.1
    > narration …
    - **Beleg:** … · Einblendung „Nagel 1974, S. 436“ · Zitat: „…“
    - **Szene:** …

A narration line of the form ``*[Hörbeispiel, 7 Sekunden, ohne Sprecher]*``
marks a pause for a sound clip after the paragraph.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'script', 'skript.md')

QUOTED = re.compile(r'„([^“]*)“')


def _overlays(beleg: str):
    """Return the on-screen citations and quotes named in a Beleg line.

    Citations are all „…“ strings between "Einblendung(en)" and "Zitat";
    quotes are the „…“ strings after "Zitat".
    """
    start = beleg.find('Einblendung')
    if start < 0:
        return [], []
    zitat = beleg.find('Zitat', start)
    cites = QUOTED.findall(beleg[start:zitat if zitat > 0 else None])
    quotes = QUOTED.findall(beleg[zitat:]) if zitat > 0 else []
    return [c.strip() for c in cites], [q.strip() for q in quotes]


def parse(path: str = SCRIPT):
    chapters, chap, para, field = [], None, None, None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        m = re.match(r'## Kapitel (\d+) – (.+)', line)
        if m:
            chap = {'n': int(m.group(1)), 'title': m.group(2).strip(), 'paragraphs': []}
            chapters.append(chap)
            para = None
            continue
        if line.startswith('## '):
            chap, para = None, None
            continue
        if chap is None:
            continue
        m = re.match(r'#### (\d+\.\d+)', line)
        if m:
            para = {'id': m.group(1), 'text': '', 'beleg': '', 'scene': '', 'clip': None}
            chap['paragraphs'].append(para)
            field = None
            continue
        if para is None:
            continue
        if line.startswith('>'):
            body = line[1:].strip()
            clip = re.match(r'\*\[Hörbeispiel, (\d+) Sekunden', body)
            if clip:
                para['clip'] = int(clip.group(1))
            elif body:
                para['text'] = (para['text'] + ' ' + body).strip()
            field = None
        elif line.startswith('- **Beleg:**'):
            field = 'beleg'
            para['beleg'] = line.split('**Beleg:**', 1)[1].strip()
        elif line.startswith('- **Szene:**'):
            field = 'scene'
            para['scene'] = line.split('**Szene:**', 1)[1].strip()
        elif line.startswith('  ') and field:
            para[field] += ' ' + line.strip()
        else:
            field = None
    for c in chapters:
        for p in c['paragraphs']:
            p['cites'], p['quotes'] = _overlays(p['beleg'])
            p['sentences'] = split_sentences(p['text'])
    return chapters


def split_sentences(text: str):
    """Split at sentence ends that are followed by an upper-case start."""
    parts = re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„0-9])', text)
    return [p.strip() for p in parts if p.strip()]


def chapter(n: int, path: str = SCRIPT):
    for c in parse(path):
        if c['n'] == n:
            return c
    raise KeyError(f'Kapitel {n} nicht im Skript')


if __name__ == '__main__':
    data = parse()
    if len(sys.argv) > 1:
        data = [c for c in data if str(c['n']) in sys.argv[1:]]
    json.dump(data, sys.stdout, ensure_ascii=False, indent=1)
