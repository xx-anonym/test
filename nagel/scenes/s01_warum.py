"""Kapitel 1 – Warum gerade eine Fledermaus? (Nagel 1974, S. 438; Nagel 2024, Vorwort)

1.1  Schematischer Stammbaum; die Zuschreibung von Erleben wird nach unten blasser
     (Nagels Beobachtung über uns, keine Messung). Grund 1: Säugetier.
1.2  Grund 2: Echoortung leistet, was bei uns das Sehen leistet – gleiche Liste,
     aber das Gleichheitszeichen fällt: anders in der Funktionsweise.
1.3  Beide Gründe als Achsen: nah genug, fremd genug. Dann die Entstehung: eine
     Fledermaus im Haus, Begegnung von beiden Seiten.
"""

from parts import *

# Leaves of the schematic tree, top (us) to bottom; mammals hang from one node,
# no finer topology is claimed.
LEAVES = ['Mensch', 'Maus', 'Fledermaus', 'Wal', 'Taube', 'Flunder', 'Wespe']


class Kapitel1(NarratedScene):
    CHAPTER = 1

    def construct(self):
        self.chapter_card()
        self.p11()
        self.p12()
        self.p13()
        self.finish()

    # ------------------------------------------------------------ 1.1
    def tree(self):
        x_leaf, x_lab = -1.5, -1.25
        ys = [1.85, 1.25, 0.65, 0.05, -0.75, -1.55, -2.35]
        nodes = {'mam': (-2.5, 0.95), 'amn': (-3.5, 0.1), 'ver': (-4.5, -0.73), 'root': (-5.5, -1.54)}
        lines = VGroup()

        def elbow(a, b):
            return VMobject(stroke_color=MUTED, stroke_width=3).set_points_as_corners(
                [[a[0], a[1], 0], [a[0], b[1], 0], [b[0], b[1], 0]])
        for y in ys[:4]:
            lines.add(elbow(nodes['mam'], (x_leaf, y)))
        lines.add(elbow(nodes['amn'], nodes['mam']), elbow(nodes['amn'], (x_leaf, ys[4])))
        lines.add(elbow(nodes['ver'], nodes['amn']), elbow(nodes['ver'], (x_leaf, ys[5])))
        lines.add(elbow(nodes['root'], nodes['ver']), elbow(nodes['root'], (x_leaf, ys[6])))
        labels = VGroup(*[txt(n, size=28).move_to([x_lab, y, 0], aligned_edge=LEFT) for n, y in zip(LEAVES, ys)])
        for lab, y in zip(labels, ys):
            lab.move_to([x_lab + lab.width / 2, y, 0])
        return lines, labels, ys

    def p11(self):
        self.wait_until(self.t('1.1'))
        self.cite(self.cite_of('1.1'))
        lines, labels, ys = self.tree()
        note = schematic_note(VGroup(lines, labels)).to_corner(DL, buff=0.35)
        self.play(Create(lines), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in labels], lag_ratio=0.15),
                  FadeIn(note), run_time=1.4)

        # „aus zwei Gründen“: two empty slots at the top right.
        slots = VGroup(*[VGroup(txt(f'{i}', size=24, color=OCHRE, weight=SEMIBOLD),
                                txt(t, size=24, color=MUTED))
                         .arrange(RIGHT, buff=0.25) for i, t in [(1, '…'), (2, '…')]])
        slots.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0.6, 2.95, 0], aligned_edge=LEFT)
        self.play_at(self.t('1.1', 1, 'zwei'), FadeIn(slots), run_time=0.6)

        # Reason 1: a mammal, like mice and whales.
        mam = VGroup(labels[1], labels[2], labels[3])
        brace = Brace(VGroup(*labels[:4]), RIGHT, color=OCHRE, buff=0.25)
        btxt = txt('Säugetiere', size=22, color=OCHRE).next_to(brace, RIGHT, buff=0.15)
        self.play_at(self.t('1.1', 2), labels[2].animate.set_color(OCHRE).scale(1.12), run_time=0.6)
        r1 = txt('erlebt unstrittig etwas', size=24).move_to(slots[0][1], aligned_edge=LEFT)
        self.play(Transform(slots[0][1], r1), run_time=0.5)
        self.play_at(self.t('1.1', 2, 'Säugetier'), GrowFromCenter(brace), FadeIn(btxt), run_time=0.7)
        self.play_at(self.t('1.1', 2, 'Mäuse'), Indicate(labels[1], color=FG, scale_factor=1.1),
                     Indicate(labels[3], color=FG, scale_factor=1.1), run_time=0.9)

        # Sentence 4: the further down, the fainter our faith in experience.
        glow = VGroup()
        for i, y in enumerate(ys):
            seg = Rectangle(width=0.22, height=0.66, stroke_width=0, fill_color=VIOLET,
                            fill_opacity=0.9 * (1 - i / (len(ys) - 0.5)) + 0.04)
            glow.add(seg.move_to([3.65, y, 0]))
        glabel = txt('Wie sicher sprechen wir\nErleben zu?', size=20, color=VIOLET)
        glabel.next_to(glow, RIGHT, buff=0.3).align_to(glow, UP)
        caption = txt('Nagels Beobachtung über unsere Zuschreibungen – keine Messung', size=20, color=MUTED)
        caption.next_to(glow, DOWN, buff=0.3).align_to(lines, LEFT).shift(RIGHT * 0.0)
        caption.move_to([1.2, -3.05, 0])
        self.wait_until(self.t('1.1', 3))
        self.play(Indicate(labels[6], color=MUTED), Indicate(labels[5], color=MUTED), run_time=0.9)
        self.play_at(self.t('1.1', 3, 'den Glauben'),
                     LaggedStart(*[FadeIn(s, shift=DOWN * 0.05) for s in glow], lag_ratio=0.12),
                     FadeIn(glabel), run_time=1.5)
        self.play(*[labels[i].animate.set_opacity(0.95 - 0.13 * i) for i in range(4, 7)], run_time=0.8)
        self.play_at(self.t('1.1', 3, 'hinabsteigt'), FadeIn(caption), run_time=0.6)
        bat_mark = SurroundingRectangle(labels[2], color=OCHRE, buff=0.1, corner_radius=0.06)
        self.play(Create(bat_mark), run_time=0.5)

        self.slots = slots
        self.wait_until(self.t('1.1', 'end') + 0.1)
        self.play(FadeOut(VGroup(lines, labels, note, brace, btxt, glow, glabel, caption, bat_mark)),
                  slots.animate.move_to([0, 2.75, 0]), run_time=0.55)

    # ------------------------------------------------------------ 1.2
    def p12(self):
        self.wait_until(self.t('1.2'))
        r2 = txt('nimmt die Welt per Echoortung wahr', size=24).move_to(self.slots[1][1], aligned_edge=LEFT)
        self.play(Transform(self.slots[1][1], r2), run_time=0.5)

        # Two columns: echolocating bat (left), seeing human (right).
        bx, hx = -3.3, 3.3
        b = bat(width=1.5).move_to([bx - 0.9, 1.45, 0])
        arcs = VGroup(*[Arc(radius=0.35 + 0.28 * k, start_angle=-PI / 5, angle=2 * PI / 5, color=OCHRE,
                            stroke_width=3).move_arc_center_to(b.get_right() + LEFT * 0.1) for k in range(4)])
        btitle = txt('Fledermaus: Echoortung', size=24, color=OCHRE).move_to([bx, 0.6, 0])
        e = eye(width=1.0).move_to([hx - 0.9, 1.45, 0])
        rays = VGroup(*[Line(e.get_right() + RIGHT * 1.3 + UP * dy, e.get_right() + RIGHT * 0.15 + UP * dy * 0.3,
                             color=FG, stroke_width=2.5) for dy in (-0.35, 0, 0.35)])
        htitle = txt('Mensch: Sehen', size=24, color=FG).move_to([hx, 0.6, 0])
        self.play(FadeIn(b), Create(arcs, lag_ratio=0.3), FadeIn(btitle), run_time=1.2)

        words = ['Entfernung', 'Größe', 'Form', 'Bewegung', 'Oberfläche']
        lists = []
        for x in (bx, hx):
            col = VGroup(*[txt(w, size=26) for w in words]).arrange(DOWN, buff=0.14).move_to([x, -0.85, 0])
            lists.append(col)
        for i, w in enumerate(words):
            self.play_at(self.t('1.2', 1, w), FadeIn(lists[0][i], shift=UP * 0.08), run_time=0.35)
        self.play_at(self.t('1.2', 1, 'bei uns'), FadeIn(e), Create(rays), FadeIn(htitle), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.08) for x in lists[1]], lag_ratio=0.15), run_time=0.9)

        # Sentence 3: same achievements, but the equals sign falls.
        eq = txt('=', size=90, color=FG).move_to([0, -0.85, 0])
        self.play(FadeIn(eq, scale=0.7), run_time=0.5)
        self.wait_until(self.t('1.2', 2))
        strike = Line(eq.get_corner(DL) + DL * 0.12, eq.get_corner(UR) + UR * 0.12, color=FG, stroke_width=7)
        self.play(Create(strike), run_time=0.5)
        same = txt('gleiche Leistung', size=22, color=MUTED).next_to(eq, UP, buff=0.35)
        diff = txt('anders in der Funktionsweise', size=22, color=MUTED).next_to(eq, DOWN, buff=0.35)
        self.play(FadeIn(same), FadeIn(diff), run_time=0.6)
        quote = QuoteCard(self.quote_of('1.2'), self.cite_of('1.2'), size=24).move_to([0, -2.85, 0])
        self.play(FadeIn(quote, shift=UP * 0.1), run_time=0.6)

        # Sentence 4: nothing in our experience or imagination to compare it with.
        self.wait_until(self.t('1.2', 3))
        left = VGroup(b, arcs, btitle, lists[0])
        right = VGroup(e, rays, htitle, lists[1])
        self.play(FadeOut(VGroup(eq, strike, same, diff, quote, lists[0], lists[1])), run_time=0.6)
        inner = InnerField(width=4.2, height=2.2, label='wie es sich für die Fledermaus anfühlt', seed=21)
        inner.move_to([bx, -1.3, 0])
        ours = VGroup(txt('was wir erleben', size=22), txt('oder uns vorstellen können', size=22)).arrange(DOWN, buff=0.1)
        ours.move_to([hx, -1.3, 0])
        self.play(FadeIn(inner), FadeIn(ours), run_time=0.8)
        probe = DashedLine(ours.get_left() + LEFT * 0.15, inner.box.get_right() + RIGHT * 1.0,
                           color=MUTED, stroke_width=3, dash_length=0.12)
        qm = txt('?', size=40, color=MUTED).next_to(probe, UP, buff=0.1)
        self.play_at(self.t('1.2', 3, 'irgendetwas'), Create(probe), run_time=0.9)
        self.play(FadeIn(qm), run_time=0.4)
        self.wait_until(self.t('1.2', 'end') + 0.1)
        self.play(FadeOut(VGroup(left, right, inner, ours, probe, qm)), run_time=0.55)

    # ------------------------------------------------------------ 1.3
    def p13(self):
        self.wait_until(self.t('1.3'))
        # The two reasons become two axes.
        origin = np.array([-3.6, -2.2, 0])
        xa = Arrow(origin, origin + RIGHT * 7.4, buff=0, color=MUTED, stroke_width=3)
        ya = Arrow(origin, origin + UP * 4.3, buff=0, color=MUTED, stroke_width=3)
        xl = txt('Sinnesapparat uns fremd →', size=22, color=OCHRE).next_to(xa, DOWN, buff=0.15).align_to(xa, RIGHT)
        yl = txt('Erleben zugeschrieben →', size=22, color=VIOLET).rotate(PI / 2).next_to(ya, LEFT, buff=0.15)
        yl.align_to(ya, UP)
        self.play(FadeOut(self.slots, shift=UP * 0.2), GrowArrow(xa), GrowArrow(ya), FadeIn(xl), FadeIn(yl),
                  run_time=0.9)
        pts = {
            'Mensch': (person(height=0.6), origin + np.array([0.7, 3.5, 0])),
            'Stein': (stone(width=0.6), origin + np.array([0.7, 0.85, 0])),
            'Fledermaus': (bat(width=0.9), origin + np.array([6.4, 3.3, 0])),
        }
        marks = VGroup()
        for name, (icon, p) in pts.items():
            icon.move_to(p)
            lab = txt(name, size=20, color=MUTED).next_to(icon, DOWN, buff=0.12)
            marks.add(VGroup(icon, lab))
        note = schematic_note(marks).to_corner(DL, buff=0.35)
        self.play(FadeIn(marks[0]), FadeIn(marks[1]), FadeIn(note), run_time=0.6)
        self.play_at(self.t('1.3', 0, 'nah genug'), FadeIn(marks[2], scale=0.8), run_time=0.6)
        near = DashedLine(marks[2].get_center() + LEFT * 0.7, [origin[0] + 0.05, marks[2].get_y(), 0],
                          color=VIOLET, stroke_width=2)
        far = DashedLine(marks[2].get_bottom() + DOWN * 0.1, [marks[2].get_x(), origin[1] + 0.05, 0],
                         color=OCHRE, stroke_width=2)
        self.play(Create(near), run_time=0.6)
        self.play_at(self.t('1.3', 0, 'fremd genug'), Create(far), run_time=0.6)
        chart = VGroup(xa, ya, xl, yl, marks, near, far, note)

        # Sentence 2: the origin story (Nagel 2024, preface).
        self.wait_until(self.t('1.3', 1))
        self.cite(self.cite_of('1.3'))
        self.play(FadeOut(chart), run_time=0.6)
        house = VGroup(
            Polygon([-3.2, -2.3, 0], [3.2, -2.3, 0], [3.2, 0.9, 0], [0, 2.7, 0], [-3.2, 0.9, 0],
                    stroke_color=MUTED, stroke_width=3, fill_opacity=0),
            Rectangle(width=1.0, height=1.0, stroke_color=DIM, stroke_width=2).move_to([-2.35, 0.1, 0]),
        )
        place = txt('Landhaus in Pennsylvania, frühe 1970er', size=22, color=MUTED).next_to(house, DOWN, buff=0.2)
        self.play_at(self.t('1.3', 1, 'In den frühen'), Create(house), FadeIn(place), run_time=1.2)
        rafter = VGroup(*[bat(width=0.45, color=DIM).rotate(PI).move_to([x, 1.75 - abs(x) * 0.55, 0])
                          for x in (-1.4, -0.9, 0.9)])
        self.play(FadeIn(rafter), run_time=0.6)

        # Sentence 3: one gets into the house – the same size as the human.
        self.wait_until(self.t('1.3', 2))
        h = person(height=1.6).move_to([-1.4, -1.45, 0])
        b = bat(width=1.6).move_to([1.4, -0.9, 0])
        self.play(FadeIn(h), FadeIn(b, shift=LEFT * 0.4), run_time=0.8)
        q1 = txt('?', size=48, color=OCHRE).next_to(h, UP, buff=0.15)
        self.play_at(self.t('1.3', 2, 'fremden'), FadeIn(q1, shift=UP * 0.1), run_time=0.5)
        # Sentence 4: the bat felt the same.
        q2 = txt('?', size=48, color=OCHRE).next_to(b, UP, buff=0.15)
        self.play_at(self.t('1.3', 3, 'genauso'), FadeIn(q2, shift=UP * 0.1), run_time=0.5)
