"""Kapitel 5 – Was Nagel nicht behauptet (Nagel 1974, S. 442 Fn. 8, 446–450 mit Fn. 15).

5.1  Der ganze Baum; der naheliegende Fehlschluss „Physikalismus ist falsch“ wird
     durchgestrichen, Knoten K erscheint.
5.2  Das Wort „ist“: Bei Wasser/H₂O sieht man, wie zwei Bezugswege auf dasselbe
     zulaufen; bei mental/physisch liegt der Treffpunkt im Nebel.
5.3  Raupe im Safe → Schmetterling: Grund zu glauben ohne Verständnis des Wie.
5.4  Kein Erkenntnisverbot: Verstehen nimmt entlang eines Kontinuums ab, fällt aber
     nicht schlagartig auf null.
5.5  Objektive Phänomenologie: Struktur statt loser Vergleiche; Ausblick auf eine
     Theorie mit neutralen Grundbegriffen.
"""

from parts import *


def fog(center, width=2.4, height=1.4, seed=3):
    rng = np.random.default_rng(seed)
    blobs = VGroup(*[Ellipse(width=rng.uniform(0.8, 1.5), height=rng.uniform(0.5, 0.9), stroke_width=0,
                             fill_color='#5a6272', fill_opacity=0.22)
                     .move_to(center + np.array([rng.uniform(-width / 2.6, width / 2.6), rng.uniform(-height / 3, height / 3), 0]))
                     for _ in range(12)])
    return blobs


class Kapitel5(NarratedScene):
    CHAPTER = 5

    def construct(self):
        self.chapter_card()
        self.p51()
        self.p52()
        self.p53()
        self.p54()
        self.p55()
        self.finish()

    def wipe(self):
        gone = [m for m in self.mobjects if m not in (self.tag, self.cite_mob)]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)

    # ------------------------------------------------------------ 5.1
    def p51(self):
        self.wait_until(self.t('5.1'))
        self.cite(self.cite_of('5.1'))
        tree = ArgTree(mini=False)
        body = [n for n in tree.nodes if n != 'K']
        self.play(*[FadeIn(tree.nodes[n]) for n in body],
                  *[FadeIn(e) for (a, b), e in tree.edges.items() if b != 'K'], run_time=0.9)

        # Sentence 2: the tempting conclusion – crossed out.
        self.wait_until(self.t('5.1', 1))
        wrong_box = DashedVMobject(RoundedRectangle(corner_radius=0.07, width=2.55, height=0.64, stroke_color=MUTED,
                                                    stroke_width=2), num_dashes=30)
        wrong_txt = txt('Physikalismus ist falsch', size=16, color=MUTED)
        wrong = VGroup(wrong_box, wrong_txt.move_to(wrong_box)).move_to(tree.nodes['K'])
        self.play(Create(tree.edges[('Z5', 'K')]), FadeIn(wrong), run_time=0.7)
        strike = Line(wrong.get_corner(DL), wrong.get_corner(UR), color=FG, stroke_width=4)
        self.play_at(self.t('5.1', 1, 'Fehler'), Create(strike), run_time=0.5)
        q = QuoteCard(self.quote_of('5.1'), self.cite_of('5.1'), size=22).move_to([-1.0, -3.0, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)

        # Sentence 3: the actual conclusion.
        self.wait_until(self.t('5.1', 2))
        self.play(VGroup(wrong, strike).animate.shift(DOWN * 1.1).set_opacity(0.45), run_time=0.6)
        self.play(FadeIn(tree.nodes['K'], scale=0.85), run_time=0.6)
        self.play(Indicate(tree.nodes['K'], color=OCHRE, scale_factor=1.12), run_time=0.7)
        detail = txt('unverstanden, weil wir nicht sehen,\nwie er wahr sein könnte', size=17, color=FG)
        detail.next_to(tree.nodes['K'], DOWN, buff=1.05)
        detail.shift(RIGHT * (6.85 - detail.get_right()[0]))
        self.play_at(self.t('5.1', 2, 'weil'), FadeOut(VGroup(wrong, strike)), FadeIn(detail), run_time=0.6)
        self.wait_until(self.t('5.1', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 5.2
    def p52(self):
        self.wait_until(self.t('5.2'))
        self.cite(self.cite_of('5.2'))
        word = txt('ist', size=96, font=SERIF, slant=ITALIC).move_to([0, 0.4, 0])
        lens = magnifier().scale(2.2).move_to(word.get_center() + RIGHT * 0.25 + DOWN * 0.1)
        self.play(FadeIn(word), run_time=0.5)
        self.play_at(self.t('5.2', 0, '„ist“'), FadeIn(lens, shift=LEFT * 0.4), run_time=0.6)
        self.play(VGroup(word, lens).animate.scale(0.45).move_to([0, 2.7, 0]), run_time=0.6)

        # Sentence 2: an identity is understood when two routes visibly converge.
        def routes(cx, a, b, color, meet=True):
            p = np.array([cx, -0.9, 0])
            la = txt(a, size=24, color=color).move_to([cx - 1.9, 1.25, 0])
            lb = txt(b, size=24, color=OCHRE).move_to([cx + 1.9, 1.25, 0])
            ra = Line(la.get_bottom() + DOWN * 0.1, p, color=color, stroke_width=3)
            rb = Line(lb.get_bottom() + DOWN * 0.1, p, color=OCHRE, stroke_width=3)
            dot = Dot(p, radius=0.1, color=FG)
            return VGroup(la, lb, ra, rb, dot)
        left = routes(-3.4, 'Wasser', 'H₂O', FG)
        same = txt('dasselbe', size=20, color=MUTED).next_to(left[4], DOWN, buff=0.15)
        self.wait_until(self.t('5.2', 1))
        self.play(FadeIn(left[0]), FadeIn(left[1]), run_time=0.4)
        self.play(Create(left[2]), Create(left[3]), run_time=0.9)
        self.play(FadeIn(left[4], scale=0.5), FadeIn(same), run_time=0.4)

        # Sentence 3: mental/physical – like „matter is energy“ for a Presocratic.
        self.wait_until(self.t('5.2', 2))
        right = routes(3.4, 'mentaler Begriff', 'physischer Begriff', VIOLET)
        right[0].shift(RIGHT * 0.3)
        right[1].shift(LEFT * 0.1)
        mist = fog(right[4].get_center(), width=2.6, height=1.6)
        self.play(FadeIn(right[0]), FadeIn(right[1]), run_time=0.4)
        self.play(Create(right[2]), Create(right[3]), FadeIn(mist), run_time=1.0)
        qm = txt('?', size=40, color=FG).move_to(right[4])
        self.play(FadeIn(qm), run_time=0.4)
        presoc = txt('„Materie ist Energie“ – im Mund eines Vorsokratikers', size=22, color=MUTED, slant=ITALIC)
        presoc.move_to([0, -2.4, 0])
        self.play_at(self.t('5.2', 2, 'Materie'), FadeIn(presoc), run_time=0.6)
        note = txt('nicht einmal der Anfang einer Vorstellung, wie es wahr sein könnte', size=20)
        note.next_to(presoc, DOWN, buff=0.2)
        self.play_at(self.t('5.2', 2, 'nicht einmal'), FadeIn(note), run_time=0.6)
        self.wait_until(self.t('5.2', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 5.3
    def p53(self):
        self.wait_until(self.t('5.3'))
        self.cite(self.cite_of('5.3'))
        head = txt('Gründe zu glauben, ohne zu verstehen, wie', size=26, color=MUTED).move_to([0, 2.75, 0])
        self.play(FadeIn(head), run_time=0.5)

        # Sentence 2: caterpillar → safe → weeks → butterfly.
        self.wait_until(self.t('5.3', 1))
        cat = caterpillar(width=1.3).move_to([-4.8, -0.2, 0])
        cat_l = txt('Raupe', size=22).next_to(cat, DOWN, buff=0.25)
        self.play(FadeIn(cat), FadeIn(cat_l), run_time=0.5)
        safe = Safe(size=2.2).move_to([0, 0.0, 0])
        safe.door_g.stretch(0.001, 0, about_edge=LEFT)
        self.play_at(self.t('5.3', 1, 'Raupe'), FadeIn(safe), run_time=0.5)
        self.play(cat.animate.move_to(safe.frame).scale(0.8), run_time=0.8)
        self.play_at(self.t('5.3', 1, 'Safe'), safe.door_g.animate.stretch(1000, 0, about_edge=LEFT), run_time=0.6)
        bar = Line([-1.2, -1.6, 0], [1.2, -1.6, 0], color=DIM, stroke_width=6)
        prog = Line([-1.2, -1.6, 0], [-1.19, -1.6, 0], color=OCHRE, stroke_width=6)
        wk = txt('Wochen', size=20, color=MUTED).next_to(bar, DOWN, buff=0.12)
        self.play(FadeIn(bar), FadeIn(wk), run_time=0.3)
        self.play_at(self.t('5.3', 1, 'Wochen'), prog.animate.put_start_and_end_on([-1.2, -1.6, 0], [1.2, -1.6, 0]),
                     run_time=1.2)
        self.remove(cat)
        bfly = butterfly(width=1.2).move_to(safe.frame)
        self.add(bfly)
        bfly.set_z_index(-1)
        safe.set_z_index(0)
        self.play_at(self.t('5.3', 1, 'Schmetterling'), safe.door_g.animate.stretch(0.001, 0, about_edge=LEFT),
                     run_time=0.6)
        bfly.set_z_index(1)
        self.play(bfly.animate.move_to([4.8, 0.0, 0]), run_time=0.9)
        bfly_l = txt('Schmetterling', size=22).next_to(bfly, DOWN, buff=0.3)
        self.play(FadeIn(bfly_l), run_time=0.3)

        cat2 = caterpillar(width=1.3).move_to([-4.8, -0.2, 0]).set_opacity(0.45)
        arc = CurvedArrow(cat2.get_top() + UP * 0.3, bfly.get_top() + UP * 0.3, angle=-PI / 3.5, color=FG,
                          stroke_width=3)
        qm = txt('?', size=44, color=OCHRE).next_to(arc, UP, buff=0.05)
        self.play_at(self.t('5.3', 1, 'ohne zu verstehen'), FadeIn(cat2), Create(arc), run_time=0.8)
        self.play(FadeIn(qm, scale=1.3), run_time=0.4)

        # Sentence 3: we may be in that position regarding physicalism.
        self.wait_until(self.t('5.3', 2))
        ana = VGroup(txt('Empfindung', size=24, color=VIOLET), txt('→ ? →', size=24, color=OCHRE),
                     txt('physischer Prozess', size=24, color=OCHRE)).arrange(RIGHT, buff=0.25).move_to([0, -2.65, 0])
        self.play(FadeIn(ana, shift=UP * 0.1), run_time=0.7)
        self.wait_until(self.t('5.3', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 5.4
    def p54(self):
        self.wait_until(self.t('5.4'))
        self.cite(self.cite_of('5.4'))
        q = QuoteCard(self.quote_of('5.4'), self.cite_of('5.4')).move_to([0, 2.3, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)

        # Continuum of points of view.
        y = -1.6
        line = Line([-5.6, y, 0], [5.6, y, 0], color=MUTED, stroke_width=3)
        stations = [(-5.0, 'ich'), (-1.7, 'andere Menschen'), (1.7, 'menschliche\nEchoorter'), (5.0, 'Fledermaus')]
        ticks = VGroup(*[Line([x, y - 0.12, 0], [x, y + 0.12, 0], color=MUTED, stroke_width=3) for x, _ in stations])
        labs = VGroup(*[txt(n, size=20, color=MUTED).next_to([x, y, 0], DOWN, buff=0.3) for x, n in stations])
        self.play(Create(line), FadeIn(ticks), FadeIn(labs[0]), FadeIn(labs[1]), FadeIn(labs[3]), run_time=0.8)

        # Sentence 2: footnote – blind people locating objects by clicks or a cane.
        self.wait_until(self.t('5.4', 1))
        self.play(FadeIn(labs[2]), run_time=0.4)
        self.play(Indicate(labs[2], color=OCHRE), run_time=0.6)
        clicks = VGroup(*[Arc(radius=0.18 + 0.14 * k, start_angle=-PI / 4, angle=PI / 2, color=OCHRE, stroke_width=2.5)
                          for k in range(3)]).next_to(labs[2], RIGHT, buff=0.1)
        self.play_at(self.t('5.4', 1, 'Klicklauten'), Create(clicks, lag_ratio=0.3), run_time=0.6)

        # Sentence 3: partial point of view – partial concept. Understanding falls, but not to zero.
        self.wait_until(self.t('5.4', 2))
        axes_h = 2.0

        def level(x):
            return 0.12 + 0.88 * np.exp(-((x + 5.0) / 5.2) ** 2)
        curve = FunctionGraph(lambda x: y + 0.2 + axes_h * level(x), x_range=[-5.0, 5.0], color=VIOLET, stroke_width=4)
        lab = txt('wie voll wir den Begriff bilden können', size=19, color=VIOLET).move_to([-1.2, y + 2.55, 0])
        lab.align_to(curve, LEFT)
        lab.next_to(curve.get_start(), RIGHT, buff=0.3).shift(UP * 0.15)
        knob = Dot(curve.get_start(), radius=0.11, color=FG)
        self.play(FadeIn(knob), FadeIn(lab), run_time=0.4)
        tracker = ValueTracker(-5.0)
        knob.add_updater(lambda d: d.move_to([tracker.get_value(), y + 0.2 + axes_h * level(tracker.get_value()), 0]))
        trail = always_redraw(lambda: FunctionGraph(lambda x: y + 0.2 + axes_h * level(x),
                                                    x_range=[-5.0, max(-4.99, tracker.get_value())], color=VIOLET,
                                                    stroke_width=4))
        self.add(trail)
        dur = max(2.5, self.t('5.4', 2, end=True) - self.now - 1.0)
        self.play(tracker.animate.set_value(5.0), run_time=dur, rate_func=smooth)
        knob.clear_updaters()
        nz = txt('klein, aber nicht null', size=19, color=MUTED).next_to(knob, UP, buff=0.2)
        self.play(FadeIn(nz), run_time=0.4)
        self.wait_until(self.t('5.4', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 5.5
    def p55(self):
        self.wait_until(self.t('5.5'))
        self.cite(self.cite_of('5.5'))
        head = txt('objektive Phänomenologie', size=40, font=SERIF, weight=SEMIBOLD).move_to([0, 2.6, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)
        q = QuoteCard(self.quote_of('5.5'), 'Nagel 1974, S. 449').next_to(head, DOWN, buff=0.3)
        self.play(FadeIn(q), run_time=0.5)

        # Sentence 2: e.g. explain to someone blind from birth what seeing is like.
        self.wait_until(self.t('5.5', 1))
        aim = txt('Ziel: Erfahrungen so beschreiben, dass sie teilweise verständlich werden\n'
                  'für Wesen, die sie nicht haben können', size=22, color=MUTED).move_to([0, 0.3, 0])
        self.play(FadeOut(q), FadeIn(aim), run_time=0.6)
        ex = txt('z. B. einem von Geburt an blinden Menschen: wie Sehen ist', size=22).next_to(aim, DOWN, buff=0.3)
        self.play_at(self.t('5.5', 1, 'blinden'), FadeIn(ex), run_time=0.5)

        # Sentence 3: loose analogies don't help; structure might.
        self.wait_until(self.t('5.5', 2))
        self.play(FadeOut(aim), FadeOut(ex), run_time=0.4)
        loose = pill('Rot ist wie der Klang einer Trompete', color=PANEL, text_color=FG, size=22).move_to([-3.3, 0.4, 0])
        self.play(FadeIn(loose), run_time=0.5)

        # A similarity space: positions and neighbourhoods are describable, the points stay empty.
        names = ['Rot', 'Orange', 'Gelb', 'Grün', 'Blau', 'Violett']
        cx, cy, r = 2.6, -0.1, 1.6
        pts = [np.array([cx + r * np.cos(PI / 2 - k * TAU / 6), cy + r * np.sin(PI / 2 - k * TAU / 6), 0]) for k in range(6)]
        rings = VGroup(*[Circle(radius=0.2, stroke_color=FG, stroke_width=2.5).move_to(p) for p in pts])
        links = VGroup(*[Line(pts[k], pts[(k + 1) % 6], color=DIM, stroke_width=2.5, buff=0.22) for k in range(6)])
        across = DashedLine(pts[0], pts[3], color=DIM, stroke_width=2, buff=0.22)
        nl = VGroup(*[txt(n, size=18, color=MUTED).move_to(p + (p - [cx, cy, 0]) * 0.36) for n, p in zip(names, pts)])
        title = txt('Struktur: Nachbarschaft und Abstand', size=20, color=OCHRE).move_to([cx, cy - 2.85, 0])
        self.play_at(self.t('5.5', 2, 'helfen'), loose.animate.shift(DOWN * 2.2).rotate(-0.35).set_opacity(0),
                     LaggedStart(*[Create(c) for c in rings], lag_ratio=0.1), Create(links), FadeIn(nl), run_time=1.0)
        self.play_at(self.t('5.5', 2, 'strukturelle'), Create(across), FadeIn(title), run_time=0.6)

        # Sentence 4: footnote 15 – a theory whose basic terms are neither clearly mental nor physical.
        self.wait_until(self.t('5.5', 3) + 2.0)
        self.play(FadeOut(VGroup(rings, links, across, nl, title)), run_time=0.5)
        m = Circle(radius=0.8, stroke_color=VIOLET, stroke_width=3).move_to([-2.0, 0.3, 0])
        p = Circle(radius=0.8, stroke_color=OCHRE, stroke_width=3).move_to([2.0, 0.3, 0])
        ml = txt('mental', size=24, color=VIOLET).move_to(m)
        pl = txt('physisch', size=24, color=OCHRE).move_to(p)
        n = Circle(radius=0.9, stroke_color=MUTED, stroke_width=3, fill_color='#2b303a', fill_opacity=1).move_to([0, -2.0, 0])
        nl2 = txt('weder klar mental\nnoch klar physisch', size=17, color=FG).move_to(n)
        a1 = Arrow(n.get_top() + LEFT * 0.3, m.get_bottom() + RIGHT * 0.2, buff=0.08, color=MUTED, stroke_width=3)
        a2 = Arrow(n.get_top() + RIGHT * 0.3, p.get_bottom() + LEFT * 0.2, buff=0.08, color=MUTED, stroke_width=3)
        self.play(Create(m), Create(p), FadeIn(ml), FadeIn(pl), run_time=0.7)
        self.play_at(self.t('5.5', 3, 'Theorie'), FadeIn(n), FadeIn(nl2), run_time=0.6)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        fwd = pill('→ Kapitel 10', color=PANEL, text_color=MUTED, size=18).move_to([4.9, -2.0, 0])
        fn = txt('Nagel 1974, S. 450, Fn. 15', size=17, color=MUTED).next_to(n, LEFT, buff=0.6)
        self.play(FadeIn(fwd), FadeIn(fn), run_time=0.4)
