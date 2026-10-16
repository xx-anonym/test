"""output/quellen.pdf: the source list (research/quellen.md) plus, as an appendix, every
paragraph of the script with its source references and on-screen citations.

    python tools/make_pdf.py

Needs pandoc and a Chromium/Chrome binary (CHROME environment variable, otherwise
/opt/pw-browsers/chromium-1194/chrome-linux/chrome or `chromium` on the PATH).
"""

import os
import re
import shutil
import subprocess
import tempfile

from script_parse import parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, 'assets', 'fonts')
OUT = os.path.join(ROOT, 'output', 'quellen.pdf')

CSS = """
@font-face { font-family: 'Source Serif 4'; src: url('file://%(f)s/SourceSerif4-Regular.ttf'); }
@font-face { font-family: 'Source Serif 4'; font-style: italic; src: url('file://%(f)s/SourceSerif4-It.ttf'); }
@font-face { font-family: 'Source Serif 4'; font-weight: 600; src: url('file://%(f)s/SourceSerif4-Semibold.ttf'); }
@font-face { font-family: 'Inter'; src: url('file://%(f)s/Inter-Regular.otf'); }
@font-face { font-family: 'Inter'; font-weight: 600; src: url('file://%(f)s/Inter-SemiBold.otf'); }
@page { size: A4; margin: 18mm 17mm 20mm 17mm; }
body { font-family: 'Source Serif 4', serif; font-size: 10.2pt; line-height: 1.42; color: #1d2230; }
h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 600; color: #10141c; }
h1 { font-size: 18pt; margin: 0 0 6mm; }
h2 { font-size: 13pt; margin: 8mm 0 3mm; border-bottom: 1px solid #c9c2b3; padding-bottom: 1mm; }
h3 { font-size: 10.5pt; margin: 5mm 0 1.5mm; break-after: avoid; }
table { border-collapse: collapse; width: 100%%; font-size: 8.8pt; margin: 2mm 0 4mm; }
th, td { border: 1px solid #d8d2c4; padding: 1.2mm 1.6mm; vertical-align: top; text-align: left; }
th { background: #f1ede4; font-family: 'Inter', sans-serif; font-weight: 600; }
code { font-size: 8.8pt; }
a { color: #6b4b12; word-break: break-all; }
ul { padding-left: 5mm; }
.ok, .meta, .sec { font-family: 'Inter', sans-serif; font-size: 8pt; font-weight: 600; padding: 0 1.2mm;
                   border-radius: 1mm; white-space: nowrap; }
.ok { background: #dcefe2; color: #1f5f35; }
.meta { background: #e6ebf3; color: #2c4466; }
.sec { background: #f7e6c8; color: #7a4c00; }
.para { break-inside: avoid; margin: 0 0 3mm; }
.para .id { font-family: 'Inter', sans-serif; font-weight: 600; }
"""

BADGES = {'✅': '<span class="ok">✔ Volltext</span>', '☑️': '<span class="meta">✔ Abstract/Metadaten</span>',
          '⚠️': '<span class="sec">⚠ Sekundärquelle</span>'}


def badges(md):
    for k, v in BADGES.items():
        md = md.replace(k, v)
    return md


def appendix():
    lines = ['', '---', '', '## Anhang: Belege je Absatz des Skripts', '',
             'Für jeden gesprochenen Absatz (Kennung Kapitel.Absatz) die Belegangabe aus '
             '`script/skript.md` und die im Video unten rechts eingeblendete Kurzangabe.', '']
    for chap in parse():
        lines += [f"### Kapitel {chap['n']} – {chap['title']}", '']
        for p in chap['paragraphs']:
            cites = ' · '.join(p['cites']) or '–'
            beleg = re.split(r'\s+·\s+Einblendung', p['beleg'])[0]
            lines.append(f"<div class=\"para\"><span class=\"id\">{p['id']}</span> &nbsp; {beleg}<br>"
                         f"<em>Einblendung:</em> {cites}</div>")
            lines.append('')
    return '\n'.join(lines)


def chrome():
    for c in (os.environ.get('CHROME'), '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
              shutil.which('chromium'), shutil.which('chromium-browser'), shutil.which('google-chrome')):
        if c and os.path.exists(c):
            return c
    raise SystemExit('Kein Chromium gefunden (Umgebungsvariable CHROME setzen).')


def main():
    md = open(os.path.join(ROOT, 'research', 'quellen.md'), encoding='utf-8').read()
    md = badges(md) + appendix()
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 'quellen.md')
        css = os.path.join(tmp, 'style.css')
        html = os.path.join(tmp, 'quellen.html')
        open(src, 'w', encoding='utf-8').write(md)
        open(css, 'w', encoding='utf-8').write(CSS % {'f': FONTS})
        subprocess.run(['pandoc', src, '-f', 'gfm', '-t', 'html5', '--standalone', '--embed-resources',
                        '--css', css, '--metadata', 'title=Quellen', '--metadata', 'lang=de',
                        '-V', 'pagetitle=Quellen', '-o', html], check=True)
        # pandoc's own title block would duplicate the document's first heading
        page = open(html, encoding='utf-8').read()
        page = re.sub(r'<header id="title-block-header">.*?</header>', '', page, flags=re.S)
        open(html, 'w', encoding='utf-8').write(page)
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        subprocess.run([chrome(), '--headless', '--no-sandbox', '--disable-gpu', '--allow-file-access-from-files',
                        '--no-pdf-header-footer', f'--print-to-pdf={OUT}', f'file://{html}'],
                       check=True, capture_output=True)
    print(OUT)


if __name__ == '__main__':
    main()
