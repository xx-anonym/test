"""Kapitel 10 – Nagels weiterer Weg (Nagel 1986; Williams 1986; Nagel 2012; Leiter & Weisberg
2012; Nagel 2024; Nagel 1974, S. 450, Fn. 15).

10.1  Ein Blick, der aus der Welt heraustritt: Die Person, die schaut, erscheint selbst im
      Bild – zweimal. Darunter der Pfeil „Objektivität“ aus Kapitel 4.
10.2  „Mind and Cosmos“: eine schematische Naturgeschichte mit Bewusstsein am Ende; der Pfeil
      biegt zurück. Rezensionskarte.
10.3  Die drei Kreise aus 5.5; der neutrale Kreis heißt jetzt „noch ohne Begriff“.
"""

from parts import *


def book(title, year, width=2.3, height=3.0, color='#2a3242'):
    """A plain book cover designed for this video: title and year only."""
    cover = RoundedRectangle(corner_radius=0.06, width=width, height=height, fill_color=color, fill_opacity=1,
                             stroke_color=MUTED, stroke_width=2)
    t = txt(title, size=22, font=SERIF, weight=SEMIBOLD).move_to(cover).shift(UP * 0.35)
    if t.width > width - 0.3:
        t.scale_to_fit_width(width - 0.3)
    y = txt(year, size=18, color=MUTED).next_to(t, DOWN, buff=0.35)
    return VGroup(cover, t, y)


class Kapitel10(NarratedScene):
    CHAPTER = 10

    def construct(self):
        self.chapter_card()
        self.p101()
        self.p102()
        self.p103()
        self.finish()

    def wipe(self):
        gone = [m for m in self.mobjects if m not in (self.tag, self.cite_mob)]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)

    # ------------------------------------------------------------ 10.1
    def p101(self):
        self.wait_until(self.t('10.1'))
        self.cite(self.cite_of('10.1'))
        b = book('The View\nfrom Nowhere', 'Nagel · 1986').move_to([-5.2, 0.6, 0])
        self.play(FadeIn(b, shift=UP * 0.1), run_time=0.6)

        # The world seen from a point of view …
        world = VGroup(
            Rectangle(width=2.4, height=1.6, stroke_color=FG, stroke_width=2.5),
            stone(width=0.5).move_to([0.55, -0.4, 0]),
            VGroup(Rectangle(width=0.08, height=0.5, fill_color=MUTED, fill_opacity=1, stroke_width=0).move_to([-0.5, -0.4, 0]),
                   Circle(radius=0.3, fill_color=MUTED, fill_opacity=1, stroke_width=0).move_to([-0.5, 0.0, 0])),
        ).move_to([1.6, 0.6, 0])
        viewer = person(height=0.6).move_to([-0.9, 0.6, 0])
        look = cone(viewer.get_right() + RIGHT * 0.05, 0, length=1.3, spread=0.55, color=OCHRE, opacity=0.15)
        self.play(FadeIn(world), FadeIn(viewer), FadeIn(look), run_time=0.8)

        # … then from further out: the viewer appears in the picture, twice.
        frames = []
        for k, (w, h, x) in enumerate([(5.0, 2.6, 0.9), (7.4, 3.7, 1.2)]):
            fr = Rectangle(width=w, height=h, stroke_color=OCHRE if k else FG, stroke_width=2.5 - k * 0.5)
            fr.move_to([x, 0.6 + 0.1 * k, 0])
            eye_k = eye(width=0.55).next_to(fr, LEFT, buff=0.35)
            ray = cone(eye_k.get_right() + RIGHT * 0.05, 0, length=1.0, spread=0.6, color=OCHRE, opacity=0.1)
            frames.append(VGroup(fr, eye_k, ray))
        key = self.t('10.1', 0, 'Buch')
        self.play_at(key - 1.6, FadeOut(b), FadeIn(frames[0]), run_time=0.8)
        self.play(FadeIn(frames[1]), run_time=0.8)
        title = txt('„The View from Nowhere“', size=24, font=SERIF, slant=ITALIC).move_to([1.2, 2.95, 0])
        self.play_at(self.t('10.1', 0, 'View'), FadeIn(title), run_time=0.5)
        ax = Arrow([-1.9, -1.75, 0], [6.6, -1.75, 0], buff=0, color=OCHRE, stroke_width=4)
        axl = txt('Objektivität →', size=20, color=OCHRE).next_to(ax, DOWN, buff=0.1).align_to(ax, RIGHT)
        self.play(GrowArrow(ax), FadeIn(axl), run_time=0.7)

        # Sentence 2: Williams – a style of understanding.
        self.wait_until(self.t('10.1', 1))
        q = QuoteCard('a style of understanding', 'Williams 1986, über Nagel', size=26).move_to([1.2, -2.75, 0])
        self.play_at(self.t('10.1', 1, 'Stil'), FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.wait_until(self.t('10.1', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 10.2
    def p102(self):
        self.wait_until(self.t('10.2'))
        self.cite(self.cite_of('10.2'))
        b = book('Mind and\nCosmos', 'Nagel · 2012').move_to([-5.2, 0.6, 0])
        self.play(FadeIn(b, shift=UP * 0.1), run_time=0.6)

        # Sentence 2: natural history, with consciousness at the end – thought anew.
        self.wait_until(self.t('10.2', 1))
        stations = ['Physik', 'Chemie', 'Leben', 'Nervensysteme', 'Bewusstsein']
        xs = np.linspace(-2.9, 5.6, len(stations))
        y = 0.9
        line = Arrow([xs[0] - 0.4, y, 0], [xs[-1] + 0.5, y, 0], buff=0, color=MUTED, stroke_width=3)
        dots = VGroup(*[Dot([x, y, 0], radius=0.07, color=MUTED) for x in xs[:-1]])
        labs = VGroup(*[txt(s, size=18, color=MUTED).next_to([x, y, 0], DOWN, buff=0.2) for x, s in zip(xs, stations)])
        glow = Circle(radius=0.22, fill_color=VIOLET, fill_opacity=0.8, stroke_color=FG, stroke_width=2).move_to([xs[-1], y, 0])
        note = txt('schematisch, ohne Zeitmaßstab', size=15, color=MUTED, slant=ITALIC).next_to(labs, DOWN, buff=0.2)
        note.align_to(line, LEFT)
        self.play(Create(line), FadeIn(dots), FadeIn(labs[:-1]), FadeIn(note), run_time=1.0)
        self.play_at(self.t('10.2', 1, 'Bewusstsein'), FadeIn(glow, scale=0.5), FadeIn(labs[-1]), run_time=0.6)
        back = CurvedArrow([xs[-1], y + 0.3, 0], [xs[0], y + 0.3, 0], angle=PI / 3, color=VIOLET, stroke_width=3)
        bq = txt('Naturgeschichte anders denken?', size=18, color=VIOLET).next_to(back, UP, buff=0.08)
        self.play_at(self.t('10.2', 1, 'Naturgeschichte'), Create(back), FadeIn(bq), run_time=1.0)

        # Sentence 3: neutral monism, teleological principles, no creator.
        self.wait_until(self.t('10.2', 2))
        tags = VGroup(pill('neutraler Monismus', color=PANEL, text_color=FG, size=18),
                      pill('zielgerichtete Naturprinzipien', color=PANEL, text_color=FG, size=18),
                      pill('kein Schöpfer', color=PANEL, text_color=MUTED, size=18)).arrange(RIGHT, buff=0.3)
        tags.move_to([1.3, -0.6, 0])
        for tg, key in zip(tags, ['Monismus', 'zielgerichtete', 'Schöpfer']):
            self.play_at(self.t('10.2', 2, key), FadeIn(tg, shift=UP * 0.1), run_time=0.4)

        # Sentence 4: sharp criticism – review card.
        self.wait_until(self.t('10.2', 3))
        q = QuoteCard('…his arguments against naturalism are unconvincing.', 'Leiter & Weisberg 2012', size=24)
        q.move_to([1.3, -2.3, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.wait_until(self.t('10.2', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 10.3
    def p103(self):
        self.wait_until(self.t('10.3'))
        self.cite(self.cite_of('10.3'))
        b = book('What Is It Like\nto Be a Bat?', 'Nagel · 2024').move_to([-5.2, 0.6, 0])
        plus = txt('+ Vortrag „Further Thoughts:\nThe Psychophysical Nexus“', size=17, color=MUTED).next_to(b, DOWN, buff=0.2)
        self.play(FadeIn(b, shift=UP * 0.1), run_time=0.6)
        self.play_at(self.t('10.3', 0, 'Vortrag'), FadeIn(plus), run_time=0.5)

        # Sentence 2: inseparable aspects of one thing for which we have no concept yet.
        self.wait_until(self.t('10.3', 1))
        m = Circle(radius=1.0, stroke_color=VIOLET, stroke_width=3).move_to([-0.2, 1.3, 0])
        p = Circle(radius=1.0, stroke_color=OCHRE, stroke_width=3).move_to([4.0, 1.3, 0])
        ml = txt('bewusste\nEigenschaften', size=16, color=VIOLET).move_to(m)
        pl = txt('neuronale\nBedingungen', size=16, color=OCHRE).move_to(p)
        n = Circle(radius=0.95, stroke_color=MUTED, stroke_width=3, fill_color='#2b303a', fill_opacity=1).move_to([1.9, -0.9, 0])
        a1 = Arrow(n.get_top() + LEFT * 0.35, m.get_bottom() + RIGHT * 0.25, buff=0.08, color=MUTED, stroke_width=3)
        a2 = Arrow(n.get_top() + RIGHT * 0.35, p.get_bottom() + LEFT * 0.25, buff=0.08, color=MUTED, stroke_width=3)
        self.play(Create(m), Create(p), FadeIn(ml), FadeIn(pl), run_time=0.7)
        self.play(FadeIn(n), GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        nl = txt('noch ohne\nBegriff', size=20, color=FG).move_to(n)
        self.play_at(self.t('10.3', 1, 'keinen Begriff'), FadeIn(nl), run_time=0.5)
        q = QuoteCard('inseparable aspects of some one thing, for which we do not at present have a concept',
                      'Nagel 2024, „Further Thoughts“', size=20, width=48).move_to([1.9, -2.75, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)

        # Sentence 3: already in the last footnote of 1974.
        self.wait_until(self.t('10.3', 2))
        fn = VGroup(txt('1974, Fn. 15:', size=17, color=OCHRE),
                    txt('eine Theorie, deren Grundbegriffe\nin keine der beiden Kategorien passen', size=17)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        fn.move_to([5.3, -0.9, 0])
        arc = CurvedArrow(fn.get_left() + LEFT * 0.1, n.get_right() + RIGHT * 0.05, angle=-PI / 4, color=MUTED,
                          stroke_width=2.5)
        self.play(FadeIn(fn), Create(arc), run_time=0.7)
        self.cite('Nagel 1974, S. 450, Fn. 15')
