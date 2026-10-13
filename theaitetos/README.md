# Theaitetos – ein Erklärvideo

Ein rund 34-minütiges Video (1920×1080, 30 fps, deutsch) über Platons Dialog *Theaitetos*:
alle drei Definitionen der Erkenntnis mit ihren Widerlegungen, Platons Bilder (Hebamme,
Wachstafel, Taubenschlag, hölzernes Pferd), der mathematische Auftakt (Spirale des
Theodoros, irrationale Zahlen, platonische Körper) und die Wirkungsgeschichte (Aristoteles,
Mittelplatonismus, Kant, Freud, Wittgenstein, Gettier) sowie die Forschungsdebatte
(Cornford, Ryle/Owen, Burnyeat, Sedley, Fine).

**Video:** [`video/Theaitetos.mp4`](video/Theaitetos.mp4) (33:56 min, 1080p, 87 MB) ·
Untertitel: [`video/Theaitetos.srt`](video/Theaitetos.srt)

Jede Aussage ist am unteren Bildrand belegt: Platon nach Stephanus-Zählung, Zitate nach
Schleiermachers Übersetzung, griechische Originalstellen nach Burnet (Perseus), Forschung
mit Autor und Jahr. Das vollständige Literaturverzeichnis läuft im Abspann
(`src/data/bibliography.json`).

## Aufbau

| Datei | Inhalt |
| --- | --- |
| `src/data/script.json` | Sprechertext und Beleg je Abschnitt (31 Szenen, 127 Abschnitte) |
| `src/data/timing.json` | gemessene Länge jeder Sprachaufnahme (von `scripts/tts.py`) |
| `src/timeline.ts` | leitet daraus Szenen- und Abschnittsanfänge ab |
| `src/scenes/part1–8.tsx` | die Animationen der einzelnen Kapitel |
| `src/components/` | Gestaltung (Farben, Typografie, Belegleiste, Kapitelkarten, Icons) |
| `scripts/tts.py` | Sprachausgabe mit Piper (Stimme `de_DE-thorsten-high`) |
| `scripts/music.py` | erzeugt den leisen Klangteppich `public/music/pad.wav` |
| `scripts/mix.py` | legt Stimme und Musik an die richtigen Stellen, normalisiert auf −16 LUFS und mischt mit dem Video |
| `scripts/srt.py` | Untertitel `out/theaitetos.srt` |
| `scripts/stills.mjs` | Standbilder zur Kontrolle, z. B. `node scripts/stills.mjs wachs:2:0.5` |

## Erzeugen

```bash
npm install
pip install piper-tts==1.8.0          # in einer eigenen virtuellen Umgebung
# Stimme: https://huggingface.co/rhasspy/piper-voices (de/de_DE/thorsten/high)
python scripts/tts.py --model de_DE-thorsten-high.onnx
python3 scripts/music.py
npx remotion render Theaitetos out/theaitetos_voice.mp4
python3 scripts/mix.py out/theaitetos_voice.mp4
python3 scripts/srt.py
```

Piper spricht nicht deterministisch: Jeder neue Durchlauf erzeugt leicht andere Längen.
`tts.py` synthetisiert deshalb nur Abschnitte neu, deren gesprochener Text sich geändert
hat. Die Sprachaufnahmen selbst sind nicht im Repository (rund 90 MB).

## Quellenarbeit

- Primärtext: Burnet/Perseus (griechisch, Stephanus-Abschnitte), Fowler (englisch) und
  Schleiermacher (deutsch, zeno.org); jede Stephanus-Angabe wurde am Text geprüft.
- Sekundärliteratur: Angaben einzeln gegen zugängliche Quellen geprüft (SEP, IEP,
  Verlags- und Zeitschriftenseiten, Scans). Nicht selbst eingesehen und als solche
  gekennzeichnet: Anderhub 1941 und Sachs 1914 (zitiert nach Bulmer-Thomas bzw. Cornford).
- Datierung der Kämpfe bei Korinth: 369 v. Chr. (Mehrheitsmeinung seit Sachs 1914),
  alternativ 394 v. Chr. (SEP, IEP); Nails 2002 vertritt 391.
