"""Kapitel 6 – Vorläufer (Farrell 1950; Sprigge 1971 nach Seager 2011; Nagel 2024, Vorwort,
Anm. 1; Uexküll 1909; Schnitzler & Kalko 2001, S. 558).

6.1  Zeitleiste; Farrell 1950: Marsianer mit „Pseudo-Radiosinn“, die Fledermaus-Frage –
     und eine Waage, die zu „kein Problem“ kippt.
6.2  Sprigge 1971; ein Pfeil von 2024 zurück: Nagel hatte beide nicht vor Augen.
6.3  Uexküll 1909: derselbe Abendgarten erst in menschlicher Sicht, dann als Echo-Welt
     (nur, was das Sonar misst, im Nahbereich). Die Umwelt schließt sich wie Mauern;
     sie gehört ins linke Feld, das rechte bleibt leer.
"""

from parts import *

YEARS = [1909, 1950, 1971, 1974, 2024]


def balance(left='Problem', right='kein Problem'):
    post = Line([0, -1.0, 0], [0, 0.4, 0], color=MUTED, stroke_width=5)
    foot = Line([-0.5, -1.0, 0], [0.5, -1.0, 0], color=MUTED, stroke_width=5)
    beam = Line([-1.4, 0.4, 0], [1.4, 0.4, 0], color=FG, stroke_width=5)

    def pan(x, label):
        strings = VGroup(Line([x, 0.4, 0], [x - 0.4, -0.3, 0], color=MUTED, stroke_width=2),
                         Line([x, 0.4, 0], [x + 0.4, -0.3, 0], color=MUTED, stroke_width=2))
        dish = Arc(radius=0.45, start_angle=PI, angle=PI, color=FG, stroke_width=4).move_to([x, -0.42, 0])
        lab = txt(label, size=18, color=MUTED).move_to([x, -0.95, 0])
        return VGroup(strings, dish, lab)
    pl, pr = pan(-1.4, left), pan(1.4, right)
    g = VGroup(foot, post, beam, pl, pr)
    g.beam, g.pl, g.pr = beam, pl, pr
    return g


def tip(scene, bal, angle=0.22, run_time=1.0):
    """Tilt the beam (right side down) and move the pans with its ends."""
    pivot = bal.beam.get_center()
    dy = 1.4 * np.sin(angle)
    scene.play(Rotate(bal.beam, -angle, about_point=pivot), bal.pl.animate.shift(UP * dy),
               bal.pr.animate.shift(DOWN * dy), run_time=run_time)


class Kapitel6(NarratedScene):
    CHAPTER = 6

    def construct(self):
        self.chapter_card()
        self.axis = YearAxis(YEARS, y=-2.75)
        self.p61()
        self.p62()
        self.p63()
        self.finish()

    def upper(self):
        """Everything but tag, source line and the year axis."""
        keep = {self.tag, self.cite_mob, *self.axis.get_family()}
        return [m for m in self.mobjects if m not in keep]

    # ------------------------------------------------------------ 6.1
    def p61(self):
        self.wait_until(self.t('6.1'))
        self.play(Create(self.axis[0]), FadeIn(self.axis.ticks), run_time=1.0)
        self.play(Indicate(self.axis.ticks[3], color=OCHRE), run_time=0.7)

        # Sentence 2: Farrell 1950 – the Martian, the bat sentence, the opposite conclusion.
        self.wait_until(self.t('6.1', 1))
        self.cite(self.cite_of('6.1', 0))
        p50 = self.axis.points[1950]
        mark = Dot(p50, radius=0.1, color=OCHRE)
        card = year_card('Farrell 1950', '„Experience“, Mind').next_to(p50, UP, buff=0.35)
        self.play(FadeIn(mark), FadeIn(card, shift=UP * 0.1), run_time=0.6)
        m = martian(height=1.1).move_to([-4.6, 1.2, 0])
        waves = VGroup(*[Arc(radius=0.25 + 0.17 * k, start_angle=-PI / 4, angle=PI / 2, color=OCHRE, stroke_width=2.5)
                         .move_arc_center_to(m.get_right() + LEFT * 0.05) for k in range(3)])
        ml = txt('Marsianer mit\n„Pseudo-Radiosinn“', size=18, color=MUTED).next_to(m, DOWN, buff=0.2)
        self.play_at(self.t('6.1', 1, 'Marsianer'), FadeIn(m), Create(waves, lag_ratio=0.3), FadeIn(ml), run_time=0.8)
        q = QuoteCard(self.quote_of('6.1'), self.cite_of('6.1', 0), size=24, width=36).move_to([0.6, 1.25, 0])
        self.play_at(self.t('6.1', 1, 'Satz'), FadeIn(q, shift=UP * 0.1), run_time=0.6)

        bal = balance().scale(0.85).move_to([4.75, 0.9, 0])
        self.play_at(self.t('6.1', 1, 'entgegengesetzten'), FadeIn(bal), run_time=0.6)
        self.cite(self.cite_of('6.1', 1))
        tip(self, bal)
        self.wait_until(self.t('6.1', 'end') + 0.1)
        self.play(*[FadeOut(x) for x in self.upper() if x is not mark], run_time=0.5)
        self.marks = {1950: mark}

    # ------------------------------------------------------------ 6.2
    def p62(self):
        self.wait_until(self.t('6.2'))
        self.cite(self.cite_of('6.2', 0))
        p71 = self.axis.points[1971]
        mark = Dot(p71, radius=0.1, color=OCHRE)
        card = year_card('Sprigge 1971', '„Final Causes“').next_to(p71, UP, buff=0.35)
        self.play(FadeIn(mark), FadeIn(card, shift=UP * 0.1), run_time=0.6)
        defin = txt('Bewusstsein ist, was man zu kennzeichnen versucht,\n'
                    'wenn man fragt, wie es ist oder wäre,\n'
                    'ein bestimmtes Objekt in einer bestimmten Lage zu sein.', size=26, font=SERIF, slant=ITALIC)
        defin.move_to([0.2, 1.7, 0])
        tag = txt('Sprigge 1971 (Wortlaut nach Seager 2011)', size=17, color=MUTED).next_to(defin, DOWN, buff=0.2)
        self.play_at(self.t('6.2', 0, 'Bewusstsein'), FadeIn(defin), FadeIn(tag), run_time=0.8)
        self.marks[1971] = mark

        # Sentence 2: 2024 – Nagel looks back.
        self.wait_until(self.t('6.2', 1))
        self.cite(self.cite_of('6.2', 1))
        self.play(FadeOut(defin), FadeOut(tag), FadeOut(card), run_time=0.4)
        p24 = self.axis.points[2024]
        m24 = Dot(p24, radius=0.1, color=FG)
        c24 = year_card('Nagel 2024', 'Neuausgabe, Vorwort').next_to(p24, UP, buff=0.35).shift(LEFT * 0.4)
        self.play(FadeIn(m24), FadeIn(c24, shift=UP * 0.1), run_time=0.6)
        arcs = VGroup(*[CurvedArrow(p24 + UP * 0.15, self.axis.points[yr] + UP * 0.15, angle=PI / 3.2, color=MUTED,
                                    stroke_width=2.5, tip_length=0.18) for yr in (1971, 1950)])
        self.play_at(self.t('6.2', 1, 'beide'), Create(arcs[0]), Create(arcs[1]), run_time=1.0)
        q = QuoteCard("When I wrote my paper, I hadn't read Sprigge and had forgotten Farrell.",
                      self.cite_of('6.2', 1), size=24, width=40).move_to([0.0, 2.1, 0])
        self.play_at(self.t('6.2', 1, 'gesteht'), FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.wait_until(self.t('6.2', 'end') + 0.1)
        self.play(*[FadeOut(x) for x in self.upper() if x not in self.marks.values()], run_time=0.5)

    # ------------------------------------------------------------ 6.3
    def garden(self, bat_pos):
        """Evening garden in the human view: colours, depth, far hills."""
        sky = Rectangle(width=14.3, height=6.0, stroke_width=0, fill_opacity=1).move_to([0, 0.75, 0])
        sky.set_fill(color=['#3a3550', '#1d2436'], opacity=1).set_sheen_direction(DOWN)
        hills = Polygon(*[[x, -0.3 + 0.35 * np.sin(x * 0.6 + 1) + 0.15 * np.sin(2.3 * x), 0] for x in np.linspace(-7.2, 7.2, 30)],
                        [7.2, -2.3, 0], [-7.2, -2.3, 0], fill_color='#2b3446', fill_opacity=1, stroke_width=0)
        lawn = Rectangle(width=14.3, height=1.4, fill_color='#26372c', fill_opacity=1, stroke_width=0).move_to([0, -1.6, 0])
        trunk = Rectangle(width=0.22, height=1.7, fill_color='#6b4f3a', fill_opacity=1, stroke_width=0).move_to([-1.4, -0.9, 0])
        crown = VGroup(*[Circle(radius=r, fill_color='#4f7a4a', fill_opacity=1, stroke_width=0).move_to(c) for r, c in
                         [(0.75, [-1.4, 0.55, 0]), (0.55, [-1.95, 0.2, 0]), (0.55, [-0.85, 0.2, 0]), (0.5, [-1.4, 1.15, 0])]])
        pond = Ellipse(width=2.6, height=0.55, fill_color='#3f6f8f', fill_opacity=1, stroke_width=0).move_to([2.6, -1.75, 0])
        bricks = VGroup()
        for row in range(4):
            for k in range(7):
                bricks.add(Rectangle(width=0.5, height=0.22, fill_color='#8a5a48', fill_opacity=1, stroke_color='#5d3c30',
                                     stroke_width=1).move_to([4.3 + k * 0.5 + (0.25 if row % 2 else 0), -1.55 + row * 0.22, 0]))
        moon = Circle(radius=0.3, fill_color='#e9e2cf', fill_opacity=0.9, stroke_width=0).move_to([5.6, 2.6, 0])
        insects = VGroup(*[insect(size=0.22).move_to(p) for p in [[-3.1, 0.7, 0], [-2.5, -0.5, 0], [-2.0, 1.3, 0], [0.8, 1.4, 0]]])
        b = bat(width=0.75).move_to(bat_pos)
        g = VGroup(sky, moon, hills, lawn, trunk, crown, pond, bricks, insects, b)
        g.trunk, g.crown, g.pond, g.bricks, g.insects, g.bat = trunk, crown, pond, bricks, insects, b
        return g

    def echoes(self, g, bat_pos, reach):
        """Echo points: surfaces facing the bat within reach; brightness falls with distance."""
        bp = np.array(bat_pos)
        pts = []
        for c in g.crown:                                 # leaves: many small reflectors
            for a in np.linspace(0, TAU, 40, endpoint=False):
                p = c.get_center() + c.width / 2 * np.array([np.cos(a), np.sin(a), 0])
                if np.dot(p - c.get_center(), bp - c.get_center()) > 0:
                    pts.append(p)
        x = g.trunk.get_left()[0]
        pts += [np.array([x, y, 0]) for y in np.linspace(-1.7, -0.1, 9)]
        for br in g.bricks:
            pts.append(br.get_left() + RIGHT * 0.02)
        dots = VGroup()
        for p in pts:
            d = np.linalg.norm(p - bp)
            if d < reach:
                dots.add(Dot(p, radius=0.035, color=OCHRE, fill_opacity=max(0.15, 1 - d / reach)))
        movers = VGroup()
        rng = np.random.default_rng(5)
        for ins in g.insects:
            p = ins.get_center()
            d = np.linalg.norm(p - bp)
            if d < reach:
                v = rng.normal(size=2)
                v = 0.45 * v / np.linalg.norm(v)
                movers.add(VGroup(Dot(p, radius=0.07, color=FG, fill_opacity=max(0.3, 1 - d / reach)),
                                  Arrow(p, p + np.array([v[0], v[1], 0]), buff=0.08, color=FG, stroke_width=2.5,
                                        max_tip_length_to_length_ratio=0.35)))
        return dots, movers

    def p63(self):
        self.wait_until(self.t('6.3'))
        self.cite(self.cite_of('6.3', 0))
        p09 = self.axis.points[1909]
        mark = Dot(p09, radius=0.1, color=OCHRE)
        card = year_card('Uexküll 1909', '„Umwelt und Innenwelt der Tiere“').next_to(p09, UP, buff=0.35).shift(RIGHT * 0.9)
        self.play(FadeIn(mark), FadeIn(card, shift=UP * 0.1), run_time=0.6)

        # Sentence 2: every form of life has its own Umwelt; the animal's standpoint decides.
        self.wait_until(self.t('6.3', 1))
        q1 = QuoteCard(self.quote_of('6.3', 0), self.cite_of('6.3', 0), size=24, width=50).move_to([0.5, 1.6, 0])
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.6)
        bat_pos = [-4.3, -0.2, 0]
        g = self.garden(bat_pos)
        human = txt('menschliche Sicht: Farben, Fernsicht', size=20, color=FG).move_to([0, 3.1, 0])
        self.play_at(self.t('6.3', 1, 'Standpunkt'), FadeOut(q1), FadeOut(card), FadeOut(mark),
                     *[FadeOut(m) for m in self.marks.values()], FadeOut(self.axis), run_time=0.5)
        self.play(FadeIn(g), FadeIn(human), run_time=1.0)

        # The same garden as an echo world: what sonar measures, near range only.
        reach = 3.3
        dots, movers = self.echoes(g, bat_pos, reach)
        dark = Rectangle(width=14.3, height=8.1, fill_color=BG, fill_opacity=1, stroke_width=0)
        rng_c = DashedVMobject(Circle(radius=reach, stroke_color=MUTED, stroke_width=2).move_to(bat_pos), num_dashes=60)
        echo_lab = txt('Echo-Welt: nur Nahbereich, Bewegung als Pfeile, Nähe als Helligkeit', size=20, color=OCHRE)
        echo_lab.move_to([0, 3.1, 0])
        b2 = bat(width=0.75).move_to(bat_pos)
        note = txt('Darstellung dessen, was das Sonar misst – nicht, wie es sich anfühlt', size=20, color=MUTED,
                   slant=ITALIC).move_to([1.6, -2.75, 0])
        reach_l = txt('Reichweite wenige Meter · Schnitzler & Kalko 2001, S. 558 · schematisch', size=15, color=MUTED)
        reach_l.next_to(note, UP, buff=0.12)
        self.play(FadeIn(dark), FadeOut(human), FadeIn(b2), run_time=0.9)
        self.play(Create(rng_c), FadeIn(echo_lab), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), FadeIn(movers), FadeIn(note), FadeIn(reach_l),
                  run_time=1.2)
        self.remove(g)

        # Sentence 3: the stimuli of the Umwelt enclose the animal like walls.
        self.wait_until(self.t('6.3', 2))
        self.cite(self.cite_of('6.3', 1))
        wall = Circle(radius=reach, stroke_color=OCHRE, stroke_width=7).move_to(bat_pos)
        q2 = QuoteCard(self.quote_of('6.3', 1), self.cite_of('6.3', 1), size=24, width=50).move_to([3.6, 1.0, 0])
        self.play(ReplacementTransform(rng_c, wall), run_time=0.9)
        self.play_at(self.t('6.3', 2, 'Mauern'), FadeIn(q2, shift=UP * 0.1), run_time=0.6)

        # Sentence 4: where Uexküll stops – painting the inner world is not for serious researchers.
        self.wait_until(self.t('6.3', 3))
        self.cite(self.cite_of('6.3', 0))
        stop = txt('Innenwelt „mit seelischen Qualitäten auszumalen“:\nfür Uexküll keine Sache ernsthafter Forscher',
                   size=22, color=FG).move_to([3.6, 1.0, 0])
        self.play(FadeOut(q2), FadeIn(stop), run_time=0.6)

        # Sentence 5: Uexküll fills the left field and leaves the right one empty.
        self.wait_until(self.t('6.3', 4))
        world = VGroup(dots, movers, wall, b2)
        self.play(FadeOut(VGroup(stop, echo_lab, note, reach_l)), run_time=0.4)
        outer, inner = two_fields(left_label='von außen: Uexkülls Umwelt', height=3.8, y=-0.2)
        self.play(world.animate.scale_to_fit_height(3.3).move_to(outer.box), FadeIn(outer), run_time=1.0)
        self.play(FadeIn(inner), run_time=0.7)
        self.remove(dark)
