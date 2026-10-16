"""Bibliography for the credits, read from research/quellen.md (single source of truth).

Each entry's citation is the paragraph under its `### KEY` heading, cut before the
working notes (verification status, usage notes, abstracts). Markdown is reduced to
plain text; DOIs are kept, other links are shortened to their address.

    python tools/bibliography.py        # print the list
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLEN = os.path.join(ROOT, 'research', 'quellen.md')

# Working notes start with one of these phrases; the citation ends before them.
NOTES = ['Geprüft', 'Verwendung:', 'Von Nagel in Fn', 'Nur ', 'Kernaussage', 'Abstract', 'Aufsatz nicht',
         'Kritische Darstellung', 'Seitenzahlen', 'Nachweis über', 'Erscheinungsmonat', 'Angaben nach',
         'Lizenz CC', 'Griffin prägte', 'Rezension von `', '„Sprigge anticipated', 'Verlag und Jahr',
         'Auch Jackson', 'Leseprobe', 'Abschn. 17.2', 'Gemeinfrei', 'Wortlaut', 'Online-Fassung',
         'Rezension von NAGEL', 'Nach SALZANI', '„Nagel\'s arguments']

# Corrections for the credits (see the notes in quellen.md).
OVERRIDES = {
    # subtitle not independently verified → credits without subtitle
    'GRIFFIN1976': 'Griffin, Donald R. (1976): The Question of Animal Awareness. New York: Rockefeller '
                   'University Press.',
}

# Sources known only through others (⚠️ in quellen.md): say so in the credits.
SECONDHAND = {
    'AKINS1993': 'nicht selbst eingesehen; zitiert nach Allen-Hermanson 2015 und Salzani 2022',
    'GRIFFIN2001': 'nicht selbst eingesehen; zitiert nach Salzani 2022',
    'SPRIGGE1971': 'Wortlaut zitiert nach Seager 2011',
}


def _doi_links(text):
    """Replace „DOI: [doi](https://doi.org/doi)“ – DOIs may contain brackets and parentheses."""
    out = ''
    while True:
        m = re.search(r'DOI(?: des Kapitels)?:\s*\[', text)
        if not m:
            return out + text
        rest = text[m.end():]
        j = rest.find('](https://doi.org/')
        if j < 0:
            return out + text
        doi = rest[:j]
        end = j + len('](https://doi.org/') + len(doi) + 1
        out += text[:m.start()] + 'DOI ' + doi
        text = rest[end:]


def _clean(text):
    text = _doi_links(text)
    text = re.sub(r'DOI:\s*', 'DOI ', text)
    text = re.sub(r'\[(?:Link|PDF)\]\(https?://([^)]+)\)', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = text.replace('*', '').replace('`', '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _cut(text):
    cut = len(text)
    for note in NOTES:
        for m in re.finditer(re.escape(note), text):
            if m.start() > 20:          # never cut inside the author/year head
                cut = min(cut, m.start())
                break
    return text[:cut].strip().rstrip(';,')


def entries():
    src = open(QUELLEN, encoding='utf-8').read()
    body = src[:src.index('## I. Medien')]
    out = []
    for m in re.finditer(r'^### (.+)\n((?:(?!- |\n|### |## ).*\n)*)', body, re.M):
        head, para = m.group(1), m.group(2)
        keys = re.findall(r'[A-Z][A-Z0-9]+\d{4}[A-Z]*', head)
        status = '⚠️' if '⚠️' in head else ('✅' if '✅' in head else '☑️')
        text = para.replace('\n', ' ')
        if len(keys) > 1:                       # combined entry: split at the dashes
            for part in text.split(' – '):
                out.append((keys[0], _cut(_clean(part)), status))
            continue
        key = keys[0]
        out.append((key, OVERRIDES.get(key) or _cut(_clean(text)), status))
    out = [(k, t if t.endswith('.') else t + '.', s) for k, t, s in out]
    out = [(k, t + (f' – {SECONDHAND[k]}.' if k in SECONDHAND else ''), s) for k, t, s in out]
    return sorted(out, key=lambda e: e[1].lower())


if __name__ == '__main__':
    for k, t, s in entries():
        print(f'{s} {t}')
