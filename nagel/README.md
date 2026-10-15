# Wie ist es, eine Fledermaus zu sein? – Erklärvideo

Deutschsprachiges Erklärvideo (Ziel: 20–25 min, 1080p, 30 fps) über Thomas Nagels Aufsatz
„What Is It Like to Be a Bat?“ (*The Philosophical Review* 83/4, 1974, S. 435–450): Rekonstruktion
des Arguments, Vorläufer, Wirkungsgeschichte, Einwände, die Biologie der Echoortung und die
heutige Debatte über Tier- und KI-Bewusstsein.

## Stand

**Phase 1–2 (Recherche, Skript) abgeschlossen – wartet auf Freigabe.** Es ist noch nichts
gerendert.

| Datei | Inhalt |
| --- | --- |
| `research/quellen.md` | alle Quellen mit Prüfstatus (✅ am Original, ☑️ Abstract/Metadaten, ⚠️ nur sekundär), Seitenzahlen, Kernaussagen, Medien- und Lizenzliste |
| `research/argument.md` | Nagels Argument als nummerierte Prämissen und Schlüsse, Zuordnung der Einwände |
| `script/skript.md` | Sprechertext mit Beleg und Szenenbeschreibung pro Absatz, offene Fragen |
| `audio/stimmproben/` | Hörproben der beiden möglichen Stimmen (Piper, Coqui) |

## Geplante Struktur

```
research/   Quellen, Argumentrekonstruktion
script/     Skript (Quelle der Wahrheit für Text und Belege)
scenes/     Manim-Szenen, je Kapitel eine Datei (s00_prolog.py … s13_abspann.py)
audio/      Sprachaufnahmen (nicht versioniert), Stimmproben
assets/     Hörbeispiel (CC0), Schriften
output/     nagel_fledermaus.mp4, untertitel.srt, quellen.pdf
```

Werkzeuge: Manim Community 0.22, NumPy/SciPy/Matplotlib (Spektrogramm, Physik), lokale TTS
(Piper oder Coqui, siehe `script/skript.md`, offene Frage 7), ffmpeg. Das Wie des Neurenderns
einzelner Szenen wird hier ergänzt, sobald die Szenen existieren.
