"""Kapitel 11 – Tiere und Maschinen heute (Cambridge Declaration 2012; New York Declaration 2024;
Nagel 1974, S. 436 mit Fn. 2, S. 439; Butlin et al. 2023; Chalmers 2023; Long et al. 2024).

Kennzeichnung durch das ganze Kapitel: grün „gesichert“, ocker „offen“.

11.1  Die Cambridger Erklärung als Karte: behauptet werden die Grundlagen („substrates“).
11.2  New York 2024: drei Zonen – starke Unterstützung, realistische Möglichkeit, offen.
11.3  Zwei Schalter: „ob“ und „wie“.
11.4  Butlin et al. 2023: Theorien → Indikatoren → System; Arbeitshypothese (umstritten).
11.5  Skala unwahrscheinlich – möglich: heutige Sprachmodelle, Nachfolger.
11.6  Der Roboter aus 3.3: Verhalten links, das Fragezeichen rechts bleibt.
"""

from parts import *


def bird(color=FG, width=1.0):
    body = Ellipse(width=0.9, height=0.42, fill_color=color, fill_opacity=1, stroke_width=0)
    head = Circle(radius=0.16, fill_color=color, fill_opacity=1, stroke_width=0).move_to([0.45, 0.16, 0])
    beak = Polygon([0.58, 0.18, 0], [0.78, 0.14, 0], [0.58, 0.1, 0], fill_color=color, fill_opacity=1, stroke_width=0)
    wing = Polygon([-0.1, 0.1, 0], [-0.45, 0.45, 0], [0.15, 0.12, 0], fill_color=color, fill_opacity=1, stroke_width=0)
    tail = Polygon([-0.42, 0.0, 0], [-0.75, 0.12, 0], [-0.7, -0.08, 0], fill_color=color, fill_opacity=1, stroke_width=0)
    return VGroup(body, head, beak, wing, tail).scale_to_fit_width(width)


def octopus(color=FG, width=1.0):
    head = Ellipse(width=0.6, height=0.7, fill_color=color, fill_opacity=1, stroke_width=0).shift(UP * 0.3)
    arms = VGroup()
    for k in range(6):
        x = -0.27 + 0.108 * k
        arm = VMobject(stroke_color=color, stroke_width=5)
        arm.set_points_smoothly([[x, 0.0, 0], [x * 1.4, -0.25, 0], [x * 1.9 + 0.06 * (-1) ** k, -0.5, 0]])
        arms.add(arm)
    return VGroup(head, arms).scale_to_fit_width(width)


def mouse(color=FG, width=1.0):
    body = Ellipse(width=0.8, height=0.42, fill_color=color, fill_opacity=1, stroke_width=0)
    head = Circle(radius=0.17, fill_color=color, fill_opacity=1, stroke_width=0).move_to([0.42, 0.06, 0])
    ear_ = Circle(radius=0.1, fill_color=color, fill_opacity=1, stroke_width=0).move_to([0.38, 0.24, 0])
    tail = VMobject(stroke_color=color, stroke_width=3).set_points_smoothly([[-0.4, 0, 0], [-0.6, 0.1, 0], [-0.75, -0.05, 0]])
    return VGroup(body, head, ear_, tail).scale_to_fit_width(width)


def fish(color=FG, width=1.0):
    body = Ellipse(width=0.8, height=0.36, fill_color=color, fill_opacity=1, stroke_width=0)
    tail = Polygon([-0.38, 0, 0], [-0.62, 0.18, 0], [-0.62, -0.18, 0], fill_color=color, fill_opacity=1, stroke_width=0)
    return VGroup(body, tail).scale_to_fit_width(width)


def status(text, settled):
    return pill(text, color=GREEN if settled else OCHRE, text_color=BG, size=16)


def switch(label, on, color=GREEN):
    track = RoundedRectangle(corner_radius=0.22, width=1.0, height=0.44, fill_color=color if on else DIM,
                             fill_opacity=1, stroke_width=0)
    knob = Circle(radius=0.17, fill_color=FG, fill_opacity=1, stroke_width=0)
    knob.move_to(track.get_right() + LEFT * 0.25 if on else track.get_left() + RIGHT * 0.25)
    lab = txt(label, size=26).next_to(track, LEFT, buff=0.35)
    return VGroup(lab, track, knob)


class Kapitel11(NarratedScene):
    CHAPTER = 11

    def construct(self):
        self.chapter_card()
        self.p111()
        self.p112()
        self.p113()
        self.p114()
        self.p115()
        self.p116()
        self.finish()

    def wipe(self):
        gone = [m for m in self.mobjects if m not in (self.tag, self.cite_mob)]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)

    # ------------------------------------------------------------ 11.1
    def p111(self):
        self.wait_until(self.t('11.1'))
        self.cite(self.cite_of('11.1'))
        quote = ('Non-human animals, including all mammals and birds, and many other creatures,\n'
                 'including octopuses, also possess these neurological substrates.')
        card = QuoteCard(quote.replace('\n', ' '), 'Cambridge Declaration on Consciousness, 7. Juli 2012', size=24,
                         width=62).move_to([0, 1.3, 0])
        self.play_at(self.t('11.1', 1), FadeIn(card, shift=UP * 0.1), run_time=0.7)
        icons = VGroup(mouse(width=1.0), bird(width=1.0), octopus(width=0.8)).arrange(RIGHT, buff=1.2).move_to([0, -0.7, 0])
        names = VGroup(*[txt(n, size=18, color=MUTED).next_to(i, DOWN, buff=0.2)
                         for n, i in zip(['Säugetiere', 'Vögel', 'z. B. Kraken'], icons)])
        for i, nme, key in zip(icons, names, ['Säugetiere', 'Vögel', 'Kraken']):
            self.play_at(self.t('11.1', 1, key), FadeIn(i, shift=UP * 0.1), FadeIn(nme), run_time=0.45)

        # Sentence 3: note the wording – the substrates, not a particular experience.
        self.wait_until(self.t('11.1', 2))
        sub = txt('behauptet: die Grundlagen („neurological substrates“)', size=22, color=GREEN).move_to([0, -2.25, 0])
        nots = txt('nicht behauptet: ein bestimmtes Erleben', size=22, color=MUTED).next_to(sub, DOWN, buff=0.15)
        self.play(FadeIn(sub), run_time=0.5)
        self.play_at(self.t('11.1', 2, 'nicht ein'), FadeIn(nots), run_time=0.5)
        self.wait_until(self.t('11.1', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 11.2
    def p112(self):
        self.wait_until(self.t('11.2'))
        self.cite(self.cite_of('11.2'))
        c = np.array([-2.2, -0.35, 0])
        zones = VGroup(
            Circle(radius=3.0, stroke_color=DIM, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to(c),
            Circle(radius=2.05, stroke_color=OCHRE, stroke_width=2, fill_color='#2a2418', fill_opacity=1).move_to(c),
            Circle(radius=1.05, stroke_color=GREEN, stroke_width=2, fill_color='#1c2a22', fill_opacity=1).move_to(c),
        )
        self.play(FadeIn(zones[0]), run_time=0.4)

        # Sentence 3: strong support for mammals and birds.
        self.wait_until(self.t('11.2', 2))
        inner = VGroup(mouse(width=0.6), bird(width=0.6)).arrange(RIGHT, buff=0.25).move_to(c + UP * 0.15)
        il = txt('starke Unterstützung', size=17, color=GREEN).move_to(c + DOWN * 0.5)
        self.play(FadeIn(zones[2]), FadeIn(inner), FadeIn(il), run_time=0.7)

        # Sentence 4: realistic possibility – all vertebrates, many invertebrates.
        self.wait_until(self.t('11.2', 3))
        ring2 = VGroup(fish(width=0.55).move_to(c + np.array([-1.45, 0.6, 0])),
                       octopus(width=0.45).move_to(c + np.array([1.5, 0.55, 0])),
                       insect(size=0.45).move_to(c + np.array([1.35, -0.95, 0])))
        ml = txt('realistische Möglichkeit', size=17, color=OCHRE).move_to(c + DOWN * 1.55)
        self.play(FadeIn(zones[1]), zones[2].animate.set_z_index(1), inner.animate.set_z_index(2),
                  il.animate.set_z_index(2), run_time=0.6)
        self.play(FadeIn(ring2), FadeIn(ml), run_time=0.6)
        ol = txt('offen', size=17, color=MUTED).move_to(c + DOWN * 2.55)
        self.play(FadeIn(ol), run_time=0.3)
        lst = VGroup(txt('alle Wirbeltiere', size=19), txt('mindestens: Kopffüßer,', size=19),
                     txt('Zehnfußkrebse, Insekten', size=19)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lst.move_to([3.6, 0.9, 0])
        lt = txt('realistische Möglichkeit', size=20, color=OCHRE).next_to(lst, UP, buff=0.2).align_to(lst, LEFT)
        self.play_at(self.t('11.2', 3, 'Wirbellose'), FadeIn(lt), FadeIn(lst), run_time=0.6)

        # Sentence 5: then it is irresponsible to ignore it in decisions.
        self.wait_until(self.t('11.2', 4))
        sign = VGroup(RoundedRectangle(corner_radius=0.1, width=4.6, height=1.0, stroke_color=FG, stroke_width=2,
                                       fill_color=PANEL, fill_opacity=1),
                      txt('Folgerung: bei Entscheidungen\nnicht übergehen', size=20))
        sign[1].move_to(sign[0])
        sign.move_to([3.6, -1.6, 0])
        self.play(FadeIn(sign, shift=UP * 0.1), run_time=0.6)
        self.wait_until(self.t('11.2', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 11.3
    def p113(self):
        self.wait_until(self.t('11.3'))
        self.cite(self.cite_of('11.3'))
        s1 = switch('ob', True)
        s2 = switch('wie', False)
        grp = VGroup(s1, s2).arrange(DOWN, buff=0.7, aligned_edge=RIGHT).move_to([-1.2, 0.3, 0])
        t1 = txt('vernünftig, mit Erleben zu rechnen', size=20, color=GREEN).next_to(s1, RIGHT, buff=0.5)
        t2 = txt('wie es für eine Biene ist: offen', size=20, color=MUTED).next_to(s2, RIGHT, buff=0.5)
        self.play(FadeIn(s2), FadeIn(t2), run_time=0.6)
        self.play_at(self.t('11.3', 0, 'vernünftig'), FadeIn(s1), FadeIn(t1), run_time=0.6)
        note = txt('dieselbe Trennung wie bei Nagel: schematisch vs. spezifisch', size=19, color=MUTED)
        note.move_to([0, -2.0, 0])
        self.play_at(self.t('11.3', 0, 'Trennung'), FadeIn(note), run_time=0.5)
        self.wait_until(self.t('11.3', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 11.4
    def p114(self):
        self.wait_until(self.t('11.4'))
        self.cite(self.cite_of('11.4'))
        open_ = status('offen', False).move_to([5.6, 2.95, 0])
        self.play_at(self.t('11.4', 1), FadeIn(open_), run_time=0.4)

        # Sentence 3: the report – theories → indicators → current systems.
        self.wait_until(self.t('11.4', 2))
        theories = ['rekurrente Verarbeitung', 'globaler Arbeitsbereich', 'höherstufige Theorien',
                    'prädiktive Verarbeitung', 'Aufmerksamkeitsschema']
        col = VGroup(*[pill(t, color=PANEL, text_color=FG, size=17) for t in theories]).arrange(DOWN, buff=0.14,
                                                                                               aligned_edge=LEFT)
        col.move_to([-3.6, 0.0, 0])
        ct = txt('Theorien des Bewusstseins', size=19, color=MUTED).next_to(col, UP, buff=0.25)
        ind = VGroup(*[VGroup(Square(0.22, stroke_color=OCHRE, stroke_width=2), txt(f'Indikator {k + 1}', size=16))
                       .arrange(RIGHT, buff=0.15) for k in range(5)]).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        ind.move_to([0.6, 0.0, 0])
        it = txt('„Indikator-Eigenschaften“', size=19, color=OCHRE).next_to(ind, UP, buff=0.25)
        arrows = VGroup(*[Arrow(p.get_right(), i.get_left(), buff=0.12, color=DIM, stroke_width=2.5) for p, i in zip(col, ind)])
        sys_ = chip(size=1.6).move_to([4.4, 0.0, 0])
        sl = txt('KI-System 2023', size=18, color=MUTED).next_to(sys_, DOWN, buff=0.2)
        self.play(FadeIn(ct), LaggedStart(*[FadeIn(p) for p in col], lag_ratio=0.15), run_time=1.0)
        self.play(FadeIn(it), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(ind), run_time=1.0)
        self.play(FadeIn(sys_), FadeIn(sl), run_time=0.5)
        verdict = txt('kein damaliges System bewusst –\nkeine offensichtlichen technischen Hürden', size=18)
        verdict.next_to(sys_, UP, buff=0.3)
        self.play_at(self.t('11.4', 2, 'kein damaliges'), FadeIn(verdict), run_time=0.6)

        # Sentence 4: working hypothesis – computation suffices (disputed).
        self.wait_until(self.t('11.4', 3))
        hyp = VGroup(txt('Arbeitshypothese: die richtige Art von Berechnung genügt', size=20),
                     txt('(laut Autoren verbreitet, aber umstritten)', size=17, color=MUTED)).arrange(DOWN, buff=0.08)
        hyp.move_to([0.4, -2.55, 0])
        self.play(FadeIn(hyp, shift=UP * 0.1), run_time=0.6)

        # Sentence 5: consciousness defined with Nagel's formula.
        self.wait_until(self.t('11.4', 4))
        f = txt('Definition: „something it is like“ – nach Nagel', size=18, color=VIOLET).move_to([0.4, 2.95, 0])
        self.play(FadeIn(f), run_time=0.5)
        self.wait_until(self.t('11.4', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 11.5
    def p115(self):
        self.wait_until(self.t('11.5'))
        self.cite(self.cite_of('11.5'))
        y = 0.4
        bar = Line([-5.0, y, 0], [5.0, y, 0], color=MUTED, stroke_width=6)
        l0 = txt('unwahrscheinlich', size=20, color=MUTED).next_to(bar, DOWN, buff=0.25).align_to(bar, LEFT)
        l1 = txt('ernsthaft möglich', size=20, color=MUTED).next_to(bar, DOWN, buff=0.25).align_to(bar, RIGHT)
        self.play(Create(bar), FadeIn(l0), FadeIn(l1), run_time=0.7)

        def marker(x, text):
            tri = Triangle(fill_color=OCHRE, fill_opacity=1, stroke_width=0).scale(0.14).rotate(PI).move_to([x, y + 0.25, 0])
            lab = txt(text, size=19, color=FG).next_to(tri, UP, buff=0.12)
            return VGroup(tri, lab)
        m1 = marker(-2.7, 'heutige große Sprachmodelle')
        m2 = marker(2.7, 'ihre Nachfolger')
        self.play_at(self.t('11.5', 0, 'heutige'), FadeIn(m1, shift=DOWN * 0.1), run_time=0.5)
        self.play_at(self.t('11.5', 0, 'Nachfolger'), FadeIn(m2, shift=DOWN * 0.1), run_time=0.5)
        who = txt('Einschätzung von David Chalmers, 2023', size=17, color=MUTED).move_to([0, 2.0, 0])
        self.play(FadeIn(who), run_time=0.3)

        # Sentence 2: some call for procedures now (Long et al. 2024).
        self.wait_until(self.t('11.5', 1))
        prep = txt('Forderung: Verfahren vorbereiten, falls KI-Systeme moralisch zählen (Long et al. 2024)', size=19)
        prep.move_to([0, -1.5, 0])
        deb = status('offene Debatte', False).next_to(prep, DOWN, buff=0.35)
        self.play(FadeIn(prep), run_time=0.5)
        self.play(FadeIn(deb), run_time=0.4)
        self.wait_until(self.t('11.5', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 11.6
    def p116(self):
        self.wait_until(self.t('11.6'))
        self.cite(self.cite_of('11.6'))
        outer, inner = two_fields(left_label='von außen: Sprache, Verhalten', right_label='für das System selbst',
                                  height=3.6, y=-0.1)
        r = robot(height=1.0).move_to(outer.box.get_corner(UL) + [0.8, -0.75, 0])
        self.play(FadeIn(outer), FadeIn(inner), FadeIn(r), run_time=0.7)

        # Sentences 2–3: the tool – behaviour does not settle experience.
        self.wait_until(self.t('11.6', 1))
        lines = VGroup(*[RoundedRectangle(corner_radius=0.12, width=w, height=0.36, fill_color=PANEL, fill_opacity=1,
                                          stroke_color=OCHRE, stroke_width=1.5) for w in (3.6, 2.8, 3.3, 2.4)])
        lines.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(outer.box.get_center() + RIGHT * 0.6 + DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in lines], lag_ratio=0.25), run_time=1.2)
        qm = txt('?', size=72, color=VIOLET).move_to(inner.box)
        self.play_at(self.t('11.6', 2, 'irgendwie'), FadeIn(qm, scale=1.2), run_time=0.6)
        g = status('gesichert: Verhalten legt Erleben logisch nicht fest', True).next_to(outer.box, DOWN, buff=0.3)
        g.align_to(outer.box, LEFT)
        self.play(FadeIn(g), run_time=0.5)

        # Sentences 4–6: the warning – footnote 2; the question is open.
        self.wait_until(self.t('11.6', 3))
        fn = txt('Fn. 2: Vielleicht hat alles, was komplex genug ist,\nsich wie ein Mensch zu verhalten, Erfahrungen.',
                 size=19, color=FG).move_to([0, 2.65, 0])
        self.play(FadeIn(fn), run_time=0.6)
        self.wait_until(self.t('11.6', 5))
        o = status('offen: ob solche Systeme erleben', False).next_to(inner.box, DOWN, buff=0.3).align_to(inner.box, RIGHT)
        self.play(FadeIn(o), Indicate(qm, color=OCHRE), run_time=0.6)
