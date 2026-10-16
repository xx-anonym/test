"""Kapitel 9 – Die echte Fledermaus (Griffin & Galambos 1941; Griffin 1944; OpenStax 2016;
Schnitzler & Kalko 2001; Suga 1988; O'Neill & Suga 1982; Kaldari 2020 (CC0); Thaler et al.
2011; Nagel 1974; Nagel 2024; Griffin 2001 nach Salzani 2022).

9.1  Maßstäbliche Draufsicht: Fledermaus, Insekt in 1 m, Mauer in 3 m; Wellenfronten mit
     c = 343 m/s, Echos per Spiegelquelle; darunter das Zeitdiagramm (0 / 5,8 / 17,5 ms)
     und r = c·Δt/2.
9.2  Zwei Rufformen als Spektrogramm-Skizzen (FM, CF-FM); im CF-Echo der Flügelschlag.
9.3  Doppler: 61,0 → 62,8 kHz bei 5 m/s; Kompensation: Ruf 59,3 kHz, Echo im Fenster.
9.4  Schematische Hörkortex-Karte nach Suga 1988: Entfernungsachse 7–310 cm, gekoppelt an
     die Draufsicht; das gespreizte Band 61–62 kHz.
9.5  Echtes Spektrogramm der Aufnahme mit Abspielkopf, doppelte Frequenzachse.
9.6  Menschliche Echoortung: Klick und Echo, schematisches Gehirn, n = 2.
9.7  Leitmotiv: Das linke Feld ist voll, das rechte leer.
9.8  Nagel und Griffin; „paralytic perfectionism“.
"""

from parts import *

C = 343.0                       # m/s at 20 °C (OpenStax 2016, 17.2)
SPEC = os.path.join(ROOT, 'assets', 'img', 'spectrogram_buzz.png')


def head_profile(color=FG, height=1.8):
    """Simple human head in profile, facing right."""
    pts = [[-0.45, -0.9], [-0.5, -0.2], [-0.55, 0.35], [-0.35, 0.8], [0.05, 0.95], [0.42, 0.75], [0.55, 0.35],
           [0.58, 0.1], [0.72, -0.05], [0.58, -0.15], [0.6, -0.3], [0.55, -0.45], [0.45, -0.55], [0.3, -0.6],
           [0.15, -0.9]]
    h = VMobject(stroke_color=color, stroke_width=3).set_points_smoothly([[x, y, 0] for x, y in pts])
    return h.scale_to_fit_height(height)


def brain_side(width=3.4):
    """Schematic human brain, side view, front to the right; returns (outline, occipital, auditory)."""
    outline = Ellipse(width=width, height=width * 0.62, stroke_color=MUTED, stroke_width=3, fill_color=PANEL,
                      fill_opacity=1)
    occ = Ellipse(width=width * 0.24, height=width * 0.26, stroke_width=0, fill_color=DIM, fill_opacity=1)
    occ.move_to(outline.get_center() + LEFT * width * 0.36 + DOWN * width * 0.02)
    aud = Ellipse(width=width * 0.3, height=width * 0.13, stroke_width=0, fill_color=DIM, fill_opacity=1)
    aud.move_to(outline.get_center() + DOWN * width * 0.12 + RIGHT * width * 0.02).rotate(0.15)
    return outline, occ, aud


class Kapitel9(NarratedScene):
    CHAPTER = 9

    def construct(self):
        self.chapter_card()
        self.keep = []          # small copies for the summary field in 9.7
        self.p91()
        self.p92()
        self.p93()
        self.p94()
        self.p95()
        self.p96()
        self.p97()
        self.p98()
        self.finish()

    def wipe(self):
        gone = [m for m in self.mobjects if m not in (self.tag, self.cite_mob)]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)

    # ------------------------------------------------------------ 9.1
    def p91(self):
        self.wait_until(self.t('9.1'))
        # Sentence 2: Griffin & Galambos 1941; the word „echolocation“ (Griffin 1944).
        self.wait_until(self.t('9.1', 1))
        self.cite(self.cite_of('9.1', 0))
        word = txt('echolocation', size=44, font=SERIF, slant=ITALIC, color=OCHRE).move_to([0, 1.0, 0])
        who = txt('Griffin & Galambos 1941: Ausweichen mit Echos · Griffin 1944: das Wort', size=20, color=MUTED)
        who.next_to(word, DOWN, buff=0.3)
        self.play(FadeIn(who), run_time=0.5)
        self.play_at(self.t('9.1', 1, 'echolocation'), Write(word), run_time=1.0)

        # Sentence 3: the physics – to scale.
        self.wait_until(self.t('9.1', 2))
        self.cite(self.cite_of('9.1', 1))
        self.play(FadeOut(word), FadeOut(who), run_time=0.4)
        S = 2.35                                    # scene units per metre
        y0 = 1.2
        bx = -5.3
        bp = np.array([bx, y0, 0])
        ip = np.array([bx + 1.0 * S, y0, 0])
        wx = bx + 3.0 * S
        b = bat(width=0.6).move_to(bp)
        ins = insect(size=0.3).move_to(ip)
        wall = VGroup(*[Rectangle(width=0.18, height=0.34, fill_color='#8a5a48', fill_opacity=1, stroke_color='#5d3c30',
                                  stroke_width=1).move_to([wx + 0.09 + (0.09 if k % 2 else 0) * 0, y0 - 1.36 + 0.34 * k, 0])
                        for k in range(9)])
        scale = VGroup(Line([bx, y0 - 1.75, 0], [bx + S, y0 - 1.75, 0], color=MUTED, stroke_width=3),
                       txt('1 m', size=16, color=MUTED).move_to([bx + S / 2, y0 - 1.95, 0]))
        lab_i = txt('Insekt, 1 m', size=16, color=MUTED).next_to(ins, UP, buff=0.5)
        lab_w = txt('Mauer, 3 m', size=16, color=MUTED).next_to(wall, UP, buff=0.1)
        cval = txt('c ≈ 343 m/s (20 °C)', size=20, color=OCHRE).move_to([3.9, 2.7, 0])
        self.play(FadeIn(b), FadeIn(ins), FadeIn(wall), FadeIn(scale), FadeIn(lab_i), FadeIn(lab_w), run_time=0.7)
        self.play_at(self.t('9.1', 2, '343'), FadeIn(cval), run_time=0.5)

        # time diagram
        ty = -1.9
        tx0, tx1 = -5.3, 5.9
        tms = 20.0

        def tx(ms):
            return tx0 + (tx1 - tx0) * ms / tms
        tline = Arrow([tx0, ty, 0], [tx1 + 0.3, ty, 0], buff=0, color=MUTED, stroke_width=3)
        tlab = txt('Zeit (ms)', size=16, color=MUTED).next_to(tline, DOWN, buff=0.1).align_to(tline, RIGHT)
        tticks = VGroup(*[VGroup(Line([tx(m), ty - 0.07, 0], [tx(m), ty + 0.07, 0], color=MUTED, stroke_width=2),
                                 txt(f'{m}', size=14, color=MUTED).move_to([tx(m), ty - 0.25, 0]))
                          for m in range(0, 21, 5)])
        self.play(GrowArrow(tline), FadeIn(tlab), FadeIn(tticks), run_time=0.6)

        t_ins = 2 * 1.0 / C * 1000          # 5.83 ms
        t_wall = 2 * 3.0 / C * 1000         # 17.49 ms
        clock = ValueTracker(0.0)            # milliseconds

        def r_of(ms):                        # wavefront radius in scene units
            return C * ms / 1000 * S

        out = always_redraw(lambda: Circle(radius=max(0.01, r_of(clock.get_value())), stroke_color=OCHRE,
                                           stroke_width=3, stroke_opacity=0.9).move_to(bp)
                            if r_of(clock.get_value()) < 7.5 * S else VGroup())

        def echo_ins():
            ms = clock.get_value() - t_ins / 2
            if ms <= 0:
                return VGroup()
            return Circle(radius=r_of(ms), stroke_color=FG, stroke_width=2.5, stroke_opacity=0.8).move_to(ip)

        def echo_wall():
            r = r_of(clock.get_value())
            img = np.array([wx + (wx - bx), y0, 0])          # mirror source behind the wall
            d = img[0] - wx
            if r <= d:
                return VGroup()
            th = np.arccos(-d / r)
            return Arc(radius=r, start_angle=th, angle=2 * PI - 2 * th, arc_center=img, stroke_color=FG,
                       stroke_width=2.5, stroke_opacity=0.8)
        e1 = always_redraw(echo_ins)
        e2 = always_redraw(echo_wall)
        head = always_redraw(lambda: Line([tx(clock.get_value()), ty - 0.1, 0], [tx(clock.get_value()), ty + 0.55, 0],
                                          color=OCHRE, stroke_width=3))
        slow = txt('Zeitlupe: 20 ms in 5 s (250-fach)', size=16, color=MUTED).move_to([3.9, 2.3, 0])
        self.add(out, e1, e2, head)
        self.play(FadeIn(slow), run_time=0.3)
        call = VGroup(Line([tx(0), ty, 0], [tx(0), ty + 0.5, 0], color=OCHRE, stroke_width=5),
                      txt('Ruf', size=16, color=OCHRE).move_to([tx(0), ty + 0.7, 0]))
        self.add(call)
        marks = VGroup()
        for target_ms, name in ((t_ins, 'Insekt 5,8 ms'), (t_wall, 'Mauer 17,5 ms')):
            self.play(clock.animate.set_value(target_ms), run_time=(target_ms - clock.get_value()) / tms * 5.0,
                      rate_func=linear)
            m = VGroup(Line([tx(target_ms), ty, 0], [tx(target_ms), ty + 0.5, 0], color=FG, stroke_width=4),
                       txt(name, size=16).move_to([tx(target_ms), ty + 0.7, 0]))
            self.add(m)
            marks.add(m)
        self.play(clock.animate.set_value(tms), run_time=(tms - clock.get_value()) / tms * 5.0, rate_func=linear)
        self.remove(out, e1, e2, head)

        # Sentence 4: 6 ms → about one metre.
        self.wait_until(self.t('9.1', 3))
        f1 = txt('r = c · Δt / 2', size=34, font=SERIF, slant=ITALIC).move_to([3.9, 1.35, 0])
        f2 = txt('343 m/s · 5,8 ms / 2 ≈ 1,0 m', size=20, color=FG).next_to(f1, DOWN, buff=0.25)
        self.play(Write(f1), run_time=0.8)
        self.play(FadeIn(f2), Indicate(marks[0], color=OCHRE), run_time=0.7)

        # Sentence 5: short range.
        self.wait_until(self.t('9.1', 4))
        self.cite(self.cite_of('9.1', 2))
        rng = txt('günstigstes Ziel: kaum mehr als ≈ 10 m', size=20, color=OCHRE).next_to(f2, DOWN, buff=0.3)
        self.play(FadeIn(rng), run_time=0.5)
        self.keep.append(VGroup(b, ins, wall, marks, tline).copy())
        self.wait_until(self.t('9.1', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 9.2
    def sketch_axes(self, x, title):
        ax = Axes(x_range=[0, 10, 10], y_range=[0, 10, 10], x_length=4.6, y_length=3.0, tips=False,
                  axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': False})
        ax.move_to([x, 0.1, 0])
        xl = txt('Zeit', size=16, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.1).align_to(ax.x_axis, RIGHT)
        yl = txt('Frequenz', size=16, color=MUTED).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.1)
        tt = txt(title, size=22, color=FG).next_to(ax, UP, buff=0.3)
        return ax, VGroup(ax, xl, yl, tt)

    def p92(self):
        self.wait_until(self.t('9.2'))
        self.cite(self.cite_of('9.2'))
        ax1, g1 = self.sketch_axes(-3.2, 'frequenzmoduliert (FM)')
        ax2, g2 = self.sketch_axes(3.2, 'konstantfrequent (CF-FM)')
        note = txt('schematisch', size=16, color=MUTED, slant=ITALIC).to_corner(DL, buff=0.35)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(note), run_time=0.7)

        # Sentence 2: FM – a steep downward sweep; a precise time marker.
        self.wait_until(self.t('9.2', 1))
        fm = ax1.plot(lambda t: 9.0 - 6.5 * (t - 3) / 1.6 + 1.4 * ((t - 3) / 1.6) ** 2, x_range=[3, 4.6],
                      color=OCHRE, stroke_width=5)
        self.play(Create(fm), run_time=0.8)
        mark = DashedLine(ax1.c2p(3, 0), ax1.c2p(3, 9.6), color=FG, stroke_width=2)
        ml = txt('präzise Zeitmarke', size=16, color=FG).next_to(mark, UP, buff=0.05)
        self.play_at(self.t('9.2', 1, 'Zeitmarken'), Create(mark), FadeIn(ml), run_time=0.6)

        # Sentence 3: CF – a long tone; the echo flickers with the wing beat.
        self.wait_until(self.t('9.2', 2))
        cf = VGroup(ax2.plot(lambda t: 7.0, x_range=[1.0, 6.5], color=OCHRE, stroke_width=5),
                    ax2.plot(lambda t: 7.0 - 3.2 * (t - 6.5) / 0.8, x_range=[6.5, 7.3], color=OCHRE, stroke_width=5))
        self.play(Create(cf), run_time=0.9)
        echo = ax2.plot(lambda t: 7.3 + (0.9 if (t * 2.2) % 1 < 0.12 else 0.0), x_range=[1.6, 7.0, 0.01],
                        color=FG, stroke_width=3)
        el = txt('Echo: Flügelschlag als Flackern', size=16, color=FG).next_to(ax2.c2p(4.3, 9.4), UP, buff=0.0)
        self.play_at(self.t('9.2', 2, 'Flügelschlag'), Create(echo), FadeIn(el), run_time=1.0)
        self.keep.append(VGroup(fm, cf).copy())
        self.wait_until(self.t('9.2', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 9.3
    def p93(self):
        self.wait_until(self.t('9.3'))
        self.cite(self.cite_of('9.3'))
        ax = Axes(x_range=[0, 10, 2], y_range=[58, 64, 1], x_length=8.0, y_length=4.0, tips=False,
                  axis_config={'color': MUTED, 'stroke_width': 2, 'font_size': 20},
                  y_axis_config={'numbers_to_include': [58, 59, 60, 61, 62, 63, 64]})
        ax.move_to([-1.3, -0.3, 0])
        yl = txt('Frequenz (kHz)', size=16, color=MUTED).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.55)
        xl = txt('Zeit', size=16, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT)
        win = Rectangle(width=ax.c2p(10, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 61.6)[1] - ax.c2p(0, 60.8)[1],
                        stroke_width=0, fill_color=VIOLET, fill_opacity=0.18)
        win.move_to(ax.c2p(5, 61.2))
        wl = txt('Fenster feinster Abstimmung des Innenohrs', size=16, color=VIOLET).next_to(win, UP, buff=0.05)
        wl.align_to(win, RIGHT)
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), run_time=0.8)

        def bar(t0, t1, f, color):
            return Line(ax.c2p(t0, f), ax.c2p(t1, f), color=color, stroke_width=7)
        call = bar(0.5, 4.0, 61.0, OCHRE)
        cl = txt('Ruf 61,0 kHz', size=18, color=OCHRE).next_to(call, DOWN, buff=0.1)
        echo = bar(1.0, 4.5, 62.8, FG)
        el = txt('Echo 62,8 kHz', size=18).next_to(echo, UP, buff=0.1)
        self.play(Create(call), FadeIn(cl), run_time=0.6)
        self.play_at(self.t('9.3', 0, 'höher'), Create(echo), FadeIn(el), run_time=0.6)
        form = txt('f(Echo) = f(Ruf) · (c + v) / (c − v)\n≈ f(Ruf) · (1 + 2v / c)', size=24, font=SERIF, slant=ITALIC)
        form.move_to([4.6, 1.9, 0])
        vals = txt('v = 5 m/s, f₀ = 61 kHz → Δf ≈ 1,8 kHz', size=18, color=MUTED).next_to(form, DOWN, buff=0.2)
        self.play_at(self.t('9.3', 0, 'fünf Metern'), Write(form), FadeIn(vals), run_time=1.0)

        # Sentences 2–3: compensation – the call drops, the echo lands in the window.
        self.wait_until(self.t('9.3', 1))
        self.play(FadeIn(win), FadeIn(wl), run_time=0.5)
        call2 = bar(5.5, 9.0, 59.3, OCHRE)
        cl2 = txt('Ruf 59,3 kHz', size=18, color=OCHRE).next_to(call2, DOWN, buff=0.1)
        echo2 = bar(6.0, 9.5, 61.0, FG)
        el2 = txt('Echo 61,0 kHz', size=18).next_to(echo2, UP, buff=0.1)
        comp = txt('mit Kompensation', size=18, color=MUTED).move_to(ax.c2p(7.5, 63.5))
        nocomp = txt('ohne', size=18, color=MUTED).move_to(ax.c2p(2.5, 63.5))
        self.play(FadeIn(nocomp), FadeIn(comp), run_time=0.4)
        self.play_at(self.t('9.3', 2, 'senken'), Create(call2), FadeIn(cl2), run_time=0.6)
        self.play_at(self.t('9.3', 2, 'Fenster'), Create(echo2), FadeIn(el2), Indicate(win, color=VIOLET), run_time=0.8)
        self.keep.append(VGroup(call, echo, call2, echo2).copy())
        self.wait_until(self.t('9.3', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 9.4
    def p94(self):
        self.wait_until(self.t('9.4'))
        self.cite(self.cite_of('9.4'))
        title = txt('Hörkortex der Schnurrbartfledermaus', size=24).move_to([1.5, 2.95, 0])
        note = txt('schematisch nach Suga 1988', size=16, color=MUTED, slant=ITALIC).next_to(title, DOWN, buff=0.08)
        cortex = Ellipse(width=8.6, height=4.6, stroke_color=MUTED, stroke_width=3, fill_color=PANEL,
                         fill_opacity=1).move_to([1.5, -0.4, 0])
        self.play(FadeIn(title), FadeIn(note), FadeIn(cortex), run_time=0.7)
        call = txt('Ruf: langer Ton bei ≈ 61 kHz, dann FM-Abschwung', size=18, color=OCHRE).move_to([1.5, 1.35, 0])
        self.play_at(self.t('9.4', 0, '61'), FadeIn(call), run_time=0.5)

        # Sentence 2: delay-tuned neurons along a range axis 7 cm … 310 cm.
        self.wait_until(self.t('9.4', 1))
        fmfm = RoundedRectangle(corner_radius=0.1, width=4.6, height=1.0, stroke_color=OCHRE, stroke_width=2,
                                fill_color='#2a2418', fill_opacity=1).move_to([0.2, 0.2, 0])
        fl = txt('FM-FM-Areal: Verzögerung → Entfernung', size=17, color=OCHRE).next_to(fmfm, UP, buff=0.08)
        x0, x1 = fmfm.get_left()[0] + 0.3, fmfm.get_right()[0] - 0.3
        axis = Line([x0, 0.1, 0], [x1, 0.1, 0], color=OCHRE, stroke_width=2)
        ends = VGroup(txt('7 cm', size=15, color=FG).next_to([x0, 0.1, 0], DOWN, buff=0.1),
                      txt('310 cm', size=15, color=FG).next_to([x1, 0.1, 0], DOWN, buff=0.1))
        self.play(FadeIn(fmfm), FadeIn(fl), Create(axis), FadeIn(ends), run_time=0.8)
        # coupled inset: the top view of 9.1 with a moving insect
        d = ValueTracker(3.0)                               # metres
        ib = bat(width=0.45).move_to([-5.6, -2.55, 0])
        inset_scale = 1.15
        ii = always_redraw(lambda: insect(size=0.22).move_to([-5.6 + d.get_value() * inset_scale, -2.55, 0]))
        il = txt('Abstand Fledermaus – Insekt', size=15, color=MUTED).move_to([-3.85, -2.1, 0])

        def xd(m):
            return x0 + (x1 - x0) * (np.clip(m, 0.07, 3.1) - 0.07) / (3.1 - 0.07)
        spot = always_redraw(lambda: Dot([xd(d.get_value()), 0.1, 0], radius=0.11, color=FG).set_glow_factor(0)
                             if True else VGroup())
        self.play(FadeIn(ib), FadeIn(il), run_time=0.4)
        self.add(ii, spot)
        self.play_at(self.t('9.4', 1, 'sieben'), d.animate.set_value(0.12), run_time=3.0, rate_func=smooth)
        self.play(d.animate.set_value(2.6), run_time=1.6, rate_func=smooth)

        # Sentence 3: DSCF area – the band just above 61 kHz is spread wide.
        self.wait_until(self.t('9.4', 2))
        dscf = RoundedRectangle(corner_radius=0.1, width=3.3, height=1.6, stroke_color=VIOLET, stroke_width=2,
                                fill_color='#211b33', fill_opacity=1).move_to([3.75, -1.15, 0])
        band = Rectangle(width=2.9, height=0.9, stroke_width=0, fill_color=VIOLET, fill_opacity=0.45).move_to(dscf)
        bl = txt('61–62 kHz', size=18, color=FG).move_to(band)
        dl = txt('DSCF-Areal: Geschwindigkeit', size=17, color=VIOLET).next_to(dscf, DOWN, buff=0.08)
        rest = VGroup(txt('übrige Frequenzen', size=13, color=MUTED).next_to(band, UP, buff=0.04))
        self.play(FadeIn(dscf), FadeIn(dl), run_time=0.5)
        self.play_at(self.t('9.4', 2, 'vergrößert'), GrowFromCenter(band), FadeIn(bl), FadeIn(rest), run_time=0.8)
        self.keep.append(VGroup(fmfm.copy(), axis.copy(), dscf.copy(), band.copy()))
        self.wait_until(self.t('9.4', 'end') + 0.1)
        self.remove(ii, spot)
        self.wipe()

    # ------------------------------------------------------------ 9.5
    def p95(self):
        self.wait_until(self.t('9.5'))
        self.cite(self.cite_of('9.5'))
        img = ImageMobject(SPEC)
        img.stretch_to_fit_width(9.6).stretch_to_fit_height(4.0).move_to([0.2, 0.0, 0])
        frame = Rectangle(width=9.6, height=4.0, stroke_color=MUTED, stroke_width=2).move_to(img)
        left, right = frame.get_left()[0], frame.get_right()[0]
        bottom, top = frame.get_bottom()[1], frame.get_top()[1]
        hz = VGroup()
        for k in range(0, 9, 2):                           # heard: 0–8 kHz; real ×10
            y = bottom + (top - bottom) * k / 8
            hz.add(Line([left - 0.08, y, 0], [left, y, 0], color=MUTED, stroke_width=2),
                   txt(f'{k}', size=15, color=MUTED).next_to([left - 0.08, y, 0], LEFT, buff=0.08),
                   Line([right, y, 0], [right + 0.08, y, 0], color=MUTED, stroke_width=2),
                   txt(f'{10 * k}', size=15, color=OCHRE).next_to([right + 0.08, y, 0], RIGHT, buff=0.08))
        hl = txt('gehört (verlangsamt), kHz', size=15, color=MUTED).rotate(PI / 2).next_to(frame, LEFT, buff=0.45)
        rl = txt('tatsächlich (× 10), kHz', size=15, color=OCHRE).rotate(PI / 2).next_to(frame, RIGHT, buff=0.55)
        tl = txt('0 – 7 s gehört  =  0 – 0,7 s in Wirklichkeit', size=16, color=MUTED).next_to(frame, DOWN, buff=0.15)
        self.play(FadeIn(img), Create(frame), FadeIn(hz), FadeIn(hl), FadeIn(rl), FadeIn(tl), run_time=0.9)

        # Sentence 2: more than three octaves down (factor 10).
        self.wait_until(self.t('9.5', 1))
        oct_ = txt('10-fach langsamer = gut 3 Oktaven tiefer (2³ = 8, 2⁴ = 16)', size=18, color=FG).move_to([0.2, 2.65, 0])
        self.play(FadeIn(oct_), run_time=0.5)

        # Sentence 3: each call sweeps down; the calls come ever faster.
        self.wait_until(self.t('9.5', 2))
        sweep = Arrow([left + 1.05, top - 0.6, 0], [left + 1.5, bottom + 1.4, 0], buff=0, color=FG, stroke_width=3,
                      max_tip_length_to_length_ratio=0.15)
        dense = Brace(Line([left + 6.4, bottom, 0], [left + 9.0, bottom, 0]), UP, color=FG).shift(UP * 3.55)
        dl = txt('immer dichter', size=16, color=FG).next_to(dense, UP, buff=0.05)
        self.play(GrowArrow(sweep), run_time=0.6)
        self.play_at(self.t('9.5', 2, 'dichter'), GrowFromCenter(dense), FadeIn(dl), run_time=0.6)

        # The recording itself: playhead in sync with the sound.
        clip = self.paras['9.5']['clip']
        self.wait_until(clip['start'] - 0.4)
        play = txt('▶ Aufnahme', size=18, color=OCHRE).next_to(frame, UP, buff=0.12).align_to(frame, LEFT)
        self.play(FadeIn(play), run_time=0.3)
        self.wait_until(clip['start'])
        ph = Line([left, bottom, 0], [left, top, 0], color=FG, stroke_width=3)
        self.add(ph)
        self.play(ph.animate.move_to([right, (top + bottom) / 2, 0]), run_time=clip['end'] - clip['start'],
                  rate_func=linear)
        self.keep.append(VGroup(frame.copy()))
        self.spec_small = img
        self.wait_until(clip['end'] + 0.3)
        self.wipe()

    # ------------------------------------------------------------ 9.6
    def p96(self):
        self.wait_until(self.t('9.6'))
        self.cite(self.cite_of('9.6'))
        h = head_profile(height=2.2).move_to([-4.6, 0.3, 0])
        self.play(Create(h), run_time=0.8)

        # Sentence 2: mouth clicks and echoes.
        self.wait_until(self.t('9.6', 1))
        mouth = h.get_right() + DOWN * 0.35 + LEFT * 0.05
        obj = Rectangle(width=0.25, height=1.4, fill_color=MUTED, fill_opacity=1, stroke_width=0).move_to([-1.3, 0.0, 0])
        clicks = VGroup(*[Arc(radius=0.3 + 0.35 * k, start_angle=-PI / 4, angle=PI / 2, color=OCHRE, stroke_width=3)
                          .move_arc_center_to(mouth) for k in range(4)])
        backs = VGroup(*[Arc(radius=0.3 + 0.35 * k, start_angle=3 * PI / 4, angle=PI / 2, color=FG, stroke_width=2.5)
                         .move_arc_center_to(obj.get_left()) for k in range(3)])
        self.play(FadeIn(obj), run_time=0.3)
        self.play(LaggedStart(*[Create(c) for c in clicks], lag_ratio=0.25), run_time=0.8)
        self.play(LaggedStart(*[Create(c) for c in backs], lag_ratio=0.25), run_time=0.7)

        # Sentence 3: two experts in the scanner – visual (calcarine) cortex active, auditory no difference.
        self.wait_until(self.t('9.6', 2))
        outline, occ, aud = brain_side(width=4.0)
        brain = VGroup(outline, occ, aud).move_to([3.4, 0.4, 0])
        bl = txt('schematisch', size=15, color=MUTED, slant=ITALIC).next_to(brain, DOWN, buff=0.1).align_to(brain, RIGHT)
        front = txt('vorn →', size=15, color=MUTED).next_to(brain, UP, buff=0.05).align_to(brain, RIGHT)
        self.play(FadeIn(brain), FadeIn(bl), FadeIn(front), run_time=0.6)
        ol = txt('Sehrinde (calcariner Kortex)', size=17, color=OCHRE).next_to(occ, LEFT, buff=0.25)
        ol.shift(DOWN * 0.95)
        al = txt('Hörkortex: kein Unterschied', size=17, color=MUTED).next_to(brain, DOWN, buff=0.5).align_to(brain, RIGHT)
        self.play_at(self.t('9.6', 2, 'Areal'), occ.animate.set_fill(OCHRE), FadeIn(ol), run_time=0.8)
        self.play_at(self.t('9.6', 2, 'Hörkortex'), Indicate(aud, color=MUTED), FadeIn(al), run_time=0.7)
        comp = txt('Klicks mit Echo vs. echofreie Kontrollgeräusche', size=16, color=MUTED).move_to([3.4, 2.65, 0])
        self.play(FadeIn(comp), run_time=0.4)

        # Sentence 4: n = 2 – a hint, not a proof.
        self.wait_until(self.t('9.6', 3))
        n2 = txt('n = 2', size=40, color=FG, weight=SEMIBOLD).move_to([-1.3, -2.3, 0])
        hint = txt('Hinweis, kein Beweis', size=20, color=MUTED).next_to(n2, RIGHT, buff=0.35)
        self.play(FadeIn(n2, scale=1.2), FadeIn(hint), run_time=0.6)

        # Sentence 5: Nagel's footnote.
        self.wait_until(self.t('9.6', 4))
        fn = txt('Nagel 1974, S. 442, Fn. 8: Blinde orten „by a form of sonar“', size=17, color=MUTED)
        fn.move_to([0, -3.05, 0])
        self.play(FadeIn(fn), run_time=0.5)
        self.keep.append(VGroup(outline.copy(), occ.copy()))
        self.wait_until(self.t('9.6', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 9.7
    def p97(self):
        self.wait_until(self.t('9.7'))
        self.cite(self.cite_of('9.7'))
        outer, inner = two_fields(height=4.4, y=-0.3)
        self.play(FadeIn(outer), FadeIn(inner), run_time=0.8)

        # Sentences 3–4: the left side has filled up.
        self.wait_until(self.t('9.7', 2))
        cells = []
        for k, m in enumerate(self.keep):
            m = m.copy()
            m.scale_to_fit_width(1.9)
            if m.height > 1.25:
                m.scale_to_fit_height(1.25)
            cells.append(m)
        grid = Group(*cells).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.35))
        grid.move_to(outer.box)
        spec = ImageMobject(SPEC).stretch_to_fit_width(1.9).stretch_to_fit_height(0.8).move_to(cells[4])
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.2), FadeIn(spec), run_time=2.0)
        full = txt('immer mehr Wissen von außen', size=18, color=OCHRE).next_to(outer.box, DOWN, buff=0.15)
        self.play(FadeIn(full), run_time=0.4)

        # Sentences 5–6: the right side has stayed empty; nothing transfers.
        self.wait_until(self.t('9.7', 4))
        probe = Arrow(outer.box.get_right() + LEFT * 0.5, inner.box.get_left() + RIGHT * 0.02, buff=0,
                      color=OCHRE, stroke_width=5)
        self.play(GrowArrow(probe), run_time=0.8)
        stop = Line(UP * 0.4, DOWN * 0.4, color=FG, stroke_width=6).move_to(inner.box.get_left() + LEFT * 0.06)
        self.play(FadeIn(stop), Indicate(inner.box, color=VIOLET, scale_factor=1.02), run_time=0.6)
        feel = txt('wie sich ein Echo für sie anfühlt: ?', size=18, color=VIOLET).next_to(inner.box, DOWN, buff=0.15)
        self.play_at(self.t('9.7', 5, 'anfühlt'), FadeIn(feel), run_time=0.5)
        self.wait_until(self.t('9.7', 'end') + 0.1)
        self.wipe()

    # ------------------------------------------------------------ 9.8
    def p98(self):
        self.wait_until(self.t('9.8'))
        self.cite('Nagel 2024, Vorwort')
        table = Line([-3.2, -0.6, 0], [3.2, -0.6, 0], color=MUTED, stroke_width=6)
        n = person(height=1.6).move_to([-2.4, 0.3, 0])
        g = person(height=1.6).move_to([2.4, 0.3, 0])
        nl = txt('Nagel', size=20, color=MUTED).next_to(n, DOWN, buff=0.6)
        gl = txt('Griffin', size=20, color=MUTED).next_to(g, DOWN, buff=0.6)
        where = txt('Rockefeller University, 1973–1974', size=20, color=MUTED).move_to([0, 2.5, 0])
        self.play(Create(table), FadeIn(n), FadeIn(g), FadeIn(nl), FadeIn(gl), FadeIn(where), run_time=0.8)
        sk = bat(width=1.0).move_to([0, -0.35, 0])
        self.play_at(self.t('9.8', 1, 'Fledermäuse'), FadeIn(sk, shift=UP * 0.1), run_time=0.5)
        shy = txt('Scheu der Biologen vor dem Thema Tierbewusstsein', size=18, color=MUTED).move_to([0, -1.9, 0])
        self.play_at(self.t('9.8', 1, 'Scheu'), FadeIn(shy), run_time=0.5)

        # Sentence 3: Griffin's 1976 book (cover designed here: title and year only).
        self.wait_until(self.t('9.8', 2))
        self.play(FadeOut(VGroup(table, n, g, nl, gl, sk, shy, where)), run_time=0.4)
        cover = RoundedRectangle(corner_radius=0.06, width=2.6, height=3.6, fill_color='#2a3242', fill_opacity=1,
                                 stroke_color=MUTED, stroke_width=2).move_to([-2.6, 0.0, 0])
        ct = txt('The Question\nof Animal\nAwareness', size=24, font=SERIF, weight=SEMIBOLD).move_to(cover).shift(UP * 0.5)
        cy = txt('Griffin · 1976', size=18, color=MUTED).next_to(ct, DOWN, buff=0.5)
        self.play(FadeIn(cover), FadeIn(ct), FadeIn(cy), run_time=0.7)
        follow = txt('laut Nagel eine Folge\ndieser Gespräche', size=20, color=FG).next_to(cover, RIGHT, buff=0.6)
        self.play(FadeIn(follow), run_time=0.5)

        # Sentence 4: Griffin's later reproach (secondary source).
        self.wait_until(self.t('9.8', 3))
        self.cite('Griffin 2001, S. 32 (nach Salzani 2022)')
        q = QuoteCard('paralytic perfectionism', 'Griffin 2001, S. 32 (nach Salzani 2022)', size=30).move_to([2.6, -1.8, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
