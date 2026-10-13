import React from 'react';
import { AbsoluteFill, interpolate, staticFile } from 'remotion';
import { Bird, Eye, Figure, Hand, Profile } from '../components/icons';
import { Arrow, At, Card, easeInOut, Gr, lerp, prog, Reveal, Strike, Svg, T, vis } from '../components/kit';
import { C, F } from '../theme';
import { SceneTiming } from '../timeline';
import { useScene } from './util';

type P = { t: SceneTiming };

const WAX = '#b98a3e';

/** A wax block with the texture image, an optional imprint layer and a bevel. */
const Tablet: React.FC<{ x: number; y: number; w: number; h: number; id: string; opacity?: number; children?: React.ReactNode; tint?: string }> = ({
  x,
  y,
  w,
  h,
  id,
  opacity = 1,
  children,
  tint,
}) => (
  <g opacity={opacity}>
    <defs>
      <clipPath id={`clip-${id}`}>
        <rect x={x} y={y} width={w} height={h} rx={22} />
      </clipPath>
      <filter id={`emboss-${id}`}>
        <feGaussianBlur in="SourceAlpha" stdDeviation="2" result="b" />
        <feOffset in="b" dx="2" dy="3" result="o" />
        <feComposite in="SourceGraphic" in2="o" operator="over" />
      </filter>
    </defs>
    <rect x={x - 14} y={y - 14} width={w + 28} height={h + 28} rx={30} fill="#3b2a18" stroke="#6b4a26" strokeWidth={3} />
    <image href={staticFile('img/wax.jpg')} x={x} y={y} width={w} height={h} preserveAspectRatio="xMidYMid slice" clipPath={`url(#clip-${id})`} />
    {tint && <rect x={x} y={y} width={w} height={h} rx={22} fill={tint} />}
    <rect x={x} y={y} width={w} height={h} rx={22} fill="none" stroke="rgba(0,0,0,0.35)" strokeWidth={6} />
    <g clipPath={`url(#clip-${id})`}>{children}</g>
  </g>
);

/** Engraved-looking imprint of a profile. */
const Imprint: React.FC<{ x: number; y: number; s?: number; beard?: boolean; depth?: number; blur?: number }> = ({ x, y, s = 0.55, beard, depth = 1, blur = 0 }) => (
  <g opacity={depth} style={{ filter: blur ? `blur(${blur}px)` : undefined }}>
    <circle cx={x} cy={y} r={95 * s * 1.6} fill="rgba(60,35,10,0.25)" stroke="rgba(60,35,10,0.55)" strokeWidth={3} />
    <Profile x={x + 2} y={y + 3} s={s} beard={beard} snub color="rgba(255,236,190,0.55)" sw={4} />
    <Profile x={x} y={y} s={s} beard={beard} snub color="rgba(55,30,8,0.85)" sw={4} />
  </g>
);

/* ───────────── XIX · Wachstafel ───────────── */

export const Wachs: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const stamp1 = prog(f, s(1, 0.1), 18, easeInOut);
  const stamp2 = prog(f, s(1, 0.3), 18, easeInOut);
  const ringY = (p: number, base: number) => base - 260 * (1 - p) + (p > 0.95 ? 0 : 0);
  const fade = prog(f, s(1, 0.65), 40);
  const swapP = prog(f, s(2, 0.45), 30, easeInOut);
  const freud = prog(f, s(4, 0.55), 60);
  return (
    <AbsoluteFill>
      {/* 0 · the wax block */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <Tablet x={560} y={300} w={800} h={420} id="w0" opacity={prog(f, s(0, 0.2), 30)} />
        </Svg>
        <At x={960} y={180}>
          <Reveal f={f} at={s(0, 0.1)}>
            <div style={T.label(26, C.gold)}>ein Block aus Wachs in der Seele</div>
          </Reveal>
        </At>
        <At x={960} y={830}>
          <Reveal f={f} at={s(0, 0.4)}>
            <div style={T.serif(38, C.muted)}>größer · kleiner · reiner · schmutziger · härter · weicher</div>
          </Reveal>
        </At>
        <At x={960} y={920}>
          <Reveal f={f} at={s(0, 0.75)}>
            <div style={T.italic(40)}>
              ein Geschenk der Mnemosyne, der Mutter der Musen · <Gr>Μνημοσύνη</Gr>
            </div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 1 · signet rings make imprints */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <Tablet x={460} y={330} w={1000} h={440} id="w1">
            {stamp1 > 0.9 && <Imprint x={760} y={550} beard depth={1 - fade * 0.15} />}
            {stamp2 > 0.9 && <Imprint x={1160} y={550} depth={1 - fade * 0.9} blur={fade * 6} />}
          </Tablet>
          {[
            [760, stamp1, s(1, 0.1)],
            [1160, stamp2, s(1, 0.3)],
          ].map(([x, p, at], i) => (
            <g key={i} opacity={prog(f, at as number, 8) * (1 - prog(f, (at as number) + 24, 12))}>
              <ellipse cx={x as number} cy={ringY(p as number, 470)} rx={80} ry={26} fill="none" stroke={C.gold} strokeWidth={10} />
              <rect x={(x as number) - 46} y={ringY(p as number, 470) - 80} width={92} height={60} rx={14} fill={C.gold} />
            </g>
          ))}
        </Svg>
        <At x={760} y={830}>
          <Reveal f={f} at={s(1, 0.2)}>
            <div style={T.display(44)}>Theodoros</div>
            <div style={T.label(18, C.gold)}>Abdruck bleibt: erinnert, gewusst</div>
          </Reveal>
        </At>
        <At x={1160} y={830}>
          <Reveal f={f} at={s(1, 0.4)}>
            <div style={T.display(44)}>Theaitetos</div>
            <div style={{ ...T.label(18, C.red), opacity: prog(f, s(1, 0.75), 20) }}>verwischt: vergessen</div>
          </Reveal>
        </At>
        <At x={960} y={200}>
          <Reveal f={f} at={s(1)}>
            <div style={T.label(24, C.gold)}>wie mit einem Siegelring · Tht. 191d–e</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 2 · misfitting perception to imprint */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <Svg>
          <Tablet x={160} y={330} w={760} h={380} id="w2">
            <Imprint x={360} y={520} beard s={0.5} />
            <Imprint x={720} y={520} s={0.5} />
          </Tablet>
          <g opacity={prog(f, s(2, 0.15), 20)} style={{ filter: 'blur(2.5px)' }}>
            <Figure x={1300} y={500} s={0.9} color={C.ink} />
            <Figure x={1500} y={500} s={0.9} color={C.ink} />
          </g>
          <Arrow f={f} at={s(2, 0.35)} x1={1270} y1={420} x2={lerp(400, 760, swapP)} y2={430} color={swapP > 0.5 ? C.red : C.gold} bend={0.12} />
          <Arrow f={f} at={s(2, 0.4)} x1={1500} y1={420} x2={lerp(760, 400, swapP)} y2={440} color={swapP > 0.5 ? C.red : C.gold} bend={0.18} />
          <g opacity={prog(f, s(2, 0.7), 20)}>
            <path d="M 1250 700 C 1210 700 1200 760 1215 800 C 1225 830 1265 835 1275 800 C 1285 770 1290 700 1250 700 Z" fill="rgba(236,230,217,0.06)" stroke={C.ink} strokeWidth={3} transform="rotate(14 1250 770)" />
            <path d="M 1350 700 C 1390 700 1400 760 1385 800 C 1375 830 1335 835 1325 800 C 1315 770 1310 700 1350 700 Z" fill="rgba(236,230,217,0.06)" stroke={C.ink} strokeWidth={3} transform="rotate(-14 1350 770)" />
            <text x={1300} y={690} textAnchor="middle" fontFamily={F.display} fontSize={40} fill={C.red}>
              ⇄
            </text>
            <line x1={1600} y1={700} x2={1600} y2={840} stroke={C.blue} strokeWidth={4} />
            <text x={1560} y={800} textAnchor="middle" fontFamily={F.display} fontSize={80} fill={C.ink}>
              F
            </text>
            <text x={1640} y={800} textAnchor="middle" fontFamily={F.display} fontSize={80} fill={C.ink} opacity={0.5} transform="translate(3280 0) scale(-1 1)">
              F
            </text>
          </g>
        </Svg>
        <At x={1400} y={300}>
          <Reveal f={f} at={s(2, 0.15)}>
            <div style={T.label(22)}>von weitem, undeutlich</div>
          </Reveal>
        </At>
        <At x={540} y={790} w={760}>
          <Reveal f={f} at={s(2, 0.5)}>
            <div style={T.serif(38, C.red)}>Anblick des einen → Abdruck des anderen</div>
          </Reveal>
        </At>
        <At x={1450} y={920} w={600}>
          <Reveal f={f} at={s(2, 0.72)}>
            <div style={T.label(20)}>Schuhe am falschen Fuß · Spiegelbild</div>
          </Reveal>
        </At>
        <At x={960} y={160}>
          <Reveal f={f} at={s(2, 0.02)}>
            <div style={T.label(24, C.gold)}>Irrtum: Wahrnehmung und Abdruck falsch zusammengefügt · Tht. 193b–d</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 3 · qualities of wax */}
      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 6) }}>
        <Svg>
          {[
            { x: 180, label: 'tief · glatt · geknetet', at: 0.05, blur: 0, depth: 1, tint: undefined as string | undefined, hair: false, dirt: false },
            { x: 600, label: '„zottiges Herz“', at: 0.35, blur: 2, depth: 0.6, tint: undefined, hair: true, dirt: false },
            { x: 1020, label: 'schmutzig', at: 0.5, blur: 1.5, depth: 0.55, tint: 'rgba(40,30,20,0.35)', hair: false, dirt: true },
            { x: 1440, label: 'zu weich · zu hart', at: 0.62, blur: 5, depth: 0.4, tint: undefined, hair: false, dirt: false },
          ].map((q, i) => (
            <g key={i} opacity={prog(f, s(3, q.at), 20)}>
              <Tablet x={q.x} y={360} w={300} h={260} id={`q${i}`} tint={q.tint}>
                <Imprint x={q.x + 150} y={490} s={0.4} beard={i % 2 === 0} depth={q.depth} blur={q.blur} />
                {q.hair &&
                  Array.from({ length: 40 }, (_, k) => (
                    <path key={k} d={`M ${q.x + (k * 37) % 300} ${360 + ((k * 53) % 260)} q 8 -14 18 -6`} stroke="rgba(50,30,10,0.6)" strokeWidth={2} fill="none" />
                  ))}
                {q.dirt &&
                  Array.from({ length: 60 }, (_, k) => <circle key={k} cx={q.x + ((k * 41) % 300)} cy={360 + ((k * 67) % 260)} r={2 + (k % 3)} fill="rgba(30,20,10,0.6)" />)}
              </Tablet>
              <text x={q.x + 150} y={700} textAnchor="middle" fontFamily={F.serif} fontSize={32} fill={i === 0 ? C.gold : C.ink}>
                {q.label}
              </text>
            </g>
          ))}
        </Svg>
        <At x={330} y={780}>
          <Reveal f={f} at={s(3, 0.15)}>
            <div style={T.label(20, C.gold)}>lernt gut · behält gut</div>
          </Reveal>
        </At>
        <At x={1170} y={780}>
          <Reveal f={f} at={s(3, 0.75)}>
            <div style={T.label(20, C.red)}>undeutliche Abdrücke → Irrtum</div>
          </Reveal>
        </At>
        <At x={960} y={200}>
          <Reveal f={f} at={s(3, 0.4)}>
            <div style={T.greek(40)}>κέαρ λάσιον</div>
            <div style={T.label(18)}>Homer, nach Tht. 194e</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 4 · Aristotle and Freud */}
      <AbsoluteFill style={{ opacity: vis(f, s(4)) }}>
        <Svg>
          <g opacity={prog(f, s(4, 0.05), 20)}>
            <Tablet x={250} y={380} w={460} h={300} id="ar">
              <circle cx={480} cy={530} r={70} fill="rgba(60,35,10,0.25)" stroke="rgba(60,35,10,0.6)" strokeWidth={4} />
              <path d="M 450 530 L 480 490 L 510 530 L 480 570 Z" fill="none" stroke="rgba(60,35,10,0.8)" strokeWidth={4} />
            </Tablet>
          </g>
          <g opacity={prog(f, s(4, 0.5), 20)}>
            <rect x={1120} y={600} width={560} height={70} rx={8} fill="#4a2f17" />
            <rect x={1120} y={590 - freud * 80} width={560} height={10} rx={3} fill="rgba(244,239,228,0.75)" />
            <rect x={1120} y={575 - freud * 120} width={560} height={10} rx={3} fill="rgba(200,220,240,0.5)" />
            <path d="M 1200 630 C 1260 610 1300 650 1360 625 S 1460 610 1520 640" stroke={`rgba(244,239,228,${0.15 + 0.15 * freud})`} strokeWidth={4} fill="none" />
            <path d={`M 1200 ${575 - freud * 120} C 1260 ${560 - freud * 120} 1300 ${590 - freud * 120} 1360 ${570 - freud * 120}`} stroke="#222" strokeWidth={4} fill="none" opacity={1 - freud} />
          </g>
        </Svg>
        <At x={480} y={260} w={700}>
          <Reveal f={f} at={s(4, 0.05)}>
            <div style={T.label(22, C.gold)}>Aristoteles, De anima II 12</div>
            <div style={{ ...T.serif(36), marginTop: 10 }}>Wachs nimmt die Form des Siegelrings auf – ohne Eisen oder Gold</div>
          </Reveal>
        </At>
        <At x={480} y={790} w={600}>
          <Reveal f={f} at={s(4, 0.3)}>
            <div style={T.italic(34, C.muted)}>Wahrnehmung: Form ohne Stoff</div>
          </Reveal>
        </At>
        <At x={1400} y={300} w={760}>
          <Reveal f={f} at={s(4, 0.5)}>
            <div style={T.label(22, C.gold)}>Sigmund Freud 1925 · „Wunderblock“</div>
            <div style={{ ...T.serif(36), marginTop: 10 }}>Deckblatt hebt sich: die Schrift verschwindet – Dauerspuren bleiben im Wachs</div>
          </Reveal>
        </At>
        <At x={1400} y={790} w={640}>
          <Reveal f={f} at={s(4, 0.7)}>
            <div style={T.italic(32, C.muted)}>Freud nennt Platon nicht – das Bild kehrt wieder</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XX · 5 + 7 ───────────── */

export const Elf: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(0, 0.05), 20)}>
            <ellipse cx={960} cy={440} rx={420} ry={240} fill="rgba(217,181,107,0.06)" stroke={C.gold} strokeWidth={2} />
            <circle cx={620} cy={720} r={22} fill="none" stroke={C.gold} strokeWidth={2} />
            <circle cx={560} cy={790} r={14} fill="none" stroke={C.gold} strokeWidth={2} />
          </g>
          <g opacity={prog(f, s(0, 0.5), 20)}>
            <Eye x={1540} y={700} s={1} opacity={0.6} />
            <line x1={1470} y1={640} x2={1610} y2={760} stroke={C.red} strokeWidth={5} />
          </g>
        </Svg>
        <At x={800} y={440}>
          <Reveal f={f} at={s(0, 0.3)}>
            <div style={T.display(150)}>11</div>
          </Reveal>
        </At>
        <At x={1120} y={440}>
          <Reveal f={f} at={s(0, 0.35)}>
            <div style={T.display(150)}>12</div>
          </Reveal>
        </At>
        <At x={960} y={180}>
          <Reveal f={f} at={s(0, 0.1)}>
            <div style={T.label(24, C.gold)}>nur Gedachtes – keine Wahrnehmung beteiligt</div>
          </Reveal>
        </At>
        <At x={960} y={900} w={1300}>
          <Reveal f={f} at={s(0, 0.7)}>
            <div style={T.italic(40)}>Nach der Wachstafel wäre hier kein Irrtum möglich.</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1)), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(1, 0.1)}>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 40 }}>
            <div style={T.display(190)}>5 + 7 =</div>
            <div style={{ position: 'relative' }}>
              <div style={{ ...T.display(190, C.red), textShadow: `0 0 30px rgba(224,87,75,${prog(f, s(1, 0.35), 20) * 0.6})` }}>11</div>
              <div style={{ position: 'absolute', top: -60, right: -50, ...T.display(80, C.gold), opacity: prog(f, s(1, 0.6), 20) }}>12</div>
            </div>
          </div>
        </Reveal>
        <Reveal f={f} at={s(1, 0.35)}>
          <div style={{ ...T.italic(46), marginTop: 40 }}>„Viele sagen elf.“ – Tht. 196a</div>
        </Reveal>
        <Reveal f={f} at={s(1, 0.75)}>
          <div style={{ ...T.serif(40, C.muted), marginTop: 30 }}>Gewusstes mit Gewusstem verwechselt – das Rätsel ist zurück</div>
        </Reveal>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XXI · Taubenschlag ───────────── */

const Aviary: React.FC<{ x: number; y: number; w: number; h: number; f: number; birds: { n: string; dark?: boolean; at: number }[]; grab?: { idx: number; at: number; wrong?: boolean } }> = ({
  x,
  y,
  w,
  h,
  f,
  birds,
  grab,
}) => {
  const cols = 6;
  const rows = 3;
  const cw = w / cols;
  const ch = h / rows;
  return (
    <g>
      <path d={`M ${x - 20} ${y} L ${x + w / 2} ${y - 110} L ${x + w + 20} ${y} Z`} fill="rgba(207,106,71,0.12)" stroke={C.terracotta} strokeWidth={3} />
      <rect x={x} y={y} width={w} height={h} fill="rgba(236,230,217,0.03)" stroke={C.terracotta} strokeWidth={3} />
      {Array.from({ length: cols * rows }, (_, i) => {
        const cx = x + (i % cols) * cw + cw / 2;
        const cy = y + Math.floor(i / cols) * ch + ch / 2 + 20;
        return <path key={i} d={`M ${cx - 26} ${cy + 18} V ${cy - 4} A 26 26 0 0 1 ${cx + 26} ${cy - 4} V ${cy + 18} Z`} fill="#07080c" stroke="rgba(207,106,71,0.5)" strokeWidth={2} />;
      })}
      {birds.map((b, i) => {
        const a = prog(f, b.at, 24);
        const ang = i * 2.39 + f / 50;
        const fx = x + w / 2 + Math.cos(ang) * (w * 0.36) * (0.6 + 0.4 * Math.sin(i));
        const fy = y + h / 2 + Math.sin(ang * 1.3) * (h * 0.3);
        const grabbed = grab && grab.idx === i ? prog(f, grab.at, 24, easeInOut) : 0;
        const gx = lerp(fx, x + w + 160, grabbed);
        const gy = lerp(fy, y + h / 2, grabbed);
        return (
          <g key={i} opacity={a}>
            <Bird x={lerp(x + w / 2, gx, a)} y={lerp(y - 200, gy, a)} s={0.75} flap={f / 3 + i} color={b.dark ? C.faint : grab?.wrong && grab.idx === i && grabbed > 0.5 ? C.red : C.marble} fill={b.dark ? 'rgba(10,10,14,0.9)' : 'rgba(236,230,217,0.12)'} />
            <text x={lerp(x + w / 2, gx, a)} y={lerp(y - 200, gy, a) + 44} textAnchor="middle" fontFamily={F.sans} fontSize={22} fill={b.dark ? C.muted : C.gold}>
              {b.n}
            </text>
          </g>
        );
      })}
    </g>
  );
};

export const Taubenschlag: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const birds = ['1', '2', '3', '5', '7', '8', '11', '12'].map((n, i) => ({ n, at: s(2, 0.2) + i * 6 }));
  const dark = [
    { n: '?', dark: true, at: s(4, 0.3) },
    { n: '?', dark: true, at: s(4, 0.35) },
  ];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: 40, flexWrap: 'wrap', justifyContent: 'center', width: 1400 }}>
          {['„wir wissen“', '„wir wissen nicht“', '„Erkenntnis haben“', '„nicht verstehen“', '„kennen“', '„unwissend sein“'].map((w, i) => (
            <Reveal key={w} f={f} at={s(0, 0.1 + i * 0.07)}>
              <div style={{ ...T.italic(46, i % 2 ? C.muted : C.ink), padding: '6px 20px', border: `1px solid ${C.line}`, borderRadius: 30 }}>{w}</div>
            </Reveal>
          ))}
        </div>
        <Reveal f={f} at={s(0, 0.6)}>
          <div style={{ ...T.serif(42, C.gold), marginTop: 60 }}>… während wir nicht wissen, was Wissen ist</div>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(1, 0.05), 20)}>
            <path d="M 420 300 H 620 M 520 300 V 330" stroke={C.ink} strokeWidth={4} />
            <path d="M 440 330 L 470 330 L 520 345 L 570 330 L 600 330 L 640 600 H 400 Z" fill="rgba(207,106,71,0.18)" stroke={C.terracotta} strokeWidth={3} />
          </g>
          <g opacity={prog(f, s(1, 0.25), 20)}>
            <Figure x={960} y={500} s={1.5} color={C.ink} />
            <path d="M 915 445 L 1005 445 L 1025 600 H 895 Z" fill="rgba(207,106,71,0.3)" stroke={C.terracotta} strokeWidth={3} />
          </g>
          <g opacity={prog(f, s(1, 0.6), 20)}>
            <Aviary x={1250} y={380} w={480} h={260} f={f} birds={[0, 1, 2, 3].map((i) => ({ n: '', at: s(1, 0.6) + i * 5 }))} />
          </g>
        </Svg>
        <At x={520} y={700}>
          <Reveal f={f} at={s(1, 0.1)}>
            <div style={T.display(48)}>besitzen</div>
            <div style={T.greek(36, C.muted)}>κτῆσις</div>
          </Reveal>
        </At>
        <At x={960} y={700}>
          <Reveal f={f} at={s(1, 0.3)}>
            <div style={T.display(48, C.gold)}>haben</div>
            <div style={T.greek(36, C.muted)}>ἕξις</div>
          </Reveal>
        </At>
        <At x={1490} y={760}>
          <Reveal f={f} at={s(1, 0.65)}>
            <div style={T.label(22)}>Taubenschlag · Tht. 197c–d</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2), s(4) - 6) }}>
        <Svg>
          <Aviary x={360} y={330} w={900} h={420} f={f} birds={birds} grab={{ idx: f < s(3) ? 7 : 6, at: f < s(3) ? s(2, 0.8) : s(3, 0.3), wrong: f >= s(3) }} />
          <g opacity={prog(f, s(2, 0.75), 16)}>
            <Hand x={1460} y={540} s={1.2} color={C.ink} rot={-90} />
          </g>
        </Svg>
        <At x={810} y={180}>
          <Reveal f={f} at={s(2, 0.05)}>
            <div style={T.label(24, C.gold)}>lernen = einfangen · wissen = besitzen · rechnen = hineingreifen</div>
          </Reveal>
        </At>
        <At x={1640} y={380} w={420}>
          <div style={{ opacity: vis(f, s(2, 0.8), s(3)) }}>
            <div style={T.display(48, C.gold)}>gesucht: 12</div>
          </div>
        </At>
        <At x={1640} y={380} w={420}>
          <div style={{ opacity: prog(f, s(3, 0.35), 16) }}>
            <div style={T.display(48, C.red)}>erwischt: 11</div>
            <div style={T.serif(32, C.muted)}>Ringeltaube statt Taube</div>
          </div>
        </At>
        <At x={810} y={900} w={1200}>
          <Reveal f={f} at={s(3, 0.6)}>
            <div style={T.italic(40)}>ein Fehlgriff zwischen zwei Dingen, die man beide besitzt · Tht. 199a–b</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(4), s(5) - 6) }}>
        <Svg>
          <Aviary x={160} y={360} w={560} h={270} f={f} birds={[...birds.slice(0, 4).map((b) => ({ ...b, at: s(4) })), ...dark]} />
          {[0, 1, 2].map((k) => {
            const sc = Math.pow(0.62, k + 1);
            const x0 = 860 + [0, 360, 600][k];
            const at = s(4, 0.5 + k * 0.1);
            return (
              <g key={k} opacity={prog(f, at, 18)}>
                <Arrow f={f} at={at - 6} x1={x0 - 110} y1={500} x2={x0 - 30} y2={500} color={C.muted} width={2} dur={12} />
                <g transform={`translate(${x0} ${500 - 135 * sc}) scale(${sc})`}>
                  <Aviary x={0} y={0} w={560} h={270} f={f} birds={[]} />
                </g>
              </g>
            );
          })}
          <text x={1760} y={510} fontFamily={F.display} fontSize={80} fill={C.muted} opacity={prog(f, s(4, 0.85), 16)}>
            …
          </text>
        </Svg>
        <At x={440} y={720}>
          <Reveal f={f} at={s(4, 0.25)}>
            <div style={T.label(22, C.muted)}>mit Vögeln des Unwissens</div>
          </Reveal>
        </At>
        <At x={1300} y={720} w={800}>
          <Reveal f={f} at={s(4, 0.55)}>
            <div style={T.label(22, C.gold)}>Wissen über Wissen und Unwissen – und darüber …</div>
          </Reveal>
        </At>
        <At x={960} y={900} w={1500}>
          <Reveal f={f} at={s(4, 0.75)}>
            <div style={T.italic(44, C.gold)}>ein unendlicher Regress · Tht. 200b–c</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(5)), justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 50 }}>
          <Reveal f={f} at={s(5, 0.15)}>
            <Card>
              <div style={T.serif(44)}>falsche Meinung?</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(5, 0.3)}>
            <div style={T.display(70, C.red)}>✗</div>
          </Reveal>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 40, marginTop: 50 }}>
          <Reveal f={f} at={s(5, 0.55)}>
            <Card>
              <div style={T.serif(44, C.gold)}>1 · Was ist Erkenntnis?</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(5, 0.65)}>
            <div style={T.display(60, C.gold)}>→</div>
          </Reveal>
          <Reveal f={f} at={s(5, 0.72)}>
            <Card>
              <div style={T.serif(44)}>2 · falsche Meinung</div>
            </Card>
          </Reveal>
        </div>
        <Reveal f={f} at={s(5, 0.85)}>
          <div style={{ ...T.label(22), marginTop: 30 }}>Tht. 200c–d</div>
        </Reveal>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XXII · Die Richter ───────────── */

export const Richter: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const drain = prog(f, s(0, 0.2), t.durs[0], (x) => x);
  return (
    <AbsoluteFill>
      <Svg>
        {Array.from({ length: 9 }, (_, i) => (
          <Figure key={i} x={360 + i * 110} y={760} s={0.8} color={C.ink} opacity={prog(f, s(0, 0.05) + i * 2, 12)} />
        ))}
        <g opacity={prog(f, s(0, 0.2), 20)}>
          <Figure x={860} y={420} s={1.1} color={C.terracotta} fill="rgba(207,106,71,0.15)" />
          <rect x={1060} y={330} width={70} height={90} fill="none" stroke={C.ink} strokeWidth={2} />
          <rect x={1062} y={332 + drain * 86} width={66} height={86 - drain * 86} fill={C.blue} opacity={0.6} />
          <rect x={1060} y={450} width={70} height={90} fill="none" stroke={C.ink} strokeWidth={2} />
          <rect x={1062} y={538 - drain * 86} width={66} height={drain * 86} fill={C.blue} opacity={0.6} />
        </g>
        <g opacity={prog(f, s(0, 0.6), 20)}>
          <rect x={1400} y={250} width={380} height={300} rx={20} fill="rgba(236,230,217,0.03)" stroke={C.line} strokeDasharray="8 10" />
          <Eye x={1590} y={400} s={1.4} color={C.gold} />
        </g>
        {Array.from({ length: 9 }, (_, i) => (
          <circle key={i} cx={360 + i * 110} cy={650} r={12} fill={C.gold} opacity={prog(f, s(1, 0.15) + i * 3, 10)} />
        ))}
      </Svg>
      <At x={1590} y={600} w={420}>
        <Reveal f={f} at={s(0, 0.6)}>
          <div style={T.label(22, C.gold)}>nur der Augenzeuge weiß</div>
          <div style={T.serif(30, C.muted)}>z. B. bei einem Raub</div>
        </Reveal>
      </At>
      <At x={860} y={260}>
        <Reveal f={f} at={s(0, 0.25)}>
          <div style={T.label(22, C.terracotta)}>Redner · Wasseruhr läuft</div>
        </Reveal>
      </At>
      <At x={800} y={900} w={1200}>
        <div style={{ display: 'flex', gap: 60, justifyContent: 'center', opacity: prog(f, s(1, 0.35), 20) }}>
          <div style={T.display(52, C.gold)}>wahre Meinung ✓</div>
          <div style={{ position: 'relative' }}>
            <div style={T.display(52, C.red)}>Wissen</div>
            <Strike f={f} at={s(1, 0.5)} />
          </div>
        </div>
      </At>
      <At x={960} y={130} w={1500}>
        <Reveal f={f} at={s(1, 0.75)}>
          <Card>
            <div style={T.display(50)}>wahre Meinung ≠ Erkenntnis · Tht. 201c</div>
          </Card>
        </Reveal>
      </At>
    </AbsoluteFill>
  );
};
