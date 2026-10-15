"""Shared look and timing for all chapter scenes.

Every scene subclasses NarratedScene, sets CHAPTER, and places its
animations against the narration schedule from tools/timeline.py:

    self.wait_until(self.t('3.1'))                 # paragraph start
    self.wait_until(self.t('3.1', 1))              # second sentence
    self.wait_until(self.t('3.1', 0, 'genau dann'))  # estimated word time

Word times are estimated from the character position inside the sentence,
which is close enough because the voice speaks at an even pace.
"""

import os
import random
import sys
import textwrap

import manimpango
import numpy as np
from manim import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from timeline import schedule  # noqa: E402

for _f in ('SourceSerif4-Regular.ttf', 'SourceSerif4-It.ttf',
           'SourceSerif4-Semibold.ttf', 'SourceSerif4-SemiboldIt.ttf',
           'Inter-Regular.otf', 'Inter-Medium.otf', 'Inter-SemiBold.otf', 'Inter-Bold.otf'):
    manimpango.register_font(os.path.join(ROOT, 'assets', 'fonts', _f))

# ---------------------------------------------------------------- palette
BG = '#10141c'        # night blue-grey
FG = '#ebe6dc'        # warm off-white
MUTED = '#8b93a1'
DIM = '#3a4252'
PANEL = '#171d29'
OCHRE = '#dba64b'     # the outside view: measurements, functions
VIOLET = '#8f78d0'    # the inside view
INNER = '#1b1532'     # fill of the inner field
RED = '#e3675d'       # objections
GREEN = '#74c293'     # replies, what is settled

SANS = 'Inter'
SERIF = 'Source Serif 4'

config.background_color = BG


def txt(s, size=30, color=FG, weight=NORMAL, font=SANS, slant=NORMAL, width=None, **kw):
    """Text with optional wrapping at `width` characters."""
    if width:
        s = '\n'.join(textwrap.fill(par, width) for par in s.split('\n'))
    return Text(s, font=font, font_size=size, color=color, weight=weight, slant=slant,
                line_spacing=0.85, **kw)


# ----------------------------------------------------------- components
class Cite(VGroup):
    """Source line in the bottom-right corner, e.g. „Nagel 1974, S. 436“."""

    def __init__(self, text):
        label = txt(text, size=20, color=MUTED)
        bar = Line(UP * 0.13, DOWN * 0.13, color=OCHRE, stroke_width=3)
        super().__init__(bar, label)
        self.arrange(RIGHT, buff=0.14).to_corner(DR, buff=0.32)


class QuoteCard(VGroup):
    """Short English original with its source, on a dark card."""

    def __init__(self, quote, source, width=58, size=26):
        q = txt(f'„{quote}“', size=size, font=SERIF, slant=ITALIC, width=width)
        s = txt(source, size=19, color=MUTED)
        body = VGroup(q, s).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        box = RoundedRectangle(corner_radius=0.08, width=body.width + 0.7, height=body.height + 0.45,
                               fill_color=PANEL, fill_opacity=0.96, stroke_width=0)
        accent = Line(box.get_corner(UL) + DOWN * 0.12, box.get_corner(DL) + UP * 0.12,
                      color=OCHRE, stroke_width=4).shift(RIGHT * 0.04)
        body.move_to(box).shift(RIGHT * 0.05)
        super().__init__(box, accent, body)


class ChapterTag(VGroup):
    """Small persistent chapter label in the top-left corner."""

    def __init__(self, n, title):
        num = txt(f'{n}', size=18, color=OCHRE, weight=SEMIBOLD)
        t = txt(title, size=18, color=MUTED)
        super().__init__(num, t)
        self.arrange(RIGHT, buff=0.16).to_corner(UL, buff=0.32)


def grain(rect, n=240, seed=7, color=VIOLET):
    """Static speckle inside the inner field: a texture that stays unreadable."""
    rng = random.Random(seed)
    w, h = rect.width, rect.height
    dots = VGroup()
    for _ in range(n):
        x = (rng.random() - 0.5) * (w - 0.2)
        y = (rng.random() - 0.5) * (h - 0.2)
        dots.add(Dot(rect.get_center() + RIGHT * x + UP * y, radius=0.012 + 0.012 * rng.random(),
                     color=color, fill_opacity=0.12 + 0.25 * rng.random()))
    return dots


class OuterField(VGroup):
    """The outside view: an ochre frame for descriptions, data, functions."""

    def __init__(self, width=5.4, height=2.0, label='von außen'):
        self.box = RoundedRectangle(corner_radius=0.1, width=width, height=height,
                                    stroke_color=OCHRE, stroke_width=2.2, fill_opacity=0)
        self.label = txt(label, size=18, color=OCHRE).next_to(self.box, UP, buff=0.08, aligned_edge=LEFT)
        super().__init__(self.box, self.label)


class InnerField(VGroup):
    """The inside view: a dark, speckled field that never fills with content."""

    def __init__(self, width=3.4, height=2.0, label='für das Wesen selbst', seed=7):
        self.box = RoundedRectangle(corner_radius=0.1, width=width, height=height,
                                    stroke_color=VIOLET, stroke_width=2.2,
                                    fill_color=INNER, fill_opacity=1)
        self.grain = grain(self.box, n=int(60 * width * height / 2), seed=seed)
        self.label = txt(label, size=18, color=VIOLET).next_to(self.box, UP, buff=0.08, aligned_edge=LEFT)
        super().__init__(self.box, self.grain, self.label)


# ---------------------------------------------------------------- icons
def bat(color=FG, width=2.0):
    """Stylised bat silhouette with scalloped wing edges (symmetric)."""
    right = [
        (0.00, 0.30), (0.05, 0.33), (0.10, 0.47), (0.14, 0.30), (0.20, 0.22),
        (0.45, 0.33), (0.78, 0.46), (1.05, 0.40), (1.18, 0.24),
    ]
    scallops = [(1.18, 0.24), (0.98, 0.02), (0.74, -0.06), (0.50, -0.10), (0.26, -0.16), (0.12, -0.30),
                (0.00, -0.38)]
    pts = []
    for x, y in right:
        pts.append(np.array([x, y, 0]))
    path = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    path.start_new_path(pts[0])
    for p in pts[1:]:
        path.add_line_to(p)
    # Trailing edge: each scallop bulges inward (towards the body).
    for a, b in zip(scallops[:-1], scallops[1:]):
        a, b = np.array([*a, 0]), np.array([*b, 0])
        mid = (a + b) / 2 + np.array([-0.04, 0.07, 0])
        path.add_quadratic_bezier_curve_to(mid, b)
    right_pts = path.points.copy()
    left = right_pts[::-1] * np.array([-1, 1, 1])
    full = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    full.set_points(np.concatenate([right_pts, left]))
    return full.scale_to_fit_width(width)


def person(color=FG, height=1.2):
    head = Circle(radius=0.2, fill_color=color, fill_opacity=1, stroke_width=0).shift(UP * 0.42)
    body = ArcBetweenPoints(LEFT * 0.42 + DOWN * 0.38, RIGHT * 0.42 + DOWN * 0.38, angle=-PI * 0.9)
    torso = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    torso.set_points(body.points)
    torso.add_line_to(LEFT * 0.42 + DOWN * 0.38)
    return VGroup(head, torso).scale_to_fit_height(height)


def robot(color=FG, height=1.2):
    head = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.46, fill_color=color, fill_opacity=1,
                            stroke_width=0).shift(UP * 0.36)
    eyes = VGroup(*[Square(0.09, fill_color=BG, fill_opacity=1, stroke_width=0).move_to(head).shift(RIGHT * dx)
                    for dx in (-0.13, 0.13)])
    antenna = VGroup(Line(head.get_top(), head.get_top() + UP * 0.14, color=color, stroke_width=4),
                     Dot(head.get_top() + UP * 0.17, radius=0.045, color=color))
    body = RoundedRectangle(corner_radius=0.06, width=0.84, height=0.52, fill_color=color, fill_opacity=1,
                            stroke_width=0).shift(DOWN * 0.3)
    return VGroup(head, eyes, antenna, body).scale_to_fit_height(height)


def stone(color='#7d8594', width=1.3):
    rng = np.random.default_rng(3)
    angles = np.linspace(0, TAU, 11)[:-1]
    pts = [np.array([np.cos(a) * (1 + 0.12 * rng.standard_normal()), 0.62 * np.sin(a) * (1 + 0.1 * rng.standard_normal()), 0])
           for a in angles]
    s = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    s.set_points_smoothly(pts + [pts[0]])
    return s.scale_to_fit_width(width)


def function_box(inp='Reiz', state='Zustand', out='Verhalten', color=OCHRE, scale=1.0):
    """Input → functional state → output: what a functional analysis describes."""
    box = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.62, stroke_color=color, stroke_width=2,
                           fill_color=PANEL, fill_opacity=1)
    s = txt(state, size=20, color=FG).move_to(box)
    i = txt(inp, size=20, color=MUTED).next_to(box, LEFT, buff=0.75)
    o = txt(out, size=20, color=MUTED).next_to(box, RIGHT, buff=0.75)
    a1 = Arrow(i.get_right(), box.get_left(), buff=0.1, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.25)
    a2 = Arrow(box.get_right(), o.get_left(), buff=0.1, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.25)
    return VGroup(i, a1, box, s, a2, o).scale(scale)


# ----------------------------------------------------------- the scene
class NarratedScene(Scene):
    CHAPTER: int = None

    def setup(self):
        self.sched = schedule(self.CHAPTER)
        self.paras = {p['id']: p for p in self.sched['paragraphs']}
        self.cite_mob = None
        self.tag = None

    # -- timing
    @property
    def now(self):
        return self.renderer.time

    def t(self, pid, sentence=0, word=None, end=False):
        """Time of a paragraph/sentence start (or end), optionally of a word in it."""
        p = self.paras[pid]
        if sentence == 'end' or end and sentence == 0 and word is None:
            return p['end']
        s = p['sentences'][sentence]
        if end:
            return s['end']
        if word is None:
            return s['start']
        i = s['text'].find(word)
        if i < 0:
            raise ValueError(f'„{word}“ nicht in Satz {pid}/{sentence}')
        return s['start'] + (s['end'] - s['start']) * i / max(1, len(s['text']))

    def wait_until(self, t):
        dt = t - self.now
        if dt >= 1 / 30:
            self.wait(dt)
        elif dt < -0.3:
            print(f'[timing] Szene {self.CHAPTER}: {-dt:.2f} s hinter dem Ton bei t={t:.2f}')

    def play_at(self, t, *anims, **kw):
        self.wait_until(t)
        self.play(*anims, **kw)

    # -- furniture
    def chapter_card(self):
        n, title = self.sched['chapter'], self.sched['title']
        label = txt(f'KAPITEL {n}', size=24, color=OCHRE, weight=MEDIUM)
        head = txt(title, size=66, font=SERIF, weight=SEMIBOLD)
        rule = Line(LEFT * 0.9, RIGHT * 0.9, color=OCHRE, stroke_width=2)
        card = VGroup(label, head, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(card, shift=UP * 0.15), run_time=0.8)
        self.wait_until(self.sched['card_end'] - 0.6)
        self.play(FadeOut(card), run_time=0.6)
        self.tag = ChapterTag(n, title)
        self.play(FadeIn(self.tag), run_time=0.4)

    def cite(self, text, run_time=0.4):
        """Show (or replace) the source line in the bottom-right corner."""
        new = Cite(text)
        if self.cite_mob is None:
            self.play(FadeIn(new), run_time=run_time)
        else:
            self.play(FadeOut(self.cite_mob), FadeIn(new), run_time=run_time)
        self.cite_mob = new

    def cite_of(self, pid, k=0):
        return self.paras[pid]['cites'][k]

    def quote_of(self, pid, k=0):
        return self.paras[pid]['quotes'][k]

    def finish(self):
        """Fade everything during the tail so chapters join cleanly."""
        self.wait_until(self.sched['end'] - 0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        self.wait_until(self.sched['end'])
