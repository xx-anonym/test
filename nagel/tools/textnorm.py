"""Turn script text into what the German TTS voice should actually say.

Only the spoken form changes; subtitles and the script keep the normal
spelling. English names and titles get a German-phonetic respelling so that
Piper (a German voice) pronounces them roughly as in English.
"""

import re

from num2words import num2words

# Longest keys first, so that "The View from Nowhere" wins over "Nowhere".
PRONUNCIATION = {
    'The Philosophical Review': 'The Filosofikl Riwju',
    'Consciousness Explained': 'Konschesness Explejnd',
    'The View from Nowhere': 'The Wjuu from Nouwär',
    'The Question of Animal Awareness': 'The Kwestschen of Änimel Awärness',
    'Mind and Cosmos': 'Maind änd Kosmos',
    'Rockefeller University': 'Rockefeller Juniwörsiti',
    'New Yorker': 'Nju Jorker',
    'Pennsylvania': 'Pennsilwejnia',
    'echolocation': 'ekolokäjschen',
    'Allen-Hermanson': 'Ällen-Hermanson',
    'Kathleen Akins': 'Käthlien Ejkins',
    'Akins': 'Ejkins',
    'Frank Jackson': 'Fränk Dschäckson',
    'Jackson': 'Dschäckson',
    'Joseph Levine': 'Dschosef Lewien',
    'Levine': 'Lewien',
    'David Chalmers': 'Dejwid Tschalmers',
    'Chalmers': 'Tschalmers',
    'Ned Block': 'Näd Block',
    'Daniel Dennett': 'Dänjel Dennett',
    'David Lewis': 'Dejwid Luis',
    'Lewis': 'Luis',
    'Laurence Nemirow': 'Lorenz Nemiroff',
    'Peter Hacker': 'Pieter Häcker',
    'Hacker': 'Häcker',
    'Keith Frankish': 'Kieth Fränkisch',
    'Frankish': 'Fränkisch',
    'Donald Griffin': 'Donnld Griffin',
    'Robert Galambos': 'Robert Galambos',
    'Nobuo Suga': 'Nobuo Suga',
    'Lore Thaler': 'Lore Taler',
    'Patrick Butlin': 'Pätrick Batlin',
    'Robert Long': 'Robert Long',
    'Timothy Sprigge': 'Timmoti Sprigg',
    'Sprigge': 'Sprigg',
    'B. A. Farrell': 'Bi Ej Färrel',
    'Farrell': 'Färrel',
    'Bernard Williams': 'Börnard Williams',
    'Brian Leiter': 'Braien Laiter',
    'Michael Weisberg': 'Maikel Waisberg',
    'Ullin Place': 'Ullin Pläis',
    'J. J. C. Smart': 'Dschej Dschej Ssi Smart',
    'Hilary Putnam': 'Hilleri Patnam',
    'Putnam': 'Patnam',
    'David Armstrong': 'Dejwid Armstrong',
    'Thomas Nagel': 'Tomas Nejgel',
    'Nagels': 'Nejgels',
    'Nagel': 'Nejgel',
    'Mary': 'Märi',
    'Mind': 'Maind',
    'Smart': 'Smart',
    'Fußnote': 'Fuß-Note',
    'Fußnoten': 'Fuß-Noten',
    'H₂O': 'H zwei O',
    'DNA': 'De En A',
    'KI-System': 'Ka-I-System',
    'KI-Systeme': 'Ka-I-Systeme',
    'KI-Bericht': 'Ka-I-Bericht',
}

_KEYS = sorted(PRONUNCIATION, key=len, reverse=True)
_PATTERN = re.compile('|'.join(r'(?<![\wÄÖÜäöüß])' + re.escape(k) + r'(?![\wÄÖÜäöüß])' for k in _KEYS))


def _numbers(text: str) -> str:
    # Decimal numbers with comma: 61,0 -> einundsechzig Komma null
    text = re.sub(r'\b(\d+),(\d+)\b',
                  lambda m: f"{num2words(int(m.group(1)), lang='de')} Komma "
                            + ' '.join(num2words(int(d), lang='de') for d in m.group(2)), text)
    # Years
    text = re.sub(r'\b(1[0-9]{3}|20[0-9]{2})\b',
                  lambda m: num2words(int(m.group(1)), lang='de', to='year'), text)
    return re.sub(r'\b\d+\b', lambda m: num2words(int(m.group(0)), lang='de'), text)


def spoken(text: str) -> str:
    text = _PATTERN.sub(lambda m: PRONUNCIATION[m.group(0)], text)
    text = _numbers(text)
    text = re.sub(r'[„“”‚‘’»«*]', '', text)
    text = text.replace(' – ', ', ').replace('–', ', ')
    return re.sub(r'\s+', ' ', text).strip()


if __name__ == '__main__':
    import sys
    print(spoken(' '.join(sys.argv[1:])))
