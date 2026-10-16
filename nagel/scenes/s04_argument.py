"""Kapitel 4 – Das Argument Schritt für Schritt (Nagel 1974, S. 439–445).

Links oben wächst der Argumentbaum aus research/argument.md (Kennung, Kurzform,
Seite der Erstveröffentlichung). Rechts das Bild zum jeweiligen Schritt:

4.1  Vorstellung aus eigener Erfahrung: ein Mensch mit „Aufklebern“ bleibt ein Mensch (P3, P4).
4.2  Hinzufügen, Abziehen, Abwandeln bleiben im Kreis menschlicher Erfahrung; der
     Fledermaus bleiben nur Etiketten ohne Füllung (Z2).
4.3  Spiegelung: Für die Fledermaus ist unser Innenfeld dunkel – wir wissen, dass es
     nicht leer ist (P5).
4.4  Standpunkte als Blickkegel: Typen, die sich mehr oder weniger überlappen (Z3).
4.5  Der Blitz: gesehen vs. elektrische Entladung; der augenlose Marsianer (P6).
4.6  Objektivität als Richtung: Darstellung wandert, die Sache bleibt dieselbe; das
     Hören bleibt unreduziert zurück (P7).
4.7  Bei der Erfahrung bleibt die Sache am Standpunkt: Der Abstand wächst (P8, Z4).
4.8  Die Pointe; der ganze Baum bis Z5.
"""

from parts import *

MX = 2.35          # centre of the picture area right of the mini tree


class Kapitel4(NarratedScene):
    CHAPTER = 4

    def construct(self):
        self.chapter_card()
        self.tree = ArgTree(mini=True)
        self.shown = set()
        self.cap = None
        self.p41()
        self.p42()
        self.p43()
        self.p44()
        self.p45()
        self.p46()
        self.p47()
        self.p48()
        self.finish()

    # ------------------------------------------------------------ helpers
    def node(self, *ids, flash=True):
        reveal(self, self.tree, ids, self.shown, run_time=0.7, flash=flash)
        cap = VGroup(*[self.tree.caption(n, size=17) for n in ids]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        if cap.width > 4.3:
            cap.scale_to_fit_width(4.3)
        cap.move_to([-6.75, 0.35, 0], aligned_edge=UL)
        if self.cap is None:
            self.play(FadeIn(cap), run_time=0.4)
        else:
            self.play(FadeOut(self.cap), FadeIn(cap), run_time=0.4)
        self.cap = cap

    def clear(self, keep=()):
        """Fade the picture area, keep tree, caption, tag and source line."""
        fixed = {self.tag, self.cite_mob, self.cap, self.tree, *self.tree.nodes.values(), *self.tree.edges.values()}
        for k in keep:
            fixed |= set(k.get_family())
        gone = [m for m in self.mobjects if m not in fixed]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)

    def quote(self, pid, source, y=-2.75, x=MX, size=24, width=52):
        q = QuoteCard(self.quote_of(pid), source, size=size, width=width).move_to([x, y, 0])
        if q.width > 8.6:
            q.scale_to_fit_width(8.6)
        if q.get_bottom()[1] < -3.25:           # keep clear of the source line
            q.shift(UP * (-3.25 - q.get_bottom()[1]))
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        return q

    # ------------------------------------------------------------ 4.1
    def p41(self):
        # The nodes established in chapters 1–3 are already there.
        so_far = txt('bisher (Kap. 1–3)', size=15, color=MUTED).next_to(self.tree.nodes['P2'], DOWN, buff=0.75)
        so_far.align_to(self.tree.nodes['P2'], LEFT)
        self.add(so_far.set_opacity(0))
        reveal(self, self.tree, ['D1', 'D2', 'P1', 'Z1', 'P2'], self.shown, run_time=0.3, flash=False)
        so_far.set_opacity(1)
        self.wait_until(self.t('4.1'))
        self.cite(self.cite_of('4.1'))
        self.play(FadeOut(so_far), run_time=0.3)
        self.node('P3')

        # Sentence 2: imagination works with our own experience.
        self.wait_until(self.t('4.1', 1))
        self.node('P4')
        me = person(height=1.9).move_to([MX, 0.55, 0])
        self.play(FadeIn(me), run_time=0.5)
        q = self.quote('4.1', 'Nagel 1974, S. 439')

        # Sentence 3: stickers – webbing, insects, upside down. Still a human.
        wings = bat(width=4.0, color='#4a5266').move_to(me.get_center() + UP * 0.05)
        me.set_z_index(2)
        self.play_at(self.t('4.1', 2, 'Flughäute'), FadeIn(wings), run_time=0.6)
        tags = VGroup()
        t1 = pill('Flughäute', color=PANEL, text_color=FG, size=18).next_to(wings, LEFT, buff=0.15)
        moth = insect(size=0.35).next_to(me, UP, buff=0.1).shift(RIGHT * 0.45)
        t2 = pill('Insekten fangen', color=PANEL, text_color=FG, size=18).next_to(moth, RIGHT, buff=0.2)
        self.play(FadeIn(t1, scale=0.8), run_time=0.4)
        self.play_at(self.t('4.1', 2, 'Insekten'), FadeIn(moth), FadeIn(t2, scale=0.8), run_time=0.5)
        fig = VGroup(wings, me, moth)
        t3 = pill('kopfüber', color=PANEL, text_color=FG, size=18)
        beam = Line([MX - 1.6, 1.95, 0], [MX + 1.6, 1.95, 0], color=MUTED, stroke_width=4)
        self.play_at(self.t('4.1', 2, 'kopfüber'), FadeOut(moth), FadeOut(t2),
                     Rotate(VGroup(wings, me), PI, about_point=me.get_center()), run_time=1.0)
        self.play(VGroup(wings, me).animate.next_to(beam, DOWN, buff=0.02), Create(beam), run_time=0.6)
        t3.next_to(VGroup(wings, me), RIGHT, buff=0.3)
        t1.generate_target().next_to(VGroup(wings, me), LEFT, buff=0.3)
        self.play(FadeIn(t3, scale=0.8), MoveToTarget(t1), run_time=0.4)
        self.fig = VGroup(wings, me, beam)
        self.tags = VGroup(t1, t3)
        self.q = q

    # ------------------------------------------------------------ 4.2
    def p42(self):
        self.wait_until(self.t('4.2'))
        me = self.fig[1]
        still = txt('… immer noch ich', size=22, color=MUTED).next_to(self.fig, DOWN, buff=0.25)
        self.play(FadeIn(still), run_time=0.5)
        self.play_at(self.t('4.2', 0, 'für mich'), Indicate(me, color=OCHRE), run_time=0.8)
        self.play(FadeOut(self.q), run_time=0.3)
        self.q = self.quote('4.2', 'Nagel 1974, S. 439')

        # Sentence 3: the real question.
        self.wait_until(self.t('4.2', 2) - 0.4)
        self.play(FadeOut(VGroup(self.fig, self.tags, still, self.q)), run_time=0.4)
        left_c = Circle(radius=1.75, stroke_color=FG, stroke_width=2.5).move_to([0.75, 0.55, 0])
        left_l = txt('menschliche Erfahrung', size=20, color=MUTED).next_to(left_c, DOWN, buff=0.12)
        right_c = Circle(radius=1.35, stroke_color=VIOLET, stroke_width=2.5, fill_color=INNER, fill_opacity=1)
        right_c.move_to([4.95, 0.55, 0])
        rgrain = grain(Square(1.9).move_to(right_c), n=90, seed=5)
        right_l = txt('für eine Fledermaus', size=20, color=VIOLET).next_to(right_c, DOWN, buff=0.12)
        b = bat(width=0.8).next_to(right_c, UP, buff=0.1)
        self.play(FadeIn(right_c), FadeIn(rgrain), FadeIn(right_l), FadeIn(b), run_time=0.7)
        mine = cloud(width=1.5, label='meine\nErfahrung', size=14).move_to(left_c.get_center() + LEFT * 0.5)
        self.play(Create(left_c), FadeIn(left_l), FadeIn(mine), run_time=0.8)

        # Sentence 4: add, subtract, vary – all variants stay inside.
        ops = [('+', 'hinzufüge', UP * 1.0 + RIGHT * 0.25, 1.25, 2),
               ('−', 'abziehe', DOWN * 1.0 + RIGHT * 0.2, 0.8, 3),
               ('~', 'abwandle', RIGHT * 1.0, 0.95, 4)]
        variants = VGroup()
        for sym, key, off, w, seed in ops:
            v = cloud(width=w, seed=seed, opacity=0.15).move_to(left_c.get_center() + off)
            s = txt(sym, size=26, color=OCHRE, weight=BOLD).move_to(v)
            self.wait_until(self.t('4.2', 3, key))
            self.play(TransformFromCopy(mine[0], v), FadeIn(s), run_time=0.5)
            variants.add(VGroup(v, s))
        probe = DashedLine(left_c.get_right() + LEFT * 0.4, right_c.get_left() + LEFT * 0.35, color=MUTED,
                           stroke_width=3)
        stop = Line(UP * 0.25, DOWN * 0.25, color=MUTED, stroke_width=5).move_to(probe.get_end())
        self.play_at(self.t('4.2', 3, 'keine'), Create(probe), run_time=0.6)
        self.play(FadeIn(stop), run_time=0.3)

        # Sentence 5: general types only – labels without content.
        self.wait_until(self.t('4.2', 4))
        types = ['Schmerz', 'Furcht', 'Hunger', 'räumlich nach vorn']
        tags = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.08, width=txt(t, size=16).width + 0.3, height=0.36,
                                                stroke_color=VIOLET, stroke_width=1.8),
                               txt(t, size=16, color=VIOLET)) for t in types])
        for tg in tags:
            tg[1].move_to(tg[0])
        tags.arrange(DOWN, buff=0.1).move_to(right_c)
        for tg, key in zip(tags, ['Schmerz', 'Furcht', 'Hunger', 'räumliche']):
            self.play_at(self.t('4.2', 4, key), FadeIn(tg[0]), FadeIn(tg[1]), run_time=0.35)

        # Sentence 6: only a schematic conception.
        self.wait_until(self.t('4.2', 5))
        lab = txt('nur schematisch: Typen, kein besonderer Charakter', size=20, color=MUTED)
        lab.move_to([MX + 0.3, -2.1, 0])
        self.play(FadeIn(lab), run_time=0.5)
        self.node('Z2')
        self.wait_until(self.t('4.2', 'end') + 0.1)
        self.clear()

    # ------------------------------------------------------------ 4.3
    def p43(self):
        self.wait_until(self.t('4.3'))
        self.cite(self.cite_of('4.3'))
        h = person(height=1.6).move_to([5.0, 1.35, 0])
        hf = InnerField(width=2.8, height=1.3, label='für uns selbst', seed=31).move_to([5.0, -0.75, 0])
        self.play(FadeIn(h), FadeIn(hf), run_time=0.6)

        # Sentence 2: intelligent bats or Martians try to imagine being us.
        self.wait_until(self.t('4.3', 1))
        b = bat(width=1.3).move_to([-0.6, 1.0, 0])
        m = martian(height=1.15).move_to([-0.55, -0.6, 0])
        self.play(FadeIn(b), run_time=0.4)
        self.play_at(self.t('4.3', 1, 'Marsianer'), FadeIn(m), run_time=0.4)
        beam = VGroup(*[DashedLine(src.get_right() + RIGHT * 0.1, hf.box.get_left() + UP * dy, color=MUTED,
                                   stroke_width=2.5) for src, dy in ((b, 0.35), (m, -0.35))])
        self.play_at(self.t('4.3', 1, 'vorzustellen'), Create(beam), run_time=0.8)

        # Sentence 3: they would fail.
        qm = txt('?', size=44, color=MUTED).move_to(beam.get_center() + UP * 0.45)
        self.play_at(self.t('4.3', 2), FadeIn(qm), beam.animate.set_opacity(0.3), run_time=0.5)

        # Sentence 4: wrong to conclude there is nothing – we know from our own case.
        concl = txt('„da ist nichts“', size=24, color=MUTED).move_to([1.6, -1.35, 0])
        self.play_at(self.t('4.3', 3, 'schlössen'), FadeIn(concl), run_time=0.5)
        strike = Line(concl.get_left() + LEFT * 0.08, concl.get_right() + RIGHT * 0.08, color=FG, stroke_width=4)
        lit = RoundedRectangle(corner_radius=0.1, width=2.8, height=1.3, stroke_width=0, fill_opacity=0.55,
                               fill_color=[VIOLET, OCHRE]).move_to(hf.box)
        lit.set_sheen_direction(UR)
        inside = txt('von innen: es ist\nauf bestimmte Weise', size=18, color=FG).move_to(hf.box)
        self.play_at(self.t('4.3', 3, 'das wissen'), Create(strike), FadeIn(lit), run_time=0.8)
        self.play(FadeIn(inside), run_time=0.5)

        # Sentence 5: realism about the subjective.
        self.wait_until(self.t('4.3', 4))
        self.node('P5')
        self.quote('4.3', 'Nagel 1974, S. 441', y=-2.75)
        self.wait_until(self.t('4.3', 'end') + 0.1)
        self.clear()

    # ------------------------------------------------------------ 4.4
    def p44(self):
        self.wait_until(self.t('4.4'))
        self.cite(self.cite_of('4.4'))
        base_y = -2.55
        humans = VGroup()
        cones = VGroup()
        for i, (x, a) in enumerate([(-0.9, 1.52), (-0.35, 1.6), (0.2, 1.5), (0.75, 1.58)]):
            p = person(height=0.42).move_to([x, base_y, 0])
            c = cone(p.get_top() + UP * 0.05, a, length=4.4, spread=0.42, color=OCHRE, opacity=0.1)
            humans.add(p)
            cones.add(c)
        self.play(LaggedStart(*[FadeIn(VGroup(p, c)) for p, c in zip(humans, cones)], lag_ratio=0.25), run_time=1.4)
        hl = txt('Menschen', size=18, color=OCHRE).next_to(humans, DOWN, buff=0.15)
        typ = txt('ein Standpunkt-Typ,\nkein privates Ich', size=20, color=OCHRE).move_to([-0.45, 2.6, 0])
        self.play(FadeIn(hl), run_time=0.3)
        self.play_at(self.t('4.4', 0, 'privates'), FadeIn(typ), run_time=0.5)
        self.node('Z3')

        # Sentence 2: the more unlike us, the less overlap.
        self.wait_until(self.t('4.4', 1))
        bb = bat(width=0.7).move_to([5.9, base_y, 0])
        bc = cone(bb.get_top() + UP * 0.05, 1.98, length=4.6, spread=0.42, color=VIOLET, opacity=0.18)
        self.play(FadeIn(bb), FadeIn(bc), run_time=0.8)
        btxt = txt('Fledermaus', size=18, color=VIOLET).next_to(bb, DOWN, buff=0.15)
        less = txt('je unähnlicher, desto weniger Überlappung', size=18, color=MUTED).move_to([4.15, 2.95, 0])
        self.play(FadeIn(btxt), FadeIn(less), run_time=0.5)

        # Sentence 3: even a person deaf and blind from birth.
        self.wait_until(self.t('4.4', 2))
        dp = person(height=0.42, color=MUTED).move_to([2.9, base_y, 0])
        dc = cone(dp.get_top() + UP * 0.05, 1.82, length=4.3, spread=0.3, color=FG, opacity=0.1)
        dtxt = txt('von Geburt an taubblind', size=18, color=FG).next_to(dp, DOWN, buff=0.15)
        self.play(FadeIn(dp), FadeIn(dc), run_time=0.7)
        self.play_at(self.t('4.4', 2, 'taubblinder'), FadeIn(dtxt), run_time=0.5)
        self.wait_until(self.t('4.4', 'end') + 0.1)
        self.clear()

    # ------------------------------------------------------------ 4.5
    def p45(self):
        self.wait_until(self.t('4.5'))
        self.cite(self.cite_of('4.5'))
        divider = DashedLine([MX, 2.4, 0], [MX, -1.9, 0], color=DIM, stroke_width=2)
        self.play(Create(divider), run_time=0.5)

        # Sentence 2: physical facts – understandable from many points of view.
        self.wait_until(self.t('4.5', 1))
        self.node('P6')
        head = txt('objektive Tatsachen: von vielen Standpunkten aus verständlich', size=21, color=OCHRE)
        head.move_to([MX, 2.85, 0])
        self.play(FadeIn(head), run_time=0.5)

        # Sentence 3: the example – lightning, as we see it.
        self.wait_until(self.t('4.5', 2))
        seen = lightning(color='#f4e7b5', height=2.0).move_to([MX - 2.2, 0.55, 0])
        seen_l = txt('wie er für uns aussieht', size=20, color=MUTED).next_to(seen, DOWN, buff=0.35)
        eye_i = eye(width=0.7).next_to(seen_l, DOWN, buff=0.2)
        self.play(GrowFromCenter(seen), FadeIn(seen_l), FadeIn(eye_i), run_time=0.8)

        # Sentence 4: an eyeless Martian scientist would never know that.
        self.wait_until(self.t('4.5', 3))
        m = martian(height=1.1).move_to([MX + 3.6, -1.55, 0])
        self.play(FadeIn(m), run_time=0.5)
        never = DashedLine(m.get_left() + LEFT * 0.1, seen.get_right() + RIGHT * 0.35 + DOWN * 0.6, color=MUTED,
                           stroke_width=2.5)
        nq = txt('?', size=36, color=MUTED).move_to((never.get_start() + never.get_end()) / 2 + DOWN * 0.35)
        self.play_at(self.t('4.5', 3, 'wie ein Blitz'), Create(never), FadeIn(nq), run_time=0.7)

        # Sentence 5: but he could understand what lightning is: an electric discharge.
        self.wait_until(self.t('4.5', 4))
        x0 = MX + 2.3
        bolt_path = VMobject(stroke_color=OCHRE, stroke_width=3).set_points_as_corners(
            [[x0 + 0.2, 2.0, 0], [x0 - 0.3, 1.1, 0], [x0 + 0.15, 1.0, 0], [x0 - 0.35, -0.1, 0]])
        dots = VGroup(*[Dot(radius=0.06, color=OCHRE) for _ in range(6)])
        clock = {'t': 0.0}

        def flow(g, dt):
            clock['t'] += dt
            for k, d in enumerate(g):
                d.move_to(bolt_path.point_from_proportion(((clock['t'] * 0.6) + k / len(g)) % 1))
        dots.add_updater(flow)
        field = VGroup(*[Arc(radius=r, start_angle=-PI / 2.5, angle=2 * PI / 2.5, color=DIM, stroke_width=2)
                         .move_arc_center_to([x0 - 0.1, 0.95, 0]) for r in (0.6, 0.95, 1.3)])
        field.add(*[f.copy().rotate(PI, about_point=[x0 - 0.1, 0.95, 0]) for f in field])
        dis_l = txt('elektrische Entladung', size=20, color=OCHRE).move_to([x0 - 0.1, -0.55, 0])
        self.play(Create(bolt_path), FadeIn(field), FadeIn(dots), FadeIn(dis_l), run_time=0.9)
        gauge = meter(width=0.85, value=0.2).next_to(m, LEFT, buff=0.2).shift(DOWN * 0.15)
        self.play(FadeIn(gauge), run_time=0.4)
        self.play(Rotate(gauge.needle, -PI * 0.55, about_point=gauge[-1].get_center()), run_time=0.8)

        # Sentence 6: the objective character is not exhausted by the appearance.
        self.wait_until(self.t('4.5', 5))
        q = self.quote('4.5', 'Nagel 1974, S. 443', y=-2.75)
        self.wait_until(self.t('4.5', 'end') + 0.1)
        dots.clear_updaters()
        self.clear()

    # ------------------------------------------------------------ 4.6
    def objectivity_axis(self):
        ax = Arrow([-1.7, -2.05, 0], [6.7, -2.05, 0], buff=0, color=OCHRE, stroke_width=4)
        lab = txt('Objektivität →', size=22, color=OCHRE).next_to(ax, DOWN, buff=0.1).align_to(ax, RIGHT)
        sub = txt('weniger Bindung an einen bestimmten Standpunkt', size=17, color=MUTED).next_to(ax, DOWN, buff=0.12)
        sub.align_to(ax, LEFT)
        return VGroup(ax, lab, sub)

    def p46(self):
        self.wait_until(self.t('4.6'))
        self.cite(self.cite_of('4.6'))
        self.axis = self.objectivity_axis()
        self.play(GrowArrow(self.axis[0]), FadeIn(self.axis[1]), FadeIn(self.axis[2]), run_time=0.8)
        self.node('P7')

        # Lightning row: the description moves right, the thing travels with it.
        y1 = 1.55
        rowl = txt('Blitz', size=20, color=MUTED).move_to([-1.2, y1 + 0.75, 0])
        thing = Dot(radius=0.09, color=FG).move_to([0.0, y1 + 0.75, 0])
        thing_l = txt('die Sache', size=16, color=MUTED).next_to(thing, UP, buff=0.08)
        rep = VGroup(lightning(color='#f4e7b5', height=0.8), txt('gesehen', size=18)).arrange(DOWN, buff=0.1)
        rep.move_to([0.0, y1 - 0.15, 0])
        tie = always_redraw(lambda: DashedLine(rep.get_top(), thing.get_bottom(), color=MUTED, stroke_width=2))
        self.play(FadeIn(rowl), FadeIn(rep), FadeIn(thing), FadeIn(thing_l), FadeIn(tie), run_time=0.6)
        rep2 = VGroup(charges(width=1.2), txt('gemessen', size=18)).arrange(DOWN, buff=0.12).move_to([5.0, y1 - 0.15, 0])
        self.play(rep.animate.move_to(rep2), thing.animate.move_to([5.0, y1 + 0.75, 0]),
                  thing_l.animate.move_to([5.0, y1 + 1.0, 0]), run_time=1.4)
        self.play(Transform(rep, rep2), run_time=0.5)

        # Sentence 2: sound – the hearing point of view stays behind, unreduced.
        self.wait_until(self.t('4.6', 1))
        y2 = -0.55
        rowl2 = txt('Schall', size=20, color=MUTED).move_to([-1.2, y2 + 0.75, 0])
        e = ear(height=0.75).move_to([-1.0, y2 - 0.1, 0])
        tone = VGroup(sound(height=0.55), txt('gehört', size=18)).arrange(DOWN, buff=0.1).move_to([0.4, y2, 0])
        wave = FunctionGraph(lambda x: 0.25 * np.sin(5 * x), x_range=[-0.7, 0.7], color=OCHRE, stroke_width=3)
        wave_g = VGroup(wave, txt('Welle in der Luft', size=18)).arrange(DOWN, buff=0.12).move_to([5.0, y2, 0])
        self.play(FadeIn(rowl2), FadeIn(e), FadeIn(tone), run_time=0.6)
        self.play_at(self.t('4.6', 1, 'Welle'), tone.animate.move_to(wave_g), run_time=1.4)
        self.play(Transform(tone, wave_g), run_time=0.5)
        unred = txt('bleibt unreduziert', size=18, color=VIOLET).next_to(e, DOWN, buff=0.12)
        self.play_at(self.t('4.6', 1, 'unreduziert'), FadeIn(unred), Indicate(e, color=VIOLET), run_time=0.8)

        # Sentence 3: no loss for the external world.
        self.wait_until(self.t('4.6', 2))
        ok = VGroup(check(color=OCHRE, size=0.26).next_to(rep, RIGHT, buff=0.3),
                    check(color=OCHRE, size=0.26).next_to(tone, RIGHT, buff=0.3))
        self.play(Create(ok[0]), Create(ok[1]), run_time=0.5)

        # Sentence 4: objectivity is a direction.
        self.wait_until(self.t('4.6', 3))
        self.play(Indicate(self.axis[0], color=OCHRE, scale_factor=1.03), run_time=0.8)
        self.q = self.quote('4.6', 'Nagel 1974, S. 443', x=3.3, y=0.5, size=22, width=40)
        self.wait_until(self.t('4.6', 'end') + 0.1)
        self.clear(keep=(self.axis,))

    # ------------------------------------------------------------ 4.7
    def p47(self):
        self.wait_until(self.t('4.7'))
        self.cite(self.cite_of('4.7'))
        y = 0.3
        field = InnerField(width=2.0, height=1.35, label='wie es ist, eine Fledermaus zu sein', seed=41)
        field.move_to([0.4, y, 0])
        field.label.align_to(field.box, LEFT)
        b = bat(width=0.6).move_to([-1.55, y, 0])
        view = cone(b.get_right() + RIGHT * 0.02, 0, length=0.95, spread=0.8, color=VIOLET, opacity=0.25)
        rep = pill('Beschreibung', color=PANEL, text_color=OCHRE, size=18).move_to([0.4, y - 1.2, 0])
        self.play(FadeIn(field), FadeIn(b), FadeIn(view), FadeIn(rep), run_time=0.8)
        ask = txt('Erscheinung → Wirklichkeit?', size=20, color=MUTED).move_to([4.3, y + 1.3, 0])
        self.play_at(self.t('4.7', 0, 'Erscheinung'), FadeIn(ask), run_time=0.5)

        # Sentence 2: remove the bat's viewpoint – what is left?
        self.wait_until(self.t('4.7', 1, 'entfernte'))
        ghost = DashedVMobject(field.box.copy().set_fill(opacity=0), num_dashes=40).set_stroke(MUTED)
        left_q = txt('?', size=44, color=MUTED).move_to(field.box)
        self.play(FadeOut(view), FadeOut(b), FadeOut(field.grain), field.box.animate.set_fill(opacity=0).set_stroke(opacity=0),
                  FadeIn(ghost), run_time=0.8)
        self.play(FadeIn(left_q), run_time=0.4)

        # Sentence 3: the point of view is the essence of the inner world.
        self.wait_until(self.t('4.7', 2))
        self.play(FadeOut(ghost), FadeOut(left_q), FadeIn(b), FadeIn(view), FadeIn(field.grain),
                  field.box.animate.set_fill(INNER, opacity=1).set_stroke(VIOLET, opacity=1), run_time=0.8)
        self.node('P8')

        # Sentence 4 (the key sentence): every step towards objectivity – the gap grows.
        self.wait_until(self.t('4.7', 3))
        self.q = self.quote('4.7', 'Nagel 1974, S. 444 f.', x=3.9, y=2.75, size=22, width=40)
        self.wait_until(self.t('4.7', 3, 'jeder Schritt'))
        gap = always_redraw(lambda: BraceBetweenPoints([field.box.get_right()[0], y - 1.2, 0],
                                                       [rep.get_left()[0] + 0.001, y - 1.2, 0], DOWN, color=MUTED)
                            if rep.get_left()[0] > field.box.get_right()[0] + 0.1 else VGroup())
        self.add(gap)
        dur = max(2.0, self.t('4.7', 4) - 0.1 - self.now)
        self.play(rep.animate.move_to([5.4, y - 1.2, 0]), run_time=dur, rate_func=smooth)

        # Sentence 5: further away.
        self.wait_until(self.t('4.7', 4))
        away = txt('weiter weg', size=22, color=MUTED).move_to([2.9, y - 1.95, 0])
        self.play(FadeIn(away), run_time=0.4)
        self.node('Z4', flash=False)
        self.wait_until(self.t('4.7', 'end'))
        gap.clear_updaters()
        self.clear()

    # ------------------------------------------------------------ 4.8
    def p48(self):
        self.wait_until(self.t('4.8'))
        self.cite(self.cite_of('4.8'))
        self.node('Z5')

        # Sentences 2–3: not just missing data – the method points the wrong way.
        data = txt('nicht nur: Uns fehlen Daten', size=26, color=MUTED).move_to([MX, 1.3, 0])
        self.play_at(self.t('4.8', 1), FadeIn(data), run_time=0.5)
        self.play(Create(Line(data.get_left() + LEFT * 0.1, data.get_right() + RIGHT * 0.1, color=FG,
                              stroke_width=3)), run_time=0.5)
        wrong = txt('sondern: Das erfolgreiche Verfahren\nzeigt hier in die falsche Richtung', size=26)
        wrong.move_to([MX, 0.0, 0])
        arrow = Arrow([MX - 1.5, -1.2, 0], [MX + 1.5, -1.2, 0], buff=0, color=OCHRE, stroke_width=5)
        self.play_at(self.t('4.8', 2), FadeIn(wrong), GrowArrow(arrow), run_time=0.7)
        self.play_at(self.t('4.8', 2, 'falsche'), Rotate(arrow, PI), run_time=0.8)

        # Sentence 4: the problem is unique – the whole tree.
        self.wait_until(self.t('4.8', 3) - 0.6)
        self.clear()
        self.play(FadeOut(self.cap), run_time=0.3)
        full = ArgTree(mini=False)
        anims = []
        for nid in self.shown:
            anims.append(ReplacementTransform(self.tree.nodes[nid], full.nodes[nid]))
        for (a, b2), e in self.tree.edges.items():
            if a in self.shown and b2 in self.shown:
                anims.append(ReplacementTransform(e, full.edges[(a, b2)]))
        self.play(*anims, run_time=1.2)
        q = QuoteCard(self.quote_of('4.8'), 'Nagel 1974, S. 445', size=24).move_to([5.0, -2.75, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
