"""Kapitel 8 – Einwände (Dennett 1991; Akins 1993 nach Salzani 2022; Allen-Hermanson 2015;
Lewis 1988; Nemirow 1980; Hacker 2002; Frankish 2016).

Der Argumentbaum aus Kapitel 4 kehrt zurück; jeder Einwand trifft als roter Pfeil den
Knoten, den er angreift (Tabelle in research/argument.md). Grün nur für die Gegenkritik.

8.1  Der ganze Baum; die angegriffenen Knoten werden markiert.
8.2  Dennett: Das Außenfeld füllt sich mit Daten; „zugänglich“ – Pfeil auf Z2.
8.3  Akins: Das Innenfeld wird zum Steuerpult ohne Pilot – Pfeile auf P2, Z3;
     Allen-Hermanson: grüner Gegenpfeil.
8.4  Lewis/Nemirow: „Wie ist es?“ wandert vom Regal „Wissen, dass“ ins Regal „Wissen, wie“.
8.5  Hacker: Satzbaukasten mit Kontrastfeldern; bei Fledermaus/Fledermaus bleiben sie leer.
8.6  Frankish: Das Innenfeld als Projektion – danach zurück: eine Deutung unter mehreren.
"""

from parts import *

PX = 2.5        # centre of the picture area right of the mini tree


class Kapitel8(NarratedScene):
    CHAPTER = 8

    def construct(self):
        self.chapter_card()
        self.p81()
        self.p82()
        self.p83()
        self.p84()
        self.p85()
        self.p86()
        self.finish()

    # ------------------------------------------------------------ helpers
    def fixed(self):
        keep = {self.tag, self.cite_mob}
        for m in [*self.mini.nodes.values(), *self.mini.edges.values(), *self.hits]:
            keep |= set(m.get_family())
        return keep

    def wipe(self):
        keep = self.fixed()
        gone = [m for m in self.mobjects if m not in keep]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)

    def hit(self, nid, who, color=RED, direction=DOWN, length=0.42, offset=ORIGIN):
        """Short arrow onto a node of the mini tree, plus a caption below the tree."""
        node = self.mini.nodes[nid]
        tip = node.get_edge_center(direction) + offset
        arr = Arrow(tip + direction * length, tip, buff=0.02, color=color, stroke_width=4,
                    max_tip_length_to_length_ratio=0.45)
        self.play(GrowArrow(arr), Indicate(node, color=color, scale_factor=1.25), run_time=0.6)
        self.hits.append(arr)
        cap = VGroup(txt(who, size=17, color=color, weight=SEMIBOLD),
                     txt('→', size=17, color=color),
                     self.mini.caption(nid, size=16)).arrange(RIGHT, buff=0.15)
        if cap.width > 4.5:
            cap.scale_to_fit_width(4.5)
        y = 0.35 - 0.38 * len(self.caps)
        cap.move_to([-6.75, y, 0], aligned_edge=UL)
        self.play(FadeIn(cap), run_time=0.35)
        self.caps.append(cap)
        self.hits.append(cap)
        return arr

    def reset_hits(self):
        if self.hits:
            self.play(*[FadeOut(h) for h in self.hits], run_time=0.4)
        self.hits, self.caps = [], []

    # ------------------------------------------------------------ 8.1
    def p81(self):
        self.wait_until(self.t('8.1'))
        full = ArgTree(mini=False)
        self.play(*[FadeIn(n) for n in full.nodes.values()], *[FadeIn(e) for e in full.edges.values()], run_time=1.0)
        self.wait_until(self.t('8.1', 1, 'Schritt'))
        targets = ['D1', 'D2', 'P2', 'Z2', 'P5', 'Z3']
        marks = VGroup(*[SurroundingRectangle(full.nodes[n], color=RED, buff=0.06, corner_radius=0.08, stroke_width=3)
                         for n in targets])
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.15), run_time=1.2)

        # Shrink to the mini map for the individual objections.
        self.wait_until(self.t('8.1', 'end') + 0.05)
        self.mini = ArgTree(mini=True)
        self.hits, self.caps = [], []
        self.play(FadeOut(marks), run_time=0.3)
        self.play(*[ReplacementTransform(full.nodes[n], self.mini.nodes[n]) for n in full.nodes],
                  *[ReplacementTransform(full.edges[k], self.mini.edges[k]) for k in full.edges], run_time=0.9)

    # ------------------------------------------------------------ 8.2
    def p82(self):
        self.wait_until(self.t('8.2'))
        self.cite(self.cite_of('8.2'))
        name = txt('Daniel Dennett', size=30, weight=SEMIBOLD).move_to([PX, 2.9, 0])
        fn = txt('in Nagels Fn. 1 unter den Reduktionisten', size=18, color=MUTED).next_to(name, DOWN, buff=0.1)
        self.play(FadeIn(name), FadeIn(fn), run_time=0.6)

        # Sentence 2: „I flatly deny that claim.“
        self.wait_until(self.t('8.2', 1))
        q = QuoteCard(self.quote_of('8.2'), 'Dennett 1991, S. 442', size=24).move_to([PX, 1.1, 0])
        self.play(FadeOut(fn), FadeIn(q, shift=UP * 0.1), run_time=0.6)

        # Sentence 3: a lot can be known – the outer field fills with data.
        self.wait_until(self.t('8.2', 2))
        self.play(FadeOut(q), run_time=0.3)
        outer = OuterField(width=4.6, height=3.4, label='von außen: Verhalten, Neurone, Umwelt').move_to([0.75, -0.55, 0])
        inner = InnerField(width=3.2, height=3.4, label='für die Fledermaus', seed=23).move_to([5.25, -0.55, 0])
        self.play(FadeIn(outer), FadeIn(inner), run_time=0.6)
        b = bat(width=1.0).move_to(outer.box.get_corner(UL) + [0.75, -0.5, 0])
        bars = VGroup(*[Rectangle(width=0.22, height=h, fill_color=OCHRE, fill_opacity=0.8, stroke_width=0)
                        for h in (0.4, 0.9, 0.6, 1.2, 0.8)]).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        bars.move_to(outer.box.get_corner(UR) + [-1.0, -0.9, 0])
        nets = net_pattern(cols=5, rows=2, lit=(1, 3, 7), spacing=0.32).move_to(outer.box.get_corner(DL) + [1.2, 0.75, 0])
        sweeps = VGroup(*[Arc(radius=0.5, start_angle=PI / 2, angle=-PI / 2, color=OCHRE, stroke_width=2.5)
                          .move_to(outer.box.get_corner(DR) + [-1.3 + 0.35 * k, 0.75, 0]) for k in range(3)])
        for m in (b, bars, nets, sweeps):
            self.play(FadeIn(m, shift=UP * 0.05), run_time=0.45)
        dig = txt('Struktur des Geistes so zugänglich wie\ndie des Verdauungssystems (S. 447)', size=17, color=MUTED)
        dig.next_to(outer.box, DOWN, buff=0.15)
        self.play_at(self.t('8.2', 2, 'Verdauungssystems'), FadeIn(dig), run_time=0.5)
        reach = Arrow(outer.box.get_right() + LEFT * 0.3, inner.box.get_center(), buff=0.1, color=OCHRE, stroke_width=4)
        self.play(GrowArrow(reach), inner.box.animate.set_stroke(opacity=0.4), run_time=0.7)

        # Sentence 4: the target – Z2.
        self.wait_until(self.t('8.2', 3))
        self.hit('Z2', 'Dennett')
        self.wait_until(self.t('8.2', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 8.3
    def p83(self):
        self.wait_until(self.t('8.3'))
        self.cite(self.cite_of('8.3', 0))
        name = txt('Kathleen Akins', size=30, weight=SEMIBOLD).move_to([PX, 2.9, 0])
        sp = txt('Schnurrbartfledermaus · 1993', size=18, color=MUTED).next_to(name, DOWN, buff=0.1)
        warn = txt('Akins’ Text nicht selbst eingesehen; Wortlaut nach Salzani 2022 und Allen-Hermanson 2015',
                   size=15, color=MUTED, slant=ITALIC).move_to([PX, -3.1, 0])
        self.play(FadeIn(name), FadeIn(sp), FadeIn(warn), run_time=0.6)

        # Sentence 2: sonar probably not used to represent objects.
        self.wait_until(self.t('8.3', 1))
        b = bat(width=1.1).move_to([-0.6, 0.6, 0])
        objs = VGroup(insect(size=0.45).move_to([1.6, 1.2, 0]), stone(width=0.8).move_to([1.8, 0.0, 0]))
        frame = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=2.0, height=2.3, stroke_color=MUTED),
                               num_dashes=30).move_to([1.7, 0.6, 0])
        lab = txt('Gegenstände darstellen?', size=18, color=MUTED).next_to(frame, DOWN, buff=0.12)
        self.play(FadeIn(b), FadeIn(objs), Create(frame), FadeIn(lab), run_time=0.8)
        self.play_at(self.t('8.3', 1, 'nicht'), objs.animate.set_opacity(0.15), run_time=0.6)

        # Sentence 3: no point of view – a console without a pilot.
        self.wait_until(self.t('8.3', 2))
        self.play(FadeOut(VGroup(objs, frame, lab)), run_time=0.4)
        inner = InnerField(width=5.2, height=2.6, label='für die Fledermaus?', seed=29).move_to([3.7, 0.3, 0])
        self.play(FadeIn(inner), run_time=0.5)
        echo = txt('Echo', size=18, color=OCHRE)
        proc = RoundedRectangle(corner_radius=0.08, width=1.4, height=0.56, stroke_color=OCHRE, stroke_width=2,
                                fill_color=PANEL, fill_opacity=1)
        ptxt = txt('Verarbeitung', size=15).move_to(proc)
        motor = txt('Flugbewegung', size=18, color=OCHRE)
        console = VGroup(echo, VGroup(proc, ptxt), motor).arrange(RIGHT, buff=0.4).move_to(inner.box.get_center() + UP * 0.35)
        a1 = Arrow(echo.get_right(), proc.get_left(), buff=0.08, color=OCHRE, stroke_width=3)
        a2 = Arrow(proc.get_right(), motor.get_left(), buff=0.08, color=OCHRE, stroke_width=3)
        seat = DashedVMobject(Circle(radius=0.28, stroke_color=MUTED, stroke_width=2), num_dashes=16)
        seat.move_to(inner.box.get_center() + DOWN * 0.65)
        no_pilot = txt('kein Standpunkt?', size=18, color=MUTED).next_to(seat, RIGHT, buff=0.2)
        self.play(FadeOut(inner.grain), FadeIn(console), GrowArrow(a1), GrowArrow(a2), run_time=0.9)
        self.play_at(self.t('8.3', 2, 'keinen Standpunkt'), Create(seat), FadeIn(no_pilot), run_time=0.6)

        # Sentence 4: target – Nagel's assumption that there is something it is like (P2), and Z3.
        self.wait_until(self.t('8.3', 3))
        self.hit('P2', 'Akins', direction=RIGHT, offset=DOWN * 0.06)
        self.hit('Z3', 'Akins', direction=UP)

        # Sentence 5: Allen-Hermanson 2015 – bats are not rigid automata.
        self.wait_until(self.t('8.3', 4))
        self.cite(self.cite_of('8.3', 1))
        counter = Arrow([PX + 4.2, -2.4, 0], inner.box.get_corner(DR) + [-0.3, 0.3, 0], buff=0.05, color=GREEN,
                        stroke_width=6)
        ah = txt('Allen-Hermanson 2015:\nkeine starren Automaten', size=18, color=GREEN).next_to(counter.get_start(), LEFT,
                                                                                                buff=0.15)
        self.play(GrowArrow(counter), FadeIn(ah), run_time=0.7)
        self.play(FadeOut(VGroup(console, a1, a2, seat, no_pilot)), FadeIn(inner.grain), run_time=0.7)
        self.hit('P2', 'Allen-Hermanson', color=GREEN, direction=RIGHT, offset=UP * 0.07)
        self.wait_until(self.t('8.3', 'end') + 0.1)
        self.wipe()
        self.reset_hits()

    # ------------------------------------------------------------ 8.4
    def p84(self):
        self.wait_until(self.t('8.4'))
        self.cite(self.cite_of('8.4'))
        name = txt('David Lewis · Laurence Nemirow', size=30, weight=SEMIBOLD).move_to([PX, 2.9, 0])
        self.play(FadeIn(name), run_time=0.5)

        # Sentence 2: the ability hypothesis – two shelves.
        self.wait_until(self.t('8.4', 1))
        def shelf(x, title, items, color):
            board = Line([x - 2.0, -1.4, 0], [x + 2.0, -1.4, 0], color=MUTED, stroke_width=6)
            t = txt(title, size=24, color=color, weight=SEMIBOLD).move_to([x, 1.75, 0])
            row = VGroup(*items).arrange(RIGHT, buff=0.15, aligned_edge=DOWN).next_to(board, UP, buff=0.04)
            return VGroup(board, t, row)
        books = [Rectangle(width=0.32, height=h, fill_color=c, fill_opacity=0.9, stroke_width=0)
                 for h, c in ((1.3, '#5d6b85'), (1.0, '#7a6a55'), (1.5, '#4f6f63'), (1.15, '#6b5872'))]
        formula = VGroup(RoundedRectangle(corner_radius=0.06, width=1.5, height=0.8, fill_color=PANEL, fill_opacity=1,
                                          stroke_color=MUTED, stroke_width=1.5),
                         txt('r = c·Δt / 2', size=18))
        formula[1].move_to(formula[0])
        that = shelf(-0.1, 'Wissen, dass', books + [formula], OCHRE)
        abil = [pill(t, color=PANEL, text_color=VIOLET, size=17) for t in ('erinnern', 'vorstellen', 'wiedererkennen')]
        how = VGroup(*abil).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        how_shelf = shelf(4.7, 'Wissen, wie', [how], VIOLET)
        self.play(FadeIn(that), run_time=0.6)
        self.play_at(self.t('8.4', 1, 'Fähigkeiten'), FadeIn(how_shelf), run_time=0.6)
        for p, key in zip(abil, ['erinnern', 'vorzustellen', 'wiederzuerkennen']):
            self.play_at(self.t('8.4', 1, key), Indicate(p, color=VIOLET, scale_factor=1.1), run_time=0.4)

        # Sentence 3: lessons impart information; ability is something else.
        self.wait_until(self.t('8.4', 2))
        lesson = txt('„Lessons impart information; ability is something else.“', size=20, font=SERIF, slant=ITALIC)
        lesson.move_to([PX, -2.2, 0])
        src = txt('Lewis 1988', size=16, color=MUTED).next_to(lesson, DOWN, buff=0.08)
        self.play(FadeIn(lesson), FadeIn(src), run_time=0.6)

        # Sentence 4: no physics lesson teaches what bat echolocation is like.
        self.wait_until(self.t('8.4', 3))
        qcard = pill('Wie ist es?', color=PANEL, text_color=FG, size=22).next_to(that[2], UP, buff=0.35)
        self.play(FadeIn(qcard, shift=DOWN * 0.1), run_time=0.5)
        self.play(qcard.animate.next_to(how, UP, buff=0.3), run_time=1.4, rate_func=smooth)

        # Sentence 5: target – realism about subjective facts (P5) and Z3.
        self.wait_until(self.t('8.4', 4))
        self.hit('P5', 'Lewis/Nemirow')
        self.hit('Z3', 'Lewis/Nemirow', direction=UP)
        self.wait_until(self.t('8.4', 'end') + 0.1)
        self.wipe()
        self.reset_hits()

    # ------------------------------------------------------------ 8.5
    def p85(self):
        self.wait_until(self.t('8.5'))
        self.cite(self.cite_of('8.5'))
        name = txt('Peter Hacker', size=30, weight=SEMIBOLD).move_to([PX, 2.9, 0])
        self.play(FadeIn(name), run_time=0.5)

        # Sentence 2: the question needs a contrast.
        def slot(word, color):
            t = txt(word, size=24, color=color)
            box = RoundedRectangle(corner_radius=0.08, width=max(1.6, t.width + 0.4), height=0.6, stroke_color=color,
                                   stroke_width=2)
            return VGroup(box, t.move_to(box))
        def fit(frame):
            frame.arrange(RIGHT, buff=0.16)
            if frame.width > 8.6:
                frame.scale_to_fit_width(8.6)
            return frame.move_to([PX, 1.3, 0])

        def contrast_under(sl, word, color):
            c = VGroup(txt('im Unterschied zu', size=15, color=MUTED), slot(word, color)).arrange(DOWN, buff=0.08)
            return c.next_to(sl, DOWN, buff=0.3)
        self.wait_until(self.t('8.5', 1))
        frame = fit(VGroup(txt('Wie ist es für', size=24), slot('eine Frau', FG), txt(',', size=24),
                           slot('Soldatin', FG), txt('zu sein?', size=24)))
        contrast = contrast_under(frame[1], 'einen Mann', OCHRE)
        self.play(FadeIn(frame), run_time=0.6)
        self.play_at(self.t('8.5', 1, 'Unterschied'), FadeIn(contrast, shift=UP * 0.1), run_time=0.5)

        # Sentence 3: bat/bat – the contrast fields light up empty.
        self.wait_until(self.t('8.5', 2))
        frame2 = fit(VGroup(txt('Wie ist es für', size=24), slot('eine Fledermaus', VIOLET), txt(',', size=24),
                            slot('eine Fledermaus', VIOLET), txt('zu sein?', size=24)))
        empty = contrast_under(frame2[1], '?', MUTED)
        empty2 = contrast_under(frame2[3], '?', MUTED)
        self.play(ReplacementTransform(frame, frame2), ReplacementTransform(contrast, empty), run_time=0.8)
        self.play(FadeIn(empty2), run_time=0.4)
        self.play(empty[1][0].animate.set_stroke(OCHRE, width=4), empty2[1][0].animate.set_stroke(OCHRE, width=4),
                  rate_func=there_and_back, run_time=0.8)

        # Sentence 4: „Wie war es für dich?“ asks for an evaluation.
        self.wait_until(self.t('8.5', 3))
        ask = txt('„Wie war es für dich?“', size=24).move_to([PX - 1.6, -1.2, 0])
        ans = VGroup(pill('angenehm', color=PANEL, text_color=FG, size=18), pill('aufregend', color=PANEL, text_color=FG,
                                                                              size=18)).arrange(RIGHT, buff=0.2)
        ans.next_to(ask, RIGHT, buff=0.5)
        self.play(FadeIn(ask), run_time=0.4)
        self.play_at(self.t('8.5', 3, 'Bewertung'), FadeIn(ans, shift=LEFT * 0.1), run_time=0.5)

        # Sentence 5: „malconstructed“.
        self.wait_until(self.t('8.5', 4))
        q = QuoteCard(self.quote_of('8.5'), self.cite_of('8.5'), size=26).move_to([0.2, -2.6, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.hit('D1', 'Hacker', direction=LEFT, length=0.32)
        self.hit('D2', 'Hacker', direction=LEFT, length=0.32)

        # Sentence 6: Nagel's clarification is known to him – it does not convince him.
        self.wait_until(self.t('8.5', 5))
        fn6 = VGroup(txt('Nagels Klarstellung (Fn. 6):\n„how it is for the subject himself“', size=16, font=SERIF,
                         slant=ITALIC),
                     txt('Nagel 1974, S. 440', size=14, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        fn6.move_to([4.5, -2.6, 0])
        self.play(FadeIn(fn6), run_time=0.5)
        no = txt('überzeugt Hacker nicht', size=17, color=RED).next_to(fn6, UP, buff=0.12).align_to(fn6, LEFT)
        self.play(FadeIn(no), run_time=0.4)
        self.wait_until(self.t('8.5', 'end') + 0.1)
        self.wipe()
        self.reset_hits()

    # ------------------------------------------------------------ 8.6
    def p86(self):
        self.wait_until(self.t('8.6'))
        self.cite(self.cite_of('8.6'))
        name = txt('Keith Frankish · Illusionismus', size=30, weight=SEMIBOLD).move_to([PX, 2.9, 0])
        self.play(FadeIn(name), run_time=0.5)
        outer = OuterField(width=4.0, height=3.4, label='von außen').move_to([0.3, -0.35, 0])
        inner = InnerField(width=3.6, height=3.4, label='für das Wesen selbst', seed=37).move_to([4.75, -0.35, 0])
        self.play(FadeIn(outer), FadeIn(inner), run_time=0.6)

        # Sentence 2: it seems to us that experiences have a qualitative inside.
        self.wait_until(self.t('8.6', 1))
        seems = txt('es scheint so', size=22, color=VIOLET).move_to(inner.box)
        self.play(FadeIn(seems), run_time=0.5)

        # Sentence 3: but there are no such phenomenal properties – a projection.
        self.wait_until(self.t('8.6', 2))
        proj = VGroup(RoundedRectangle(corner_radius=0.08, width=1.0, height=0.6, fill_color=MUTED, fill_opacity=1,
                                       stroke_width=0),
                      Circle(radius=0.17, fill_color=BG, fill_opacity=1, stroke_width=0).shift(RIGHT * 0.5))
        proj.move_to(outer.box.get_center() + RIGHT * 0.7)
        beam = Polygon(proj[1].get_center(), inner.box.get_corner(UL) + [0.15, -0.15, 0],
                       inner.box.get_corner(DL) + [0.15, 0.15, 0], stroke_width=0, fill_color=FG, fill_opacity=0.08)
        plab = txt('Projektor', size=18, color=MUTED).next_to(proj, DOWN, buff=0.15)
        self.play(FadeIn(proj), FadeIn(plab), run_time=0.5)
        self.play(FadeIn(beam), inner.box.animate.set_fill(opacity=0.35), run_time=0.8)
        screen = txt('nur Anschein?', size=20, color=MUTED).next_to(seems, DOWN, buff=0.2)
        self.play_at(self.t('8.6', 2, 'wirklich'), FadeIn(screen), run_time=0.5)

        # Sentence 4: the illusion problem replaces the hard problem.
        self.wait_until(self.t('8.6', 3))
        ip = VGroup(txt('hartes Problem', size=22, color=MUTED), txt('→', size=22, color=MUTED),
                    txt('Illusionsproblem: Wie entsteht der Anschein,\nund warum ist er so hartnäckig?', size=20))
        ip.arrange(RIGHT, buff=0.25).move_to([PX, -2.7, 0])
        strike = Line(ip[0].get_left(), ip[0].get_right(), color=MUTED, stroke_width=3)
        self.play(FadeIn(ip), run_time=0.6)
        self.play(Create(strike), run_time=0.4)

        # Sentence 5: target – the definition itself (D1). Then back: one reading among several.
        self.wait_until(self.t('8.6', 4))
        self.hit('D1', 'Frankish', direction=LEFT, length=0.32)
        self.play(FadeOut(VGroup(proj, plab, beam, screen)), inner.box.animate.set_fill(opacity=1), run_time=0.8)
        one = txt('eine Deutung unter mehreren', size=18, color=MUTED).next_to(seems, DOWN, buff=0.25)
        self.play(FadeIn(one), run_time=0.4)
