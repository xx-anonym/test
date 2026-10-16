"""Kapitel 0 – Prolog.

0.1  Dämmerung: Eine Fledermaus fliegt aus, ruft, die Rufe kommen als Echos vom
     Insekt zurück; die Rufspur oben verdichtet sich bis zum Fang (bis 200/s,
     Schnitzler & Kalko 2001, S. 567). Dann das Leitmotiv: links, was sich messen
     lässt, rechts das leere Innenfeld mit der Frage.
0.2  Titelkarte des Aufsatzes; Dennetts Einordnung (1991, S. 441); die vier
     Teile des Videos.
"""

from parts import *


class Calls(VGroup):
    """Emits sound rings from the bat; rings that pass the insect send an echo back.

    Also feeds a tick strip at the top that shows the call rate.
    """

    def __init__(self, flyer, target, strip_y=3.35, speed=2.6):
        super().__init__()
        self.flyer, self.target, self.speed = flyer, target, speed
        self.interval, self.clock, self.since = 0.55, 0.0, 0.0
        self.active = True
        self.rings, self.echoes, self.ticks = VGroup(), VGroup(), VGroup()
        self.strip = Line([-6.6, strip_y, 0], [6.6, strip_y, 0], color=DIM, stroke_width=2)
        self.strip_y = strip_y
        self.add(self.rings, self.echoes, self.strip, self.ticks)
        self.add_updater(self._step)

    def _step(self, mob, dt):
        self.clock += dt
        self.since += dt
        if self.active and self.since >= self.interval:
            self.since = 0.0
            r = Circle(radius=0.05, stroke_color=OCHRE, stroke_width=3).move_to(self.flyer.pos)
            r.echoed = False
            r.maxr = min(3.2, 0.7 + 4.5 * self.interval)   # buzz calls are short and soft
            self.rings.add(r)
            tick = Line(UP * 0.12, DOWN * 0.12, color=OCHRE, stroke_width=3).move_to([6.5, self.strip_y, 0])
            self.ticks.add(tick)
        for r in list(self.rings):
            new_r = r.width / 2 + self.speed * dt
            r.scale_to_fit_width(2 * new_r)
            op = max(0.0, 1 - new_r / r.maxr)
            r.set_stroke(opacity=op)
            t = self.target
            if t is not None and t.get_fill_opacity() > 0.2 and not r.echoed and \
                    new_r >= np.linalg.norm(r.get_center() - t.get_center()):
                r.echoed = True
                e = Circle(radius=0.05, stroke_color=FG, stroke_width=2).move_to(t.get_center())
                self.echoes.add(e)
            if op <= 0:
                self.rings.remove(r)
        for e in list(self.echoes):
            new_r = e.width / 2 + self.speed * dt
            e.scale_to_fit_width(2 * new_r)
            op = max(0.0, 0.8 - new_r / 1.6)
            e.set_stroke(opacity=op)
            if op <= 0:
                self.echoes.remove(e)
        for tick in list(self.ticks):
            tick.shift(LEFT * 1.6 * dt)
            if tick.get_x() < -6.5:
                self.ticks.remove(tick)


class Kapitel0(NarratedScene):
    CHAPTER = 0

    def construct(self):
        self.p01()
        self.p02()
        self.finish()

    def p01(self):
        land = dusk()
        self.play(FadeIn(land), run_time=1.4)

        # Flight path: out of the tree on the right, towards the moth.
        path = VMobject().set_points_smoothly([
            [5.9, -0.9, 0], [4.6, 0.6, 0], [2.4, 1.6, 0], [0.4, 0.9, 0], [-1.2, 1.5, 0], [-2.3, 1.15, 0]])
        tracker = ValueTracker(0)
        flyer = Flyer(path, tracker, width=0.8)
        moth = insect(size=0.32).move_to([-2.6, 1.3, 0]).set_opacity(0)
        anchor = moth.get_center()
        clock = {'t': 0.0}

        def flutter(m, dt):
            clock['t'] += dt
            m.move_to(anchor + np.array([0.25 * np.sin(1.7 * clock['t']), 0.18 * np.sin(2.9 * clock['t']), 0]))
        moth.add_updater(flutter)
        calls = Calls(flyer, moth)
        calls.active = False

        self.wait_until(self.t('0.1', 1))
        self.add(moth, calls)
        self.play(FadeIn(flyer), tracker.animate.set_value(0.18), run_time=1.6, rate_func=linear)
        calls.active = True
        label = txt('Rufe', size=18, color=MUTED).next_to(calls.strip, DOWN, buff=0.22).align_to(calls.strip, LEFT)
        self.add(label)

        s2_end = self.t('0.1', 2, end=True)
        self.play(tracker.animate.set_value(0.55), run_time=max(1.0, self.t('0.1', 2, 'Mücke') - self.now),
                  rate_func=linear)
        self.play(moth.animate.set_opacity(1), tracker.animate.set_value(0.7), run_time=1.0, rate_func=linear)
        self.play(tracker.animate.set_value(0.8), run_time=max(0.5, s2_end - self.now), rate_func=linear)

        # Approach and terminal buzz: the call interval shrinks.
        self.wait_until(self.t('0.1', 3))
        rate = txt('kurz vor dem Fang: bis zu 200 Rufe pro Sekunde', size=20, color=OCHRE)
        rate.next_to(label, RIGHT, buff=0.5)
        self.cite(self.cite_of('0.1') + ', S. 567')
        dur = max(1.5, self.t('0.1', 3, end=True) - 0.3 - self.now)
        steps = 6
        for k in range(steps):
            calls.interval = 0.55 * (0.5 ** (k + 1)) + 0.03
            anims = [tracker.animate.set_value(0.8 + 0.2 * (k + 1) / steps)]
            if k == 0:
                anims.append(FadeIn(rate))
            self.play(*anims, run_time=dur / steps, rate_func=linear)
        calls.active = False
        moth.clear_updaters()
        self.play(FadeOut(moth, scale=0.3), Flash(flyer.pos, color=FG, line_length=0.15, flash_radius=0.3),
                  run_time=0.5)

        # The two fields.
        self.wait_until(self.t('0.1', 4) - 0.2)
        calls.clear_updaters()
        flyer.clear_updaters()
        self.play(FadeOut(VGroup(land, calls, label, rate, flyer)), run_time=0.7)
        outer, inner = two_fields(height=3.6, y=0.1)
        self.play(Create(outer.box), FadeIn(outer.label), run_time=0.6)
        facts = VGroup(*[VGroup(Dot(radius=0.05, color=OCHRE), txt(f, size=24)).arrange(RIGHT, buff=0.2)
                         for f in ['Verzögerung des Echos → Entfernung',
                                   'Vergleich beider Ohren → Richtung',
                                   'Rufrate: bis 200 pro Sekunde',
                                   'Reichweite: höchstens rund 10 Meter']])
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(outer.box)
        self.cite(self.cite_of('0.1') + ', S. 558, 567')
        span = max(1.2, self.t('0.1', 4, end=True) - self.now)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.1) for f in facts], lag_ratio=0.5), run_time=span)

        self.play_at(self.t('0.1', 5), FadeIn(inner), run_time=0.8)
        question = txt('Wie ist es, diese Fledermaus zu sein?', size=34, font=SERIF, slant=ITALIC)
        question.move_to(inner.box).set(width=min(question.width, inner.box.width - 0.6))
        self.play_at(self.t('0.1', 5, 'Wie ist es'), Write(question), run_time=1.6)
        self.fields = VGroup(outer, inner, facts, question)

    def p02(self):
        self.wait_until(self.t('0.2') - 0.6)
        self.play(FadeOut(self.fields), FadeOut(self.cite_mob), run_time=0.6)
        self.cite_mob = None
        title = txt('What Is It Like to Be a Bat?', size=60, font=SERIF, weight=SEMIBOLD)
        de = txt('Wie ist es, eine Fledermaus zu sein?', size=30, color=MUTED, font=SERIF, slant=ITALIC)
        meta = txt('Thomas Nagel · The Philosophical Review 83/4 · Oktober 1974 · S. 435–450', size=22, color=OCHRE)
        block = VGroup(title, de, meta).arrange(DOWN, buff=0.3).move_to(UP * 1.2)
        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(de), run_time=0.6)
        self.play_at(self.t('0.2', 0, 'sechzehn Seiten'), FadeIn(meta), run_time=0.6)
        self.cite(self.cite_of('0.2'))

        dq = QuoteCard(self.quote_of('0.2'), self.cite_of('0.2', 1)).move_to(DOWN * 1.0)
        self.play_at(self.t('0.2', 1), FadeIn(dq, shift=UP * 0.1), run_time=0.6)
        self.cite(self.cite_of('0.2', 1))

        parts = ['das Argument', 'die Einwände', 'die echte Fledermaus', 'Tiere und Maschinen']
        chips = VGroup(*[pill(p, color=PANEL, text_color=FG, size=22) for p in parts]).arrange(RIGHT, buff=0.3)
        chips.move_to(DOWN * 1.0)
        keys = ['Argument', 'Einwände', 'echte Fledermaus', 'Tiere und Maschinen']
        self.play_at(self.t('0.2', 2), FadeOut(dq), run_time=0.4)
        self.cite(self.cite_of('0.2'))
        for chip, key in zip(chips, keys):
            self.play_at(self.t('0.2', 2, key), FadeIn(chip, shift=UP * 0.1), run_time=0.4)
