"""Abspann: Literatur (aus research/quellen.md über tools/bibliography.py), Medien und
Werkzeuge mit Lizenzen (research/quellen.md, Abschnitt I), Hinweise zu Zitaten und
Übersetzung. Ohne Sprecher; feste Länge DURATION.
"""

from kit import *
from bibliography import entries

DURATION = 52.0
HOLD = 5.0          # final card at the end

MEDIA = [
    ('Hörbeispiel', '„Bat feeding buzz.wav“, Kaldari, Wikimedia Commons, aufgenommen 11.11.2020 in Pennsylvania; '
                    'CC0 1.0; im Video 10-fach verlangsamt wie in der Originaldatei'),
    ('Sprecherstimme', 'synthetisch: Piper (piper-tts 1.8.0), Stimme de_DE-thorsten-high (Datensatz Thorsten-Voice, '
                       'CC0; Modell feinabgestimmt aus dem englischen Basismodell „lessac“)'),
    ('Schriften', 'Inter (The Inter Project Authors) und Source Serif 4 (Adobe), beide SIL Open Font License 1.1'),
    ('Grafiken und Animation', 'alle selbst erstellt mit Manim Community 0.22, NumPy, SciPy, Matplotlib; '
                               'Ton und Schnitt mit FFmpeg'),
    ('Musik', 'keine'),
]

NOTES = [
    'Zitate erscheinen im englischen bzw. deutschen Original mit Seitenangabe; '
    'die gesprochenen deutschen Wiedergaben englischer Texte sind eigene Übersetzungen.',
    'Deutsche Ausgabe des Aufsatzes: Thomas Nagel, Wie ist es, eine Fledermaus zu sein? '
    'Englisch/Deutsch, übersetzt und herausgegeben von Ulrich Diehl, Reclam 2016.',
    'Seitenzahlen zu Nagel 1974 nach der Erstveröffentlichung in The Philosophical Review 83 (4), S. 435–450.',
    'Mit „nach …“ gekennzeichnete Angaben beruhen auf der genannten Sekundärquelle.',
    'Prüfstatus und Belegstellen jeder Quelle: research/quellen.md und output/quellen.pdf.',
]


def block(title, lines, width):
    head = txt(title, size=26, color=OCHRE, weight=SEMIBOLD)
    body = VGroup(*[txt(l, size=15, color=FG, width=width) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    return VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3)


class Kapitel13(Scene):
    def construct(self):
        refs = [t for _, t, _ in entries()]
        half = (len(refs) + 1) // 2
        cols = VGroup(*[VGroup(*[txt(r, size=14, color=FG, width=76) for r in part]).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.13)
                        for part in (refs[:half], refs[half:])]).arrange(RIGHT, aligned_edge=UP, buff=0.5)
        if cols.width > 13.2:
            cols.scale_to_fit_width(13.2)
        lit_head = txt('Literatur', size=30, color=OCHRE, weight=SEMIBOLD)
        lit = VGroup(lit_head, cols).arrange(DOWN, buff=0.35)

        media = VGroup(*[VGroup(txt(k, size=16, color=MUTED, weight=MEDIUM), txt(v, size=15, width=100))
                         .arrange(DOWN, aligned_edge=LEFT, buff=0.06) for k, v in MEDIA]).arrange(DOWN, aligned_edge=LEFT,
                                                                                                  buff=0.2)
        med = VGroup(txt('Medien, Stimme, Werkzeuge', size=30, color=OCHRE, weight=SEMIBOLD), media).arrange(DOWN, buff=0.35)
        notes = VGroup(*[txt(n, size=15, width=110) for n in NOTES]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        nts = VGroup(txt('Hinweise', size=30, color=OCHRE, weight=SEMIBOLD), notes).arrange(DOWN, buff=0.35)
        roll = VGroup(lit, med, nts).arrange(DOWN, buff=0.9)
        roll.next_to(DOWN * 4.1, DOWN, buff=0)

        final = VGroup(txt('Wie ist es, eine Fledermaus zu sein?', size=44, font=SERIF, weight=SEMIBOLD),
                       txt('Ein Erklärvideo zu Thomas Nagel, „What Is It Like to Be a Bat?“ (1974)', size=22, color=MUTED))
        final.arrange(DOWN, buff=0.3)

        travel = roll.height + 8.2
        self.play(roll.animate.shift(UP * travel), run_time=DURATION - HOLD - 1.0, rate_func=linear)
        self.remove(roll)
        self.play(FadeIn(final), run_time=1.0)
        self.wait(HOLD - 1.0 - 0.8)
        self.play(FadeOut(final), run_time=0.8)
