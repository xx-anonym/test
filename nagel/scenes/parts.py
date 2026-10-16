"""Reusable pictures for several chapters: the argument tree, the year axis,
the dusk landscape with the flying bat, sound rings, and small icons."""

import numpy as np

from kit import *

# ------------------------------------------------------------ small icons


def check(color=GREEN, size=0.32):
    m = VMobject(stroke_color=color, stroke_width=7)
    m.set_points_as_corners([LEFT * 0.5 + UP * 0.05, DOWN * 0.42 + LEFT * 0.12, RIGHT * 0.55 + UP * 0.5])
    return m.scale(size / 0.5)


def cross(mob, color=RED, width=6):
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=width),
                  Line(mob.get_corner(DL), mob.get_corner(UR), color=color, stroke_width=width))


def magnifier(color=FG):
    ring = Circle(radius=0.26, stroke_color=color, stroke_width=5)
    handle = Line(ring.point_at_angle(-PI / 4), ring.point_at_angle(-PI / 4) + (DOWN + RIGHT) * 0.24,
                  color=color, stroke_width=7)
    return VGroup(ring, handle)


def pill(text, color=OCHRE, text_color=BG, size=20):
    t = txt(text, size=size, color=text_color, weight=SEMIBOLD)
    cap = txt('H', size=size, weight=SEMIBOLD).height
    box = RoundedRectangle(corner_radius=0.17, width=t.width + 0.4, height=cap + 0.32,
                           fill_color=color, fill_opacity=1, stroke_width=0)
    # centre on the cap height, so words with and without descenders sit level
    t.move_to(box).align_to(box.get_top() + DOWN * 0.16, UP)
    return VGroup(box, t)


def eye(color=FG, width=1.2):
    top = ArcBetweenPoints(LEFT, RIGHT, angle=-PI / 2.2)
    bottom = ArcBetweenPoints(RIGHT, LEFT, angle=-PI / 2.2)
    outline = VMobject(stroke_color=color, stroke_width=4)
    outline.set_points(np.concatenate([top.points, bottom.points]))
    iris = Circle(radius=0.3, stroke_color=color, stroke_width=4)
    pupil = Dot(radius=0.12, color=color)
    return VGroup(outline, iris, pupil).scale_to_fit_width(width)


def sound(color=FG, height=1.2):
    """Sound symbol: a source with three wave arcs."""
    src = Dot(radius=0.09, color=color)
    arcs = VGroup(*[Arc(radius=r, start_angle=-PI / 4, angle=PI / 2, stroke_color=color, stroke_width=5)
                    for r in (0.3, 0.55, 0.8)])
    return VGroup(src, arcs).scale_to_fit_height(height)


def insect(color='#cdbf9f', size=0.3):
    """A small moth seen from above: swept-back triangular wings, unlike the bat."""
    body = Ellipse(width=0.07, height=0.34, fill_color=color, fill_opacity=1, stroke_width=0)
    wl = Polygon([-0.02, 0.1, 0], [-0.26, -0.16, 0], [-0.05, -0.12, 0],
                 fill_color=color, fill_opacity=0.75, stroke_width=0)
    wr = wl.copy().flip(UP, about_point=ORIGIN)
    feelers = VGroup(*[Line([0, 0.15, 0], [sx * 0.08, 0.27, 0], stroke_width=1.5, color=color) for sx in (-1, 1)])
    return VGroup(wl, wr, body, feelers).scale_to_fit_width(size)


def ring(center, radius, color=OCHRE, width=3, opacity=1.0):
    return Circle(radius=radius, stroke_color=color, stroke_width=width, stroke_opacity=opacity).move_to(center)


def schematic_note(mob, text='schematisch'):
    return txt(text, size=16, color=MUTED, slant=ITALIC).next_to(mob, DOWN, buff=0.12, aligned_edge=RIGHT)


# ------------------------------------------------------------ argument tree
# Node id: (column, y, short label, page in Nagel 1974). See research/argument.md.
TREE = {
    'D1': (0, 2.75, 'Definition: es ist irgendwie, O zu sein', '436'),
    'D2': (0, 2.0, '„wie es ist“ meint keine Ähnlichkeit', '440'),
    'P2': (0, 1.1, 'Fledermäuse erleben etwas', '438'),
    'P3': (0, 0.35, 'Sonar gleicht keinem unserer Sinne', '438'),
    'P4': (0, -0.4, 'Vorstellung nur aus eigener Erfahrung', '439'),
    'P6': (0, -1.3, 'Physikalisches ist objektiv', '442'),
    'P8': (0, -2.05, 'Standpunkt = Wesen der Innenwelt', '445'),
    'P1': (1, 2.375, 'Analysen vereinbar mit dem Fehlen', '436 f.'),
    'Z2': (1, 0.35, 'nur schematische Vorstellung', '439'),
    'P7': (1, -1.3, 'Reduktion = mehr Objektivität', '443 f.'),
    'Z1': (2, 2.375, 'Analysen erschöpfen es nicht', '437'),
    'P5': (2, 0.35, 'Realismus über das Subjektive', '440 f.'),
    'Z3': (3, 0.35, 'Tatsachen an Standpunkt gebunden', '441 f.'),
    'Z4': (3, -1.3, 'Objektivierung entfernt vom Erleben', '444 f.'),
    'Z5': (4, 1.15, 'keine verfügbare Konzeption', '445'),
    'K': (4, -0.45, 'Physikalismus unverständlich, nicht falsch', '446'),
}
TREE_EDGES = [('D1', 'P1'), ('D2', 'P1'), ('P1', 'Z1'), ('Z1', 'Z5'), ('P2', 'Z2'), ('P3', 'Z2'),
              ('P4', 'Z2'), ('Z2', 'P5'), ('P5', 'Z3'), ('Z3', 'Z4'), ('P6', 'P7'), ('P7', 'Z4'),
              ('P8', 'Z4'), ('Z4', 'Z5'), ('Z5', 'K')]
COLX = [-5.55, -2.62, 0.3, 3.2, 5.8]


def _kind_color(nid):
    return {'D': VIOLET, 'P': FG, 'Z': OCHRE, 'K': FG}[nid[0]]   # green is reserved for counter-arguments


class ArgTree(VGroup):
    """Nagel's argument as a left-to-right tree.

    mini=True gives a small map with ids only (for the corner in chapter 4).
    Nodes and edges are built up front; scenes reveal them one by one.
    """

    def __init__(self, mini=False):
        super().__init__()
        self.mini = mini
        self.nodes, self.edges = {}, {}
        for nid, (col, y, label, page) in TREE.items():
            pos = self.pos(col, y)
            if mini:
                box = RoundedRectangle(corner_radius=0.06, width=0.66, height=0.28, fill_color=PANEL,
                                       fill_opacity=1, stroke_color=_kind_color(nid), stroke_width=1.6)
                ident = txt(nid, size=14, color=_kind_color(nid), weight=SEMIBOLD).move_to(box)
                node = VGroup(box, ident)
            else:
                w = 2.42 if col < 4 else 2.55
                box = RoundedRectangle(corner_radius=0.07, width=w, height=0.64, fill_color=PANEL,
                                       fill_opacity=1, stroke_color=_kind_color(nid), stroke_width=2)
                ident = txt(nid, size=18, color=_kind_color(nid), weight=SEMIBOLD)
                pg = txt(f'S. {page}', size=11, color=MUTED)
                head = VGroup(ident, pg).arrange(DOWN, buff=0.04)
                lab = txt(label, size=13, color=FG, width=24)
                body = VGroup(head, lab).arrange(RIGHT, buff=0.14)
                if body.width > w - 0.16:
                    body.scale_to_fit_width(w - 0.16)
                if body.height > box.height - 0.1:      # three-line labels (K) get a taller box
                    box.stretch_to_fit_height(body.height + 0.14)
                body.move_to(box)
                node = VGroup(box, body)
            node.move_to(pos)
            self.nodes[nid] = node
        for a, b in TREE_EDGES:
            na, nb = self.nodes[a], self.nodes[b]
            start, end = self._ports(na, nb)
            arr = Arrow(start, end, buff=0.03, stroke_width=1.6 if mini else 2.4, color=DIM if mini else MUTED,
                        max_tip_length_to_length_ratio=0.12 if mini else 0.08,
                        tip_length=0.08 if mini else 0.14)
            self.edges[(a, b)] = arr
        self.add(*self.edges.values(), *self.nodes.values())

    def pos(self, col, y):
        if self.mini:
            return np.array([COLX[col] * 0.35 - 4.45, y * 0.46 + 1.9, 0])
        return np.array([COLX[col], y, 0])

    @staticmethod
    def _ports(na, nb):
        a, b = na.get_center(), nb.get_center()
        if abs(a[0] - b[0]) < 0.2:  # same column: vertical
            return (na.get_bottom(), nb.get_top()) if a[1] > b[1] else (na.get_top(), nb.get_bottom())
        return na.get_right(), nb.get_left()

    def incoming(self, nid, shown):
        return [e for (a, b), e in self.edges.items() if b == nid and a in shown]

    def outgoing(self, nid, shown):
        return [e for (a, b), e in self.edges.items() if a == nid and b in shown]

    def caption(self, nid, size=22):
        col, y, label, page = TREE[nid]
        return VGroup(txt(nid, size=size, color=_kind_color(nid), weight=SEMIBOLD),
                      txt(label, size=size, color=FG),
                      txt(f'S. {page}', size=size - 4, color=MUTED)).arrange(RIGHT, buff=0.2)


def reveal(scene, tree, ids, shown, run_time=0.8, flash=True):
    """Add nodes (and edges from already shown nodes) to the scene."""
    anims = []
    for nid in ids:
        node = tree.nodes[nid]
        anims.append(FadeIn(node, scale=0.85))
        for e in tree.incoming(nid, shown | set(ids)):
            anims.append(Create(e))
        for e in tree.outgoing(nid, shown):
            anims.append(Create(e))
    scene.play(*anims, run_time=run_time)
    shown |= set(ids)
    if flash:
        scene.play(*[Indicate(tree.nodes[n], scale_factor=1.15, color=_kind_color(n)) for n in ids], run_time=0.6)


def attack(tree, nid, label, direction=UP, color=RED, length=1.0):
    """A red objection arrow pointing at a node, with the objector's name."""
    node = tree.nodes[nid]
    tip = node.get_edge_center(direction)
    start = tip + direction * length
    arr = Arrow(start, tip, buff=0.04, color=color, stroke_width=5, max_tip_length_to_length_ratio=0.3)
    lab = txt(label, size=18, color=color, weight=SEMIBOLD).next_to(start, direction, buff=0.08)
    return VGroup(arr, lab)


# ------------------------------------------------------------ year axis
def year_x(year, x0=-6.2, x1=6.2, y0=1900, y1=2030):
    return x0 + (x1 - x0) * (year - y0) / (y1 - y0)


class YearAxis(VGroup):
    def __init__(self, years, y=-1.6, x0=-6.2, x1=6.2, y0=1900, y1=2030):
        line = Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=3)
        ticks = VGroup()
        self.at = {}
        last = None
        for yr in sorted(years):
            x = year_x(yr, x0, x1, y0, y1)
            self.at[yr] = np.array([x, y, 0])
            # Labels of close years alternate below/above the axis.
            below = last is None or x - last[0] > 0.7 or not last[1]
            ly = y - 0.32 if below else y + 0.32
            ticks.add(VGroup(Line([x, y - 0.08, 0], [x, y + 0.08, 0], color=MUTED, stroke_width=3),
                             txt(str(yr), size=18, color=MUTED).move_to([x, ly, 0])))
            last = (x, below)
        super().__init__(line, ticks)
        self.ticks = ticks


def year_card(title, sub, color=FG, width=None):
    t = txt(title, size=22, color=color, weight=SEMIBOLD)
    s = txt(sub, size=16, color=MUTED, width=width or 30)
    body = VGroup(t, s).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    box = RoundedRectangle(corner_radius=0.07, width=body.width + 0.36, height=body.height + 0.26,
                           fill_color=PANEL, fill_opacity=1, stroke_color=color, stroke_width=1.6)
    body.move_to(box)
    return VGroup(box, body)


# ------------------------------------------------------------ dusk landscape
def dusk(seed=4):
    """Night sky, moon, stars, a line of hills and tree silhouettes."""
    rng = np.random.default_rng(seed)
    sky = Rectangle(width=14.3, height=8.1, fill_color=BG, fill_opacity=1, stroke_width=0)
    glow = Rectangle(width=14.3, height=2.2, stroke_width=0, fill_opacity=1)
    glow.set_fill(color=[BG, '#1a2030'], opacity=1)
    glow.set_sheen_direction(DOWN).move_to(DOWN * 1.9)
    stars = VGroup(*[Dot([rng.uniform(-7, 7), rng.uniform(0.6, 3.9), 0], radius=rng.uniform(0.008, 0.02),
                         color=FG, fill_opacity=rng.uniform(0.2, 0.7)) for _ in range(70)])
    moon = Circle(radius=0.42, fill_color='#e9e2cf', fill_opacity=0.9, stroke_width=0).move_to([4.6, 2.7, 0])
    xs = np.linspace(-7.3, 7.3, 40)
    hill = [np.array([x, -2.5 + 0.35 * np.sin(x * 0.7) + 0.15 * np.sin(x * 2.1), 0]) for x in xs]
    ground = Polygon(*hill, [7.3, -4.2, 0], [-7.3, -4.2, 0], fill_color='#0a0d13', fill_opacity=1, stroke_width=0)
    trees = VGroup()
    for x, h in [(-6.1, 1.6), (-5.3, 1.1), (-2.2, 1.9), (2.8, 1.3), (5.9, 2.1), (6.6, 1.4)]:
        base = -2.5 + 0.35 * np.sin(x * 0.7) + 0.15 * np.sin(x * 2.1)
        trunk = Rectangle(width=0.1, height=h * 0.35, fill_color='#090c11', fill_opacity=1, stroke_width=0)
        trunk.move_to([x, base + h * 0.17, 0])
        crown = VGroup(*[Circle(radius=h * r, fill_color='#090c11', fill_opacity=1, stroke_width=0).move_to(
            [x + dx * h, base + h * (0.55 + dy), 0]) for r, dx, dy in
            [(0.32, 0, 0.1), (0.25, -0.2, -0.05), (0.25, 0.2, -0.05), (0.22, 0, 0.35)]])
        trees.add(VGroup(trunk, crown))
    return VGroup(sky, glow, stars, moon, ground, trees)


class Flyer(VGroup):
    """A flapping bat whose position follows a ValueTracker along a path."""

    def __init__(self, path, tracker, width=0.75, flap_hz=7.0):
        self.base = bat(width=width)
        super().__init__(self.base.copy())
        self.path, self.tracker, self.flap_hz = path, tracker, flap_hz
        self.clock = 0.0
        self.add_updater(self._update)

    def _update(self, mob, dt):
        self.clock += dt
        s = 1.0 - 0.45 * (0.5 + 0.5 * np.sin(TAU * self.flap_hz * self.clock))
        pos = self.path.point_from_proportion(min(max(self.tracker.get_value(), 0), 1))
        new = self.base.copy().stretch(s, 1).move_to(pos)
        mob[0].become(new)

    @property
    def pos(self):
        return self.path.point_from_proportion(min(max(self.tracker.get_value(), 0), 1))


# ------------------------------------------------------------ the two fields
def two_fields(left_label='von außen', right_label='für die Fledermaus', height=4.2, y=-0.15):
    outer = OuterField(width=6.6, height=height, label=left_label).move_to([-3.45, y, 0])
    inner = InnerField(width=6.0, height=height, label=right_label, seed=17).move_to([3.6, y, 0])
    outer.label.align_to(outer.box, LEFT)
    inner.label.align_to(inner.box, LEFT)
    return outer, inner


# ------------------------------------------------------------ science icons
def water_drop(color='#6fa8d6', height=0.9):
    pts = [np.array([0.5 * np.sin(a) * (1 - np.cos(a)) * 0.9, -np.cos(a) * 0.62 + 0.0, 0])
           for a in np.linspace(0, TAU, 40)]
    d = VMobject(fill_color=color, fill_opacity=0.9, stroke_width=0).set_points_smoothly(pts)
    return d.rotate(PI).scale_to_fit_height(height)


def molecule_h2o(height=0.9):
    o = Circle(radius=0.32, fill_color='#d9695f', fill_opacity=1, stroke_width=0)
    hs = VGroup()
    for ang in (-PI / 2 + 0.91, -PI / 2 - 0.91):        # 104.5° between the bonds
        p = np.array([np.cos(ang), np.sin(ang), 0]) * 0.46
        hs.add(Circle(radius=0.2, fill_color=FG, fill_opacity=1, stroke_width=0).move_to(p))
    lab = VGroup(txt('O', size=20, color=BG, weight=BOLD).move_to(o),
                 *[txt('H', size=16, color=BG, weight=BOLD).move_to(h) for h in hs])
    return VGroup(hs, o, lab).scale_to_fit_height(height)


def lightning(color=OCHRE, height=1.0):
    bolt = Polygon([0.1, 0.5, 0], [-0.18, 0.02, 0], [0.0, 0.02, 0], [-0.12, -0.5, 0], [0.2, 0.1, 0],
                   [0.02, 0.1, 0], [0.22, 0.5, 0], fill_color=color, fill_opacity=1, stroke_width=0)
    return bolt.scale_to_fit_height(height)


def charges(width=1.6, n=6, color=OCHRE):
    wire = Line(LEFT * width / 2, RIGHT * width / 2, color=DIM, stroke_width=10)
    dots = VGroup(*[Dot(wire.point_from_proportion((k + 0.5) / n), radius=0.06, color=color) for k in range(n)])
    arrow = Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=color, stroke_width=3).next_to(wire, DOWN, buff=0.12)
    return VGroup(wire, dots, arrow)


def neuron(color=FG, size=1.0):
    soma = Circle(radius=0.16, fill_color=color, fill_opacity=1, stroke_width=0)
    dend = VGroup(*[Line(ORIGIN, 0.42 * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=3)
                    for a in (0.6, 1.5, 2.4, 3.3)])
    axon = Line(ORIGIN, [0.0, -0.75, 0], color=color, stroke_width=3)
    term = VGroup(*[Line([0, -0.75, 0], [dx, -0.9, 0], color=color, stroke_width=3) for dx in (-0.12, 0.12)])
    return VGroup(dend, axon, term, soma).scale(size)


def chip(color=FG, size=1.0):
    body = Square(0.62, fill_color=PANEL, fill_opacity=1, stroke_color=color, stroke_width=3)
    core = Square(0.26, fill_color=color, fill_opacity=0.5, stroke_width=0)
    pins = VGroup()
    for k in range(4):
        off = -0.21 + 0.14 * k
        for d in (UP, DOWN, LEFT, RIGHT):
            perp = np.array([d[1], d[0], 0])
            pins.add(Line(d * 0.31 + perp * off, d * 0.43 + perp * off, color=color, stroke_width=2.5))
    return VGroup(pins, body, core).scale(size)


def net_pattern(cols=5, rows=3, lit=(1, 6, 8, 12), color=OCHRE, spacing=0.42, seed=2):
    """A small grid of nerve cells, some active: „a pattern of activity“."""
    rng = np.random.default_rng(seed)
    pts = [np.array([c * spacing + rng.uniform(-0.06, 0.06), r * spacing + rng.uniform(-0.06, 0.06), 0])
           for r in range(rows) for c in range(cols)]
    edges = VGroup()
    for i, p in enumerate(pts):
        for j, q in enumerate(pts):
            if j > i and np.linalg.norm(p - q) < spacing * 1.5:
                edges.add(Line(p, q, color=DIM, stroke_width=2))
    nodes = VGroup(*[Dot(p, radius=0.07, color=(color if i in lit else MUTED)) for i, p in enumerate(pts)])
    g = VGroup(edges, nodes)
    g.nodes, g.edges = nodes, edges
    return g.move_to(ORIGIN)


def martian(color='#9fb7a0', height=1.4):
    """An eyeless alien scientist: round head with antennae, no eyes."""
    head = Circle(radius=0.36, fill_color=color, fill_opacity=1, stroke_width=0).shift(UP * 0.42)
    ants = VGroup(*[VGroup(Line(head.get_top() + RIGHT * dx * 0.5, head.get_top() + RIGHT * dx + UP * 0.28,
                                color=color, stroke_width=4),
                           Dot(head.get_top() + RIGHT * dx + UP * 0.3, radius=0.05, color=color))
                    for dx in (-0.22, 0.22)])
    body = RoundedRectangle(corner_radius=0.18, width=0.7, height=0.75, fill_color=color, fill_opacity=1,
                            stroke_width=0).shift(DOWN * 0.3)
    return VGroup(ants, head, body).scale_to_fit_height(height)


def meter(color=OCHRE, width=1.2, value=0.7):
    """A dial gauge; the needle angle shows a reading."""
    arc = Arc(radius=0.5, start_angle=PI, angle=-PI, color=color, stroke_width=4)
    ticks = VGroup(*[Line(0.42 * np.array([np.cos(a), np.sin(a), 0]), 0.5 * np.array([np.cos(a), np.sin(a), 0]),
                          color=color, stroke_width=2) for a in np.linspace(PI, 0, 7)])
    ang = PI * (1 - value)
    needle = Line(ORIGIN, 0.44 * np.array([np.cos(ang), np.sin(ang), 0]), color=FG, stroke_width=4)
    base = Line(LEFT * 0.6, RIGHT * 0.6, color=color, stroke_width=3)
    g = VGroup(arc, ticks, base, needle, Dot(ORIGIN, radius=0.05, color=FG))
    g.needle = needle
    return g.scale_to_fit_width(width)


def ear(color=FG, height=1.0):
    outer = VMobject(stroke_color=color, stroke_width=5)
    outer.set_points_smoothly([[0.1, -0.55, 0], [-0.05, -0.2, 0], [-0.25, 0.15, 0], [-0.15, 0.5, 0], [0.15, 0.6, 0],
                               [0.38, 0.4, 0], [0.38, 0.05, 0], [0.22, -0.15, 0], [0.22, -0.4, 0], [0.1, -0.55, 0]])
    inner = VMobject(stroke_color=color, stroke_width=4)
    inner.set_points_smoothly([[0.0, 0.05, 0], [0.05, 0.35, 0], [0.22, 0.32, 0], [0.18, 0.08, 0]])
    return VGroup(outer, inner).scale_to_fit_height(height)


def cone(apex, angle, length=4.0, spread=0.5, color=FG, opacity=0.14):
    """A viewing cone (point of view) from apex in direction `angle`."""
    d1 = np.array([np.cos(angle - spread / 2), np.sin(angle - spread / 2), 0])
    d2 = np.array([np.cos(angle + spread / 2), np.sin(angle + spread / 2), 0])
    return Polygon(apex, apex + d1 * length, apex + d2 * length, stroke_color=color, stroke_width=1.5,
                   stroke_opacity=0.5, fill_color=color, fill_opacity=opacity)


def cloud(width=1.6, color=FG, opacity=0.25, seed=1, label=None, size=18):
    rng = np.random.default_rng(seed)
    angles = np.linspace(0, TAU, 9)[:-1]
    pts = [np.array([np.cos(a) * (1 + 0.15 * rng.standard_normal()), 0.6 * np.sin(a) * (1 + 0.15 * rng.standard_normal()), 0])
           for a in angles]
    c = VMobject(fill_color=color, fill_opacity=opacity, stroke_color=color, stroke_width=2)
    c.set_points_smoothly(pts + [pts[0]])
    c.scale_to_fit_width(width)
    if label:
        return VGroup(c, txt(label, size=size).move_to(c))
    return c


def caterpillar(color='#a9b46a', width=1.3):
    segs = VGroup(*[Circle(radius=0.13, fill_color=color, fill_opacity=1, stroke_width=0)
                    .move_to([0.2 * k, 0.04 * np.sin(k * 1.3), 0]) for k in range(6)])
    head = Circle(radius=0.16, fill_color=color, fill_opacity=1, stroke_width=0).move_to([1.22, 0.06, 0])
    eye_d = Dot([1.28, 0.1, 0], radius=0.03, color=BG)
    legs = VGroup(*[Line([0.2 * k, -0.1, 0], [0.2 * k, -0.2, 0], color=color, stroke_width=3) for k in range(6)])
    return VGroup(legs, segs, head, eye_d).scale_to_fit_width(width)


def butterfly(color='#7fb3c8', width=1.4):
    up = Ellipse(width=0.62, height=0.5, fill_color=color, fill_opacity=0.9, stroke_width=0)
    lo = Ellipse(width=0.42, height=0.36, fill_color=color, fill_opacity=0.7, stroke_width=0)
    left = VGroup(up.copy().rotate(0.5).move_to([-0.3, 0.17, 0]), lo.copy().rotate(-0.5).move_to([-0.22, -0.2, 0]))
    right = left.copy().flip(UP, about_point=ORIGIN)
    body = Ellipse(width=0.08, height=0.62, fill_color=FG, fill_opacity=1, stroke_width=0)
    feel = VGroup(*[Line([0, 0.3, 0], [sx * 0.12, 0.48, 0], color=FG, stroke_width=2) for sx in (-1, 1)])
    return VGroup(left, right, body, feel).scale_to_fit_width(width)


class Safe(VGroup):
    """A steel safe; .door can be closed/opened by stretching."""

    def __init__(self, size=2.2):
        super().__init__()
        self.frame = RoundedRectangle(corner_radius=0.08, width=size, height=size * 0.9, stroke_color=MUTED,
                                      stroke_width=4, fill_color=PANEL, fill_opacity=1)
        self.door = Rectangle(width=size - 0.25, height=size * 0.9 - 0.25, fill_color='#2a3242', fill_opacity=1,
                              stroke_color=MUTED, stroke_width=2)
        dial = VGroup(Circle(radius=size * 0.12, stroke_color=FG, stroke_width=3),
                      *[Line(UP * size * 0.09, UP * size * 0.12, color=FG, stroke_width=2).rotate(a, about_point=ORIGIN)
                        for a in np.linspace(0, TAU, 9)[:-1]])
        handle = Line(LEFT * size * 0.12, RIGHT * size * 0.12, color=FG, stroke_width=5).shift(DOWN * size * 0.22)
        self.knobs = VGroup(dial, handle)
        self.door_g = VGroup(self.door, self.knobs)
        self.add(self.frame, self.door_g)
