# Wie ist es, eine Fledermaus zu sein? – Erklärvideo

Deutschsprachiges Erklärvideo (1080p, 30 fps) über Thomas Nagels Aufsatz
„What Is It Like to Be a Bat?“ (*The Philosophical Review* 83/4, 1974, S. 435–450): Rekonstruktion
des Arguments, Vorläufer, Wirkungsgeschichte, Einwände, die Biologie der Echoortung und die
heutige Debatte über Tier- und KI-Bewusstsein.

## Ergebnis

| Datei | Inhalt |
| --- | --- |
| `output/nagel_fledermaus.mp4` | das fertige Video (nicht im Repository, siehe unten) |
| `output/untertitel.srt` | deutsche Untertitel zum Gesamtvideo |
| `output/quellen.pdf` | Quellenverzeichnis mit Prüfstatus und Anhang „Belege je Absatz“ |

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| `research/quellen.md` | alle Quellen mit Prüfstatus, Seitenzahlen, Kernaussagen; Abschnitt I: Medien, Stimme, Lizenzen |
| `research/argument.md` | Nagels Argument als Prämissen und Schlüsse, Zuordnung der Einwände |
| `script/skript.md` | freigegebener Sprechertext mit Beleg und Szenenbeschreibung pro Absatz – einzige Quelle für Text und Einblendungen |
| `scenes/kit.py` | Gestaltung (Farben, Schriften, Belegleiste, Zitatkarte, Kapitelkarte, Leitmotiv) und Synchronisation an die Sprache |
| `scenes/parts.py` | wiederverwendbare Bausteine (Argumentbaum, Zeitachse, Abendlandschaft, Fledermausflug, Symbole) |
| `scenes/sNN_*.py` | eine Manim-Szene pro Kapitel (Klasse `KapitelN`); `s13_abspann.py` ist der Abspann |
| `tools/script_parse.py` | liest das Skript (Sprechertext, Sätze, Einblendungen, Zitate) |
| `tools/textnorm.py` | Aussprache für die Sprachausgabe (Zahlen, Namen, englische Titel) |
| `tools/tts.py` | Piper-Sprachausgabe satzweise, mit Satzzeiten; `--verify` prüft jeden Satz mit Whisper |
| `tools/timeline.py` | gemeinsamer Zeitplan für Szene, Tonspur und Untertitel |
| `tools/build.py` | Tonspur, Untertitel, Zusammenführen einer Szene (`scene N`) oder des Gesamtvideos (`final`) |
| `tools/render.py` | Stimme, Animation, Ton und Untertitel für ein oder mehrere Kapitel in einem Schritt |
| `tools/make_spectrogram.py` | Spektrogramm der CC0-Aufnahme für Kapitel 9 (`assets/img/`) |
| `tools/bibliography.py` | Literaturliste für den Abspann, gelesen aus `research/quellen.md` |
| `tools/make_pdf.py` | erzeugt `output/quellen.pdf` (pandoc + Chromium) |
| `tools/asr_check.py` | Whisper-Gegenprobe einzelner Absätze |
| `audio/timing.json` | gemessene Längen und Satzzeiten der Sprachaufnahmen |
| `assets/` | Schriften (OFL), Hörbeispiel (CC0), Spektrogramm |

## Einrichten

Systempakete: ffmpeg, pandoc, Chromium (für das PDF), Pango/Cairo-Entwicklerdateien
(für Manim; unter Debian/Ubuntu `libpango1.0-dev`, `libcairo2-dev`, `pkg-config`).

```bash
python3 -m venv venv
venv/bin/pip install manim==0.22.0 piper-tts==1.8.0 num2words scipy matplotlib faster-whisper
mkdir -p voices && cd voices
base=https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/high
curl -LO $base/de_DE-thorsten-high.onnx -LO $base/de_DE-thorsten-high.onnx.json
cd ..
```

## Eine Szene neu rendern

```bash
venv/bin/python tools/render.py 4             # Stimme (nur geänderte Absätze), Animation, Ton, Untertitel
venv/bin/python tools/render.py 4 --verify    # dazu jeden Satz mit Whisper gegenhören
venv/bin/python tools/render.py 4 --skip-tts  # nur Animation/Ton neu, Stimme unverändert
venv/bin/python tools/render.py 13 --skip-tts # Abspann (ohne Sprecher)
```

Ergebnis: `output/scenes/s04_argument.mp4` und `.srt`. Ändert sich ein Absatz im Skript,
wird nur dieser neu gesprochen; die Szene passt ihr Timing automatisch an die neuen
Satzzeiten an (`audio/timing.json`). Die Kapitelnummern und Dateinamen stehen in
`tools/build.py` (`SCENE_FILES`).

Nur die Animation, ohne Ton (schneller, zum Ausprobieren):

```bash
cd scenes && ../venv/bin/manim render --config_file manim.cfg -o s04_argument s04_argument.py Kapitel4
```

## Gesamtvideo und Quellen-PDF

```bash
venv/bin/python tools/build.py final    # output/nagel_fledermaus.mp4 + output/untertitel.srt
venv/bin/python tools/make_pdf.py       # output/quellen.pdf
```

`final` setzt die gerenderten Kapitel 0–13 aneinander (Video unverändert kopiert), legt eine
durchgehende Tonspur aus denselben Zeitplänen an (Lautheit einmal auf −16 LUFS normalisiert)
und verschiebt die Untertitel um die Kapitelanfänge.

Hinweise:
- Piper spricht nicht deterministisch. Die Sprachaufnahmen (`audio/narration/`) sind nicht im
  Repository; nach einem frischen Klon entstehen sie neu, mit leicht anderen Längen.
- `--verify` erzeugt jeden Satz bis zu dreimal und behält die Fassung, die Whisper am
  vollständigsten erkennt. Nicht sauber erkannte Sätze stehen in `audio/asr_report.txt`.
- Lizenzen von Stimme, Schriften und Hörbeispiel: `research/quellen.md`, Abschnitt I.
