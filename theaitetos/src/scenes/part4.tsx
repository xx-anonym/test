import React from 'react';
import { AbsoluteFill, interpolate } from 'remotion';
import { Cup, Eye, Figure, Hand, Profile, Stoa } from '../components/icons';
import { Arrow, At, Card, easeInOut, Gr, prog, Reveal, Strike, Svg, T, vis } from '../components/kit';
import { C } from '../theme';
import { SceneTiming } from '../timeline';
import { useScene } from './util';

type P = { t: SceneTiming };

const Pig: React.FC<{ x: number; y: number; s?: number; color?: string }> = ({ x, y, s = 1, color = C.ink }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} fill="rgba(236,230,217,0.05)" stroke={color} strokeWidth={3} strokeLinejoin="round">
    <path d="M -58 -40 L -40 -78 L -22 -50 M 58 -40 L 40 -78 L 22 -50" />
    <ellipse cx={0} cy={0} rx={70} ry={60} />
    <ellipse cx={0} cy={22} rx={30} ry={20} />
    <circle cx={-10} cy={22} r={5} fill={color} />
    <circle cx={10} cy={22} r={5} fill={color} />
    <circle cx={-28} cy={-14} r={5} fill={color} />
    <circle cx={28} cy={-14} r={5} fill={color} />
  </g>
);

const Baboon: React.FC<{ x: number; y: number; s?: number; color?: string }> = ({ x, y, s = 1, color = C.ink }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} fill="rgba(236,230,217,0.05)" stroke={color} strokeWidth={3} strokeLinejoin="round">
    <path d="M -60 -10 C -70 -60 -30 -80 0 -80 C 30 -80 70 -60 60 -10 C 56 20 30 30 0 30 C -30 30 -56 20 -60 -10 Z" />
    <path d="M -26 0 C -30 50 -14 80 0 80 C 14 80 30 50 26 0" />
    <circle cx={-22} cy={-30} r={6} fill={color} />
    <circle cx={22} cy={-30} r={6} fill={color} />
    <path d="M -8 66 L -4 72 M 8 66 L 4 72" />
  </g>
);

/* ───────────── X · Erste Prüfungen ───────────── */

export const Kritik1: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const glyphs = ['M 0 0 L 20 -30 L 40 0 M 8 -12 H 32', 'M 0 -30 V 0 H 30 M 0 -15 H 22', 'M 0 0 C 0 -40 40 -40 40 -10 C 40 10 10 10 10 -10', 'M 0 -30 L 30 0 M 30 -30 L 0 0', 'M 15 -30 V 0 M 0 -20 H 30 M 0 -8 H 30', 'M 0 0 Q 20 -50 40 0 Q 20 -20 0 0'];
  const closeLid = prog(f, s(1, 0.55), 20);
  return (
    <AbsoluteFill>
      {/* 0 · pig and baboon */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(0, 0.25), 20)}>
            <circle cx={620} cy={470} r={170} fill="rgba(207,106,71,0.07)" stroke={C.line} />
            <Pig x={620} y={480} s={1.5} />
          </g>
          <g opacity={prog(f, s(0, 0.35), 20)}>
            <circle cx={1300} cy={470} r={170} fill="rgba(207,106,71,0.07)" stroke={C.line} />
            <Baboon x={1300} y={470} s={1.4} />
          </g>
        </Svg>
        <At x={960} y={190} w={1500}>
          <Reveal f={f} at={s(0, 0.1)}>
            <div style={T.display(64)}>Das Maß aller Dinge ist …</div>
          </Reveal>
        </At>
        <At x={620} y={720}>
          <Reveal f={f} at={s(0, 0.25)}>
            <div style={T.display(52)}>das Schwein?</div>
          </Reveal>
        </At>
        <At x={1300} y={720}>
          <Reveal f={f} at={s(0, 0.35)}>
            <div style={T.display(52)}>der Pavian?</div>
          </Reveal>
        </At>
        <At x={960} y={860} w={1500}>
          <Reveal f={f} at={s(0, 0.65)}>
            <div style={T.italic(40, C.muted)}>Und wozu dann Lehrgeld für Protagoras?</div>
            <div style={{ ...T.greek(34, C.faint), marginTop: 8 }}>ὗς ἢ κυνοκέφαλος · Tht. 161c</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 1 · foreign letters, memory */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <g transform="translate(330 420)" opacity={prog(f, s(1, 0.05), 20)}>
            {glyphs.map((d, i) => (
              <path key={i} d={d} transform={`translate(${i * 70} 0) scale(1.4)`} stroke={C.ink} strokeWidth={2.4} fill="none" strokeLinecap="round" />
            ))}
          </g>
          <g opacity={prog(f, s(1, 0.5), 20)}>
            <Eye x={1340} y={420} s={1.7} open={1 - closeLid * 0.95} />
            <circle cx={1500} cy={300} r={16} fill="none" stroke={C.gold} strokeWidth={2} opacity={prog(f, s(1, 0.65), 12)} />
            <circle cx={1540} cy={250} r={24} fill="none" stroke={C.gold} strokeWidth={2} opacity={prog(f, s(1, 0.68), 12)} />
            <g opacity={prog(f, s(1, 0.72), 16)}>
              <ellipse cx={1640} cy={170} rx={120} ry={70} fill="rgba(217,181,107,0.1)" stroke={C.gold} strokeWidth={2} />
              <circle cx={1640} cy={170} r={30} fill={C.gold} opacity={0.7} />
            </g>
          </g>
        </Svg>
        <At x={530} y={600}>
          <Reveal f={f} at={s(1, 0.2)}>
            <div style={T.display(52)}>wahrgenommen</div>
            <div style={{ ...T.display(52, C.red), marginTop: 4 }}>≠ verstanden</div>
          </Reveal>
        </At>
        <At x={1400} y={620}>
          <Reveal f={f} at={s(1, 0.7)}>
            <div style={T.display(52, C.gold)}>erinnert</div>
            <div style={{ ...T.display(52), marginTop: 4 }}>ohne Wahrnehmung</div>
          </Reveal>
        </At>
        <At x={960} y={860}>
          <Reveal f={f} at={s(1, 0.85)}>
            <div style={T.italic(40)}>Erinnerung: Wissen ohne Wahrnehmen · Tht. 163d–164b</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 2 · one eye covered */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(2, 0.05), 20)}>
            <Eye x={780} y={470} s={1.8} />
            <Eye x={1140} y={470} s={1.8} />
          </g>
          <g transform={`translate(0 ${(1 - prog(f, s(2, 0.3), 24)) * 300})`} opacity={prog(f, s(2, 0.3), 20)}>
            <Hand x={780} y={490} s={2.1} color={C.terracotta} fill={C.bg2} />
          </g>
        </Svg>
        <At x={780} y={720}>
          <Reveal f={f} at={s(2, 0.55)}>
            <div style={T.display(52, C.red)}>sieht nicht</div>
          </Reveal>
        </At>
        <At x={1140} y={720}>
          <Reveal f={f} at={s(2, 0.6)}>
            <div style={T.display(52, C.gold)}>sieht</div>
          </Reveal>
        </At>
        <At x={960} y={860}>
          <Reveal f={f} at={s(2, 0.78)}>
            <div style={T.italic(42)}>Also: weiß und weiß zugleich nicht?</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 3 · let Protagoras speak */}
      <AbsoluteFill style={{ opacity: vis(f, s(3)) }}>
        <Svg>
          <g opacity={prog(f, s(3, 0.4), 30)}>
            <circle cx={960} cy={430} r={190} fill="rgba(207,106,71,0.08)" stroke={C.gold} strokeWidth={2} />
            <Profile x={960} y={440} s={1.15} beard snub={false} />
          </g>
        </Svg>
        <At x={960} y={200}>
          <Reveal f={f} at={s(3, 0.1)}>
            <div style={{ position: 'relative', display: 'inline-block' }}>
              <div style={T.italic(46, C.muted)}>Argumente wie ein Wortverdreher</div>
              <Strike f={f} at={s(3, 0.35)} color={C.muted} width={3} />
            </div>
          </Reveal>
        </At>
        <At x={960} y={720}>
          <Reveal f={f} at={s(3, 0.55)}>
            <div style={T.display(66)}>Protagoras</div>
            <div style={{ ...T.label(22, C.gold), marginTop: 8 }}>darf sich verteidigen · Tht. 166a</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XI · Apologie des Protagoras ───────────── */

export const Apologie: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const cure = prog(f, s(1, 0.3), 30, easeInOut);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: 120, alignItems: 'center' }}>
          <Reveal f={f} at={s(0, 0.25)}>
            <div style={{ position: 'relative', textAlign: 'center' }}>
              <div style={T.display(80, C.muted)}>wahr · falsch</div>
              <Strike f={f} at={s(0, 0.45)} />
            </div>
          </Reveal>
          <Reveal f={f} at={s(0, 0.6)}>
            <div style={T.display(80, C.gold)}>besser · schlechter</div>
          </Reveal>
        </div>
        <Reveal f={f} at={s(0, 0.1)}>
          <div style={{ ...T.italic(42), marginTop: 70 }}>„Niemand hat je falsch geurteilt.“</div>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(1, 0.02), 20)}>
            <Figure x={380} y={470} s={1.5} color={cure > 0.5 ? C.gold : C.blue} fill="rgba(127,163,201,0.1)" />
            <Figure x={720} y={470} s={1.5} color={C.ink} />
            <Cup x={550} y={420} s={0.8} />
          </g>
          <g opacity={prog(f, s(1, 0.55), 30)}>
            <Stoa x={1430} y={470} s={0.95} />
          </g>
          <Arrow f={f} at={s(1, 0.65)} x1={1180} y1={760} x2={1680} y2={760} color={C.gold} />
        </Svg>
        <At x={380} y={680}>
          <Reveal f={f} at={s(1, 0.05)}>
            <div style={T.display(46)}>Kranker</div>
            <div style={T.display(50, cure > 0.5 ? C.gold : C.blue)}>{cure > 0.5 ? 'süß' : 'bitter'}</div>
          </Reveal>
        </At>
        <At x={720} y={680}>
          <Reveal f={f} at={s(1, 0.15)}>
            <div style={T.display(46)}>Arzt</div>
            <div style={T.label(20)}>verändert den Zustand</div>
          </Reveal>
        </At>
        <At x={1430} y={240} w={600}>
          <Reveal f={f} at={s(1, 0.55)}>
            <div style={T.display(46)}>Die Stadt</div>
            <div style={T.italic(32, C.muted)}>gerecht ist, was ihr gerecht erscheint</div>
          </Reveal>
        </At>
        <At x={1430} y={830} w={700}>
          <Reveal f={f} at={s(1, 0.7)}>
            <div style={T.serif(36)}>
              der Weise: <span style={{ color: C.red }}>schädlich</span> → <span style={{ color: C.gold }}>nützlich</span>
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2)) }}>
        <Svg>
          <Arrow f={f} at={s(2, 0.05)} x1={960} y1={250} x2={960} y2={830} color={C.line} width={2} dur={20} />
        </Svg>
        <At x={560} y={480} w={700}>
          <Reveal f={f} at={s(2, 0.15)}>
            <div style={T.label(26, C.muted)}>Wahrheit</div>
            <div style={{ ...T.display(84), marginTop: 12 }}>relativ</div>
          </Reveal>
        </At>
        <At x={1360} y={480} w={700}>
          <Reveal f={f} at={s(2, 0.3)}>
            <div style={T.label(26, C.gold)}>Nutzen</div>
            <div style={{ ...T.display(84, C.gold), marginTop: 12 }}>Expertise</div>
          </Reveal>
        </At>
        <At x={1360} y={700}>
          <Reveal f={f} at={s(2, 0.7)}>
            <div style={T.italic(38)}>↑ hier setzt Sokrates an</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XII · Peritrope ───────────── */

export const Peritrope: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const nodes = [
    { a: -90, text: 'Jede Meinung ist wahr – für den, der sie hat.' },
    { a: 30, text: 'Die meisten meinen: Protagoras irrt.' },
    { a: 150, text: 'Also ist wahr: Protagoras irrt.' },
  ];
  const spin = interpolate(f, [s(1, 0.75), s(2)], [0, 360], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: easeInOut });
  const rise = prog(f, s(2, 0.15), 30) * (1 - prog(f, s(2, 0.8), 24, easeInOut));
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <At x={960} y={260} w={1300}>
          <Reveal f={f} at={s(0, 0.1)}>
            <Card>
              <div style={T.serif(46)}>„Was jemandem wahr erscheint, ist für ihn wahr.“</div>
            </Card>
          </Reveal>
        </At>
        <Svg>
          {Array.from({ length: 15 }, (_, i) => (
            <Figure key={i} x={360 + i * 86} y={700 + (i % 2) * 30} s={0.75} color={C.muted} opacity={prog(f, s(0, 0.6) + i * 2, 12)} />
          ))}
        </Svg>
        <At x={960} y={890}>
          <Reveal f={f} at={s(0, 0.75)}>
            <div style={T.display(56, C.red)}>„Protagoras irrt.“</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <g transform={`rotate(${spin} 960 540)`}>
            {nodes.map((n, i) => {
              const a1 = ((n.a + 25) * Math.PI) / 180;
              const a2 = ((nodes[(i + 1) % 3].a - 25) * Math.PI) / 180;
              const R = 300;
              return (
                <path
                  key={i}
                  d={`M ${960 + Math.cos(a1) * R} ${540 + Math.sin(a1) * R} A ${R} ${R} 0 0 1 ${960 + Math.cos(a2) * R} ${540 + Math.sin(a2) * R}`}
                  stroke={C.gold}
                  strokeWidth={4}
                  fill="none"
                  pathLength={1}
                  strokeDasharray={1}
                  strokeDashoffset={1 - prog(f, s(1, 0.15 + i * 0.18), 20)}
                />
              );
            })}
          </g>
        </Svg>
        {nodes.map((n, i) => {
          const a = ((n.a + spin) * Math.PI) / 180;
          return (
            <At key={i} x={960 + Math.cos(a) * 300} y={540 + Math.sin(a) * 300} w={420}>
              <Reveal f={f} at={s(1, 0.05 + i * 0.18)}>
                <Card style={{ padding: '18px 22px' }} accent={i === 2 ? C.red : C.gold}>
                  <div style={T.serif(32, i === 2 ? C.red : C.ink)}>{n.text}</div>
                </Card>
              </Reveal>
            </At>
          );
        })}
        <At x={960} y={540}>
          <Reveal f={f} at={s(1, 0.65)}>
            <div style={T.greek(64)}>περιτροπή</div>
            <div style={T.label(22)}>Umwendung</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <Svg>
          <defs>
            <clipPath id="ground">
              <rect x={0} y={0} width={1920} height={760} />
            </clipPath>
          </defs>
          <g clipPath="url(#ground)">
            <g transform={`translate(0 ${(1 - rise) * 420})`}>
              <Profile x={960} y={620} s={1.2} beard snub={false} />
            </g>
          </g>
          <path d="M 200 760 H 1720" stroke={C.terracotta} strokeWidth={4} />
          {Array.from({ length: 30 }, (_, i) => (
            <line key={i} x1={220 + i * 52} y1={772} x2={200 + i * 52} y2={800} stroke={C.terracotta} strokeWidth={2} opacity={0.5} />
          ))}
        </Svg>
        <At x={1340} y={420} w={520}>
          <div style={{ opacity: prog(f, s(2, 0.4), 12) * (1 - prog(f, s(2, 0.75), 12)) }}>
            <Card accent={C.red}>
              <div style={T.serif(38)}>„Unsinn, ihr beiden!“</div>
            </Card>
          </div>
        </At>
        <At x={960} y={900}>
          <Reveal f={f} at={s(2, 0.05)}>
            <div style={T.italic(38, C.muted)}>„… bis an den Hals …“ – Tht. 171d</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(3)) }}>
        <div style={{ position: 'absolute', top: 280, left: 220, right: 220, display: 'flex', gap: 50 }}>
          <Reveal f={f} at={s(3, 0.1)} style={{ flex: 1 }}>
            <Card accent={C.muted}>
              <div style={T.label(22)}>Ausweg?</div>
              <div style={{ ...T.serif(40), marginTop: 12 }}>„Meine Lehre ist nur für mich wahr.“</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(3, 0.45)} style={{ flex: 1 }}>
            <Card>
              <div style={T.label(22, C.gold)}>Burnyeat 1976</div>
              <div style={{ ...T.serif(40), marginTop: 12 }}>Wer lehrt und ein Buch namens „Wahrheit“ schreibt, beansprucht Wahrheit für andere.</div>
            </Card>
          </Reveal>
        </div>
        <At x={960} y={760}>
          <Reveal f={f} at={s(3, 0.7)}>
            <div style={T.greek(56)}>Ἀλήθεια</div>
            <div style={T.label(20)}>Titel der Schrift des Protagoras · Tht. 161c</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XIII · Exkurs ───────────── */

export const Exkurs: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const drain = prog(f, s(0, 0.1), s(1) - s(0, 0.1), (x) => x);
  const fall = prog(f, s(1, 0.35), 24, easeInOut);
  const stars = Array.from({ length: 70 }, (_, i) => {
    const r = ((i * 7919) % 1000) / 1000;
    const q = ((i * 104729) % 1000) / 1000;
    return { x: 120 + r * 1680, y: 90 + q * 380, z: 1 + ((i * 31) % 3) };
  });
  return (
    <AbsoluteFill>
      {/* 0 · clepsydra */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g transform="translate(560 220)" opacity={prog(f, s(0, 0.05), 20)}>
            <path d="M -110 0 H 110 L 80 220 H -80 Z" fill="none" stroke={C.ink} strokeWidth={3} />
            <clipPath id="upper">
              <path d="M -110 0 H 110 L 80 220 H -80 Z" />
            </clipPath>
            <rect x={-120} y={20 + drain * 200} width={240} height={220} fill={C.blue} opacity={0.5} clipPath="url(#upper)" />
            <line x1={0} y1={220} x2={0} y2={400} stroke={C.blue} strokeWidth={4} strokeDasharray="10 8" strokeDashoffset={-f * 2} opacity={1 - drain} />
            <path d="M -120 380 H 120 L 100 560 H -100 Z" fill="none" stroke={C.ink} strokeWidth={3} />
            <clipPath id="lower">
              <path d="M -120 380 H 120 L 100 560 H -100 Z" />
            </clipPath>
            <rect x={-130} y={560 - drain * 170} width={260} height={200} fill={C.blue} opacity={0.5} clipPath="url(#lower)" />
          </g>
        </Svg>
        <At x={560} y={900}>
          <Reveal f={f} at={s(0, 0.2)}>
            <div style={T.greek(38)}>κατεπείγει γὰρ ὕδωρ ῥέον</div>
            <div style={T.label(20)}>„denn das fließende Wasser drängt“ · Tht. 172e</div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', left: 1000, top: 300, width: 760, display: 'flex', flexDirection: 'column', gap: 34 }}>
          <Reveal f={f} at={s(0, 0.2)}>
            <Card accent={C.red}>
              <div style={T.label(22, C.red)}>Redner vor Gericht</div>
              <div style={{ ...T.serif(36), marginTop: 8 }}>Zeitdruck · Gegner · Herr auf dem Richterstuhl</div>
              <div style={{ ...T.italic(34, C.muted), marginTop: 6 }}>scharfsinnig, aber klein und krumm</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(0, 0.75)}>
            <Card>
              <div style={T.label(22, C.gold)}>Philosoph</div>
              <div style={{ ...T.serif(36), marginTop: 8 }}>
                Muße · <Gr>σχολή</Gr>
              </div>
            </Card>
          </Reveal>
        </div>
      </AbsoluteFill>

      {/* 1 · Thales and the Thracian maid */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          {stars.map((st, i) => (
            <circle key={i} cx={st.x} cy={st.y} r={st.z} fill={C.marble} opacity={(0.3 + 0.5 * Math.abs(Math.sin(f / 20 + i))) * prog(f, s(1), 30)} />
          ))}
          <g opacity={prog(f, s(1, 0.05), 20)}>
            <ellipse cx={760} cy={830} rx={120} ry={34} fill="#05060a" stroke={C.ink} strokeWidth={3} />
            <path d="M 640 830 V 880 M 880 830 V 880" stroke={C.ink} strokeWidth={3} />
          </g>
          <defs>
            <clipPath id="wellclip">
              <rect x={0} y={0} width={1920} height={832} />
            </clipPath>
          </defs>
          <g clipPath="url(#wellclip)">
            <g transform={`translate(${interpolate(f, [s(1, 0.05), s(1, 0.35)], [-200, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })} ${fall * 260})`}>
              <Figure x={760} y={720} s={1.3} color={C.ink} rot={-8 + fall * 30} opacity={prog(f, s(1, 0.05), 20)} />
            </g>
          </g>
          <g opacity={prog(f, s(1, 0.5), 20)}>
            <Figure x={1300} y={740} s={1.2} color={C.terracotta} fill="rgba(207,106,71,0.15)" />
          </g>
        </Svg>
        <At x={1300} y={560}>
          <Reveal f={f} at={s(1, 0.55)}>
            <div style={T.display(60, C.terracotta)}>ha!</div>
          </Reveal>
        </At>
        <At x={1300} y={900} w={600}>
          <Reveal f={f} at={s(1, 0.6)}>
            <div style={T.label(22, C.terracotta)}>die thrakische Magd</div>
          </Reveal>
        </At>
        <At x={760} y={600}>
          <Reveal f={f} at={s(1, 0.08)} out={s(1, 0.4)}>
            <div style={T.label(22)}>Thales</div>
          </Reveal>
        </At>
        <At x={960} y={180} w={1500}>
          <Reveal f={f} at={s(1, 0.7)}>
            <div style={T.italic(42)}>will wissen, was am Himmel ist – und übersieht, was vor seinen Füßen liegt</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 2 · homoiosis theoi */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <div
          style={{
            position: 'absolute',
            left: 860,
            top: 0,
            width: 200,
            height: 1080,
            background: 'linear-gradient(180deg, rgba(217,181,107,0.35), rgba(217,181,107,0))',
            filter: 'blur(30px)',
            opacity: prog(f, s(2, 0.3), 60),
          }}
        />
        <Reveal f={f} at={s(2, 0.45)} dur={40}>
          <div style={{ ...T.greek(76), textShadow: '0 0 30px rgba(217,181,107,0.4)' }}>ὁμοίωσις θεῷ κατὰ τὸ δυνατόν</div>
        </Reveal>
        <Reveal f={f} at={s(2, 0.6)}>
          <div style={{ ...T.italic(46), marginTop: 30 }}>„Verähnlichung mit Gott soweit als möglich“</div>
        </Reveal>
        <Reveal f={f} at={s(2, 0.8)}>
          <div style={{ ...T.serif(38, C.muted), marginTop: 20 }}>gerecht und fromm sein – mit Einsicht</div>
          <div style={{ ...T.label(20), marginTop: 18, textAlign: 'center' }}>Tht. 176b · Übers. Schleiermacher</div>
        </Reveal>
      </AbsoluteFill>

      {/* 3 · reception */}
      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 6) }}>
        <div style={{ position: 'absolute', top: 300, left: 220, right: 220, display: 'flex', gap: 50 }}>
          <Reveal f={f} at={s(3, 0.05)} style={{ flex: 1 }}>
            <Card>
              <div style={T.label(22, C.gold)}>Mittelplatonismus · Alkinoos, Didaskalikos 28</div>
              <div style={{ ...T.serif(40), marginTop: 12 }}>Angleichung an Gott als Ziel des menschlichen Lebens</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(3, 0.45)} style={{ flex: 1 }}>
            <Card accent={C.terracotta}>
              <div style={T.label(22, C.terracotta)}>Hans Blumenberg 1987</div>
              <div style={{ ...T.serif(40), marginTop: 12 }}>
                <i>Das Lachen der Thrakerin.</i> Eine Urgeschichte der Theorie
              </div>
            </Card>
          </Reveal>
        </div>
      </AbsoluteFill>

      {/* 4 · whose measure? */}
      <AbsoluteFill style={{ opacity: vis(f, s(4)) }}>
        <Svg>
          <g opacity={prog(f, s(4, 0.3), 20)}>
            <Figure x={560} y={560} s={1.6} />
            <line x1={420} y1={680} x2={700} y2={680} stroke={C.muted} strokeWidth={3} />
          </g>
          <g opacity={prog(f, s(4, 0.55), 30)}>
            <rect x={1300} y={160} width={120} height={600} fill="url(#goldGlow)" />
            <line x1={1360} y1={160} x2={1360} y2={760} stroke={C.gold} strokeWidth={3} />
          </g>
        </Svg>
        <At x={560} y={790}>
          <Reveal f={f} at={s(4, 0.3)}>
            <div style={T.display(48)}>Der Mensch als Maß</div>
            <div style={T.label(20)}>Protagoras</div>
          </Reveal>
        </At>
        <At x={1360} y={820} w={700}>
          <Reveal f={f} at={s(4, 0.55)}>
            <div style={T.display(48, C.gold)}>ein Maß jenseits des Menschen</div>
            <div style={{ ...T.italic(30, C.muted), marginTop: 8 }}>vgl. Nomoi IV 716c: „Gott wäre für uns das Maß aller Dinge“</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XIV · Zukunft ───────────── */

export const Zukunft: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const rows = [
    { q: 'Wird er Fieber bekommen?', lay: 'Laie: ja', exp: 'Arzt: nein', at: 0.1 },
    { q: 'Wird der Wein süß?', lay: 'Kitharaspieler', exp: 'Winzer', at: 0.55 },
  ];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <Arrow f={f} at={s(0, 0.2)} x1={300} y1={540} x2={1620} y2={540} color={C.gold} width={4} dur={40} />
        </Svg>
        <At x={360} y={470}>
          <Reveal f={f} at={s(0, 0.2)}>
            <div style={T.label(26, C.muted)}>jetzt</div>
          </Reveal>
        </At>
        <At x={1560} y={470}>
          <Reveal f={f} at={s(0, 0.45)}>
            <div style={T.label(26, C.gold)}>Zukunft</div>
          </Reveal>
        </At>
        <At x={960} y={680} w={1400}>
          <Reveal f={f} at={s(0, 0.6)}>
            <div style={T.serif(44)}>
              nützlich = was sich <span style={{ color: C.gold }}>künftig</span> als gut erweisen wird
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        {rows.map((r, i) => (
          <div key={r.q} style={{ position: 'absolute', top: 230 + i * 300, left: 220, right: 220 }}>
            <Reveal f={f} at={s(1, r.at)}>
              <div style={T.display(56)}>{r.q}</div>
              <div style={{ display: 'flex', gap: 60, marginTop: 24 }}>
                <div style={{ position: 'relative' }}>
                  <div style={T.serif(40, C.muted)}>{r.lay}</div>
                  <Strike f={f} at={s(1, r.at + 0.25)} color={C.red} width={3} />
                </div>
                <div style={{ ...T.serif(40, C.gold), opacity: prog(f, s(1, r.at + 0.2), 16) }}>{r.exp} ✓</div>
              </div>
            </Reveal>
          </div>
        ))}
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2)), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(2, 0.05)}>
          <div style={T.serif(44, C.muted)}>Protagoras sagt besser voraus, welche Rede überzeugt</div>
        </Reveal>
        <Reveal f={f} at={s(2, 0.4)}>
          <Card style={{ marginTop: 50 }}>
            <div style={T.display(64)}>Für die Zukunft ist nicht jeder das Maß.</div>
          </Card>
        </Reveal>
        <Reveal f={f} at={s(2, 0.8)}>
          <div style={{ ...T.italic(44, C.gold), marginTop: 50 }}>Übrig: die gegenwärtige Wahrnehmung</div>
        </Reveal>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XV · Radikaler Fluss ───────────── */

export const Fluss2: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const move = (f - s(0, 0.2)) / 40;
  const tone = Math.round(interpolate(Math.sin((f - s(0, 0.55)) / 18), [-1, 1], [30, 240]));
  const word = 'WEISS';
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(0, 0.2), 20)}>
            <circle cx={560 + Math.sin(move) * 160} cy={480} r={60} fill="rgba(217,181,107,0.2)" stroke={C.gold} strokeWidth={3} />
            <line x1={560 + Math.sin(move) * 160} y1={480} x2={560 + Math.sin(move) * 160 + Math.cos(move * 3) * 60} y2={480 + Math.sin(move * 3) * 60} stroke={C.gold} strokeWidth={3} />
          </g>
          <g opacity={prog(f, s(0, 0.55), 20)}>
            <rect x={1300} y={420} width={120} height={120} rx={12} fill={f > s(0, 0.55) ? `rgb(${tone},${tone},${tone})` : '#222'} stroke={C.ink} strokeWidth={3} />
          </g>
        </Svg>
        <At x={560} y={680}>
          <Reveal f={f} at={s(0, 0.2)}>
            <div style={T.display(54)}>Ortsbewegung</div>
            <div style={T.greek(38, C.muted)}>φορά</div>
          </Reveal>
        </At>
        <At x={1360} y={680}>
          <Reveal f={f} at={s(0, 0.55)}>
            <div style={T.display(54)}>Veränderung</div>
            <div style={T.greek(38, C.muted)}>ἀλλοίωσις</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: 10 }}>
          {word.split('').map((ch, i) => {
            const p = prog(f, s(1, 0.15) + i * 4, 14);
            const melt = prog(f, s(1, 0.45) + i * 5, 40);
            return (
              <div
                key={i}
                style={{
                  ...T.display(220, `rgb(${236 - melt * 120},${230 - melt * 100},${217 - melt * 60})`),
                  opacity: p * (1 - melt * 0.85),
                  transform: `translate(${melt * (i - 2) * 30}px, ${melt * (40 + i * 18)}px) rotate(${melt * (i - 2) * 9}deg)`,
                  filter: `blur(${melt * 10}px)`,
                }}
              >
                {ch}
              </div>
            );
          })}
        </div>
        <Reveal f={f} at={s(1, 0.65)}>
          <div style={{ ...T.italic(44), marginTop: 150 }}>Noch während man spricht, ist es schon anders.</div>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: 80 }}>
          {['sehen', 'nicht sehen'].map((w, i) => (
            <Reveal key={w} f={f} at={s(2, 0.03 + i * 0.05)}>
              <div style={T.display(70, C.muted)}>{w}</div>
            </Reveal>
          ))}
        </div>
        <Reveal f={f} at={s(2, 0.15)}>
          <div style={{ ...T.serif(40, C.red), marginTop: 10 }}>gleich richtig – also keines</div>
        </Reveal>
        <div style={{ display: 'flex', gap: 80, marginTop: 60 }}>
          {['„so“', '„nicht so“'].map((w, i) => (
            <Reveal key={w} f={f} at={s(2, 0.45 + i * 0.06)}>
              <div style={{ position: 'relative' }}>
                <div style={T.display(70)}>{w}</div>
                <Strike f={f} at={s(2, 0.6 + i * 0.04)} />
              </div>
            </Reveal>
          ))}
        </div>
        <Reveal f={f} at={s(2, 0.78)}>
          <div style={{ ...T.greek(70), marginTop: 50 }}>οὐδʼ οὕτως</div>
          <div style={{ ...T.label(22), textAlign: 'center' }}>„überhaupt nicht“ · Tht. 183b</div>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(3)) }}>
        <Svg>
          <defs>
            <radialGradient id="sphere" cx="40%" cy="35%" r="65%">
              <stop offset="0%" stopColor="#c9d7ea" stopOpacity="0.9" />
              <stop offset="60%" stopColor={C.blue} stopOpacity="0.45" />
              <stop offset="100%" stopColor="#1b2433" stopOpacity="0.9" />
            </radialGradient>
          </defs>
          <circle cx={960} cy={450} r={190 * prog(f, s(3, 0.45), 40)} fill="url(#sphere)" />
        </Svg>
        <At x={960} y={180} w={1500}>
          <Reveal f={f} at={s(3, 0.05)}>
            <div style={T.italic(44)}>Die Flusslehre macht schon das Sprechen unmöglich.</div>
          </Reveal>
        </At>
        <At x={960} y={760}>
          <Reveal f={f} at={s(3, 0.5)}>
            <div style={T.display(58, C.blue)}>Parmenides · das unbewegte Sein</div>
          </Reveal>
        </At>
        <At x={960} y={880}>
          <Reveal f={f} at={s(3, 0.7)}>
            <div style={T.greek(42)}>αἰδοῖός τέ μοι εἶναι ἅμα δεινός τε</div>
            <div style={T.label(20)}>„ehrwürdig und furchtbar zugleich“ · Tht. 183e</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

