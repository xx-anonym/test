import React from 'react';
import { AbsoluteFill, interpolate } from 'remotion';
import { Egg, Profile } from '../components/icons';
import { At, Card, Draw, easeInOut, Gr, prog, Reveal, Svg, T, vis } from '../components/kit';
import { C, F } from '../theme';
import { SceneTiming } from '../timeline';
import { useScene } from './util';

type P = { t: SceneTiming };

/* ───────────── geometry helpers ───────────── */

/** Vertices A_1..A_n of the spiral of Theodorus (|OA_k| = √k). */
const spiralPoints = (n: number) => {
  const pts: [number, number][] = [[1, 0]];
  for (let k = 1; k < n; k++) {
    const [x, y] = pts[k - 1];
    const r = Math.hypot(x, y);
    pts.push([x - y / r, y + x / r]);
  }
  return pts;
};

type V3 = [number, number, number];
const PHI = (1 + Math.sqrt(5)) / 2;
const octa: V3[] = [
  [1, 0, 0],
  [-1, 0, 0],
  [0, 1, 0],
  [0, -1, 0],
  [0, 0, 1],
  [0, 0, -1],
];
const ico: V3[] = [];
for (const a of [-1, 1]) for (const b of [-1, 1]) ico.push([0, a, b * PHI], [a, b * PHI, 0], [b * PHI, 0, a]);
const edgesOf = (vs: V3[]) => {
  let min = Infinity;
  for (let i = 0; i < vs.length; i++) for (let j = i + 1; j < vs.length; j++) min = Math.min(min, dist(vs[i], vs[j]));
  const es: [number, number][] = [];
  for (let i = 0; i < vs.length; i++) for (let j = i + 1; j < vs.length; j++) if (Math.abs(dist(vs[i], vs[j]) - min) < 1e-6) es.push([i, j]);
  return es;
};
const dist = (a: V3, b: V3) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
const rot = ([x, y, z]: V3, ay: number, ax: number): V3 => {
  const x1 = x * Math.cos(ay) + z * Math.sin(ay);
  const z1 = -x * Math.sin(ay) + z * Math.cos(ay);
  const y1 = y * Math.cos(ax) - z1 * Math.sin(ax);
  const z2 = y * Math.sin(ax) + z1 * Math.cos(ax);
  return [x1, y1, z2];
};

const Solid: React.FC<{ vs: V3[]; cx: number; cy: number; size: number; f: number; at: number; color: string }> = ({ vs, cx, cy, size, f, at, color }) => {
  const es = edgesOf(vs);
  const ay = f / 70;
  const ax = 0.5 + Math.sin(f / 90) * 0.3;
  const norm = Math.max(...vs.map((v) => Math.hypot(...v)));
  const pv = vs.map((v) => rot(v, ay, ax)).map(([x, y, z]) => [cx + (x / norm) * size, cy + (y / norm) * size, z / norm] as const);
  const a = prog(f, at, 40);
  return (
    <g opacity={a}>
      {es
        .map(([i, j]) => ({ i, j, z: (pv[i][2] + pv[j][2]) / 2 }))
        .sort((p, q) => p.z - q.z)
        .map(({ i, j, z }) => (
          <line
            key={`${i}-${j}`}
            x1={pv[i][0]}
            y1={pv[i][1]}
            x2={pv[j][0]}
            y2={pv[j][1]}
            stroke={color}
            strokeWidth={1.5 + (z + 1) * 1.4}
            opacity={0.25 + (z + 1) * 0.37}
            strokeLinecap="round"
          />
        ))}
      {pv.map(([x, y, z], i) => (
        <circle key={i} cx={x} cy={y} r={3 + (z + 1) * 2.5} fill={color} opacity={0.4 + (z + 1) * 0.3} />
      ))}
    </g>
  );
};

/* ───────────── IV · Mathematik ───────────── */

export const Mathematik: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const U = 74; // grid unit in px
  const pts = spiralPoints(17);
  const sx = 640;
  const sy = 560;
  const P = ([x, y]: [number, number]) => [sx + x * 92, sy - y * 92] as const;
  // triangles appear over segments 1 and 2
  const triStart = s(1, 0.05);
  const triEnd = s(2, 0.55);
  const shown = interpolate(f, [triStart, triEnd], [0, 16], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const angleSum = (k: number) => {
    let a = 0;
    for (let i = 1; i <= k; i++) a += Math.atan(1 / Math.sqrt(i));
    return (a * 180) / Math.PI;
  };

  const DotGrid: React.FC<{ n: number; cols: number; x: number; y: number; at: number; color: string }> = ({ n, cols, x, y, at, color }) => {
    const rows = n / cols;
    return (
      <g>
        <rect
          x={x - 20}
          y={y - 20}
          width={cols * 40}
          height={rows * 40}
          rx={8}
          fill="none"
          stroke={color}
          strokeWidth={2}
          strokeDasharray="5 6"
          opacity={prog(f, at + 10, 20)}
        />
        {Array.from({ length: n }, (_, i) => (
          <circle key={i} cx={x + (i % cols) * 40} cy={y + Math.floor(i / cols) * 40} r={11} fill={color} opacity={prog(f, at + i * 2, 12)} />
        ))}
      </g>
    );
  };

  // ruler measuring √5 with ever finer units
  const side = Math.sqrt(5);
  const level = Math.floor(interpolate(f, [s(0, 0.55), s(0, 0.95)], [0, 4.99], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const step = 1 / 2 ** level;
  const ticks = Math.floor(side / step);

  return (
    <AbsoluteFill>
      {/* 0 · √5 square, not measurable by the foot */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g transform="translate(330 250)" opacity={prog(f, 4, 20)}>
            {Array.from({ length: 6 }, (_, i) => (
              <g key={i}>
                <line x1={0} y1={i * U} x2={5 * U} y2={i * U} stroke={C.line} strokeWidth={1} />
                <line x1={i * U} y1={0} x2={i * U} y2={5 * U} stroke={C.line} strokeWidth={1} />
              </g>
            ))}
            <path
              d={`M ${U} ${4 * U} L ${3 * U} ${3 * U} L ${4 * U} ${U} L ${2 * U} ${2 * U} Z`.replace(/L (\d+(?:\.\d+)?) (\d+(?:\.\d+)?) Z/, (m) => m)}
              fill="none"
            />
            <polygon
              points={`${U},${3 * U} ${3 * U},${4 * U} ${4 * U},${2 * U} ${2 * U},${U}`}
              fill="rgba(217,181,107,0.18)"
              stroke={C.gold}
              strokeWidth={3}
              opacity={prog(f, s(0, 0.1), 24)}
            />
            <text x={2.5 * U} y={2.62 * U} textAnchor="middle" fontFamily={F.display} fontSize={48} fill={C.ink} opacity={prog(f, s(0, 0.2), 20)}>
              5
            </text>
            <line x1={0} y1={5.5 * U} x2={U} y2={5.5 * U} stroke={C.ink} strokeWidth={4} opacity={prog(f, s(0, 0.25), 20)} />
            <text x={U / 2} y={5.5 * U + 40} textAnchor="middle" fontFamily={F.sans} fontSize={22} fill={C.muted} opacity={prog(f, s(0, 0.25), 20)}>
              1 FUSS
            </text>
          </g>
          {/* ruler along the side √5 */}
          <g transform="translate(1000 520)" opacity={prog(f, s(0, 0.5), 20)}>
            <line x1={0} y1={0} x2={side * 260} y2={0} stroke={C.gold} strokeWidth={5} strokeLinecap="round" />
            {Array.from({ length: ticks + 1 }, (_, i) => (
              <line key={i} x1={i * step * 260} y1={-14 - (i * step === Math.floor(i * step) ? 14 : 0)} x2={i * step * 260} y2={14} stroke={C.ink} strokeWidth={2} />
            ))}
            <rect x={ticks * step * 260} y={-24} width={(side - ticks * step) * 260} height={48} fill="rgba(224,87,75,0.25)" stroke={C.red} />
            <text x={side * 130} y={80} textAnchor="middle" fontFamily={F.display} fontSize={46} fill={C.ink}>
              Seite √5 = 2,2360679…
            </text>
            <text x={side * 130} y={124} textAnchor="middle" fontFamily={F.sans} fontSize={22} fill={C.red} letterSpacing={2}>
              {`EINHEIT 1/${2 ** level} – ES BLEIBT EIN REST`}
            </text>
          </g>
        </Svg>
        <At x={1300} y={300} w={760}>
          <Reveal f={f} at={s(0, 0.3)}>
            <div style={T.label(24, C.gold)}>inkommensurabel</div>
            <div style={{ ...T.serif(40), marginTop: 10 }}>keine gemeinsame Maßeinheit mit dem Fuß</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 1–2 · spiral of Theodorus */}
      <AbsoluteFill style={{ opacity: vis(f, s(1) - 6, s(3) - 6) }}>
        <Svg>
          {pts.slice(0, 16).map((a, k) => {
            const b = pts[k + 1];
            const p = Math.min(1, Math.max(0, shown - k));
            if (p <= 0) return null;
            const [ax, ay] = P(a);
            const [bx, by] = P(b);
            const isLast = k === 15;
            const hue = k / 16;
            return (
              <g key={k} opacity={p}>
                <polygon
                  points={`${sx},${sy} ${ax},${ay} ${bx},${by}`}
                  fill={`rgba(217,181,107,${0.05 + hue * 0.12})`}
                  stroke={isLast ? C.gold : 'rgba(236,230,217,0.55)'}
                  strokeWidth={isLast ? 3 : 1.6}
                />
                <text
                  x={sx + (bx - sx) * 1.08 + (bx - sx) * 0.02}
                  y={sy + (by - sy) * 1.08 + 8}
                  textAnchor="middle"
                  fontFamily={F.display}
                  fontSize={k < 4 ? 30 : 34}
                  fill={isLast ? C.gold : C.ink}
                >
                  √{k + 2}
                </text>
              </g>
            );
          })}
          {/* the next triangle would overlap */}
          <g opacity={prog(f, s(2, 0.62), 20)}>
            {(() => {
              const a = pts[16];
              const r = Math.hypot(...a);
              const b: [number, number] = [a[0] - a[1] / r, a[1] + a[0] / r];
              const [ax, ay] = P(a);
              const [bx, by] = P(b);
              return (
                <polygon points={`${sx},${sy} ${ax},${ay} ${bx},${by}`} fill="rgba(224,87,75,0.2)" stroke={C.red} strokeWidth={2.5} strokeDasharray="8 8" />
              );
            })()}
          </g>
          <circle cx={sx} cy={sy} r={6} fill={C.gold} />
        </Svg>
        <At x={1450} y={330} w={700}>
          <Reveal f={f} at={s(1, 0.1)}>
            <div style={T.label(24, C.gold)}>Theodoros, Tht. 147d</div>
            <div style={{ ...T.display(66), marginTop: 12 }}>√3, √5 … √17</div>
          </Reveal>
        </At>
        <At x={1450} y={560} w={700}>
          <Reveal f={f} at={s(2, 0.05)}>
            <div style={T.label(22)}>Spirale des Theodoros (moderne Hypothese)</div>
            <div style={{ ...T.serif(36), marginTop: 12 }}>
              Winkelsumme bis √17: <span style={{ color: C.gold }}>{angleSum(Math.max(1, Math.round(shown))).toFixed(1)}°</span>
            </div>
            <div style={{ ...T.serif(36), marginTop: 6, opacity: prog(f, s(2, 0.62), 20) }}>
              mit √18: <span style={{ color: C.red }}>{angleSum(17).toFixed(1)}° &gt; 360°</span>
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 3 · square and oblong numbers */}
      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 6) }}>
        <Svg>
          <DotGrid n={4} cols={2} x={330} y={420} at={s(3, 0.3)} color={C.gold} />
          <DotGrid n={9} cols={3} x={520} y={400} at={s(3, 0.35)} color={C.gold} />
          <DotGrid n={3} cols={3} x={1080} y={440} at={s(3, 0.62)} color={C.blue} />
          <DotGrid n={5} cols={5} x={1260} y={440} at={s(3, 0.66)} color={C.blue} />
          <DotGrid n={6} cols={3} x={1560} y={420} at={s(3, 0.7)} color={C.blue} />
        </Svg>
        <At x={500} y={290}>
          <Reveal f={f} at={s(3, 0.3)}>
            <div style={T.label(24, C.gold)}>Quadratzahlen</div>
            <div style={{ ...T.greek(40, C.muted), marginTop: 6 }}>τετράγωνος</div>
          </Reveal>
        </At>
        <At x={1340} y={290}>
          <Reveal f={f} at={s(3, 0.62)}>
            <div style={T.label(24, C.blue)}>längliche Zahlen</div>
            <div style={{ ...T.greek(40, C.muted), marginTop: 6 }}>προμήκης</div>
          </Reveal>
        </At>
        <At x={960} y={700} w={1500}>
          <Reveal f={f} at={s(3, 0.08)}>
            <div style={T.serif(40)}>Theaitetos und der jüngere Sokrates ordnen alle Zahlen in zwei Klassen</div>
          </Reveal>
        </At>
        <At x={960} y={800}>
          <Reveal f={f} at={s(3, 0.5)}>
            <div style={T.serif(36, C.muted)}>4 = 2 · 2 &nbsp;·&nbsp; 9 = 3 · 3 &nbsp;&nbsp;|&nbsp;&nbsp; 3 = 1 · 3 &nbsp;·&nbsp; 5 = 1 · 5 &nbsp;·&nbsp; 6 = 2 · 3</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 4 · length vs. power */}
      <AbsoluteFill style={{ opacity: vis(f, s(4), s(5) - 6) }}>
        <Svg>
          <g transform="translate(470 520)">
            <rect x={-135} y={-135} width={270} height={270} fill="rgba(217,181,107,0.15)" stroke={C.gold} strokeWidth={3} opacity={prog(f, s(4, 0.05), 20)} />
            {[1, 2].map((i) => (
              <g key={i} opacity={prog(f, s(4, 0.12), 20) * 0.5}>
                <line x1={-135 + i * 90} y1={-135} x2={-135 + i * 90} y2={135} stroke={C.gold} />
                <line x1={-135} y1={-135 + i * 90} x2={135} y2={-135 + i * 90} stroke={C.gold} />
              </g>
            ))}
            <Draw f={f} at={s(4, 0.15)} d="M -135 160 H 135" stroke={C.ink} strokeWidth={6} />
          </g>
          <g transform="translate(1390 520)">
            <rect x={-121} y={-121} width={242} height={242} fill="rgba(127,163,201,0.15)" stroke={C.blue} strokeWidth={3} opacity={prog(f, s(4, 0.45), 20)} />
            <Draw f={f} at={s(4, 0.5)} d="M -121 146 H 121" stroke={C.ink} strokeWidth={6} />
          </g>
        </Svg>
        <At x={470} y={520}>
          <div style={{ ...T.display(80), opacity: prog(f, s(4, 0.1), 20) }}>9</div>
        </At>
        <At x={1390} y={520}>
          <div style={{ ...T.display(80), opacity: prog(f, s(4, 0.48), 20) }}>5</div>
        </At>
        <At x={470} y={760}>
          <Reveal f={f} at={s(4, 0.2)}>
            <div style={T.display(56)}>Seite 3</div>
            <div style={{ ...T.label(24, C.gold), marginTop: 10 }}>Länge · <Gr>μῆκος</Gr></div>
          </Reveal>
        </At>
        <At x={1390} y={760}>
          <Reveal f={f} at={s(4, 0.55)}>
            <div style={T.display(56)}>Seite √5</div>
            <div style={{ ...T.label(24, C.blue), marginTop: 10 }}>Potenz · <Gr>δύναμις</Gr></div>
          </Reveal>
        </At>
        <At x={960} y={200} w={1500}>
          <Reveal f={f} at={s(4, 0.72)}>
            <div style={T.serif(40)}>
              √n ist genau dann ganzzahlig, wenn n eine Quadratzahl ist – <span style={{ color: C.gold }}>sonst irrational</span>
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 5 · many → one */}
      <AbsoluteFill style={{ opacity: vis(f, s(5), s(6) - 6) }}>
        {['√2', '√3', '√5', '√6', '√7', '√8', '√10', '…'].map((w, i) => {
          const g = prog(f, s(5, 0.25), 30, easeInOut);
          return (
            <At key={w} x={300 + i * 70 + g * (560 - (300 + i * 70))} y={300 + (i % 2) * 70 + g * (440 - (300 + (i % 2) * 70))}>
              <div style={{ ...T.display(54), opacity: prog(f, s(5) + i * 3, 12) * (1 - g * 0.9) }}>{w}</div>
            </At>
          );
        })}
        <At x={600} y={460}>
          <Reveal f={f} at={s(5, 0.4)}>
            <div style={T.greek(80)}>δύναμις</div>
          </Reveal>
        </At>
        {['Geometrie', 'Schusterei', 'Astronomie', 'Zimmermannskunst', '…'].map((w, i) => {
          const g = prog(f, s(5, 0.55), 30, easeInOut);
          return (
            <At key={w} x={1220 + (i % 2) * 260 + g * (1360 - (1220 + (i % 2) * 260))} y={280 + i * 60 + g * (460 - (280 + i * 60))}>
              <div style={{ ...T.serif(40), opacity: prog(f, s(5, 0.3) + i * 3, 12) * (1 - g * 0.9) }}>{w}</div>
            </At>
          );
        })}
        <At x={1360} y={460}>
          <Reveal f={f} at={s(5, 0.7)}>
            <div style={T.display(110, C.gold)}>?</div>
          </Reveal>
        </At>
        <At x={960} y={760} w={1400}>
          <Reveal f={f} at={s(5, 0.15)}>
            <div style={T.serif(42)}>unendlich viele Fälle – ein einziger Begriff</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 6 · Theaetetus' legacy: Euclid X and XIII */}
      <AbsoluteFill style={{ opacity: vis(f, s(6)) }}>
        <Svg>
          <Solid vs={octa} cx={620} cy={470} size={200} f={f} at={s(6, 0.4)} color={C.gold} />
          <Solid vs={ico} cx={1300} cy={470} size={220} f={f} at={s(6, 0.5)} color={C.blue} />
        </Svg>
        <At x={620} y={760}>
          <Reveal f={f} at={s(6, 0.45)}>
            <div style={T.display(56)}>Oktaeder</div>
          </Reveal>
        </At>
        <At x={1300} y={760}>
          <Reveal f={f} at={s(6, 0.55)}>
            <div style={T.display(56)}>Ikosaeder</div>
          </Reveal>
        </At>
        <At x={960} y={170} w={1600}>
          <Reveal f={f} at={s(6, 0.15)}>
            <div style={T.label(24, C.gold)}>Euklid, Elemente X · Irrationalitäten &nbsp;&nbsp;|&nbsp;&nbsp; Elemente XIII · regelmäßige Körper</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── V · Hebammenkunst ───────────── */

export const Hebamme: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const pulse = 1 + 0.06 * Math.sin(f / 6);
  const early = ['Apologie', 'Kriton', 'Euthyphron', 'Laches', 'Charmides', 'Protagoras', 'Gorgias', 'Menon'];
  return (
    <AbsoluteFill>
      {/* 0 · labour pains */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Svg>
          {[0, 1, 2].map((i) => (
            <circle
              key={i}
              cx={960}
              cy={470}
              r={(140 + i * 60) * pulse}
              fill="none"
              stroke={C.gold}
              strokeWidth={2}
              opacity={(0.5 - i * 0.15) * prog(f, i * 8, 20)}
            />
          ))}
        </Svg>
        <At x={960} y={470}>
          <div style={{ ...T.display(150, C.gold), opacity: prog(f, 10, 20) }}>?</div>
        </At>
        <At x={960} y={800}>
          <Reveal f={f} at={s(0, 0.5)}>
            <div style={T.italic(46)}>„Geburtswehen“</div>
            <div style={{ ...T.label(22), marginTop: 10 }}><Gr>ὠδίνεις</Gr> · Tht. 148e</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 1 · Socrates the midwife */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(1), 30)}>
            <circle cx={520} cy={480} r={230} fill="rgba(207,106,71,0.08)" stroke={C.line} />
            <Profile x={520} y={490} s={1.35} beard bald snub color={C.ink} />
          </g>
        </Svg>
        <div style={{ position: 'absolute', left: 900, top: 250, width: 880, display: 'flex', flexDirection: 'column', gap: 30 }}>
          <Reveal f={f} at={s(1, 0.05)}>
            <div style={T.label(24, C.gold)}>Sohn der Hebamme Phainarete</div>
          </Reveal>
          <Reveal f={f} at={s(1, 0.3)}>
            <div style={T.serif(44)}>Männer statt Frauen</div>
          </Reveal>
          <Reveal f={f} at={s(1, 0.38)}>
            <div style={T.serif(44)}>Seelen statt Körper</div>
          </Reveal>
          <Reveal f={f} at={s(1, 0.6)}>
            <Card>
              <div style={T.greek(50)}>ἄγονός εἰμι σοφίας</div>
              <div style={{ ...T.italic(36, C.muted), marginTop: 6 }}>„unfruchtbar an Weisheit“ – Tht. 150c</div>
            </Card>
          </Reveal>
        </div>
      </AbsoluteFill>

      {/* 2 · genuine child or wind-egg */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(2, 0.05), 20)}>
            <circle cx={620} cy={460} r={170 * prog(f, s(2, 0.45), 30)} fill="url(#goldGlow)" />
            <Egg x={620} y={460} s={2.2} crack={prog(f, s(2, 0.4), 24)} color={C.gold} />
            {Array.from({ length: 10 }, (_, i) => {
              const a = (i / 10) * Math.PI * 2;
              const p = prog(f, s(2, 0.45), 24);
              return <line key={i} x1={620 + Math.cos(a) * 140} y1={470 + Math.sin(a) * 140} x2={620 + Math.cos(a) * (140 + 70 * p)} y2={470 + Math.sin(a) * (140 + 70 * p)} stroke={C.gold} strokeWidth={3} opacity={p} strokeLinecap="round" />;
            })}
          </g>
          <g opacity={prog(f, s(2, 0.1), 20)}>
            <Egg x={1300} y={460} s={2.2} crack={prog(f, s(2, 0.55), 24)} color={C.muted} />
            {[0, 1, 2].map((i) => {
              const p = prog(f, s(2, 0.6) + i * 4, 30);
              return <circle key={i} cx={1300 + (i - 1) * 40} cy={440 - p * 180} r={18 + p * 30} fill="none" stroke={C.muted} strokeWidth={2} opacity={(1 - p) * 0.8} />;
            })}
          </g>
        </Svg>
        <At x={620} y={760}>
          <Reveal f={f} at={s(2, 0.45)}>
            <div style={T.greek(46)}>γόνιμόν τε καὶ ἀληθές</div>
            <div style={{ ...T.label(22), marginTop: 8 }}>fruchtbar und wahr</div>
          </Reveal>
        </At>
        <At x={1300} y={760}>
          <Reveal f={f} at={s(2, 0.58)}>
            <div style={T.greek(46, C.muted)}>εἴδωλον καὶ ψεῦδος</div>
            <div style={{ ...T.label(22), marginTop: 8 }}>Trugbild · Windei · <Gr>ἀνεμιαῖον</Gr></div>
          </Reveal>
        </At>
        <At x={960} y={170}>
          <Reveal f={f} at={s(2)}>
            <div style={T.label(24, C.gold)}>Die Prüfung · Tht. 150b–c</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 3 · Platonic invention */}
      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 6) }}>
        <At x={960} y={170}>
          <Reveal f={f} at={s(3)}>
            <div style={T.label(24, C.gold)}>Sokrates als Hebamme – nur im Theaitetos</div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', top: 260, left: 0, right: 0, display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: 22, padding: '0 220px' }}>
          {early.map((w, i) => (
            <Reveal key={w} f={f} at={s(3, 0.05 + i * 0.03)}>
              <div style={{ ...T.serif(38, C.muted), padding: '10px 22px', border: `1px solid ${C.line}`, borderRadius: 12 }}>{w}</div>
            </Reveal>
          ))}
          <Reveal f={f} at={s(3, 0.35)}>
            <div style={{ ...T.serif(38, C.gold), padding: '10px 22px', border: `2px solid ${C.gold}`, borderRadius: 12, boxShadow: `0 0 24px rgba(217,181,107,0.3)` }}>
              Theaitetos
            </div>
          </Reveal>
        </div>
        <div style={{ position: 'absolute', top: 560, left: 260, right: 260, display: 'flex', gap: 40 }}>
          <Reveal f={f} at={s(3, 0.4)} style={{ flex: 1 }}>
            <Card>
              <div style={T.label(22, C.gold)}>Burnyeat 1977</div>
              <div style={{ ...T.serif(36), marginTop: 10 }}>Die Hebammenkunst ist Platons Erfindung, nicht Erbe des historischen Sokrates.</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(3, 0.65)} style={{ flex: 1 }}>
            <Card>
              <div style={T.label(22, C.gold)}>Sedley 2004</div>
              <div style={{ ...T.serif(36), marginTop: 10 }}>
                <i>The Midwife of Platonism</i>: Sokrates bringt Gedanken zur Welt, die erst Platon ausarbeitet.
              </div>
            </Card>
          </Reveal>
        </div>
      </AbsoluteFill>

      {/* 4 · three newborns */}
      <AbsoluteFill style={{ opacity: vis(f, s(4)) }}>
        <Svg>
          {[0, 1, 2].map((i) => (
            <g key={i} opacity={prog(f, s(4, 0.3 + i * 0.12), 20)}>
              <Egg x={560 + i * 400} y={470} s={1.8} color={C.ink} />
            </g>
          ))}
        </Svg>
        {['Wahrnehmung', 'wahre Meinung', 'wahre Meinung mit Logos'].map((w, i) => (
          <At key={w} x={560 + i * 400} y={700} w={360}>
            <Reveal f={f} at={s(4, 0.32 + i * 0.12)}>
              <div style={T.display(70, C.gold)}>{i + 1}</div>
              <div style={{ ...T.serif(36), marginTop: 4 }}>{w}</div>
            </Reveal>
          </At>
        ))}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
