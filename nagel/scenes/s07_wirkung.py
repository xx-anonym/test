"""Kapitel 7 – Wirkungsgeschichte (Jackson 1982; Levine 1983; Chalmers 1995; Block 1995).

Oben wächst ein Netzwerk der Texte. Durchgezogene Kanten: der spätere Text bezieht
sich ausdrücklich auf Nagel (Jackson 1982, Fn. 10; Levine 1983, Fn. 3; Chalmers 1995).
Gestrichelt: Vorwegnahme ohne Einfluss (Farrell, Sprigge; Nagel 2024, Anm. 1) bzw. bloße
Verwendung der Formel (Block 1995, S. 227).

7.1  Marys schwarz-weißer Raum; die Tür geht auf, die Tomate wird rot.
7.2  Nagel: Grenze der Vorstellung – Jackson: Lücke in der Information.
7.3  Levine: „Wärme = Molekülbewegung“ ist lückenlos abgeleitet, bei „Schmerz =
     C-Faser-Feuern“ bleibt ein Spalt.
7.4  Chalmers: leichte Probleme vs. das harte Problem; Block: P- und A-Bewusstsein.
"""

from parts import *

NET_Y = 2.5
NODES = {   # id: (x, y, label, colour)
    'farrell': (-5.75, NET_Y, 'Farrell 1950', MUTED),
    'sprigge': (-3.75, NET_Y, 'Sprigge 1971', MUTED),
    'nagel': (-1.6, NET_Y, 'Nagel 1974', OCHRE),
    'jackson': (0.65, NET_Y, 'Jackson 1982', FG),
    'levine': (2.75, NET_Y, 'Levine 1983', FG),
    'chalmers': (5.0, NET_Y + 0.3, 'Chalmers 1995', FG),
    'block': (5.0, NET_Y - 0.3, 'Block 1995', FG),
}
TOMATO = '#e0533d'


def net_node(key):
    x, y, label, color = NODES[key]
    p = pill(label, color=PANEL, text_color=color, size=17)
    p[0].set_stroke(color, width=1.5)
    return p.move_to([x, y, 0])


def link(a, b, dashed=False, color=MUTED, below=False):
    """Arc from the later text a back to the earlier text b, bulging above the strip
    (or below it, for a node that sits under another one)."""
    if below:
        pa, pb = a.get_left() + LEFT * 0.02, b.get_bottom() + DOWN * 0.02
        angle = PI / 5 if pa[0] < pb[0] else -PI / 5
    else:
        pa, pb = a.get_top() + UP * 0.02, b.get_top() + UP * 0.02
        angle = PI / 4 if pa[0] > pb[0] else -PI / 4
    arc = ArcBetweenPoints(pa, pb, angle=angle, color=color, stroke_width=2.2)
    if dashed:
        arc = DashedVMobject(arc, num_dashes=24)
    return arc


class Kapitel7(NarratedScene):
    CHAPTER = 7

    def construct(self):
        self.chapter_card()
        self.nodes = {}
        self.p71()
        self.p72()
        self.p73()
        self.p74()
        self.finish()

    def add_node(self, key, to='nagel', dashed=False, run_time=0.6, below=False):
        n = net_node(key)
        self.nodes[key] = n
        anims = [FadeIn(n, scale=0.85)]
        if to:
            e = link(n, self.nodes[to], dashed=dashed, below=below)
            anims.append(Create(e))
            self.nodes[key + '_edge'] = e
        self.play(*anims, run_time=run_time)
        return n

    def below(self):
        keep = {self.tag, self.cite_mob}
        for v in self.nodes.values():
            keep |= set(v.get_family())
        return [m for m in self.mobjects if m not in keep]

    def wipe(self):
        gone = self.below()
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)

    # ------------------------------------------------------------ 7.1
    def p71(self):
        self.wait_until(self.t('7.1'))
        nagel = net_node('nagel')
        self.nodes['nagel'] = nagel
        self.play(FadeIn(nagel), run_time=0.5)
        self.add_node('farrell', dashed=True, run_time=0.5)
        self.add_node('sprigge', dashed=True, run_time=0.5)
        formula = txt('„wie es ist“ / „what it is like“', size=30, font=SERIF, slant=ITALIC, color=OCHRE)
        formula.move_to([0, 0.6, 0])
        self.play_at(self.t('7.1', 0, 'Standardformel'), FadeIn(formula, scale=1.1), run_time=0.7)

        # Sentence 2: Jackson 1982.
        self.wait_until(self.t('7.1', 1))
        self.cite(self.cite_of('7.1'))
        self.play(FadeOut(formula), run_time=0.4)
        self.add_node('jackson')

        # Sentences 3–4: Mary in the black-and-white room.
        self.wait_until(self.t('7.1', 2))
        room = Rectangle(width=7.4, height=4.0, stroke_color=MUTED, stroke_width=3, fill_color='#1f2226',
                         fill_opacity=1).move_to([-1.9, -0.75, 0])
        mary = person(height=1.4, color='#b8b8b8').move_to([-4.3, -1.6, 0])
        mon = RoundedRectangle(corner_radius=0.06, width=2.6, height=1.7, stroke_color='#9a9a9a', stroke_width=3,
                               fill_color='#2c2c2c', fill_opacity=1).move_to([-1.9, -0.55, 0])
        stand = Line(mon.get_bottom(), mon.get_bottom() + DOWN * 0.45, color='#9a9a9a', stroke_width=4)
        wave = FunctionGraph(lambda x: 0.18 * np.sin(9 * x), x_range=[-1.0, 1.0], color='#d0d0d0', stroke_width=2.5)
        wave.move_to(mon.get_center() + UP * 0.45)
        lam = txt('λ = 650 nm', size=16, color='#d0d0d0').next_to(wave, DOWN, buff=0.08)
        scan = net_pattern(cols=6, rows=2, lit=(2, 9), color='#e0e0e0', spacing=0.3).move_to(mon.get_center() + DOWN * 0.45)
        door = Rectangle(width=0.9, height=2.2, stroke_color='#9a9a9a', stroke_width=3, fill_color='#3a3a3a',
                         fill_opacity=1).move_to([1.4, -1.65, 0])
        self.play(FadeIn(room), FadeIn(mary), FadeIn(door), run_time=0.7)
        self.play_at(self.t('7.1', 2, 'Bildschirm'), FadeIn(mon), FadeIn(stand), Create(wave), FadeIn(lam),
                     FadeIn(scan), run_time=0.9)
        knows = txt('alles Physikalische über Farbensehen', size=20, color='#d0d0d0').next_to(room, UP, buff=0.12)
        knows.align_to(room, LEFT)
        self.play_at(self.t('7.1', 3), FadeIn(knows), run_time=0.6)

        # Sentence 5: does she learn something new when she sees colour?
        self.wait_until(self.t('7.1', 4))
        tomato = VGroup(Circle(radius=0.42, fill_color='#8a8a8a', fill_opacity=1, stroke_width=0),
                        Star(5, outer_radius=0.16, inner_radius=0.07, fill_color='#6a6a6a', fill_opacity=1,
                             stroke_width=0).shift(UP * 0.4)).move_to([3.6, -1.2, 0])
        self.play(door.animate.stretch(0.1, 0, about_edge=RIGHT), FadeIn(tomato), run_time=0.8)
        self.play(mary.animate.move_to([2.5, -1.6, 0]), run_time=1.0)
        self.play_at(self.t('7.1', 4, 'Farben'), tomato[0].animate.set_fill(TOMATO), tomato[1].animate.set_fill('#4f8a3d'),
                     run_time=0.8)
        new = txt('etwas Neues?', size=26, color=FG).next_to(tomato, UP, buff=0.35)
        self.play(FadeIn(new), run_time=0.4)

        # Sentence 6: if so, physical knowledge was incomplete – physicalism false (Jackson).
        self.wait_until(self.t('7.1', 5))
        chain = txt('wenn ja: physikalisches Wissen unvollständig → Physikalismus falsch (Jackson)', size=20,
                    color=FG).move_to([0.3, -3.05, 0])
        self.play(FadeIn(chain), run_time=0.6)
        self.wait_until(self.t('7.1', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 7.2
    def p72(self):
        self.wait_until(self.t('7.2'))
        self.cite(self.cite_of('7.2'))
        nb = VGroup(txt('Nagel', size=28, color=OCHRE, weight=SEMIBOLD),
                    txt('Grenze der Vorstellung', size=24),
                    txt('(Standpunkt)', size=20, color=MUTED)).arrange(DOWN, buff=0.15)
        jb = VGroup(txt('Jackson', size=28, color=FG, weight=SEMIBOLD),
                    txt('Lücke in der Information', size=24),
                    txt('(Eigenschaft)', size=20, color=MUTED)).arrange(DOWN, buff=0.15)
        boxes = []
        for g, x, c in ((nb, -3.0, OCHRE), (jb, 3.0, FG)):
            box = RoundedRectangle(corner_radius=0.1, width=4.6, height=2.2, stroke_color=c, stroke_width=2,
                                   fill_color=PANEL, fill_opacity=1).move_to([x, -0.3, 0])
            g.move_to(box)
            boxes.append(VGroup(box, g))
        debt = txt('„much indebted“ – und doch eine Abgrenzung', size=20, color=MUTED).move_to([0, 1.55, 0])
        self.play(FadeIn(debt), run_time=0.5)
        self.play_at(self.t('7.2', 0, 'Grenzen'), FadeIn(boxes[0], shift=RIGHT * 0.1), run_time=0.6)
        nothing = txt('dazu sagt der Physikalismus nichts', size=18, color=MUTED).next_to(boxes[0], DOWN, buff=0.2)
        self.play_at(self.t('7.2', 0, 'darüber'), FadeIn(nothing), run_time=0.5)

        self.wait_until(self.t('7.2', 1))
        self.play(FadeIn(boxes[1], shift=LEFT * 0.1), run_time=0.6)
        more = txt('behauptet mehr', size=18, color=MUTED).next_to(boxes[1], DOWN, buff=0.2)
        self.play_at(self.t('7.2', 1, 'Eigenschaft'), FadeIn(more), run_time=0.5)
        # the link in the network becomes dashed: related, but different
        old = self.nodes['jackson_edge']
        new = link(self.nodes['jackson'], self.nodes['nagel'], dashed=True)
        lab = txt('verwandt, aber verschieden', size=15, color=MUTED).next_to(new, UP, buff=0.05)
        self.play(ReplacementTransform(old, new), FadeIn(lab), run_time=0.7)
        self.nodes['jackson_edge'] = new
        self.nodes['jackson_lab'] = lab
        self.wait_until(self.t('7.2', 'end') + 0.1)
        self.wipe()
        self.play(FadeOut(lab), run_time=0.3)
        del self.nodes['jackson_lab']

    # ------------------------------------------------------------ 7.3
    def bridge(self, y, left, right, missing=0, n=7, x0=-3.4, x1=3.4):
        l = txt(left, size=26, color=VIOLET if missing else FG).move_to([x0 - 1.1, y, 0])
        r = txt(right, size=26, color=OCHRE).move_to([x1 + 1.6, y, 0])
        w = (x1 - x0) / n
        segs = VGroup(*[Rectangle(width=w - 0.06, height=0.32, stroke_width=0, fill_color=OCHRE, fill_opacity=0.85)
                        .move_to([x0 + w * (k + 0.5), y, 0]) for k in range(n)])
        return l, r, segs

    def p73(self):
        self.wait_until(self.t('7.3'))
        self.cite(self.cite_of('7.3'))
        self.add_node('levine')
        term = txt('die Erklärungslücke', size=34, font=SERIF, slant=ITALIC).move_to([0, 1.55, 0])
        self.play(FadeIn(term), run_time=0.6)

        # Sentence 2: heat = molecular motion – fully explanatory.
        self.wait_until(self.t('7.3', 1))
        l1, r1, s1 = self.bridge(0.35, 'Wärme', 'Molekülbewegung')
        self.play(FadeIn(l1), FadeIn(r1), run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(s, RIGHT) for s in reversed(s1)], lag_ratio=0.15), run_time=1.2)
        ok = txt('erklärt alles, was wir an Wärme erklären wollen', size=18, color=MUTED).next_to(s1, DOWN, buff=0.15)
        self.play(FadeIn(ok), run_time=0.4)

        # Sentence 3: pain = C-fibre firing – the causal role is derived, the feel is not.
        self.wait_until(self.t('7.3', 2))
        l2, r2, s2 = self.bridge(-1.55, 'Schmerz', 'C-Faser-Feuern', missing=2)
        self.play(FadeIn(l2), FadeIn(r2), run_time=0.4)
        built = s2[2:]
        self.play(LaggedStart(*[GrowFromEdge(s, RIGHT) for s in reversed(built)], lag_ratio=0.15), run_time=1.0)
        role = txt('was Schmerz bewirkt', size=18, color=MUTED).next_to(built, DOWN, buff=0.15)
        self.play_at(self.t('7.3', 2, 'bewirkt'), FadeIn(role), run_time=0.4)
        gap = DashedVMobject(Rectangle(width=s2[0].width * 2 + 0.06, height=0.32, stroke_color=VIOLET, stroke_width=2),
                             num_dashes=20).move_to(VGroup(s2[0], s2[1]))
        feel = txt('warum er sich so anfühlt?', size=18, color=VIOLET).next_to(gap, DOWN, buff=0.15)
        self.play_at(self.t('7.3', 2, 'warum'), Create(gap), FadeIn(feel), run_time=0.7)

        # Sentence 4: not materialism false, but understanding missing; Nagel as influence.
        self.wait_until(self.t('7.3', 3))
        verdict = txt('nicht: Materialismus falsch – sondern: uns fehlt ein Verstehen', size=21, color=FG)
        verdict.move_to([0, -2.85, 0])
        self.play(FadeIn(verdict), run_time=0.6)
        infl = txt('Einfluss: Nagel (Levine 1983, S. 361, Fn. 3)', size=15, color=MUTED)
        infl.next_to(self.nodes['levine_edge'], UP, buff=0.05)
        self.play_at(self.t('7.3', 3, 'Einfluss'), FadeIn(infl), Indicate(self.nodes['levine_edge'], color=OCHRE),
                     run_time=0.8)
        self.wait_until(self.t('7.3', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 7.4
    def p74(self):
        self.wait_until(self.t('7.4'))
        self.cite(self.cite_of('7.4', 0))
        self.add_node('chalmers')
        easy = VGroup(txt('„leichte“ Probleme', size=26, color=OCHRE, weight=SEMIBOLD),
                      *[txt('· ' + t, size=22) for t in ['Reize unterscheiden', 'Information integrieren',
                                                         'über eigene Zustände berichten']])
        easy.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.2, 0.2, 0])
        hard = VGroup(txt('das „harte“ Problem', size=26, color=VIOLET, weight=SEMIBOLD),
                      txt('die Erfahrung', size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.0, 0.5, 0])
        self.play(FadeIn(easy[0]), run_time=0.4)
        for row, key in zip(easy[1:], ['Reize', 'Information', 'berichten']):
            self.play_at(self.t('7.4', 0, key), FadeIn(row, shift=RIGHT * 0.1), run_time=0.35)
        self.play_at(self.t('7.4', 0, 'harten'), FadeIn(hard), run_time=0.6)

        # Sentence 2: Chalmers explicitly invokes Nagel's formula.
        self.wait_until(self.t('7.4', 1))
        q = QuoteCard('As Nagel (1974) has put it, there is something it is like to be a conscious organism.',
                      'Chalmers 1995', size=22, width=46).move_to([0, -2.35, 0])
        self.play(Indicate(self.nodes['chalmers_edge'], color=OCHRE), FadeIn(q, shift=UP * 0.1), run_time=0.8)

        # Sentence 3: Block – phenomenal vs. access consciousness.
        self.wait_until(self.t('7.4', 2))
        self.cite(self.cite_of('7.4', 1))
        self.play(*[FadeOut(m) for m in (easy, hard, q)], run_time=0.4)
        self.add_node('block', dashed=True, below=True)
        uses = txt('nutzt die Formel', size=14, color=MUTED).next_to(self.nodes['block'], DOWN, buff=0.08)
        self.play(FadeIn(uses), run_time=0.3)
        lower = RoundedRectangle(corner_radius=0.08, width=8.4, height=1.15, stroke_color=VIOLET, stroke_width=2,
                                 fill_color=INNER, fill_opacity=1).move_to([0, -1.6, 0])
        upper = RoundedRectangle(corner_radius=0.08, width=8.4, height=1.15, stroke_color=OCHRE, stroke_width=2,
                                 fill_color=PANEL, fill_opacity=1).move_to([0, 0.15, 0])
        lt = txt('P – phänomenal: wie es ist, in einem Zustand zu sein', size=22, color=VIOLET).move_to(lower)
        ut = txt('A – Zugang: verfügbar für Denken, Sprechen, Handeln', size=22, color=OCHRE).move_to(upper)
        self.play_at(self.t('7.4', 2, 'phänomenale'), FadeIn(lower), FadeIn(lt), run_time=0.6)
        self.play_at(self.t('7.4', 2, 'Zugangsbewusstsein'), FadeIn(upper), FadeIn(ut), run_time=0.6)
