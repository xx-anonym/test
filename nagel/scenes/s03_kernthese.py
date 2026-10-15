"""Kapitel 3 – Die Kernthese (Nagel 1974, S. 436–437, 440 Fn. 6, 436 Fn. 2).

3.1  Nagels Definition baut sich Zeile für Zeile auf; der Teil „für ihn selbst“
     ist der subjektive Charakter.
3.2  Zwei Lesarten von „wie es ist“: Vergleich (verworfen) und „wie es für das
     Wesen selbst ist“; Stein ohne, Fledermaus mit Innenfeld.
3.3  Leitmotiv: dieselbe funktionale Beschreibung (links) für Mensch und
     Roboter; die rechte Seite ist dadurch nicht festgelegt.
3.4  Fußnote 2: Vielleicht hätte der Roboter doch Erfahrungen – das entscheidet
     keine Begriffsanalyse; Verweis auf Kapitel 11.
"""

from kit import *


def check(color=GREEN, size=0.32):
    m = VMobject(stroke_color=color, stroke_width=7)
    m.set_points_as_corners([LEFT * 0.5 + UP * 0.05, DOWN * 0.42 + LEFT * 0.12, RIGHT * 0.55 + UP * 0.5])
    return m.scale(size / 0.5)


def cross(mob, color=RED):
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=6),
                  Line(mob.get_corner(DL), mob.get_corner(UR), color=color, stroke_width=6))


def magnifier(color=FG):
    ring = Circle(radius=0.26, stroke_color=color, stroke_width=5)
    handle = Line(ring.point_at_angle(-PI / 4), ring.point_at_angle(-PI / 4) + (DOWN + RIGHT) * 0.24,
                  color=color, stroke_width=7)
    return VGroup(ring, handle)


class Kapitel3(NarratedScene):
    CHAPTER = 3

    def construct(self):
        self.chapter_card()
        self.p31()
        self.p32()
        self.p33()
        self.p34()
        self.finish()

    # ------------------------------------------------------------ 3.1
    def p31(self):
        self.wait_until(self.t('3.1'))
        self.cite(self.cite_of('3.1'))
        l1 = txt('Ein Organismus hat bewusste Zustände', size=40)
        l2 = txt('genau dann, wenn', size=30, color=OCHRE, weight=MEDIUM)
        l3 = txt('es irgendwie ist, dieser Organismus zu sein', size=40)
        l4 = txt('– irgendwie für ihn selbst.', size=40, color=VIOLET, weight=MEDIUM)
        lines = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.3).move_to(UP * 1.65)
        self.play_at(self.t('3.1', 0, 'Ein Organismus'), Write(l1), run_time=1.3)
        self.play_at(self.t('3.1', 0, 'genau dann'), FadeIn(l2, shift=DOWN * 0.1), run_time=0.6)
        self.play_at(self.t('3.1', 0, 'wenn es irgendwie'), Write(l3), run_time=1.3)
        self.play_at(self.t('3.1', 0, 'irgendwie für den'), Write(l4), run_time=1.0)

        quote = QuoteCard(self.quote_of('3.1'), self.cite_of('3.1')).move_to(DOWN * 1.85)
        self.play(FadeIn(quote, shift=UP * 0.15), run_time=0.6)

        # Sentence 2: the inner part gets its name.
        frame = SurroundingRectangle(l4, color=VIOLET, buff=0.14, corner_radius=0.08, stroke_width=2.5)
        name = txt('= der subjektive Charakter der Erfahrung', size=28, color=VIOLET)
        name.next_to(frame, DOWN, buff=0.22)
        self.wait_until(self.t('3.1', 1, 'subjektiven'))
        self.play(Create(frame), run_time=0.6)
        self.play(FadeIn(name, shift=UP * 0.1), run_time=0.6)

        # Gap: the definition shrinks into a header for the rest of the chapter.
        self.header = txt('bewusst = es ist irgendwie, dieses Wesen zu sein – für es selbst', size=21,
                          color=MUTED, t2c={'für es selbst': VIOLET}).move_to(UP * 3.05)
        self.wait_until(self.t('3.1', 1, end=True) + 0.15)
        self.play(FadeOut(VGroup(lines, frame, name, quote), shift=UP * 0.3), FadeIn(self.header, shift=UP * 0.2),
                  run_time=0.7)

    # ------------------------------------------------------------ 3.2
    def p32(self):
        self.wait_until(self.t('3.2'))
        self.cite(self.cite_of('3.2'))
        h_left = txt('wie es ist = wem es ähnelt', size=28)
        h_right = txt('wie es ist = wie es für\ndas Wesen selbst ist', size=28)
        h_left.move_to(LEFT * 3.5 + UP * 1.75)
        h_right.move_to(RIGHT * 3.5 + UP * 1.75)

        # Left: comparing the bat's experience with ours.
        b1 = bat(width=1.7).move_to(LEFT * 4.9 + DOWN * 0.1)
        approx = txt('≈ ?', size=40, color=MUTED).move_to(LEFT * 3.5 + DOWN * 0.1)
        p1 = person(height=1.15).move_to(LEFT * 2.1 + DOWN * 0.1)
        left = VGroup(h_left, b1, approx, p1)

        # Right: the bat with its own inner field.
        b2 = bat(width=1.7).move_to(RIGHT * 3.5 + DOWN * 0.45)
        own = InnerField(width=1.9, height=0.8, label='', seed=11).next_to(b2, UP, buff=0.12)
        right = VGroup(h_right, b2, own)

        self.play(FadeIn(h_left), FadeIn(h_right), run_time=0.6)
        self.play(FadeIn(VGroup(b1, approx, p1)), FadeIn(VGroup(b2, own)), run_time=0.8)

        x = cross(VGroup(b1, approx, p1).copy().scale(1.05))
        self.play_at(self.t('3.2', 1, 'kein Vergleich'), Create(x), left.animate.set_opacity(0.35), run_time=0.7)
        tick = check().next_to(h_right, LEFT, buff=0.25)
        quote = QuoteCard(self.quote_of('3.2'), self.cite_of('3.2')).move_to(DOWN * 1.95)
        self.play_at(self.t('3.2', 1, 'sondern'), Create(tick), FadeIn(quote, shift=UP * 0.15), run_time=0.7)

        # Stone and bat.
        self.wait_until(self.t('3.2', 2) - 0.45)
        self.play(FadeOut(VGroup(left, x, right, tick, quote)), run_time=0.45)
        st = stone(width=1.5).move_to(LEFT * 3.3 + DOWN * 0.7)
        st_field = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=2.2, height=1.0, stroke_color=MUTED,
                                                   stroke_width=2), num_dashes=40).next_to(st, UP, buff=0.3)
        st_none = txt('—', size=34, color=MUTED).move_to(st_field)
        st_lab = txt('Stein', size=22, color=MUTED).next_to(st, DOWN, buff=0.25)
        b3 = bat(width=2.0).move_to(RIGHT * 3.3 + DOWN * 0.7)
        b3_field = InnerField(width=2.2, height=1.0, label='', seed=5).next_to(b3, UP, buff=0.3)
        b3_lab = txt('Fledermaus', size=22, color=MUTED).next_to(b3, DOWN, buff=0.25)
        self.play_at(self.t('3.2', 2, 'Von einem Stein'), FadeIn(st), FadeIn(st_lab), run_time=0.5)
        self.play(Create(st_field), FadeIn(st_none), run_time=0.7)
        self.play_at(self.t('3.2', 2, 'von einer Fledermaus'), FadeIn(b3), FadeIn(b3_lab), run_time=0.5)
        self.play(GrowFromCenter(b3_field), run_time=0.7)
        self.stone_bat = VGroup(st, st_field, st_none, st_lab, b3, b3_field, b3_lab)

    # ------------------------------------------------------------ 3.3
    def p33(self):
        self.wait_until(self.t('3.3') - 0.5)
        self.play(FadeOut(self.stone_bat), run_time=0.45)
        self.cite(self.cite_of('3.3'))
        ya, yb = 0.95, -1.3
        outer_a = OuterField(width=5.5, height=1.75, label='von außen: Funktion').move_to(LEFT * 1.55 + UP * ya)
        inner_a = InnerField(width=3.6, height=1.75, label='für das Wesen selbst', seed=21)
        inner_a.move_to(RIGHT * 3.55 + UP * ya)
        human = person(height=1.15).move_to(LEFT * 5.75 + UP * ya)
        outer_a.label.align_to(outer_a.box, LEFT)
        inner_a.label.align_to(inner_a.box, LEFT)
        self.play(FadeIn(human), Create(outer_a.box), FadeIn(outer_a.label), FadeIn(inner_a), run_time=0.9)

        fa = function_box(scale=0.82).move_to(outer_a.box)
        self.play_at(self.t('3.3', 1, 'Analysen'), FadeIn(fa, lag_ratio=0.15), run_time=1.0)

        # The same functional description, a second time.
        outer_b = OuterField(width=5.5, height=1.75, label='').move_to(LEFT * 1.55 + UP * yb)
        inner_b_box = RoundedRectangle(corner_radius=0.1, width=3.6, height=1.75, stroke_color=VIOLET,
                                       stroke_width=2.2, fill_color=INNER, fill_opacity=1).move_to(RIGHT * 3.55 + UP * yb)
        fb = fa.copy().move_to(outer_b.box)
        same = txt('=', size=40, color=OCHRE).move_to(LEFT * 1.55 + UP * ((ya + yb) / 2))
        self.play_at(self.t('3.3', 1, 'dass genau'), Create(outer_b.box), FadeIn(inner_b_box), run_time=0.6)
        self.play(TransformFromCopy(fa, fb), FadeIn(same), run_time=1.1)

        bot = robot(height=1.15).move_to(LEFT * 5.75 + UP * yb)
        self.play_at(self.t('3.3', 2, 'Robotern'), FadeIn(bot, shift=RIGHT * 0.15), run_time=0.6)
        q = txt('?', size=72, color=VIOLET, weight=BOLD).move_to(inner_b_box)
        self.play_at(self.t('3.3', 2, 'aber nichts'), FadeIn(q, scale=0.6), run_time=0.6)

        tick = check(size=0.26).next_to(outer_a.label, RIGHT, buff=0.2)
        self.play_at(self.t('3.3', 3, 'bestreitet nicht'), Create(tick), run_time=0.6)
        self.play_at(self.t('3.3', 3, 'funktional'), Indicate(fa, color=OCHRE, scale_factor=1.06), run_time=1.0)

        quote = QuoteCard(self.quote_of('3.3'), 'Nagel 1974, S. 437').move_to(UP * 3.0 + RIGHT * 0.9)
        self.play_at(self.t('3.3', 4), FadeOut(self.header), FadeIn(quote, shift=DOWN * 0.1), run_time=0.6)
        self.play_at(self.t('3.3', 4, 'erschöpft'), Indicate(inner_a.box, color=VIOLET, scale_factor=1.04),
                     run_time=1.0)

        # Leaving the inner side out: the field empties, the problem is mis-posed.
        gone = DashedVMobject(inner_a.box.copy().set_fill(opacity=0).set_stroke(RED, 2.2), num_dashes=60)
        left_out = txt('weggelassen', size=24, color=RED, weight=MEDIUM).move_to(inner_a.box).shift(UP * 0.42)
        wrong = txt('→ Problem\nfalsch gestellt', size=21, color=RED).move_to(inner_a.box).shift(DOWN * 0.22)
        self.play_at(self.t('3.3', 5, 'subjektiven'), FadeOut(inner_a.box), FadeOut(inner_a.grain), FadeIn(gone),
                     FadeIn(left_out), run_time=0.7)
        self.play_at(self.t('3.3', 5, 'stellt'), FadeIn(wrong, shift=UP * 0.08), run_time=0.5)
        self.rows = dict(human=human, outer_a=outer_a, inner_a=inner_a, fa=fa, tick=tick, same=same,
                         bot=bot, outer_b=outer_b, inner_b=inner_b_box, fb=fb, q=q,
                         undo=(gone, left_out, wrong, quote))

    # ------------------------------------------------------------ 3.4
    def p34(self):
        r = self.rows
        self.wait_until(self.t('3.4'))
        gone, left_out, wrong, quote = r['undo']
        self.play(FadeOut(VGroup(gone, left_out, wrong, quote)), FadeIn(r['inner_a'].box), FadeIn(r['inner_a'].grain),
                  FadeIn(self.header), run_time=0.6)
        self.cite(self.cite_of('3.4'))
        row_a = VGroup(r['human'], r['outer_a'], r['inner_a'], r['fa'], r['tick'], r['same'])
        veil = Rectangle(width=row_a.width + 0.4, height=row_a.height + 0.25, fill_color=BG, fill_opacity=0.72,
                         stroke_width=0).move_to(row_a)
        self.play(FadeIn(veil), run_time=0.6)

        note = txt('Fußnote 2', size=20, color=OCHRE, weight=MEDIUM).next_to(r['bot'], UP, buff=0.22)
        self.play_at(self.t('3.4', 1, 'Fußnote'), FadeIn(note, shift=DOWN * 0.1), run_time=0.5)
        maybe = grain(r['inner_b'], n=190, seed=33)
        self.play_at(self.t('3.4', 1, 'hätte alles'), FadeIn(maybe), run_time=1.6)
        vielleicht = txt('vielleicht', size=22, color=VIOLET).next_to(r['q'], DOWN, buff=0.08)
        self.play(FadeIn(vielleicht), run_time=0.4)

        lens = magnifier().move_to(r['outer_b'].box.get_left() + RIGHT * 0.6)
        self.play_at(self.t('3.4', 2, 'Analyse'), FadeIn(lens), run_time=0.4)
        self.play(lens.animate.move_to(r['outer_b'].box.get_right() + LEFT * 0.6), run_time=1.6)
        verdict = txt('Begriffsanalyse entscheidet das nicht', size=20, color=MUTED)
        verdict.next_to(r['fb'], DOWN, buff=0.2)
        self.play(FadeOut(lens), FadeIn(verdict), run_time=0.5)

        pill_text = txt('→ Kapitel 11', size=20, color=BG, weight=SEMIBOLD)
        pill = VGroup(RoundedRectangle(corner_radius=0.17, width=pill_text.width + 0.4, height=0.38,
                                       fill_color=OCHRE, fill_opacity=1, stroke_width=0), pill_text)
        pill_text.move_to(pill[0])
        pill.move_to(r['inner_b'].get_corner(UR) + LEFT * 0.75 + DOWN * 0.02)
        self.play_at(self.t('3.4', 3, 'künstlichen'), FadeIn(pill, scale=0.8), run_time=0.5)
