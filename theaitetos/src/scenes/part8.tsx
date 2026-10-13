import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Coin, Figure, Profile } from '../components/icons';
import { Arrow, At, Card, easeInOut, Gr, lerp, prog, Reveal, Strike, Svg, T, vis } from '../components/kit';
import { C, F } from '../theme';
import { SceneTiming } from '../timeline';
import { useScene } from './util';

type P = { t: SceneTiming };

/* ───────────── XXVIII · Deutungen ───────────── */

export const Deutung: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const fly = prog(f, s(4, 0.55), 40, easeInOut);
  return (
    <AbsoluteFill>
      {/* Forms absent */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(0, 0.2), 30)} filter="url(#glow)">
            <circle cx={700} cy={360} r={80} fill="none" stroke={C.gold} strokeWidth={3} />
            <polygon points="960,270 1050,430 870,430" fill="none" stroke={C.gold} strokeWidth={3} />
            <rect x={1150} y={290} width={140} height={140} fill="none" stroke={C.gold} strokeWidth={3} />
          </g>
          <line x1={400} y1={540} x2={1520} y2={540} stroke={C.line} strokeWidth={2} strokeDasharray="10 10" opacity={prog(f, s(0, 0.3), 20)} />
        </Svg>
        <At x={960} y={160}>
          <Reveal f={f} at={s(0, 0.1)}>
            <div style={T.label(24, C.gold)}>
              die Ideen · <Gr>εἴδη</Gr> – in Phaidon und Politeia Grundlage des Wissens
            </div>
          </Reveal>
        </At>
        <At x={960} y={700} w={1500}>
          <Reveal f={f} at={s(0, 0.55)}>
            <div style={T.display(60)}>Im Theaitetos: nicht ausdrücklich da</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* Cornford */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(1, 0.05)}>
          <div style={T.label(26, C.gold)}>F. M. Cornford, Plato's Theory of Knowledge (1935)</div>
        </Reveal>
        <Reveal f={f} at={s(1, 0.25)}>
          <Card style={{ marginTop: 40, maxWidth: 1400 }}>
            <div style={T.italic(46)}>„… without them there is no knowledge at all.“</div>
            <div style={{ ...T.serif(38, C.muted), marginTop: 14 }}>„… ohne sie [die Ideen] gibt es überhaupt kein Wissen.“ – S. 28</div>
          </Card>
        </Reveal>
        <Reveal f={f} at={s(1, 0.65)}>
          <div style={{ ...T.serif(40), marginTop: 40 }}>Der Dialog scheitert absichtlich.</div>
        </Reveal>
      </AbsoluteFill>

      {/* Revisionists and Burnyeat's two readings */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <At x={960} y={170} w={1600}>
          <Reveal f={f} at={s(2, 0.05)}>
            <div style={T.serif(40)}>
              <span style={{ color: C.gold }}>Revisionisten</span> (Ryle, Owen u. a.): Der späte Platon prüft seine Ideenlehre kritisch.
            </div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', top: 330, left: 220, right: 220, display: 'flex', gap: 50 }}>
          <Reveal f={f} at={s(2, 0.45)} style={{ flex: 1 }}>
            <Card>
              <div style={T.label(22, C.gold)}>Lesart A · Cornford</div>
              <div style={{ ...T.serif(38), marginTop: 12 }}>Wahrnehmung scheitert, weil der eigentliche Gegenstand des Wissens die Ideen sind.</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(2, 0.7)} style={{ flex: 1 }}>
            <Card accent={C.blue}>
              <div style={T.label(22, C.blue)}>Lesart B · Burnyeat</div>
              <div style={{ ...T.serif(38), marginTop: 12 }}>Wahrnehmung scheitert, weil sie nicht einmal ein einfaches Urteil fassen kann.</div>
            </Card>
          </Reveal>
        </div>
        <At x={960} y={850}>
          <Reveal f={f} at={s(2, 0.5)}>
            <div style={T.label(22)}>Burnyeat 1990 · für den ersten Teil, Tht. 151–187</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* Sedley */}
      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(3, 0.1), 24)}>
            <circle cx={560} cy={480} r={170} fill="rgba(207,106,71,0.08)" stroke={C.line} />
            <Profile x={560} y={490} s={1} beard bald snub />
          </g>
          <Arrow f={f} at={s(3, 0.35)} x1={760} y1={480} x2={1120} y2={480} color={C.gold} width={4} />
          <g opacity={prog(f, s(3, 0.45), 30)}>
            <circle cx={1360} cy={480} r={170} fill="url(#goldGlow)" />
            <circle cx={1360} cy={480} r={120} fill="none" stroke={C.gold} strokeWidth={3} />
          </g>
        </Svg>
        <At x={560} y={720}>
          <Reveal f={f} at={s(3, 0.1)}>
            <div style={T.display(48)}>der historische Sokrates</div>
          </Reveal>
        </At>
        <At x={1360} y={480}>
          <Reveal f={f} at={s(3, 0.5)}>
            <div style={T.display(48, C.gold)}>Platonismus</div>
          </Reveal>
        </At>
        <At x={1360} y={720}>
          <Reveal f={f} at={s(3, 0.6)}>
            <div style={T.label(20)}>Politeia · Phaidon</div>
          </Reveal>
        </At>
        <At x={960} y={170}>
          <Reveal f={f} at={s(3, 0.05)}>
            <div style={T.label(24, C.gold)}>David Sedley, The Midwife of Platonism (2004)</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* Sophist: Theaetetus flies */}
      <AbsoluteFill style={{ opacity: vis(f, s(4)) }}>
        <Svg>
          <g opacity={prog(f, s(4, 0.35), 24)}>
            <Figure x={560} y={600} s={1.3} color={C.gold} />
            <rect x={490} y={680} width={140} height={20} fill="rgba(236,230,217,0.2)" stroke={C.ink} />
          </g>
          <g opacity={prog(f, s(4, 0.5), 24) * 0.5} transform={`translate(0 ${-fly * 160})`}>
            <Figure x={1360} y={600} s={1.3} color={C.muted} fill="none" />
            <path d="M 1300 560 C 1240 520 1220 470 1250 440 M 1420 560 C 1480 520 1500 470 1470 440" stroke={C.muted} strokeWidth={3} fill="none" />
          </g>
        </Svg>
        <At x={960} y={170} w={1600}>
          <Reveal f={f} at={s(4, 0.05)}>
            <div style={T.label(24, C.gold)}>am nächsten Morgen · Sophistes, mit dem Fremden aus Elea</div>
          </Reveal>
        </At>
        <At x={560} y={820}>
          <Reveal f={f} at={s(4, 0.35)}>
            <div style={T.display(52, C.gold)}>„Theaitetos sitzt.“</div>
            <div style={T.label(20)}>wahr</div>
          </Reveal>
        </At>
        <At x={1360} y={820}>
          <Reveal f={f} at={s(4, 0.5)}>
            <div style={T.display(52)}>„Theaitetos fliegt.“</div>
            <div style={T.label(20, C.red)}>falsch – aber nicht „nichts“</div>
          </Reveal>
        </At>
        <At x={960} y={940} w={1600}>
          <Reveal f={f} at={s(4, 0.75)}>
            <div style={T.italic(38)}>sagt von etwas, das ist, etwas aus, das von dem verschieden ist, was über ihn wahr ist · Sophistes 263b</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XXIX · Gettier ───────────── */

export const Gettier: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const job = prog(f, s(3, 0.15), 30, easeInOut);
  const tri = [
    { x: 960, y: 260, w: 'wahr' },
    { x: 700, y: 680, w: 'geglaubt' },
    { x: 1220, y: 680, w: 'gerechtfertigt' },
  ];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <path d="M 960 300 L 720 640 L 1200 640 Z" fill="rgba(217,181,107,0.06)" stroke={C.gold} strokeWidth={3} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - prog(f, s(0, 0.15), 40, easeInOut)} />
        </Svg>
        {tri.map((p, i) => (
          <At key={p.w} x={p.x} y={p.y}>
            <Reveal f={f} at={s(0, 0.2 + i * 0.08)}>
              <div style={T.display(52)}>{p.w}</div>
            </Reveal>
          </At>
        ))}
        <At x={960} y={540}>
          <Reveal f={f} at={s(0, 0.5)}>
            <div style={T.display(56, C.gold)}>Wissen?</div>
          </Reveal>
        </At>
        <At x={960} y={860}>
          <Reveal f={f} at={s(0, 0.7)}>
            <div style={T.label(24)}>„justified true belief“ – zurückgeführt auf Tht. 201c–d · Menon 98a</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(1, 0.1)}>
          <Card style={{ width: 1100, padding: '50px 60px' }}>
            <div style={T.label(22, C.gold)}>Analysis 23 (1963), S. 121–123</div>
            <div style={{ ...T.display(66), marginTop: 18 }}>Is Justified True Belief Knowledge?</div>
            <div style={{ ...T.serif(36, C.muted), marginTop: 10 }}>Edmund L. Gettier</div>
            <div style={{ height: 1, background: C.line, margin: '30px 0' }} />
            <div style={{ ...T.serif(30, C.muted), opacity: prog(f, s(1, 0.6), 20) }}>
              Fußnote 1: … <span style={{ color: C.gold }}>Theaetetus 201</span> … <span style={{ color: C.gold }}>Meno 98</span>
            </div>
          </Card>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2), s(4) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(2, 0.05), 20)}>
            <Figure x={560} y={560} s={1.5} color={C.ink} />
          </g>
          <g opacity={prog(f, s(2, 0.12), 20)}>
            <Figure x={1360} y={560} s={1.5} color={C.ink} />
          </g>
          {Array.from({ length: 10 }, (_, i) => (
            <g key={`j${i}`} opacity={prog(f, s(2, 0.35) + i * 2, 10)}>
              <Coin x={1240 + (i % 5) * 60} y={780 + Math.floor(i / 5) * 60} s={0.8} />
            </g>
          ))}
          {Array.from({ length: 10 }, (_, i) => (
            <g key={`s${i}`} opacity={prog(f, s(3, 0.45) + i * 2, 10)}>
              <Coin x={440 + (i % 5) * 60} y={780 + Math.floor(i / 5) * 60} s={0.8} color={C.olive} />
            </g>
          ))}
          <g transform={`translate(${lerp(1360, 560, job)} ${360 - Math.sin(job * Math.PI) * 120})`} opacity={prog(f, s(2, 0.25), 16)}>
            <rect x={-70} y={-34} width={140} height={60} rx={10} fill={C.bg} stroke={C.gold} strokeWidth={3} />
            <text x={0} y={6} textAnchor="middle" fontFamily={F.sans} fontSize={22} fill={C.gold} letterSpacing={2}>
              STELLE
            </text>
          </g>
        </Svg>
        <At x={560} y={240}>
          <Reveal f={f} at={s(2, 0.05)}>
            <div style={T.display(56)}>Smith</div>
          </Reveal>
        </At>
        <At x={1360} y={240}>
          <Reveal f={f} at={s(2, 0.12)}>
            <div style={T.display(56)}>Jones</div>
          </Reveal>
        </At>
        <At x={960} y={130} w={1400}>
          <div style={{ opacity: vis(f, s(2, 0.6), s(3, 0.1)) }}>
            <Card>
              <div style={T.italic(38)}>Smith schließt: „Der Mann, der die Stelle bekommt, hat zehn Münzen in der Tasche.“</div>
            </Card>
          </div>
        </At>
        <At x={960} y={130} w={1500}>
          <div style={{ opacity: prog(f, s(3, 0.6), 16), display: 'flex', gap: 50, justifyContent: 'center' }}>
            <div style={T.display(52, C.gold)}>wahr ✓</div>
            <div style={T.display(52, C.gold)}>gerechtfertigt ✓</div>
            <div style={{ position: 'relative' }}>
              <div style={T.display(52, C.red)}>Wissen</div>
              <Strike f={f} at={s(3, 0.75)} />
            </div>
          </div>
        </At>
        <At x={560} y={960}>
          <div style={{ ...T.label(20, C.olive), opacity: prog(f, s(3, 0.5), 16) }}>ohne es zu wissen</div>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(4)) }}>
        <div style={{ position: 'absolute', top: 260, left: 220, right: 220, display: 'flex', gap: 50 }}>
          <Reveal f={f} at={s(4, 0.05)} style={{ flex: 1 }}>
            <Card accent={C.muted}>
              <div style={T.label(22)}>Rechtfertigung (modern)</div>
              <div style={{ ...T.serif(38), marginTop: 12 }}>gute Gründe für eine Überzeugung</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(4, 0.2)} style={{ flex: 1 }}>
            <Card>
              <div style={T.label(22, C.gold)}>Logos (Platon)</div>
              <div style={{ ...T.serif(38), marginTop: 12 }}>Erklärung und Verständnis – warum etwas so ist</div>
            </Card>
          </Reveal>
        </div>
        <At x={960} y={720} w={1500}>
          <Reveal f={f} at={s(4, 0.6)}>
            <div style={T.greek(50)}>ἕως ἄν τις αὐτὰς δήσῃ αἰτίας λογισμῷ</div>
            <div style={{ ...T.italic(38), marginTop: 10 }}>wahre Meinungen werden festgebunden „durch Begründung der Ursache“</div>
            <div style={{ ...T.label(20), marginTop: 12 }}>Menon 97d–98a · die Statuen des Daidalos</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XXX · Was bleibt ───────────── */

export const Schluss: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const rows = [
    { d: 'Wahrnehmung', why: 'Erkenntnis verlangt Urteilen', at: 0.12 },
    { d: 'wahre Meinung', why: 'man kann zufällig richtig liegen', at: 0.38 },
    { d: '+ Logos', why: 'worin die Erklärung besteht, bleibt offen', at: 0.62 },
  ];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <At x={960} y={150}>
          <Reveal f={f} at={s(0, 0.02)}>
            <div style={T.label(26, C.gold)}>Eine Landkarte statt einer Definition</div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', top: 280, left: 260, right: 260, display: 'flex', flexDirection: 'column', gap: 40 }}>
          {rows.map((r, i) => (
            <Reveal key={r.d} f={f} at={s(0, r.at)}>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 40 }}>
                <div style={{ ...T.display(44, C.gold), width: 60 }}>{i + 1}</div>
                <div style={{ ...T.display(58), width: 520 }}>{r.d}</div>
                <div style={T.italic(42, C.muted)}>{r.why}</div>
              </div>
            </Reveal>
          ))}
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1)), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(1, 0.05)} dur={40}>
          <div style={{ ...T.display(150), textAlign: 'center' }}>Theaitetos</div>
        </Reveal>
        <Reveal f={f} at={s(1, 0.4)}>
          <div style={{ ...T.greek(56), marginTop: 30 }}>οὐκ οἰόμενος εἰδέναι ἃ μὴ οἶσθα</div>
        </Reveal>
        <Reveal f={f} at={s(1, 0.55)}>
          <div style={{ ...T.italic(44, C.muted), marginTop: 16 }}>„nicht glauben zu wissen, was du nicht weißt“ – Tht. 210c</div>
        </Reveal>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
