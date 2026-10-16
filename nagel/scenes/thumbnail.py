"""YouTube thumbnail in the look of the video.

    cd scenes && ../venv/bin/manim render --config_file manim.cfg -s -r 1920,1080 -o thumbnail thumbnail.py Thumbnail

    ffmpeg -i ../media/images/thumbnail/thumbnail.png -vf scale=1280:720:flags=lanczos -q:v 2 ../output/thumbnail.jpg

The bat flies in front of the moon and calls (ochre
echo arcs: the outside view); the question mark is violet, the colour of the inside view.
"""

from kit import *  # noqa: F401,F403

MOON = '#e9e2cf'
GLOW = '#b4bccc'    # cool moonlight around the disc


class Thumbnail(Scene):
    def construct(self):
        rng = np.random.default_rng(3)
        sky = Rectangle(width=14.3, height=8.1, stroke_width=0, fill_opacity=1)
        sky.set_fill(color=['#1a2131', BG], opacity=1).set_sheen_direction(UP)
        stars = VGroup(*[Dot([rng.uniform(-7, 7), rng.uniform(-1.5, 3.9), 0], radius=rng.uniform(0.01, 0.025),
                             color=FG, fill_opacity=rng.uniform(0.15, 0.6)) for _ in range(60)])

        c = np.array([5.3, 0.2, 0])
        r = 2.65
        halo = VGroup(*[Circle(radius=r + 0.09 * i, stroke_width=0, fill_color=GLOW,
                               fill_opacity=0.02).move_to(c) for i in range(1, 24)])
        moon = Circle(radius=r, stroke_width=0, fill_color=MOON, fill_opacity=1).move_to(c)
        craters = VGroup(*[Circle(radius=q, stroke_width=0, fill_color='#d6cdb6', fill_opacity=0.55).move_to(c + d)
                           for q, d in [(0.42, [-1.0, 1.25, 0]), (0.26, [1.35, 1.0, 0]),
                                        (0.2, [0.5, 1.75, 0]), (0.3, [-1.6, -0.6, 0])]])
        b = bat(color=BG, width=3.4).move_to(c + UP * 0.25)
        mouth = b.get_top() + DOWN * 0.95
        arcs = VGroup(*[Arc(radius=q, start_angle=-PI / 2 - 0.45, angle=0.9, arc_center=mouth,
                            color=OCHRE, stroke_width=10 - 2 * i) for i, q in enumerate([1.05, 1.45, 1.85])])

        xs = np.linspace(-7.3, 7.3, 50)
        hill = [np.array([x, -3.15 + 0.3 * np.sin(x * 0.6 + 1) + 0.12 * np.sin(x * 2.3), 0]) for x in xs]
        ground = Polygon(*hill, [7.3, -4.2, 0], [-7.3, -4.2, 0], fill_color='#080a0f', fill_opacity=1,
                         stroke_width=0)

        kicker = txt('THOMAS NAGEL · 1974', size=36, color=OCHRE, weight=BOLD)
        l1 = txt('Wie ist es,', size=82, font=SERIF, weight=SEMIBOLD)
        l2 = txt('eine Fledermaus', size=82, font=SERIF, weight=SEMIBOLD)
        l3a = txt('zu sein', size=82, font=SERIF, weight=SEMIBOLD)
        l3b = txt('?', size=98, font=SERIF, weight=SEMIBOLD, color=VIOLET)
        l3 = VGroup(l3a, l3b).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        title = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        block = VGroup(kicker, title).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        block.to_edge(LEFT, buff=0.6).shift(UP * 0.3)

        self.add(sky, stars, halo, moon, craters, arcs, b, ground, block)
