import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Ear, Eye, Hand, Mouth, Nose } from '../components/icons';
import { Arrow, At, Card, easeInOut, Formula, Gr, lerp, prog, Quote, Reveal, Strike, Svg, T, vis } from '../components/kit';
import { C, F } from '../theme';
import { SceneTiming } from '../timeline';
import { useScene } from './util';

type P = { t: SceneTiming };

const SENSES = [Eye, Ear, Nose, Mouth, Hand];

/* ───────────── XVI · Das hölzerne Pferd ───────────── */

export const Pferd: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const toSoul = prog(f, s(0, 0.6), 40, easeInOut);
  const koina = ['Sein', 'Nichtsein', 'Ähnlich', 'Unähnlich', 'Dasselbe', 'Verschieden', 'Eins', 'Zahl', 'Gerade', 'Ungerade'];
  const horseOpacity = prog(f, s(0, 0.05), 24) * (1 - prog(f, s(0, 0.55), 20));
  return (
    <AbsoluteFill>
      {/* 0 · Trojan horse → one soul */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g opacity={horseOpacity} stroke={C.terracotta} strokeWidth={3} fill="rgba(207,106,71,0.08)" strokeLinejoin="round">
            <path d="M 640 330 C 640 290 680 280 720 280 H 1240 C 1300 280 1320 310 1320 350 V 520 C 1320 560 1300 580 1260 580 H 700 C 660 580 640 560 640 520 Z" />
            {[320, 370, 420, 470, 520].map((y) => (
              <line key={y} x1={650} y1={y} x2={1310} y2={y} opacity={0.4} />
            ))}
            <path d="M 700 300 L 600 140 L 560 90 L 470 110 L 450 160 L 520 180 L 600 300" />
            <path d="M 560 90 L 590 50 L 600 100" />
            <circle cx={530} cy={125} r={6} fill={C.terracotta} />
            <path d="M 1320 340 C 1380 360 1400 420 1380 480" fill="none" />
            {[700, 820, 1140, 1260].map((x) => (
              <rect key={x} x={x - 18} y={580} width={36} height={140} />
            ))}
            <rect x={620} y={720} width={720} height={30} />
            {[680, 860, 1100, 1280].map((x) => (
              <circle key={x} cx={x} cy={770} r={30} />
            ))}
          </g>
          {SENSES.map((Comp, i) => {
            const hx = 760 + i * 110;
            const hy = 430;
            const a = (i / SENSES.length) * Math.PI * 2 - Math.PI / 2;
            const sx = 960 + Math.cos(a) * 260;
            const sy = 560 + Math.sin(a) * 260;
            const x = lerp(hx, sx, toSoul);
            const y = lerp(hy, sy, toSoul);
            return (
              <g key={i} opacity={prog(f, s(0, 0.12) + i * 4, 16)}>
                <Comp x={x} y={y} s={0.75} color={C.ink} />
                <line x1={x} y1={y} x2={960} y2={560} stroke={C.gold} strokeWidth={2} strokeDasharray="6 8" opacity={prog(f, s(0, 0.8), 20) * 0.8} />
              </g>
            );
          })}
          <circle cx={960} cy={560} r={90 * toSoul} fill="rgba(217,181,107,0.15)" stroke={C.gold} strokeWidth={3} />
        </Svg>
        <At x={960} y={560}>
          <div style={{ ...T.greek(54), opacity: toSoul }}>ψυχή</div>
        </At>
        <At x={960} y={150}>
          <Reveal f={f} at={s(0, 0.05)} out={s(0, 0.55)}>
            <div style={T.label(24, C.terracotta)}>„wie Krieger im hölzernen Pferd“ · Tht. 184d</div>
          </Reveal>
        </At>
        <At x={960} y={150}>
          <Reveal f={f} at={s(0, 0.7)}>
            <div style={T.label(24, C.gold)}>
              nicht <i>mit</i> den Augen – <span style={{ color: C.ink }}>durch</span> die Augen · Werkzeuge der Seele
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 1 · each sense its own domain */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(1, 0.05), 20)}>
            <Eye x={500} y={360} s={1.3} />
            <rect x={760} y={310} width={110} height={110} rx={14} fill={C.terracotta} />
          </g>
          <g opacity={prog(f, s(1, 0.12), 20)}>
            <Ear x={500} y={640} s={1.5} />
            {[0, 1, 2].map((i) => (
              <path key={i} d={`M ${780 + i * 30} ${600 - i * 12} Q ${810 + i * 30} 640 ${780 + i * 30} ${680 + i * 12}`} stroke={C.blue} strokeWidth={4} fill="none" />
            ))}
          </g>
          <Arrow f={f} at={s(1, 0.08)} x1={580} y1={360} x2={740} y2={360} />
          <Arrow f={f} at={s(1, 0.15)} x1={580} y1={640} x2={750} y2={640} color={C.blue} />
          <g opacity={prog(f, s(1, 0.25), 12) * (1 - prog(f, s(1, 0.45), 12))}>
            <Arrow f={f} at={s(1, 0.25)} x1={560} y1={420} x2={760} y2={600} color={C.red} dashed />
            <text x={700} y={520} fill={C.red} fontFamily={F.display} fontSize={60}>
              ✗
            </text>
          </g>
        </Svg>
        <div style={{ position: 'absolute', left: 1020, top: 240, width: 760, display: 'flex', flexDirection: 'column', gap: 22 }}>
          <Reveal f={f} at={s(1, 0.45)}>
            <div style={T.label(24, C.gold)}>Ton und Farbe:</div>
          </Reveal>
          {['beide sind', 'jedes ist vom anderen verschieden', 'jedes ist mit sich selbst dasselbe', 'zusammen sind sie zwei'].map((w, i) => (
            <Reveal key={w} f={f} at={s(1, 0.5 + i * 0.07)}>
              <div style={T.serif(42)}>{w}</div>
            </Reveal>
          ))}
          <Reveal f={f} at={s(1, 0.85)}>
            <div style={{ ...T.display(52, C.gold), marginTop: 20 }}>Durch welches Organ?</div>
          </Reveal>
        </div>
      </AbsoluteFill>

      {/* 2 · the common notions */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <Svg>
          <circle cx={960} cy={500} r={110} fill="rgba(217,181,107,0.12)" stroke={C.gold} strokeWidth={3} opacity={prog(f, s(2), 20)} />
          <circle cx={960} cy={500} r={330} fill="none" stroke={C.line} strokeDasharray="4 10" opacity={prog(f, s(2, 0.1), 20)} />
        </Svg>
        <At x={960} y={500}>
          <div style={{ opacity: prog(f, s(2), 20) }}>
            <div style={T.greek(56)}>ψυχή</div>
          </div>
        </At>
        {koina.map((k, i) => {
          const a = (i / koina.length) * Math.PI * 2 - Math.PI / 2 + (f - s(2)) / 400;
          return (
            <At key={k} x={960 + Math.cos(a) * 330} y={500 + Math.sin(a) * 330}>
              <Reveal f={f} at={s(2, 0.12 + i * 0.05)}>
                <div style={{ ...T.serif(38), background: C.bg, padding: '2px 12px', borderRadius: 8 }}>{k}</div>
              </Reveal>
            </At>
          );
        })}
        <At x={960} y={900} w={1600}>
          <Reveal f={f} at={s(2, 0.75)}>
            <div style={T.greek(42)}>αὐτὴ διʼ αὑτῆς ἡ ψυχὴ τὰ κοινά … ἐπισκοπεῖν</div>
            <div style={T.label(20)}>„die Seele selbst, durch sich selbst, betrachtet das Gemeinsame“ · Tht. 185e</div>
          </Reveal>
        </At>
        <At x={960} y={110}>
          <Reveal f={f} at={s(2, 0.05)}>
            <div style={T.label(24, C.gold)}>
              <Gr>τὰ κοινά</Gr> · das Gemeinsame · Tht. 185c–d
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 3 · being and truth only in reasoning */}
      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 6) }}>
        <Svg>
          <rect x={360} y={600} width={1200} height={160} rx={20} fill="rgba(127,163,201,0.08)" stroke={C.blue} strokeWidth={2} opacity={prog(f, s(3, 0.05), 20)} />
          <rect x={360} y={240} width={1200} height={160} rx={20} fill="rgba(217,181,107,0.08)" stroke={C.gold} strokeWidth={2} opacity={prog(f, s(3, 0.15), 20)} />
          <Arrow f={f} at={s(3, 0.3)} x1={960} y1={590} x2={960} y2={420} color={C.gold} width={4} />
          <g opacity={prog(f, s(3, 0.5), 20)}>
            <Arrow f={f} at={s(3, 0.5)} x1={600} y1={590} x2={600} y2={430} color={C.red} dashed />
            <text x={630} y={520} fill={C.red} fontFamily={F.display} fontSize={56}>
              ✗
            </text>
          </g>
        </Svg>
        <At x={960} y={680}>
          <Reveal f={f} at={s(3, 0.05)}>
            <div style={T.display(48)}>Eindrücke</div>
            <div style={T.greek(34, C.blue)}>παθήματα · Wahrnehmung</div>
          </Reveal>
        </At>
        <At x={960} y={320}>
          <Reveal f={f} at={s(3, 0.15)}>
            <div style={T.display(48)}>Schließen über sie</div>
            <div style={T.greek(34)}>συλλογισμός → οὐσία · ἀλήθεια</div>
          </Reveal>
        </At>
        <At x={960} y={900}>
          <Reveal f={f} at={s(3, 0.8)}>
            <div style={T.display(72)}>
              <span style={{ fontFamily: F.greek }}>αἴσθησις</span> <span style={{ color: C.red }}>≠</span>{' '}
              <span style={{ fontFamily: F.greek, color: C.gold }}>ἐπιστήμη</span>
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 4 · Kant */}
      <AbsoluteFill style={{ opacity: vis(f, s(4)), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(4, 0.05)}>
          <div style={{ ...T.display(66), marginBottom: 60 }}>
            Erkennen <span style={{ color: C.gold }}>=</span> Urteilen
          </div>
        </Reveal>
        <Quote f={f} at={s(4, 0.55)} de="Gedanken ohne Inhalt sind leer, Anschauungen ohne Begriffe sind blind." src="Kant, Kritik der reinen Vernunft, A 51 / B 75" width={1400} size={52} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XVII · Erkenntnis ist wahre Meinung ───────────── */

export const Def2: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const cells = [
    ['kenne A', 'kenne B'],
    ['kenne A', 'kenne B nicht'],
    ['kenne A nicht', 'kenne B'],
    ['kenne A nicht', 'kenne B nicht'],
  ];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Formula f={f} at={s(0, 0.4)} left="ἐπιστήμη" right="δόξα ἀληθής" leftDe="Erkenntnis" rightDe="wahre Meinung" size={104} />
        <Reveal f={f} at={s(0, 0.15)}>
          <div style={{ ...T.serif(36, C.muted), marginTop: 70 }}>
            <Gr>δοξάζειν</Gr> – meinen, urteilen: die Seele selbst beschäftigt sich mit dem Seienden
          </div>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(1, 0.3)}>
          <div style={T.display(84)}>Wie ist eine falsche Meinung möglich?</div>
        </Reveal>
        <Reveal f={f} at={s(1, 0.55)}>
          <div style={{ ...T.greek(60), marginTop: 30 }}>ψευδὴς δόξα</div>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <div style={{ position: 'absolute', top: 210, left: 360, width: 1200, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 30 }}>
          {cells.map(([a, b], i) => (
            <Reveal key={i} f={f} at={s(2, 0.12 + i * 0.12)}>
              <Card style={{ height: 250, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                <div style={T.serif(38)}>
                  {a} · {b}
                </div>
                <div style={{ position: 'relative', marginTop: 16 }}>
                  <div style={T.italic(40, C.muted)}>„A ist B“?</div>
                  <Strike f={f} at={s(2, 0.22 + i * 0.12)} />
                </div>
              </Card>
            </Reveal>
          ))}
        </div>
        <At x={960} y={130}>
          <Reveal f={f} at={s(2, 0.02)}>
            <div style={T.label(24, C.gold)}>Wissen oder Nichtwissen · Tht. 188a–c</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(3)) }}>
        <Svg>
          <g opacity={prog(f, s(3, 0.1), 20)}>
            <Eye x={420} y={480} s={1.6} look={1} />
          </g>
          <circle cx={800} cy={480} r={70} fill="none" stroke={C.muted} strokeWidth={2} strokeDasharray="6 8" opacity={prog(f, s(3, 0.2), 20)} />
        </Svg>
        <div style={{ position: 'absolute', left: 980, top: 300, display: 'flex', flexDirection: 'column', gap: 28 }}>
          {['das Nichtseiende meinen', '= nichts meinen', '= überhaupt nicht meinen'].map((w, i) => (
            <Reveal key={w} f={f} at={s(3, 0.3 + i * 0.15)}>
              <div style={T.display(56, i === 2 ? C.red : C.ink)}>{w}</div>
            </Reveal>
          ))}
        </div>
        <At x={960} y={860}>
          <Reveal f={f} at={s(3, 0.8)}>
            <div style={T.label(24)}>Tht. 188c–189b</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XVIII · Denken als Gespräch ───────────── */

export const Dialog: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const swap = prog(f, s(0, 0.45), 30, easeInOut);
  const talk = [
    ['Ist es so?', 'L'],
    ['Ja.', 'R'],
    ['Und dies?', 'L'],
    ['Nein.', 'R'],
  ] as const;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(0, 0.2), 20)}>
            <circle cx={lerp(760, 1160, swap)} cy={500 - Math.sin(swap * Math.PI) * 120} r={90} fill="rgba(217,181,107,0.15)" stroke={C.gold} strokeWidth={3} />
            <rect
              x={lerp(1160, 760, swap) - 85}
              y={500 + Math.sin(swap * Math.PI) * 120 - 85}
              width={170}
              height={170}
              rx={14}
              fill="rgba(127,163,201,0.15)"
              stroke={C.blue}
              strokeWidth={3}
            />
          </g>
        </Svg>
        <At x={960} y={180}>
          <Reveal f={f} at={s(0, 0.1)}>
            <div style={T.greek(64)}>ἀλλοδοξία</div>
            <div style={T.label(22)}>etwas für etwas anderes halten</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <circle cx={960} cy={430} r={260} fill="rgba(217,181,107,0.05)" stroke={C.line} strokeWidth={2} opacity={prog(f, s(1), 20)} />
        </Svg>
        {talk.map(([w, side], i) => (
          <At key={i} x={side === 'L' ? 820 : 1100} y={290 + i * 90}>
            <Reveal f={f} at={s(1, 0.1 + i * 0.08)} x={side === 'L' ? -30 : 30}>
              <div style={{ ...T.serif(40, side === 'L' ? C.ink : C.gold), padding: '8px 22px', borderRadius: 24, border: `1.5px solid ${side === 'L' ? C.line : C.gold}` }}>{w}</div>
            </Reveal>
          </At>
        ))}
        <At x={960} y={780} w={1600}>
          <Reveal f={f} at={s(1, 0.5)}>
            <div style={T.greek(46)}>λόγον ὃν αὐτὴ πρὸς αὑτὴν ἡ ψυχὴ διεξέρχεται</div>
            <div style={{ ...T.italic(38), marginTop: 10 }}>„eine Rede, welche die Seele bei sich selbst durchgeht“</div>
          </Reveal>
        </At>
        <At x={960} y={920}>
          <Reveal f={f} at={s(1, 0.78)}>
            <div style={T.label(22, C.gold)}>
              Meinung: <Gr>σιγῇ πρὸς αὑτόν</Gr> – schweigend zu sich selbst · Tht. 189e–190a
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2)), justifyContent: 'center', alignItems: 'center' }}>
        {['„Der Ochse ist ganz gewiss ein Pferd.“', '„Zwei ist eins.“'].map((w, i) => (
          <Reveal key={w} f={f} at={s(2, 0.15 + i * 0.12)}>
            <div style={{ position: 'relative', margin: '24px 0' }}>
              <div style={T.display(70)}>{w}</div>
              <Strike f={f} at={s(2, 0.45 + i * 0.06)} />
            </div>
          </Reveal>
        ))}
        <Reveal f={f} at={s(2, 0.7)}>
          <div style={{ ...T.italic(44, C.muted), marginTop: 40 }}>Das sagt niemand zu sich selbst – nicht einmal im Wahnsinn.</div>
          <div style={{ ...T.label(20), marginTop: 14, textAlign: 'center' }}>Tht. 190b–c</div>
        </Reveal>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

