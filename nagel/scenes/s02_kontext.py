"""Kapitel 2 – Die Lage 1974 (Nagel 1974, S. 435 mit Fn. 1, 436; Place 1956; Smart 1959; Putnam 1967).

2.1  Zwei Ebenen: Alltag oben, grundlegendere Wissenschaft unten; Wasser → H₂O,
     Blitz → Ladungsfluss; das Programm: auch Mentales nach unten verbinden.
2.2  Drei Diagramme: Behaviorismus (leerer Kasten zwischen Reiz und Verhalten),
     Identitätstheorie (Empfindung = Erregungsmuster), Funktionalismus (Rolle,
     austauschbares Material).
2.3  Fußnotenkarte mit den Namen aus Fn. 1; Nagels Analogien als Paare – das
     letzte Paar „Bewusstsein = ?“ hält nicht.
"""

from parts import *


class Kapitel2(NarratedScene):
    CHAPTER = 2

    def construct(self):
        self.chapter_card()
        self.p21()
        self.p22()
        self.p23()
        self.finish()

    # ------------------------------------------------------------ 2.1
    def p21(self):
        self.wait_until(self.t('2.1'))
        self.cite(self.cite_of('2.1'))
        top_y, bot_y = 1.55, -1.45
        band_top = Rectangle(width=12.6, height=1.9, stroke_width=0, fill_color=PANEL, fill_opacity=1).move_to([0.3, top_y, 0])
        band_bot = band_top.copy().move_to([0.3, bot_y, 0])
        lt = txt('Alltag', size=22, color=MUTED).next_to(band_top, LEFT, buff=-1.45).shift(UP * 0.62)
        lb = txt('grundlegendere\nWissenschaft', size=22, color=OCHRE).move_to(band_bot.get_corner(UL) + [0.95, -0.5, 0])
        lt.move_to(band_top.get_corner(UL) + [0.55, -0.32, 0])
        self.play(FadeIn(band_top), FadeIn(band_bot), FadeIn(lt), FadeIn(lb), run_time=0.8)

        cols = [-1.6, 1.4, 4.4]
        pairs = [
            (water_drop(height=0.85), 'Wasser', molecule_h2o(height=0.9), 'H₂O'),
            (lightning(height=0.95), 'Blitz', charges(), 'Ladungsfluss'),
        ]
        groups = []
        for x, (a, an, b, bn) in zip(cols, pairs):
            a.move_to([x, top_y + 0.2, 0])
            b.move_to([x, bot_y + 0.2, 0])
            al = txt(an, size=22).next_to(a, DOWN, buff=0.15)
            bl = txt(bn, size=22).next_to(b, DOWN, buff=0.15)
            arr = Arrow([x, top_y - 0.85, 0], [x, bot_y + 0.85, 0], buff=0, color=OCHRE, stroke_width=4)
            groups.append((VGroup(a, al), arr, VGroup(b, bl)))

        self.wait_until(self.t('2.1', 1))
        for top, arr, bot in groups:
            self.play(FadeIn(top), run_time=0.5)
            self.play(GrowArrow(arr), FadeIn(bot, shift=DOWN * 0.1), run_time=0.8)
        euph = txt('„reduktionistische Euphorie“', size=26, color=OCHRE, font=SERIF, slant=ITALIC)
        euph.move_to([0.3, 3.0, 0])
        self.play_at(self.t('2.1', 1, 'Euphorie'), FadeIn(euph, shift=DOWN * 0.1), run_time=0.6)

        # The programme: the mental, too, should turn out to be something below.
        x = cols[2]
        mental = txt('Mentales', size=26, color=VIOLET, weight=MEDIUM).move_to([x, top_y + 0.1, 0])
        target = txt('… dasselbe wie\netwas hier unten?', size=22, color=MUTED).move_to([x, bot_y + 0.1, 0])
        darr = DashedLine([x, top_y - 0.45, 0], [x, bot_y + 0.6, 0], color=VIOLET, stroke_width=3).add_tip(tip_length=0.18)
        self.play_at(self.t('2.1', 1, 'Mentales'), FadeIn(mental), run_time=0.5)
        self.play(Create(darr), FadeIn(target), run_time=1.0)
        self.wait_until(self.t('2.1', 'end') + 0.1)
        self.play(FadeOut(VGroup(band_top, band_bot, lt, lb, euph, mental, target, darr,
                                 *[m for g in groups for m in g])), run_time=0.55)

    # ------------------------------------------------------------ 2.2
    def p22(self):
        self.wait_until(self.t('2.2'))
        xs = [-4.55, 0, 4.55]
        titles = ['Behaviorismus', 'Identitätstheorie', 'Funktionalismus']
        heads = VGroup(*[txt(t, size=28, weight=MEDIUM).move_to([x, 2.35, 0]) for x, t in zip(xs, titles)])
        seps = VGroup(*[Line([x, 2.6, 0], [x, -2.7, 0], color=DIM, stroke_width=2) for x in (-2.27, 2.27)])
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.1) for h in heads], lag_ratio=0.3), Create(seps),
                  run_time=1.2)
        self.play(heads[1].animate.set_opacity(0.35), heads[2].animate.set_opacity(0.35), run_time=0.4)

        # Behaviourism: stimulus → (empty, dashed) → behaviour.
        self.wait_until(self.t('2.2', 1))
        x = xs[0]
        box = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=1.1, height=0.75, stroke_color=MUTED,
                                              stroke_width=2.5), num_dashes=24).move_to([x, 0.6, 0])
        r = txt('Reiz', size=22, color=MUTED).next_to(box, LEFT, buff=0.55)
        v = txt('Verhalten', size=22).next_to(box, RIGHT, buff=0.55)
        VGroup(r, box, v).move_to([x, 0.6, 0])
        a1 = Arrow(r.get_right(), box.get_left(), buff=0.08, color=OCHRE, stroke_width=3)
        a2 = Arrow(box.get_right(), v.get_left(), buff=0.08, color=OCHRE, stroke_width=3)
        cap1 = txt('mentale Begriffe =\nRede über Verhalten\nund Verhaltensneigungen', size=21, color=MUTED)
        cap1.move_to([x, -1.4, 0])
        self.play(FadeIn(r), GrowArrow(a1), Create(box), GrowArrow(a2), FadeIn(v), run_time=1.2)
        self.play_at(self.t('2.2', 1, 'Rede über'), FadeIn(cap1), run_time=0.6)

        # Identity theory: sensation = a pattern of nerve activity.
        self.wait_until(self.t('2.2', 2))
        self.cite(self.cite_of('2.2', 0))
        self.play(heads[0].animate.set_opacity(0.35), heads[1].animate.set_opacity(1), run_time=0.4)
        x = xs[1]
        sens = txt('Empfindung', size=24, color=VIOLET).move_to([x, 1.3, 0])
        eq = txt('=', size=40).move_to([x, 0.75, 0])
        net = net_pattern().scale(0.85).move_to([x, 0.0, 0])
        cap2 = txt('Empfindungen sind\nGehirnprozesse', size=21, color=MUTED).move_to([x, -1.4, 0])
        self.play(FadeIn(sens), run_time=0.5)
        self.play(FadeIn(eq), Create(net.edges), FadeIn(net.nodes), run_time=1.0)
        self.play_at(self.t('2.2', 2, 'Empfindungen'), FadeIn(cap2), Indicate(net.nodes, color=OCHRE, scale_factor=1.15),
                     run_time=0.9)

        # Functionalism: defined by role; the material can be swapped.
        self.wait_until(self.t('2.2', 3))
        self.cite(self.cite_of('2.2', 1))
        self.play(heads[1].animate.set_opacity(0.35), heads[2].animate.set_opacity(1), run_time=0.4)
        x = xs[2]
        role = RoundedRectangle(corner_radius=0.08, width=1.2, height=0.7, stroke_color=OCHRE, stroke_width=2.5,
                                fill_color=PANEL, fill_opacity=1).move_to([x, 1.15, 0])
        rl = txt('Rolle', size=22).move_to(role)
        cin = txt('Ursache', size=20, color=MUTED).next_to(role, LEFT, buff=0.45)
        cout = txt('Wirkung', size=20, color=MUTED).next_to(role, RIGHT, buff=0.45)
        f1 = Arrow(cin.get_right(), role.get_left(), buff=0.06, color=OCHRE, stroke_width=3)
        f2 = Arrow(role.get_right(), cout.get_left(), buff=0.06, color=OCHRE, stroke_width=3)
        n = neuron(size=0.8).move_to([x - 0.9, -0.25, 0])
        c = chip(size=0.85).move_to([x + 0.9, -0.25, 0])
        oder = txt('oder', size=20, color=MUTED).move_to([x, -0.25, 0])
        up1 = DashedLine(n.get_top() + UP * 0.05, role.get_bottom() + LEFT * 0.3, color=MUTED, stroke_width=2)
        up2 = DashedLine(c.get_top() + UP * 0.05, role.get_bottom() + RIGHT * 0.3, color=MUTED, stroke_width=2)
        cap3 = txt('dieselbe Rolle,\nverschiedenes Material', size=21, color=MUTED).move_to([x, -1.4, 0])
        self.play(FadeIn(role), FadeIn(rl), run_time=0.5)
        self.play_at(self.t('2.2', 3, 'was sie auslöst'), FadeIn(cin), GrowArrow(f1), run_time=0.5)
        self.play_at(self.t('2.2', 3, 'was sie bewirken'), GrowArrow(f2), FadeIn(cout), run_time=0.5)
        self.play_at(self.t('2.2', 3, 'gleichgültig'), FadeIn(n), Create(up1), run_time=0.6)
        self.play(FadeIn(oder), FadeIn(c), Create(up2), FadeIn(cap3), run_time=0.8)
        self.play(*[h.animate.set_opacity(1) for h in heads], run_time=0.4)

        self.wait_until(self.t('2.2', 'end') + 0.1)
        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in (self.tag, self.cite_mob)])), run_time=0.55)

    # ------------------------------------------------------------ 2.3
    def p23(self):
        self.wait_until(self.t('2.3'))
        self.cite(self.cite_of('2.3'))
        # Footnote 1 (selection of the named reductionists).
        names = ['J. J. C. Smart 1963', 'D. Lewis 1966', 'H. Putnam 1967', 'D. M. Armstrong 1968', 'D. C. Dennett 1969']
        fn_title = txt('Nagel 1974, Fn. 1 (Auswahl)', size=19, color=OCHRE)
        fn_names = VGroup(*[txt(n, size=21) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fn_body = VGroup(fn_title, fn_names).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fn_box = RoundedRectangle(corner_radius=0.08, width=fn_body.width + 0.5, height=fn_body.height + 0.4,
                                  fill_color=PANEL, fill_opacity=1, stroke_width=0)
        fn = VGroup(fn_box, fn_body.move_to(fn_box)).move_to([5.35, 0.6, 0])
        self.play(FadeIn(fn_box), FadeIn(fn_title), run_time=0.5)
        for key, row in zip(['Smart', 'Lewis', 'Putnam', None, 'Dennett'], fn_names):
            if key:
                self.wait_until(self.t('2.3', 0, key))
            self.play(FadeIn(row, shift=RIGHT * 0.08), run_time=0.3)

        # Sentence 2: the favourite analogies as pairs.
        rows = [('Wasser', 'H₂O', 'Wasser'), ('Blitz', 'elektrische Entladung', 'Blitz'), ('Gen', 'DNA', 'Gen')]
        lines = VGroup()
        for a, b, _ in rows + [('Bewusstsein', '?', None)]:
            la = txt(a, size=30)
            e = txt('=', size=30, color=OCHRE)
            lb = txt(b, size=30)
            lines.add(VGroup(la, e, lb))
        # align the equals signs in one column
        for row, y in zip(lines, [1.9, 1.05, 0.2, -0.95]):
            row[1].move_to([-2.4, y, 0])
            row[0].next_to(row[1], LEFT, buff=0.3)
            row[2].next_to(row[1], RIGHT, buff=0.3)
        ticks = VGroup(*[check(color=OCHRE, size=0.28).move_to([2.45, row.get_y(), 0]) for row in lines[:3]])
        for row, tick, (_, _, key) in zip(lines[:3], ticks, rows):
            self.wait_until(self.t('2.3', 1, key))
            self.play(FadeIn(row, shift=UP * 0.08), run_time=0.45)
            self.play(Create(tick), run_time=0.3)

        # Sentence 3: consciousness – the equals sign flickers and goes out.
        last = lines[3]
        last[0].set_color(VIOLET)
        last[2].set_color(MUTED)
        self.wait_until(self.t('2.3', 2, 'das Bewusstsein'))
        self.play(FadeIn(last[0]), FadeIn(last[1]), run_time=0.5)
        for op in (0.2, 1, 0.15, 0.8, 0.0):
            self.play(last[1].animate.set_opacity(op), run_time=0.13)
        self.play(FadeIn(last[2]), run_time=0.4)

        # Sentences 4–5: without consciousness interesting, with it hopeless.
        quote = QuoteCard(self.quote_of('2.3'), 'Nagel 1974, S. 436').move_to([0, -2.55, 0])
        self.play_at(self.t('2.3', 4), FadeIn(quote, shift=UP * 0.1), run_time=0.6)
