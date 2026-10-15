# Wie ist es, eine Fledermaus zu sein? – Erklärvideo

Deutschsprachiges Erklärvideo (Ziel: 20–25 min, 1080p, 30 fps) über Thomas Nagels Aufsatz
„What Is It Like to Be a Bat?“ (*The Philosophical Review* 83/4, 1974, S. 435–450): Rekonstruktion
des Arguments, Vorläufer, Wirkungsgeschichte, Einwände, die Biologie der Echoortung und die
heutige Debatte über Tier- und KI-Bewusstsein.

## Stand

- Recherche und Skript: freigegeben (16.10.2026).
- **Prototyp:** Kapitel 3 „Die Kernthese“ als Stil-Muster gerendert (Animation, Ton,
  Untertitel); wartet auf Abnahme.
- Übrige Kapitel: nach Abnahme des Prototyps.

| Pfad | Inhalt |
| --- | --- |
| `research/quellen.md` | alle Quellen mit Prüfstatus, Seitenzahlen, Kernaussagen, Medien- und Lizenzliste |
| `research/argument.md` | Nagels Argument als Prämissen und Schlüsse, Zuordnung der Einwände |
| `script/skript.md` | freigegebener Sprechertext mit Beleg und Szenenbeschreibung pro Absatz – einzige Quelle für Text und Einblendungen |
| `scenes/kit.py` | Gestaltung (Farben, Schriften, Belegleiste, Zitatkarte, Kapitelkarte, Leitmotiv, Icons) und Synchronisation an die Sprache |
| `scenes/sNN_*.py` | eine Manim-Szene pro Kapitel (Klasse `KapitelN`) |
| `tools/script_parse.py` | liest das Skript (Sprechertext, Einblendungen, Zitate) |
| `tools/textnorm.py` | Aussprache für die Sprachausgabe (Zahlen, Namen, englische Titel) |
| `tools/tts.py` | Piper-Sprachausgabe satzweise, mit Satzzeiten; `--verify` prüft jeden Satz mit Whisper |
| `tools/timeline.py` | gemeinsamer Zeitplan für Szene, Tonspur und Untertitel |
| `tools/build.py` | Tonspur, Untertitel, Zusammenführen mit ffmpeg |
| `tools/render.py` | alles in einem Schritt für ein oder mehrere Kapitel |
| `tools/asr_check.py` | Whisper-Gegenprobe einzelner Absätze |
| `audio/timing.json` | gemessene Längen und Satzzeiten der Sprachaufnahmen |
| `assets/` | Schriften (OFL), Hörbeispiel (CC0) |

## Einrichten

Systempakete: ffmpeg, Pango/Cairo-Entwicklerdateien (für Manim; unter Debian/Ubuntu
`libpango1.0-dev`, `libcairo2-dev`, `pkg-config`).

```bash
python3 -m venv venv
venv/bin/pip install manim==0.22.0 piper-tts==1.8.0 num2words scipy faster-whisper
mkdir -p voices && cd voices
base=https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/high
curl -LO $base/de_DE-thorsten-high.onnx -LO $base/de_DE-thorsten-high.onnx.json
cd ..
```

## Eine Szene neu rendern

```bash
venv/bin/python tools/render.py 3             # Stimme (nur geänderte Absätze), Animation, Ton, Untertitel
venv/bin/python tools/render.py 3 --verify    # dazu jeden Satz mit Whisper gegenhören
venv/bin/python tools/render.py 3 --skip-tts  # nur Animation/Ton neu, Stimme unverändert
```

Ergebnis: `output/scenes/s03_kernthese.mp4` und `.srt`. Ändert sich ein Absatz im Skript,
wird nur dieser neu gesprochen; die Szene passt ihr Timing automatisch an die neuen
Satzzeiten an (`audio/timing.json`).

Hinweise:
- Piper spricht nicht deterministisch. Die Sprachaufnahmen (`audio/narration/`) sind nicht im
  Repository; nach einem frischen Klon entstehen sie neu, mit leicht anderen Längen.
- `--verify` erzeugt jeden Satz bis zu dreimal und behält die Fassung, die Whisper am
  vollständigsten erkennt. Nicht sauber erkannte Sätze stehen in `audio/asr_report.txt`.
