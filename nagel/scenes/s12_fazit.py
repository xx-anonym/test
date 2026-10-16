"""Kapitel 12 – Fazit (Chalmers 1995; Block 1995; Butlin et al. 2023; Nagel 1974, S. 444–445, 449;
Nagel 2024, Vorwort; Einwände nach research/argument.md).

12.1  Der vollständige Argumentbaum; D1 (die Bestimmung) und Z4 (die Diagnose) leuchten auf.
12.2  Alle Einwände gleichzeitig als rote Pfeile – keiner trennt den Baum vollständig.
12.3  Was offen ist; zurück in die Abendszene des Prologs: links alles Gemessene, rechts dunkel.
"""

from parts import *
from s00_prolog import Calls

TS = 0.82                       # tree scale
TY = -0.6                       # tree vertical offset


class Kapitel12(NarratedScene):
    CHAPTER = 12

    def construct(self):
        self.chapter_card()
        self.p121()
        self.p122()
        self.p123()
        self.finish()

    def wipe(self):
        gone = [m for m in self.mobjects if m not in (self.tag, self.cite_mob)]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=0.6)

    # ------------------------------------------------------------ 12.1
    def p121(self):
        self.wait_until(self.t('12.1'))
        tree = ArgTree(mini=False)
        tree.scale(TS).shift(UP * TY)
        self.tree = tree
        self.play(*[FadeIn(n) for n in tree.nodes.values()], *[FadeIn(e) for e in tree.edges.values()], run_time=1.0)

        # Sentence 2: the definition has prevailed.
        self.wait_until(self.t('12.1', 1))
        self.cite(self.cite_of('12.1'))
        d1 = tree.nodes['D1']
        ring1 = SurroundingRectangle(d1, color=VIOLET, buff=0.06, corner_radius=0.08, stroke_width=4)
        lab1 = txt('1  die Bestimmung', size=22, color=VIOLET, weight=SEMIBOLD).move_to([-3.2, 2.95, 0])
        self.play(Create(ring1), FadeIn(lab1), run_time=0.7)

        # Sentence 3: Chalmers, Block, the 2023 AI report start from it.
        self.wait_until(self.t('12.1', 2))
        users = VGroup(*[pill(t, color=PANEL, text_color=FG, size=16) for t in
                         ('Chalmers 1995', 'Block 1995', 'Butlin et al. 2023')]).arrange(RIGHT, buff=0.2)
        users.move_to([1.6, 2.95, 0])
        links = VGroup(*[Arrow(u.get_bottom(), d1.get_right() + UP * 0.05, buff=0.08, color=DIM, stroke_width=2,
                               max_tip_length_to_length_ratio=0.06) for u in users])
        self.play(LaggedStart(*[FadeIn(u) for u in users], lag_ratio=0.2), Create(links), run_time=1.0)

        # Sentence 4: the diagnosis – Z4.
        self.wait_until(self.t('12.1', 3))
        self.play(FadeOut(users), FadeOut(links), run_time=0.4)
        z4 = tree.nodes['Z4']
        ring2 = SurroundingRectangle(z4, color=OCHRE, buff=0.06, corner_radius=0.08, stroke_width=4)
        lab2 = txt('2  die Diagnose', size=22, color=OCHRE, weight=SEMIBOLD).move_to([3.0, 2.95, 0])
        self.play(Create(ring2), FadeIn(lab2), run_time=0.7)
        self.rings = VGroup(ring1, ring2, lab1, lab2)

    # ------------------------------------------------------------ 12.2
    def p122(self):
        self.wait_until(self.t('12.2'))
        self.cite(self.cite_of('12.2'))
        self.play(FadeOut(self.rings), run_time=0.4)
        n = self.tree.nodes

        def hit(nid, name, direction, length=0.55, side=None):
            node = n[nid]
            tip = node.get_edge_center(direction)
            start = tip + direction * length
            arr = Arrow(start, tip, buff=0.02, color=RED, stroke_width=5, max_tip_length_to_length_ratio=0.35)
            lab = txt(name, size=15, color=RED, weight=SEMIBOLD)
            lab.next_to(start, side if side is not None else direction, buff=0.06)
            return VGroup(arr, lab)
        hits = VGroup(
            hit('D1', 'Hacker · Frankish', UP),
            hit('D2', 'Hacker', LEFT, length=0.45, side=UP),
            hit('P2', 'Akins', LEFT, length=0.45, side=UP),
            hit('Z2', 'Dennett', DOWN, length=0.45, side=RIGHT),
            hit('P5', 'Lewis/Nemirow', DOWN, length=0.6),
            hit('Z3', 'Akins · Lewis/Nemirow', UP, length=0.45),
        )
        keys = ['Annahme', 'Tatsachen', 'Grammatik', 'Wirklichkeit']
        order = [[2, 5], [4], [0, 1], [0]]
        shown = set()
        for key, idx in zip(keys, order):
            new = [hits[i] for i in idx if i not in shown]
            shown |= set(idx)
            if new:
                self.play_at(self.t('12.2', 0, key), *[GrowArrow(h[0]) for h in new], *[FadeIn(h[1]) for h in new],
                             run_time=0.6)
            else:
                self.play_at(self.t('12.2', 0, key), Indicate(hits[idx[0]], color=RED), run_time=0.6)
        self.play(FadeIn(hits[3]), GrowArrow(hits[3][0]), run_time=0.5)

        # Sentence 2: none of them ended the debate – the tree still stands.
        self.wait_until(self.t('12.2', 1))
        stands = txt('Der Baum steht noch – angegriffen, nicht gefällt.', size=22, color=FG).move_to([0, 3.0, 0])
        self.play(FadeIn(stands), *[Indicate(e, color=FG, scale_factor=1.0) for e in self.tree.edges.values()],
                  run_time=1.0)

        # Sentence 3: no agreement after fifty years.
        self.wait_until(self.t('12.2', 2))
        agree = txt('Nagel 2024: bis heute keine Einigkeit, wie mit diesen Problemen umzugehen ist', size=19,
                    color=MUTED).move_to([0, -3.1, 0])
        agree.shift(LEFT * 0.9)
        self.play(FadeIn(agree), run_time=0.6)
        self.wait_until(self.t('12.2', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 12.3
    def p123(self):
        self.wait_until(self.t('12.3'))
        self.cite(self.cite_of('12.3'))
        notc = txt('nicht: „Die Wissenschaft kann Bewusstsein nicht verstehen.“', size=24, color=MUTED).move_to([0, 2.4, 0])
        strike = Line(notc.get_left() + LEFT * 0.05, notc.get_right() + RIGHT * 0.05, color=FG, stroke_width=3)
        self.play(FadeIn(notc), run_time=0.5)
        self.play_at(self.t('12.3', 0, 'nicht verstehen'), Create(strike), run_time=0.5)

        # Sentence 2: our idea of scientific understanding must widen.
        self.wait_until(self.t('12.3', 1))
        circ = Circle(radius=1.3, stroke_color=OCHRE, stroke_width=3).move_to([0, -0.2, 0])
        cl = txt('wissenschaftliches\nVerstehen', size=22, color=OCHRE).move_to(circ)
        self.play(Create(circ), FadeIn(cl), run_time=0.7)
        self.play_at(self.t('12.3', 1, 'erweitern'), circ.animate.scale(1.6), run_time=1.4, rate_func=smooth)

        # Sentence 3: how – open.
        self.wait_until(self.t('12.3', 2))
        ways = VGroup(*[pill(t, color=PANEL, text_color=FG, size=18) for t in
                        ('neue Begriffe', 'objektive Phänomenologie', 'Nachweis einer Illusion')]).arrange(RIGHT, buff=0.3)
        ways.move_to([0, -2.55, 0])
        for w, key in zip(ways, ['Begriffe', 'Phänomenologie', 'Illusion']):
            self.play_at(self.t('12.3', 2, key), FadeIn(w, shift=UP * 0.1), run_time=0.4)
        op = pill('offen', color=OCHRE, text_color=BG, size=18).next_to(ways, RIGHT, buff=0.35)
        self.play(FadeIn(op), run_time=0.4)

        # Sentence 4: the bat flies on through the dusk.
        self.wait_until(self.t('12.3', 3) - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.tag, self.cite_mob)], run_time=0.5)
        land = dusk(seed=4)
        path = VMobject().set_points_smoothly([[-6.5, 0.4, 0], [-3.5, 1.5, 0], [-0.5, 0.9, 0], [2.5, 1.7, 0],
                                              [5.0, 1.0, 0], [7.2, 1.6, 0]])
        tr = ValueTracker(0.0)
        flyer = Flyer(path, tr, width=0.8)
        self.play(FadeIn(land), FadeIn(flyer), run_time=0.8)
        calls = Calls(flyer, None)
        self.add(calls)
        dur = max(2.0, self.t('12.3', 5) - 0.9 - self.now)
        self.play(tr.animate.set_value(0.55), run_time=dur, rate_func=linear)

        # Sentences 5–6: left everything measured, right dark.
        calls.active = False
        calls.clear_updaters()
        flyer.clear_updaters()
        outer, inner = two_fields(height=3.8, y=-0.1)
        items = VGroup(txt('Rufe, Echos, Laufzeiten', size=20), txt('Doppler-Kompensation', size=20),
                       txt('Karten im Hörkortex', size=20), txt('Verhalten, Reichweite', size=20)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).move_to(outer.box)
        self.play(FadeOut(VGroup(land, calls, flyer)), FadeIn(outer), FadeIn(items), run_time=0.8)
        self.play_at(self.t('12.3', 5), FadeIn(inner), run_time=0.9)
