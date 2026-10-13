import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Cup, Die, Eye, Figure, Stone } from '../components/icons';
import { Arrow, At, Card, easeInOut, Formula, Gr, prog, Quote, Reveal, Strike, Svg, T, vis } from '../components/kit';
import { C } from '../theme';
import { SceneTiming } from '../timeline';
import { useScene } from './util';

type P = { t: SceneTiming };

/** Drifting horizontal particle streams ("everything flows"). */
const Flow: React.FC<{ f: number; y0: number; y1: number; n?: number; color?: string; speed?: number; opacity?: number }> = ({
  f,
  y0,
  y1,
  n = 70,
  color = C.gold,
  speed = 2.2,
  opacity = 1,
}) => (
  <g opacity={opacity}>
    {Array.from({ length: n }, (_, i) => {
      const seed = (i * 9301 + 49297) % 233280;
      const r = seed / 233280;
      const y = y0 + (y1 - y0) * ((i * 0.618) % 1);
      const v = speed * (0.6 + r);
      const x = ((r * 1920 + f * v * 3) % 2100) - 90;
      const wob = Math.sin(f / 30 + i) * 8;
      return <line key={i} x1={x} y1={y + wob} x2={x + 26 + r * 40} y2={y + wob} stroke={color} strokeWidth={2 + r * 2} strokeLinecap="round" opacity={0.15 + r * 0.45} />;
    })}
  </g>
);

/* ───────────── VI · Erkenntnis ist Wahrnehmung ───────────── */

export const Def1: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const windLines = Array.from({ length: 9 }, (_, i) => i);
  const shiver = Math.sin(f * 1.7) * 3 * prog(f, s(2, 0.4), 10);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Formula f={f} at={s(0, 0.1)} left="ἐπιστήμη" right="αἴσθησις" leftDe="Erkenntnis" rightDe="Wahrnehmung" size={110} />
        <Reveal f={f} at={s(0, 0.55)}>
          <div style={{ ...T.italic(40, C.muted), marginTop: 70 }}>„… ist Erkenntnis nichts anderes als Wahrnehmung.“</div>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Quote
          f={f}
          at={s(1, 0.35)}
          de="Der Mensch ist das Maß aller Dinge, der seienden, wie sie sind, der nichtseienden, wie sie nicht sind."
          gr="πάντων χρημάτων μέτρον ἄνθρωπον εἶναι, τῶν μὲν ὄντων ὡς ἔστι, τῶν δὲ μὴ ὄντων ὡς οὐκ ἔστιν"
          src="Protagoras bei Platon, Theaitetos 152a"
          width={1500}
          size={54}
        />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2), s(4)) }}>
        <Svg>
          {windLines.map((i) => {
            const y = 300 + i * 46;
            const off = ((f * 9 + i * 140) % 1800) - 300;
            return (
              <path
                key={i}
                d={`M ${off} ${y} C ${off + 120} ${y - 30} ${off + 220} ${y + 30} ${off + 340} ${y}`}
                stroke={C.ink}
                strokeWidth={2.5}
                fill="none"
                opacity={0.35 * prog(f, s(2, 0.05), 20)}
                strokeLinecap="round"
              />
            );
          })}
          <g transform={`translate(${shiver} 0)`} opacity={prog(f, s(2, 0.15), 20)}>
            <Figure x={560} y={600} s={1.8} color={C.blue} fill="rgba(127,163,201,0.12)" />
          </g>
          <g opacity={prog(f, s(2, 0.2), 20)}>
            <Figure x={1360} y={600} s={1.8} color={C.terracotta} fill="rgba(207,106,71,0.12)" />
          </g>
        </Svg>
        <At x={960} y={190}>
          <Reveal f={f} at={s(2, 0.05)}>
            <div style={T.label(26, C.gold)}>Derselbe Wind</div>
          </Reveal>
        </At>
        <At x={560} y={820}>
          <Reveal f={f} at={s(2, 0.45)}>
            <div style={T.display(60, C.blue)}>kalt</div>
            <div style={{ ...T.label(22), marginTop: 8, opacity: prog(f, s(3, 0.05), 20) }}>für den, der friert</div>
          </Reveal>
        </At>
        <At x={1360} y={820}>
          <Reveal f={f} at={s(2, 0.55)}>
            <div style={T.display(60, C.terracotta)}>nicht kalt</div>
            <div style={{ ...T.label(22), marginTop: 8, opacity: prog(f, s(3, 0.1), 20) }}>für den anderen</div>
          </Reveal>
        </At>
        <At x={960} y={540}>
          <Reveal f={f} at={s(2, 0.8)} out={s(3, 0.3)}>
            <div style={T.display(100, C.gold)}>?</div>
          </Reveal>
        </At>
        <At x={960} y={500} w={760}>
          <Reveal f={f} at={s(3, 0.4)}>
            <Card>
              <div style={T.serif(38)}>Wahrnehmung ist immer von etwas, das ist,</div>
              <div style={{ ...T.serif(38, C.gold) }}>und unfehlbar – wie Erkenntnis.</div>
              <div style={{ ...T.greek(34, C.muted), marginTop: 12 }}>αἴσθησις ἄρα τοῦ ὄντος ἀεί ἐστιν καὶ ἀψευδές</div>
            </Card>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── VII · Nichts ist, alles wird ───────────── */

export const Fluss: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const names = ['Protagoras', 'Herakleitos', 'Empedokles', 'Epicharmos', 'Homer'];
  const DiceRow: React.FC<{ n: number; x: number; y: number; at: number; cols: number }> = ({ n, x, y, at, cols }) => (
    <g>
      {Array.from({ length: n }, (_, i) => (
        <Die key={i} x={x + (i % cols) * 72} y={y + Math.floor(i / cols) * 72} n={(i % 6) + 1} opacity={prog(f, at + i * 2, 12)} s={0.95} />
      ))}
    </g>
  );
  return (
    <AbsoluteFill>
      {/* 0 · ist → wird */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <Flow f={f} y0={160} y1={920} n={90} opacity={prog(f, 0, 30) * 0.8} />
        </Svg>
        <At x={960} y={420}>
          <Reveal f={f} at={s(0, 0.45)}>
            <div style={{ display: 'flex', gap: 80, alignItems: 'baseline' }}>
              <div style={{ position: 'relative' }}>
                <div style={T.display(150, C.muted)}>ist</div>
                <Strike f={f} at={s(0, 0.62)} />
              </div>
              <div style={{ ...T.display(150, C.gold), opacity: prog(f, s(0, 0.66), 20) }}>wird</div>
            </div>
          </Reveal>
        </At>
        <At x={960} y={660}>
          <Reveal f={f} at={s(0, 0.7)}>
            <div style={T.greek(50)}>ἔστι μὲν γὰρ οὐδέποτʼ οὐδέν, ἀεὶ δὲ γίγνεται</div>
            <div style={{ ...T.italic(34, C.muted), marginTop: 10 }}>„Nichts ist je, alles wird immer.“ – Tht. 152e</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 1 · the wise and Parmenides */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <Flow f={f} y0={250} y1={760} n={60} opacity={0.45} />
          <g opacity={prog(f, s(1, 0.75), 30)}>
            <rect x={1500} y={330} width={230} height={350} rx={20} fill="rgba(127,163,201,0.12)" stroke={C.blue} strokeWidth={3} />
          </g>
        </Svg>
        {names.map((n, i) => {
          const drift = ((f - s(1)) * 1.4) % 60;
          return (
            <At key={n} x={260 + i * 240 + drift} y={360 + (i % 2) * 180}>
              <Reveal f={f} at={s(1, 0.08 + i * 0.08)}>
                <div style={T.display(58)}>{n}</div>
              </Reveal>
            </At>
          );
        })}
        <At x={1615} y={505} w={230}>
          <Reveal f={f} at={s(1, 0.78)}>
            <div style={T.display(48, C.blue)}>Parmenides</div>
            <div style={{ ...T.label(18), marginTop: 10 }}>steht abseits</div>
          </Reveal>
        </At>
        <At x={700} y={860} w={1200}>
          <Reveal f={f} at={s(1, 0.55)}>
            <div style={T.greek(42)}>Ὠκεανόν τε θεῶν γένεσιν καὶ μητέρα Τηθύν</div>
            <div style={{ ...T.italic(32, C.muted), marginTop: 6 }}>„Okeanos, Ursprung der Götter, und Mutter Tethys“ – Ilias 14, 201</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 2 · six dice */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(2, 0.05), 20)}>
            <DiceRow n={6} x={888} y={470} at={s(2, 0.05)} cols={3} />
          </g>
          <DiceRow n={4} x={350} y={470} at={s(2, 0.2)} cols={2} />
          <DiceRow n={12} x={1350} y={430} at={s(2, 0.5)} cols={4} />
          <Arrow f={f} at={s(2, 0.3)} x1={840} y1={505} x2={530} y2={505} color={C.gold} />
          <Arrow f={f} at={s(2, 0.6)} x1={1100} y1={505} x2={1320} y2={505} color={C.blue} />
        </Svg>
        <At x={960} y={290}>
          <Reveal f={f} at={s(2, 0.05)}>
            <div style={T.display(60)}>sechs Spielsteine</div>
            <div style={{ ...T.label(20), marginTop: 6 }}><Gr>ἀστράγαλοι</Gr> · Tht. 154c</div>
          </Reveal>
        </At>
        <At x={440} y={720}>
          <Reveal f={f} at={s(2, 0.32)}>
            <div style={T.display(56, C.gold)}>mehr</div>
            <div style={T.serif(34, C.muted)}>anderthalbmal so viele</div>
          </Reveal>
        </At>
        <At x={1460} y={720}>
          <Reveal f={f} at={s(2, 0.62)}>
            <div style={T.display(56, C.blue)}>weniger</div>
            <div style={T.serif(34, C.muted)}>halb so viele</div>
          </Reveal>
        </At>
        <At x={960} y={860} w={1400}>
          <Reveal f={f} at={s(2, 0.8)}>
            <div style={T.italic(40)}>größer und kleiner geworden – ohne Zuwachs, ohne Verlust</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 3 · wonder */}
      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Quote
          f={f}
          at={s(3, 0.35)}
          de="Gar sehr ist dies der Zustand eines Freundes der Weisheit, die Verwunderung; ja es gibt keinen andern Anfang der Philosophie als diesen."
          gr="μάλα γὰρ φιλοσόφου τοῦτο τὸ πάθος, τὸ θαυμάζειν· οὐ γὰρ ἄλλη ἀρχὴ φιλοσοφίας ἢ αὕτη"
          src="Tht. 155d · Übers. Schleiermacher"
          width={1500}
          size={52}
        />
      </AbsoluteFill>

      {/* 4 · Aristotle */}
      <AbsoluteFill style={{ opacity: vis(f, s(4)), justifyContent: 'center', alignItems: 'center' }}>
        <Quote
          f={f}
          at={s(4, 0.15)}
          de="Durch das Staunen haben die Menschen jetzt wie zuerst zu philosophieren begonnen."
          gr="διὰ γὰρ τὸ θαυμάζειν οἱ ἄνθρωποι καὶ νῦν καὶ τὸ πρῶτον ἤρξαντο φιλοσοφεῖν"
          src="Aristoteles, Metaphysik I 2, 982b12–13"
          width={1500}
          size={52}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── VIII · Zwillingsgeburt ───────────── */

export const Zwillinge: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const meet = prog(f, s(0, 0.45), 30, easeInOut);
  const twins = prog(f, s(0, 0.7), 24);
  const streamP = prog(f, s(1, 0.35), 40);
  return (
    <AbsoluteFill>
      {/* 0 · acting and suffering motion */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <circle cx={560 + meet * 300} cy={480} r={110} fill="rgba(217,181,107,0.1)" stroke={C.gold} strokeWidth={3} opacity={prog(f, s(0, 0.1), 20)} />
          <circle cx={1360 - meet * 300} cy={480} r={110} fill="rgba(127,163,201,0.1)" stroke={C.blue} strokeWidth={3} opacity={prog(f, s(0, 0.15), 20)} />
          <circle cx={960} cy={300 - twins * 40} r={34} fill={C.gold} opacity={twins} filter="url(#glow)" />
          <circle cx={960} cy={660 + twins * 40} r={34} fill={C.marble} opacity={twins} filter="url(#glow)" />
        </Svg>
        <At x={560 + meet * 300} y={480}>
          <div style={{ ...T.greek(40), opacity: prog(f, s(0, 0.1), 20) }}>ποιεῖν</div>
          <div style={{ ...T.label(18), opacity: prog(f, s(0, 0.1), 20) }}>wirken</div>
        </At>
        <At x={1360 - meet * 300} y={480}>
          <div style={{ ...T.greek(40, C.blue), opacity: prog(f, s(0, 0.15), 20) }}>πάσχειν</div>
          <div style={{ ...T.label(18), opacity: prog(f, s(0, 0.15), 20) }}>leiden</div>
        </At>
        <At x={960} y={170}>
          <div style={{ opacity: twins }}>
            <div style={T.display(48, C.gold)}>Wahrnehmung</div>
          </div>
        </At>
        <At x={960} y={800}>
          <div style={{ opacity: twins }}>
            <div style={T.display(48, C.marble)}>Wahrgenommenes</div>
          </div>
        </At>
        <At x={1600} y={190} w={420}>
          <Reveal f={f} at={s(0, 0.85)}>
            <div style={T.label(22, C.gold)}>Zwillinge · Tht. 156a–b</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 1 · eye and stone */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(1), 20)}>
            <Eye x={420} y={500} s={2.1} look={0.6} color={C.ink} sw={2.5} />
            <circle cx={420} cy={500} r={140 * streamP} fill="url(#goldGlow)" opacity={streamP} />
          </g>
          <g opacity={prog(f, s(1, 0.05), 20)}>
            <Stone x={1500} y={500} s={2.2} color={C.ink} />
            <circle cx={1500} cy={500} r={150 * streamP} fill="rgba(244,239,228,0.18)" filter="url(#softglow)" />
          </g>
          {Array.from({ length: 16 }, (_, i) => {
            const p = ((f - s(1, 0.3)) / 40 + i / 16) % 1;
            if (f < s(1, 0.3)) return null;
            return (
              <g key={i}>
                <circle cx={1360 - p * 800} cy={460 + Math.sin(p * 9 + i) * 14} r={7} fill={C.gold} opacity={(1 - p) * 0.9} />
                <circle cx={560 + p * 800} cy={540 + Math.sin(p * 9 + i) * 14} r={7} fill={C.marble} opacity={(1 - p) * 0.9} />
              </g>
            );
          })}
        </Svg>
        <At x={420} y={700}>
          <Reveal f={f} at={s(1, 0.1)}>
            <div style={T.display(48)}>Auge</div>
            <div style={T.label(18)}>langsame Bewegung</div>
          </Reveal>
        </At>
        <At x={1500} y={700}>
          <Reveal f={f} at={s(1, 0.15)}>
            <div style={T.display(48)}>Stein</div>
            <div style={T.label(18)}>langsame Bewegung</div>
          </Reveal>
        </At>
        <At x={960} y={400}>
          <Reveal f={f} at={s(1, 0.4)}>
            <div style={T.serif(38, C.gold)}>← Sehen</div>
          </Reveal>
        </At>
        <At x={960} y={610}>
          <Reveal f={f} at={s(1, 0.5)}>
            <div style={T.serif(38, C.marble)}>Weiß →</div>
          </Reveal>
        </At>
        <At x={960} y={860} w={1400}>
          <Reveal f={f} at={s(1, 0.75)}>
            <div style={T.italic(40)}>Jetzt erst: ein sehendes Auge – ein weißer Stein</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 2 · only relations */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: 70, alignItems: 'baseline' }}>
          <Reveal f={f} at={s(2, 0.05)}>
            <div style={{ position: 'relative' }}>
              <div style={T.display(110, C.muted)}>ist</div>
              <Strike f={f} at={s(2, 0.45)} />
            </div>
          </Reveal>
          <Reveal f={f} at={s(2, 0.5)}>
            <div style={T.display(110, C.gold)}>wird</div>
          </Reveal>
        </div>
        <div style={{ display: 'flex', gap: 60, marginTop: 50 }}>
          {['für jemanden', 'von etwas', 'in Bezug auf etwas'].map((w, i) => (
            <Reveal key={w} f={f} at={s(2, 0.6 + i * 0.08)}>
              <div style={T.serif(44)}>{w}</div>
            </Reveal>
          ))}
        </div>
        <Reveal f={f} at={s(2, 0.85)}>
          <div style={{ ...T.greek(40, C.muted), marginTop: 40 }}>τινὶ εἶναι ἢ τινὸς ἢ πρός τι ῥητέον · vgl. Tht. 160b</div>
        </Reveal>
      </AbsoluteFill>

      {/* 3 · scholarly dispute */}
      <AbsoluteFill style={{ opacity: vis(f, s(3)) }}>
        <div style={{ position: 'absolute', top: 300, left: 220, right: 220, display: 'flex', gap: 50 }}>
          <Reveal f={f} at={s(3, 0.45)} style={{ flex: 1 }}>
            <Card>
              <div style={T.label(22, C.gold)}>Lesart 1 · etwa Cornford</div>
              <div style={{ ...T.serif(38), marginTop: 12 }}>Platon übernimmt die Theorie – als Beschreibung der Sinnenwelt.</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(3, 0.6)} style={{ flex: 1 }}>
            <Card accent={C.blue}>
              <div style={T.label(22, C.blue)}>Lesart 2 · etwa Burnyeat</div>
              <div style={{ ...T.serif(38), marginTop: 12 }}>Platon entwickelt sie nur, um die Definition so stark wie möglich zu machen.</div>
            </Card>
          </Reveal>
        </div>
        <At x={960} y={200}>
          <Reveal f={f} at={s(3, 0.05)}>
            <div style={T.label(24, C.gold)}>Sinnesqualitäten entstehen erst in der Begegnung</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── IX · Wachen, Träumen, Kranksein ───────────── */

export const Traum: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const merge = prog(f, s(2, 0.55), 40, easeInOut);
  const orbit = (f - s(3, 0.3)) / 35;
  return (
    <AbsoluteFill>
      {/* 0 · asleep or awake */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(0, 0.4), 24)}>
            <line x1={560} y1={400} x2={1360} y2={400} stroke={C.ink} strokeWidth={4} />
            <line x1={960} y1={400} x2={960} y2={760} stroke={C.ink} strokeWidth={4} />
            <path d="M 880 760 H 1040" stroke={C.ink} strokeWidth={6} />
            <path d="M 560 400 L 500 520 H 620 Z M 1360 400 L 1300 520 H 1420 Z" fill="none" stroke={C.ink} strokeWidth={2.5} />
            <path d="M 520 480 a 40 40 0 1 0 50 -50 a 32 32 0 1 1 -50 50 Z" fill={C.blue} opacity={0.9} />
            <circle cx={1360} cy={470} r={34} fill={C.gold} />
          </g>
        </Svg>
        <At x={960} y={220} w={1400}>
          <Reveal f={f} at={s(0, 0.3)}>
            <div style={T.display(66)}>Schlafen wir – oder sind wir wach?</div>
          </Reveal>
        </At>
        <At x={560} y={600}>
          <Reveal f={f} at={s(0, 0.6)}>
            <div style={T.label(22, C.blue)}>Traum</div>
          </Reveal>
        </At>
        <At x={1360} y={600}>
          <Reveal f={f} at={s(0, 0.6)}>
            <div style={T.label(22, C.gold)}>Wachen</div>
          </Reveal>
        </At>
        <At x={960} y={860}>
          <Reveal f={f} at={s(0, 0.75)}>
            <div style={T.italic(40, C.muted)}>gleich lange Zeit · in beiden halten wir alles für wahr</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 1 · healthy and sick Socrates */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(1, 0.1), 20)}>
            <Figure x={440} y={540} s={1.7} color={C.gold} fill="rgba(217,181,107,0.12)" />
          </g>
          <g opacity={prog(f, s(1, 0.2), 20)}>
            <Figure x={1480} y={540} s={1.7} color={C.blue} fill="rgba(127,163,201,0.12)" />
          </g>
          <g opacity={prog(f, s(1, 0.3), 20)}>
            <Cup x={960} y={520} s={1.6} />
          </g>
          <Arrow f={f} at={s(1, 0.45)} x1={850} y1={500} x2={560} y2={480} color={C.gold} bend={0.15} />
          <Arrow f={f} at={s(1, 0.55)} x1={1070} y1={500} x2={1360} y2={480} color={C.blue} bend={-0.15} />
        </Svg>
        <At x={440} y={790}>
          <Reveal f={f} at={s(1, 0.15)}>
            <div style={T.display(48)}>Sokrates, gesund</div>
            <div style={{ ...T.display(56, C.gold), marginTop: 10, opacity: prog(f, s(1, 0.5), 20) }}>süß</div>
          </Reveal>
        </At>
        <At x={1480} y={790}>
          <Reveal f={f} at={s(1, 0.25)}>
            <div style={T.display(48)}>Sokrates, krank</div>
            <div style={{ ...T.display(56, C.blue), marginTop: 10, opacity: prog(f, s(1, 0.6), 20) }}>bitter</div>
          </Reveal>
        </At>
        <At x={960} y={250}>
          <Reveal f={f} at={s(1, 0.75)}>
            <div style={T.italic(42)}>Beides wahr – jedes für seinen Wahrnehmenden</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 2 · three theses become one */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <Svg>
          {[0, 1, 2].map((i) => (
            <path
              key={i}
              d={`M ${420 + i * 540} 330 C ${420 + i * 540} 520 960 520 960 ${700}`}
              stroke={[C.blue, C.terracotta, C.gold][i]}
              strokeWidth={4}
              fill="none"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - merge}
              opacity={0.85}
            />
          ))}
          <circle cx={960} cy={720} r={30 * merge} fill={C.gold} filter="url(#glow)" />
        </Svg>
        {[
          ['Homer · Herakleitos', 'alles fließt'],
          ['Protagoras', 'der Mensch ist das Maß'],
          ['Theaitetos', 'Wahrnehmung ist Erkenntnis'],
        ].map(([a, b], i) => (
          <At key={a} x={420 + i * 540} y={250}>
            <Reveal f={f} at={s(2, 0.08 + i * 0.13)}>
              <div style={T.display(50, [C.blue, C.terracotta, C.gold][i])}>{a}</div>
              <div style={T.italic(34, C.muted)}>{b}</div>
            </Reveal>
          </At>
        ))}
        <At x={960} y={820}>
          <Reveal f={f} at={s(2, 0.85)}>
            <div style={T.label(24, C.gold)}>eine einzige These · Tht. 160d–e</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 3 · Amphidromia */}
      <AbsoluteFill style={{ opacity: vis(f, s(3)) }}>
        <Svg>
          <g opacity={prog(f, s(3, 0.1), 20)}>
            <ellipse cx={960} cy={540} rx={300} ry={190} fill="none" stroke={C.line} strokeWidth={2} strokeDasharray="6 10" />
            {[0, 1, 2].map((i) => (
              <path
                key={i}
                d={`M ${930 + i * 30} 580 C ${920 + i * 30} ${540 - Math.sin(f / 5 + i) * 10} ${950 + i * 20} 510 ${945 + i * 15} ${480 - Math.sin(f / 7 + i) * 12} C ${975 + i * 10} 520 ${985} 545 ${965 + i * 10} 580 Z`}
                fill={[C.red, C.terracotta, C.gold][i]}
                opacity={0.8}
              />
            ))}
            <rect x={900} y={580} width={120} height={22} rx={6} fill="rgba(236,230,217,0.15)" stroke={C.ink} />
          </g>
          {f > s(3, 0.3) && (
            <g>
              <circle cx={960 + Math.cos(orbit) * 300} cy={540 + Math.sin(orbit) * 190} r={18} fill={C.marble} filter="url(#glow)" />
            </g>
          )}
        </Svg>
        <At x={960} y={200}>
          <Reveal f={f} at={s(3, 0.1)}>
            <div style={T.display(64)}>Amphidromien</div>
            <div style={{ ...T.label(22), marginTop: 8 }}>das Kind wird um den Herd getragen · Tht. 160e</div>
          </Reveal>
        </At>
        <At x={960} y={860}>
          <Reveal f={f} at={s(3, 0.7)}>
            <div style={T.italic(44, C.gold)}>rechte Geburt – oder Windei?</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

