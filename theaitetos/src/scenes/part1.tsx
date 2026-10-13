import React from 'react';
import { AbsoluteFill, interpolate } from 'remotion';
import { Meander } from '../components/chrome';
import { Figure, Profile, Stoa } from '../components/icons';
import { Arrow, At, Card, Draw, easeInOut, prog, Reveal, Strike, Svg, T, vis } from '../components/kit';
import { C, F } from '../theme';
import { SceneTiming } from '../timeline';
import { useScene } from './util';

type P = { t: SceneTiming };

/* ───────────────────────── Intro ───────────────────────── */

export const Intro: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const zoom = interpolate(f, [0, s(1)], [1.08, 1], { extrapolateRight: 'clamp' });
  const defs = [
    ['Wahrnehmung', '151e'],
    ['wahre Meinung', '187b'],
    ['wahre Meinung mit Logos', '201c–d'],
  ];
  return (
    <AbsoluteFill>
      {/* 1 · Athens, 399 */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 10) }}>
        <At x={960} y={430}>
          <div style={{ ...T.display(420, 'rgba(217,181,107,0.10)'), transform: `scale(${zoom})`, letterSpacing: '0.02em' }}>399</div>
        </At>
        <At x={960} y={300}>
          <Reveal f={f} at={8}>
            <div style={{ ...T.label(30, C.gold), letterSpacing: '0.5em' }}>Athen · 399 v. Chr.</div>
          </Reveal>
        </At>
        <Svg>
          <g style={{ opacity: prog(f, 20, 40) }} transform={`translate(960 640) scale(${1.05 + 0.05 * prog(f, 0, s(1))})`}>
            <Stoa color={C.ink} opacity={0.7} />
          </g>
        </Svg>
        <At x={960} y={860}>
          <Reveal f={f} at={s(0, 0.45)}>
            <div style={T.italic(40, C.muted)}>Anklage des Meletos gegen Sokrates</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 2 · the question */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 8), justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ position: 'absolute', width: 900, height: 900, borderRadius: '50%', background: 'radial-gradient(circle, rgba(217,181,107,0.12), rgba(0,0,0,0) 60%)' }} />
        <Reveal f={f} at={s(1, 0.45)} dur={40}>
          <div style={{ ...T.greek(150, C.gold), textShadow: `0 0 40px rgba(217,181,107,0.45)` }}>τί ἐστιν ἐπιστήμη;</div>
        </Reveal>
        <Reveal f={f} at={s(1, 0.7)} dur={30}>
          <div style={{ ...T.italic(64), marginTop: 30 }}>Was ist Erkenntnis?</div>
        </Reveal>
      </AbsoluteFill>

      {/* 3 · three answers, all refuted */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 8) }}>
        <At x={960} y={210}>
          <Reveal f={f} at={s(2, 0.02)}>
            <div style={{ ...T.display(110), letterSpacing: '0.18em' }}>ΘΕΑΙΤΗΤΟΣ</div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', top: 400, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 50 }}>
          {defs.map(([name, st], i) => (
            <Reveal key={name} f={f} at={s(2, 0.3 + i * 0.08)}>
              <Card style={{ width: 500, height: 220, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                <div style={T.label(22, C.gold)}>Definition {i + 1}</div>
                <div style={{ ...T.italic(30, C.muted), marginTop: 12 }}>Erkenntnis ist</div>
                <div style={{ position: 'relative', marginTop: 4 }}>
                  <div style={{ ...T.serif(42), textAlign: 'center', whiteSpace: 'nowrap' }}>{name}</div>
                  <Strike f={f} at={s(2, 0.6 + i * 0.07)} />
                </div>
                <div style={{ ...T.label(19), marginTop: 14 }}>Tht. {st}</div>
              </Card>
            </Reveal>
          ))}
        </div>
        <At x={960} y={790}>
          <Reveal f={f} at={s(2, 0.86)}>
            <div style={T.greek(76, C.gold)}>ἀπορία</div>
            <div style={{ ...T.label(22), marginTop: 6 }}>Ratlosigkeit · kein Ergebnis</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 4 · title */}
      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 8), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(3, 0.02)} dur={36}>
          <div style={{ ...T.label(28, C.gold), letterSpacing: '0.5em', textAlign: 'center' }}>Platon</div>
          <div style={{ ...T.display(200), marginTop: 10 }}>Theaitetos</div>
        </Reveal>
        <div style={{ marginTop: 20 }}>
          <Meander f={f} at={s(3, 0.1)} width={720} />
        </div>
        <Reveal f={f} at={s(3, 0.2)}>
          <div style={{ ...T.italic(46, C.muted), marginTop: 26 }}>Ein Dialog über das Wissen</div>
        </Reveal>
        <div style={{ display: 'flex', gap: 80, marginTop: 70 }}>
          {['Argumente', 'Bilder', 'Forschung'].map((w, i) => (
            <Reveal key={w} f={f} at={s(3, 0.55 + i * 0.1)}>
              <div style={T.label(26, C.ink)}>{w}</div>
            </Reveal>
          ))}
        </div>
      </AbsoluteFill>

      {/* 5 · how sources are cited */}
      <AbsoluteFill style={{ opacity: vis(f, s(4)) }}>
        <At x={960} y={400}>
          <Reveal f={f} at={s(4, 0.05)}>
            <div style={{ ...T.display(190), letterSpacing: '0.02em' }}>
              <span style={{ color: C.muted }}>Tht.</span> <span>151</span>
              <span style={{ color: C.gold }}>e</span>
            </div>
          </Reveal>
        </At>
        <Svg>
          <Arrow f={f} at={s(4, 0.18)} x1={700} y1={520} x2={560} y2={650} color={C.muted} />
          <Arrow f={f} at={s(4, 0.26)} x1={1000} y1={520} x2={960} y2={650} />
          <Arrow f={f} at={s(4, 0.34)} x1={1205} y1={520} x2={1360} y2={650} />
        </Svg>
        <At x={560} y={720} w={420}>
          <Reveal f={f} at={s(4, 0.2)}>
            <div style={T.serif(34)}>Theaitetos</div>
          </Reveal>
        </At>
        <At x={960} y={735} w={480}>
          <Reveal f={f} at={s(4, 0.28)}>
            <div style={T.serif(34)}>Seite der Ausgabe von Henricus Stephanus, Genf 1578</div>
          </Reveal>
        </At>
        <At x={1360} y={720} w={420}>
          <Reveal f={f} at={s(4, 0.36)}>
            <div style={T.serif(34)}>Abschnitt a–e</div>
          </Reveal>
        </At>
        <At x={960} y={880}>
          <Reveal f={f} at={s(4, 0.62)}>
            <div style={T.italic(34, C.muted)}>Zitate nach der Übersetzung von Friedrich Schleiermacher</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────────────────── I · Rahmen ───────────────────────── */

const Waves: React.FC<{ y: number; f: number; opacity?: number }> = ({ y, f, opacity = 0.5 }) => (
  <g opacity={opacity}>
    {[0, 1, 2].map((r) => {
      let d = '';
      for (let x = 120; x <= 1800; x += 60) {
        const yy = y + r * 26 + Math.sin(x / 70 + f / 25 + r) * 5;
        d += `${x === 120 ? 'M' : 'L'} ${x} ${yy} `;
      }
      return <path key={r} d={d} stroke={C.blue} strokeWidth={2} fill="none" opacity={1 - r * 0.3} />;
    })}
  </g>
);

export const Rahmen: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const cities = [
    { x: 380, name: 'Korinth', sub: 'Heerlager' },
    { x: 960, name: 'Megara', sub: 'Hafen · Eukleides' },
    { x: 1540, name: 'Athen', sub: 'Heimat des Theaitetos' },
  ];
  const travel = prog(f, s(0, 0.3), s(0, 0.95) - s(0, 0.3), easeInOut);
  const dotX = 380 + travel * 1160;
  const lines = [
    ['Sokrates', 'Sag mir, Theaitetos, lernst du bei Theodoros Geometrie?', 'fragte ich'],
    ['Theaitetos', 'Ja, das tue ich.', 'stimmte er zu'],
    ['Sokrates', 'Und Astronomie, Harmonik und Rechenkunst?', 'sagte ich'],
  ];
  const collapse = prog(f, s(2, 0.55), 30, easeInOut);
  const tl = (y: number) => 380 + ((399 - y) / 60) * 1300;
  return (
    <AbsoluteFill>
      {/* route Korinth → Megara → Athen */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 8) }}>
        <Svg>
          <Waves y={720} f={f} opacity={prog(f, 10, 40) * 0.5} />
          <Draw f={f} at={6} dur={40} d="M 380 520 C 600 470 760 560 960 520 C 1160 480 1320 560 1540 520" stroke={C.gold} strokeWidth={3} strokeDasharray="1" />
          {cities.map((c, i) => (
            <g key={c.name} opacity={prog(f, 14 + i * 8, 20)}>
              <circle cx={c.x} cy={520} r={22} fill={C.bg} stroke={C.gold} strokeWidth={3} />
              <circle cx={c.x} cy={520} r={8} fill={C.gold} />
            </g>
          ))}
          <g opacity={prog(f, s(0, 0.3), 10) * (1 - prog(f, s(0, 0.97), 10))}>
            <circle cx={dotX} cy={520 + Math.sin(travel * Math.PI * 2) * 22} r={14} fill={C.red} filter="url(#glow)" />
          </g>
        </Svg>
        {cities.map((c, i) => (
          <At key={c.name} x={c.x} y={420}>
            <Reveal f={f} at={14 + i * 8}>
              <div style={T.display(64)}>{c.name}</div>
              <div style={{ ...T.label(20), marginTop: 6 }}>{c.sub}</div>
            </Reveal>
          </At>
        ))}
        <At x={960} y={830}>
          <Reveal f={f} at={s(0, 0.55)}>
            <div style={T.italic(40, C.muted)}>Theaitetos – verwundet und an der Ruhr erkrankt</div>
          </Reveal>
        </At>
        <At x={960} y={180}>
          <Reveal f={f} at={4}>
            <div style={T.label(24, C.gold)}>Rahmendialog · Eukleides und Terpsion</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* the book: written, checked, corrected, read aloud */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 8) }}>
        <Svg>
          <g transform="translate(960 430)" opacity={prog(f, s(1), 20)}>
            <rect x={-420 * prog(f, s(1), 40, easeInOut)} y={-150} width={840 * prog(f, s(1), 40, easeInOut)} height={300} rx={8} fill="rgba(244,239,228,0.08)" stroke={C.gold} strokeWidth={2} />
            <rect x={-440 * prog(f, s(1), 40, easeInOut) - 18} y={-170} width={36} height={340} rx={18} fill={C.bg} stroke={C.gold} strokeWidth={2.5} />
            <rect x={440 * prog(f, s(1), 40, easeInOut) - 18} y={-170} width={36} height={340} rx={18} fill={C.bg} stroke={C.gold} strokeWidth={2.5} />
            {Array.from({ length: 8 }, (_, i) => (
              <rect key={i} x={-360} y={-118 + i * 32} width={(i % 3 === 2 ? 480 : 700) * prog(f, s(1, 0.1) + i * 4, 20)} height={8} rx={4} fill={C.ink} opacity={0.25} />
            ))}
          </g>
        </Svg>
        <div style={{ position: 'absolute', top: 700, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 40 }}>
          {['aufgeschrieben', 'bei Sokrates nachgefragt', 'verbessert', 'vorgelesen'].map((w, i) => (
            <Reveal key={w} f={f} at={s(1, 0.3 + i * 0.15)}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                <div style={{ ...T.display(44, C.gold) }}>{i + 1}</div>
                <div style={T.serif(36)}>{w}</div>
              </div>
            </Reveal>
          ))}
        </div>
      </AbsoluteFill>

      {/* narrative tags removed */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 8) }}>
        <At x={960} y={200}>
          <Reveal f={f} at={s(2)}>
            <div style={T.label(24, C.gold)}>Erzählung → Drama</div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', top: 330, left: 280, width: 1360 }}>
          {lines.map(([who, said, tag], i) => (
            <Reveal key={i} f={f} at={s(2, 0.05 + i * 0.07)}>
              <div style={{ display: 'flex', alignItems: 'baseline', marginBottom: 34, ...T.serif(42) }}>
                <span style={{ ...T.label(24, C.gold), width: 220, flexShrink: 0 }}>{who}</span>
                <span>{said}</span>
                <span
                  style={{
                    position: 'relative',
                    display: 'inline-block',
                    overflow: 'hidden',
                    whiteSpace: 'nowrap',
                    maxWidth: 360 * (1 - collapse),
                    marginLeft: 18 * (1 - collapse),
                    color: C.red,
                    fontStyle: 'italic',
                    opacity: 1 - collapse,
                  }}
                >
                  ‹{tag}›
                  <Strike f={f} at={s(2, 0.32 + i * 0.05)} />
                </span>
              </div>
            </Reveal>
          ))}
        </div>
        <At x={960} y={800}>
          <Reveal f={f} at={s(2, 0.7)}>
            <div style={T.italic(38, C.muted)}>„… damit die Zwischenreden nicht lästig fallen“</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* timeline */}
      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 8) }}>
        <Svg>
          <Draw f={f} at={s(3)} dur={40} d={`M 200 520 H 1720`} stroke={C.line} strokeWidth={3} />
          {[
            { y: 399, top: 'Gespräch · Prozess des Sokrates', at: 0.05, color: C.gold },
            { y: 369, top: 'Kämpfe bei Korinth · Tod des Theaitetos', at: 0.3, color: C.red },
            { y: 394, top: 'oder 394?', at: 0.42, color: C.muted, below: true },
            { y: 347, top: 'Tod Platons', at: 0.55, color: C.muted },
          ].map((m: { y: number; top: string; at: number; color: string; below?: boolean }) => (
            <g key={m.y} opacity={prog(f, s(3, m.at), 20)}>
              <circle cx={tl(m.y)} cy={520} r={m.below ? 9 : 14} fill={m.below ? 'none' : m.color} stroke={m.color} strokeWidth={3} />
              {!m.below && (
                <text x={tl(m.y)} y={600} textAnchor="middle" fontFamily={F.display} fontSize={54} fill={C.ink}>
                  {m.y}
                </text>
              )}
              <text x={tl(m.y)} y={m.below ? 660 : 460} textAnchor="middle" fontFamily={F.sans} fontSize={22} letterSpacing="2" fill={m.color}>
                {m.top.toUpperCase()}
              </text>
            </g>
          ))}
          <g opacity={prog(f, s(3, 0.62), 24)}>
            <rect x={tl(369) + 20} y={500} width={tl(347) - tl(369) - 40} height={40} rx={20} fill={C.goldSoft} stroke={C.gold} strokeDasharray="6 8" />
            <text x={(tl(369) + tl(347)) / 2} y={527} textAnchor="middle" fontFamily={F.sans} fontSize={20} fill={C.gold}>
              ABFASSUNG
            </text>
          </g>
        </Svg>
        <div style={{ position: 'absolute', top: 730, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 34 }}>
          {['Politeia', 'Theaitetos', 'Sophistes', 'Politikos'].map((w, i) => (
            <Reveal key={w} f={f} at={s(3, 0.72 + i * 0.05)}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 34 }}>
                {i > 0 && <div style={{ ...T.display(44, C.muted) }}>→</div>}
                <div style={{ ...T.serif(44, i === 1 ? C.gold : C.ink) }}>{w}</div>
              </div>
            </Reveal>
          ))}
        </div>
        <At x={960} y={180}>
          <Reveal f={f} at={s(3)}>
            <div style={T.label(24, C.gold)}>Datierung · v. Chr.</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* memorial stele */}
      <AbsoluteFill style={{ opacity: vis(f, s(4)), justifyContent: 'center', alignItems: 'center' }}>
        <Svg>
          <g opacity={prog(f, s(4), 30)}>
            <path d="M 760 280 L 960 200 L 1160 280 Z" fill="rgba(236,230,217,0.05)" stroke={C.ink} strokeWidth={2.5} />
            <rect x={780} y={280} width={360} height={560} fill="rgba(236,230,217,0.05)" stroke={C.ink} strokeWidth={2.5} />
            <rect x={740} y={840} width={440} height={30} fill="rgba(236,230,217,0.05)" stroke={C.ink} strokeWidth={2.5} />
          </g>
        </Svg>
        <At x={960} y={430}>
          <Reveal f={f} at={s(4, 0.1)}>
            <div style={{ ...T.display(50), letterSpacing: '0.2em' }}>ΘΕΑΙΤΗΤΟΣ</div>
          </Reveal>
        </At>
        <At x={960} y={560} w={300}>
          <Reveal f={f} at={s(4, 0.3)}>
            <div style={T.italic(32, C.muted)}>Mathematiker</div>
            <div style={{ ...T.italic(32, C.muted), marginTop: 10 }}>Schüler des Theodoros</div>
            <div style={{ ...T.italic(32, C.muted), marginTop: 10 }}>Gesprächspartner des Sokrates</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────────────────── II · Personen ───────────────────────── */

export const Personen: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const focus = (i: number) => (i === 0 ? vis(f, s(0, 0.05), s(1)) : i === 1 ? vis(f, s(1), s(2)) : 0);
  const people = [
    { x: 400, name: 'Theodoros', from: 'aus Kyrene', beard: true, bald: false, snub: false },
    { x: 960, name: 'Theaitetos', from: 'aus Athen', beard: false, bald: false, snub: true },
    { x: 1520, name: 'Sokrates', from: 'aus Athen', beard: true, bald: true, snub: true },
  ];
  const noses = prog(f, s(1, 0.65), 24) * (1 - prog(f, s(2, 0.92), 12));
  return (
    <AbsoluteFill>
      <Svg>
        {people.map((p, i) => {
          const a = prog(f, 8 + i * 10, 30);
          const hi = focus(i);
          return (
            <g key={p.name} opacity={a}>
              <circle cx={p.x} cy={420} r={190} fill="rgba(207,106,71,0.08)" stroke={hi > 0.1 ? C.gold : C.line} strokeWidth={2 + hi * 2} />
              <circle cx={p.x} cy={420} r={172} fill="none" stroke={C.line} strokeWidth={1} strokeDasharray="3 9" />
              <Profile
                x={p.x}
                y={430}
                s={1.05}
                beard={p.beard}
                bald={p.bald}
                snub={p.snub}
                eyeBulge={p.snub && noses > 0.2}
                noseColor={p.snub && noses > 0.05 ? C.gold : undefined}
                color={C.ink}
              />
              {p.snub && noses > 0 && <circle cx={p.x + 72} cy={441} r={24} fill="none" stroke={C.gold} strokeWidth={3} opacity={noses} filter="url(#glow)" />}
            </g>
          );
        })}
      </Svg>
      {people.map((p, i) => (
        <At key={p.name} x={p.x} y={680}>
          <Reveal f={f} at={14 + i * 10}>
            <div style={T.display(58)}>{p.name}</div>
            <div style={{ ...T.label(20), marginTop: 8 }}>{p.from}</div>
          </Reveal>
        </At>
      ))}
      <At x={400} y={820} w={520}>
        <Reveal f={f} at={s(0, 0.3)} out={s(1)}>
          <div style={T.italic(34, C.muted)}>berühmter Mathematiker,</div>
          <div style={T.italic(34, C.muted)}>Freund des Protagoras</div>
        </Reveal>
      </At>
      <At x={960} y={820} w={620}>
        <Reveal f={f} at={s(1, 0.15)} out={s(2)}>
          <div style={T.italic(34, C.muted)}>lernt schnell · sanft · tapfer</div>
          <div style={{ ...T.italic(34, C.gold), marginTop: 6, opacity: prog(f, s(1, 0.6), 20) }}>stumpfe Nase, hervortretende Augen</div>
        </Reveal>
      </At>
      <At x={960} y={860} w={1200}>
        <Reveal f={f} at={s(2, 0.2)}>
          <div style={T.serif(40)}>
            Am Ende entscheidet eine stumpfe Nase über eine Definition – <span style={{ color: C.gold }}>Tht. 209b–c</span>
          </div>
        </Reveal>
      </At>
    </AbsoluteFill>
  );
};

/* ───────────────────────── III · Die Frage ───────────────────────── */

export const Frage: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const examples = ['Geometrie', 'Astronomie', 'Harmonik', 'Rechenkunst', 'Schusterei', 'Zimmermannskunst'];
  const gather = prog(f, s(1, 0.62), 30, easeInOut);
  return (
    <AbsoluteFill>
      {/* episteme */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(0, 0.2)} dur={30}>
          <div style={{ ...T.greek(170, C.gold), textShadow: '0 0 40px rgba(217,181,107,0.35)' }}>ἐπιστήμη</div>
        </Reveal>
        <Reveal f={f} at={s(0, 0.55)}>
          <div style={{ ...T.label(28), marginTop: 20 }}>Epistéme · Erkenntnis · Wissen</div>
        </Reveal>
      </AbsoluteFill>

      {/* examples */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        {examples.map((w, i) => {
          const a = (i / examples.length) * Math.PI * 2 - Math.PI / 2;
          const r = 330 * (1 - gather);
          return (
            <At key={w} x={960 + Math.cos(a) * r * 1.35} y={500 + Math.sin(a) * r}>
              <div style={{ opacity: prog(f, s(1, 0.08 + i * 0.06), 18) * (1 - gather * 0.85), transform: `scale(${1 - gather * 0.6})` }}>
                <Card style={{ padding: '18px 30px' }} accent={i < 4 ? C.gold : C.terracotta}>
                  <div style={T.serif(40)}>{w}</div>
                </Card>
              </div>
            </At>
          );
        })}
        <At x={960} y={500}>
          <div style={{ opacity: gather, transform: `scale(${0.6 + gather * 0.4})` }}>
            <div style={T.display(120, C.gold)}>?</div>
          </div>
        </At>
        <At x={960} y={880} w={1400}>
          <Reveal f={f} at={s(1, 0.7)}>
            <div style={T.serif(42)}>
              Nicht: <i>wovon</i> es Erkenntnis gibt – sondern: <span style={{ color: C.gold }}>was Erkenntnis selbst ist</span>
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* clay */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <At x={960} y={200}>
          <Reveal f={f} at={s(2)}>
            <div style={T.display(76)}>Was ist Lehm?</div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', top: 340, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 60 }}>
          {['Töpfer', 'Ofen', 'Ziegel'].map((w, i) => (
            <Reveal key={w} f={f} at={s(2, 0.12 + i * 0.07)}>
              <div style={{ ...T.serif(56), position: 'relative' }}>
                {w}
                <span style={{ color: C.red, textShadow: `0 0 ${prog(f, s(2, 0.4), 20) * 20}px ${C.red}` }}>lehm</span>
              </div>
            </Reveal>
          ))}
        </div>
        <At x={960} y={480}>
          <Reveal f={f} at={s(2, 0.4)}>
            <div style={T.italic(36, C.red)}>setzt voraus, was erklärt werden soll</div>
          </Reveal>
        </At>
        <At x={960} y={680}>
          <Reveal f={f} at={s(2, 0.68)}>
            <div style={T.display(80)}>
              Lehm = <span style={{ color: C.gold }}>Erde + Flüssigkeit</span>
            </div>
            <div style={{ ...T.greek(44), marginTop: 16 }}>γῆ ὑγρῷ φυραθεῖσα πηλὸς ἂν εἴη</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* Geach */}
      <AbsoluteFill style={{ opacity: vis(f, s(3)) }}>
        <At x={960} y={190}>
          <Reveal f={f} at={s(3)}>
            <div style={T.label(26, C.gold)}>Der „sokratische Fehlschluss“ · Peter Geach 1966</div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', top: 290, left: 260, right: 260, display: 'flex', flexDirection: 'column', gap: 28 }}>
          <Reveal f={f} at={s(3, 0.12)}>
            <Card>
              <div style={T.serif(40)}>
                <b style={{ color: C.gold }}>A</b> &nbsp;Wer weiß, dass er einen Begriff richtig anwendet, muss ein allgemeines Kriterium angeben können.
              </div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(3, 0.3)}>
            <Card>
              <div style={T.serif(40)}>
                <b style={{ color: C.gold }}>B</b> &nbsp;Beispiele helfen nicht, dieses Kriterium zu finden.
              </div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(3, 0.68)}>
            <Card accent={C.red}>
              <div style={T.serif(40)}>
                <b style={{ color: C.red }}>Einwand</b> &nbsp;Wir erkennen vieles zuverlässig, ohne es definieren zu können.
              </div>
            </Card>
          </Reveal>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export { Figure };
